import datetime
import logging
from typing import Any

from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
from django.db.models import Field, DateField, IntegerField
from django.contrib.postgres.fields import ArrayField
from django.db.models.query_utils import DeferredAttribute
from django.db.models.fields.related_descriptors import (
    ForwardManyToOneDescriptor,
    ManyToManyDescriptor,
)
from pygrister.api import GristApi

from .models import GristModel

logger = logging.getLogger(__name__)


class GristLoader:
    model = None
    pygrister_config = None
    table = None
    required_cols = tuple()
    fields: dict[
        str,
        DeferredAttribute | ForwardManyToOneDescriptor | ManyToManyDescriptor,
    ] = dict()
    filter: dict[str, list[Any]] = dict()

    def __init__(self):
        if not issubclass(self.model, GristModel):
            raise ImproperlyConfigured(
                "GristLoader model must be a subclass of GristModel"
            )
        if not isinstance(self.table, str):
            raise ImproperlyConfigured(
                "GristLoader table must be a str: it's the name of a Grist table"
            )
        if not isinstance(self.pygrister_config, dict):
            raise ImproperlyConfigured(
                "GristLoader pygrister_config must be a dict as defined here: https://pygrister.readthedocs.io/en/latest/conf.html#configuration-keys"
            )
        self.gristapi = GristApi(config=self.pygrister_config)
        self.current_obj = None
        self.current_row = None

    def _load_field(self, column_name: str, field: Field) -> bool:
        value = self.current_row[column_name]
        if isinstance(field, DateField):
            if value:
                try:
                    value = datetime.date.fromtimestamp(value)
                except TypeError:
                    logger.debug(
                        f"Table {self.table}, row {self.current_row['id']}: column {column_name} ignored as it cannot be cast to a date"
                    )
                    return False
        elif isinstance(field, IntegerField):
            if value and not isinstance(value, int):
                logger.debug(
                    f"Table {self.table}, row {self.current_row['id']}: column {column_name} ignored as it's not an int'"
                )
                return False
        elif isinstance(field, ArrayField):
            if value:
                if isinstance(value, list):
                    value = value[1:]
                else:
                    logger.debug(
                        f"Table {self.table}, row {self.current_row['id']}: column {column_name} ignored as it's not a list'"
                    )
                    return False

        if getattr(self.current_obj, field.name) != value:
            setattr(self.current_obj, field.name, value)
            return True
        return False

    def _load_fk(self, column_name: str, field: Field) -> bool:
        fk = getattr(self.current_obj, field.name)
        value = self.current_row[column_name]

        if not isinstance(value, int):
            logger.debug(
                f"Table {self.table}, row {self.current_row['id']}: column {column_name} ignored as it's not an int"
            )
            return False

        if value and (fk is None or fk.external_id != value):
            remote_model = field.remote_field.model
            try:
                setattr(
                    self.current_obj,
                    field.name,
                    remote_model.objects.get(external_id=self.current_row[column_name]),
                )
                return True
            except remote_model.DoesNotExist:
                logger.debug(
                    f"Table {self.table}, row {self.current_row['id']}: FK {field.name} (remote model {remote_model._meta.model_name}) not found"
                )
        return False

    def _load_m2m(self, column_name: str, field: Field) -> bool:
        m2m = getattr(self.current_obj, field.name)
        if self.current_row[column_name]:
            if not isinstance(self.current_row[column_name], list):
                logger.debug(
                    f"Table {self.table}, row {self.current_row['id']}: column {column_name} ignored as it's not a list"
                )
                return False
            external_ids = self.current_row[column_name][1:]
        else:
            external_ids = None
        if m2m.values_list("external_id", flat=True) != external_ids:
            m2m.clear()
            if external_ids:
                m2m.add(*m2m.model.objects.filter(external_id__in=external_ids))
            return True
        return False

    def load(self):
        logger.debug(
            f"Loading table {self.table} into model {self.model._meta.model_name}"
        )
        status, rows = self.gristapi.list_records(self.table, filter=self.filter)
        for row in rows:
            # check if all required cols do have a value
            # ignore the row if not
            is_valid = True
            for field in self.required_cols:
                if not row[field]:
                    is_valid = False
                    break
            if not is_valid:
                logger.info(
                    f"Table {self.table}, row {row['id']} is ignored because required field {field} is empty"
                )
                continue

            self.current_row = row
            modified = False

            self.current_obj, created = self.model.objects.get_or_create(
                external_id=row["id"]
            )
            if created:
                logger.debug(
                    f"Table {self.table}, row {row['id']} has been created, will be completed"
                )
            else:
                logger.debug(f"Table {self.table}, row {row['id']} will be updated")

            for column_name, field_descriptor in self.fields.items():
                if isinstance(field_descriptor, DeferredAttribute):
                    logger.debug(
                        f"Table {self.table}, row {row['id']}, column {column_name} as a field"
                    )
                    modified |= self._load_field(column_name, field_descriptor.field)
                elif isinstance(field_descriptor, ForwardManyToOneDescriptor):
                    logger.debug(
                        f"Table {self.table}, row {row['id']}, column {column_name} as a fk"
                    )
                    modified |= self._load_fk(column_name, field_descriptor.field)
                elif isinstance(field_descriptor, ManyToManyDescriptor):
                    logger.debug(
                        f"Table {self.table}, row {row['id']}, column {column_name} as a m2m"
                    )
                    modified |= self._load_m2m(column_name, field_descriptor.field)

            if modified:
                self.current_obj.save()
                logger.debug(f"Table {self.table}, row {row['id']} has been saved")


registry: list[type[GristLoader]] = list()


def register_grist_loader(loader: type[GristLoader]):
    registry.append(loader)
    return loader
