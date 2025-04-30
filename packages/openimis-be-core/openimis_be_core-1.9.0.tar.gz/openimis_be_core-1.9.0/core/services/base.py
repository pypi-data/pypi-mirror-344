from abc import ABC
from typing import Type
import asyncio
from django.db import transaction

from core.models import HistoryModel, MutationLog
from core.services.utils import check_authentication as check_authentication, output_exception, \
    model_representation, output_result_success, build_delete_instance_payload
from core.validation.base import BaseModelValidation
from core.utils import to_json_safe_value


class BaseService(ABC):

    @property
    def OBJECT_TYPE(self) -> Type[HistoryModel]:
        """
        Django ORM model. It's expected that it'll be inheriting from HistoryModel.
        """
        raise NotImplementedError("Class has to define OBJECT_TYPE for service.")

    def __init__(self, user, validation_class: Type[BaseModelValidation] = BaseModelValidation):
        self.user = user
        self.validation_class = validation_class

    @check_authentication
    def create(self, obj_data):
        try:
            with transaction.atomic():
                obj_data = self._adjust_create_payload(obj_data)
                self.validation_class.validate_create(self.user, **obj_data)
                obj_ = self.OBJECT_TYPE(**obj_data)
                return self.save_instance(obj_)
        except Exception as exc:
            return output_exception(model_name=self.OBJECT_TYPE.__name__, method="create", exception=exc)

    @check_authentication
    def update(self, obj_data):
        try:
            with transaction.atomic():
                obj_data = self._adjust_update_payload(obj_data)
                self.validation_class.validate_update(self.user, **obj_data)
                obj_ = self.OBJECT_TYPE.objects.filter(id=obj_data['id']).first()
                obj_.update(data=obj_data, user=self.user, save=False)
                return self.save_instance(obj_)
        except Exception as exc:
            return output_exception(model_name=self.OBJECT_TYPE.__name__, method="update", exception=exc)

    @check_authentication
    def delete(self, obj_data):
        try:
            with transaction.atomic():
                self.validation_class.validate_delete(self.user, **obj_data)
                obj_ = self.OBJECT_TYPE.objects.filter(id=obj_data['id']).first()
                return self.delete_instance(obj_)
        except Exception as exc:
            return output_exception(model_name=self.OBJECT_TYPE.__name__, method="delete", exception=exc)

    def save_instance(self, obj_):
        obj_.save(user=self.user, username=self.user.username)
        dict_repr = model_representation(obj_)
        return output_result_success(dict_representation=dict_repr)

    def delete_instance(self, obj_):
        obj_.delete(user=self.user, username=self.user.username)
        return build_delete_instance_payload()

    def _adjust_create_payload(self, payload_data):
        return self._base_payload_adjust(payload_data)

    def _adjust_update_payload(self, payload_data):
        self._align_json_ext(payload_data)
        return self._base_payload_adjust(payload_data)

    def _align_json_ext(self, payload_data):
        json_ext = payload_data.get('json_ext')
        if isinstance(json_ext, dict):
            for key, value in payload_data.items():
                if key in json_ext and json_ext[key] != value:
                    json_ext[key] = to_json_safe_value(value)

    def _base_payload_adjust(self, obj_data):
        return obj_data


def wait_for_mutation(client_mutation_id):
    mutation = MutationLog.objects.filter(
        client_mutation_id=client_mutation_id
    ).first()
    if not mutation:
        return
    loop_count = 0
    while mutation.status == MutationLog.RECEIVED and loop_count<10:
        asyncio.sleep(0.3)
        loop_count += 1
    return
