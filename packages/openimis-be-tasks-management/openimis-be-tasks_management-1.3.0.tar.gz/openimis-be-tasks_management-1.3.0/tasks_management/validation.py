from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType

from core.models import User
from core.validation import BaseModelValidation, UniqueCodeValidationMixin, ObjectExistsValidationMixin, \
    StringFieldValidationMixin
from tasks_management.models import TaskGroup, TaskExecutor, Task


class TaskGroupValidation(BaseModelValidation, UniqueCodeValidationMixin, ObjectExistsValidationMixin,
                          StringFieldValidationMixin):
    OBJECT_TYPE = TaskGroup

    @classmethod
    def validate_create(cls, user, **data):
        super().validate_create(user, **data)
        cls.validate_unique_code_name(data.get('code'))
        errors = validate_task_group(data)
        if errors:
            raise ValidationError(errors)

    @classmethod
    def validate_update(cls, user, **data):
        super().validate_update(user, **data)
        uuid = data.get('id')
        cls.validate_object_exists(uuid)
        existing = cls.OBJECT_TYPE.objects.filter(id=uuid).first()

        incoming_code = data.get('code')
        if incoming_code != existing.code:
            cls.validate_unique_code_name(data.get('code'))
        errors = validate_task_group(data, uuid)
        if errors:
            raise ValidationError(errors)


class TaskExecutorValidation(BaseModelValidation):
    OBJECT_TYPE = TaskExecutor

    @classmethod
    def validate_create(cls, user, **data):
        super().validate_create(user, **data)
        errors = validate_task_executor(data)
        if errors:
            raise ValidationError(errors)


class TaskValidation(BaseModelValidation, ObjectExistsValidationMixin):
    OBJECT_TYPE = Task

    @classmethod
    def validate_create(cls, user, **data):
        super().validate_create(user, **data)
        errors = validate_existing_task(data)
        if errors:
            raise ValidationError(errors)

    @classmethod
    def validate_update(cls, user, **data):
        super().validate_update(user, **data)
        uuid = data.get('id')
        cls.validate_object_exists(uuid)
        errors = validate_task_status(uuid)
        if errors:
            raise ValidationError(errors)

    @classmethod
    def validate_delete(cls, user, **data):
        super().validate_delete(user, **data)


def validate_task_group(data, uuid=None):
    return [
        *validate_not_empty_field(data.get("code"), "code"),
        *validate_unique_task_source(data.get("task_sources"), uuid)
    ]


def validate_task_executor(data, uuid=None):
    return [
        *validate_user_exists(data.get("user_id"))
    ]


def validate_task_status(uuid):
    instance = Task.objects.get(id=uuid)
    instance_status = instance.status
    if instance_status in [Task.Status.COMPLETED, Task.Status.FAILED]:
        return [
            {"message": _("tasks_management.validation.task.updating_completed_task") % {'status': instance_status}}]
    return []


def validate_user_exists(user_id):
    if not User.objects.filter(id=user_id).exists():
        return [{"message": _("tasks_management.validation.group_executor.user_does_not_exist") % {'code': user_id}}]
    return []


def validate_not_empty_field(string, field):
    try:
        TaskGroupValidation().validate_empty_string(string)
        TaskGroupValidation().validate_string_whitespace_end(string)
        TaskGroupValidation().validate_string_whitespace_start(string)
        return []
    except ValidationError as e:
        return [{"message": _("tasks_management.validation.field_empty") % {'field': field}}]


def validate_existing_task(data):
    content_type = data.get('entity_type')
    entity_id = data.get('entity_id')

    if isinstance(content_type, ContentType):
        try:
            entity_instance = content_type.get_object_for_this_type(id=entity_id)
        except content_type.model_class().DoesNotExist:
            return [{"message": _("tasks_management.validation.entity_not_found") % {'entity_id': entity_id}}]

        filtered_tasks = Task.objects.filter(
            Q(entity_type=content_type) &
            Q(entity_id=str(entity_id)) &
            (Q(status=Task.Status.ACCEPTED) | Q(status=Task.Status.RECEIVED))
        )

        if filtered_tasks.exists():
            return [
                {"message": _("tasks_management.validation.another_task_pending") % {'instance': str(entity_instance)}}]
    return []


def validate_unique_task_source(task_sources, group_id=None):
    task_groups_by_source = {}

    queryset = TaskGroup.objects.filter(is_deleted=False)
    if group_id:
        queryset = queryset.exclude(id=group_id)

    for task_source in task_sources:
        instance = queryset.filter(json_ext__contains={"task_sources": [task_source]}).first()
        if instance:
            task_groups_by_source[task_source] = instance.code

    if task_groups_by_source:
        return [{"message": _("tasks_management.validation.validate_unique_task_source") % {
            'task_groups_by_source': task_groups_by_source}}]
    return []
