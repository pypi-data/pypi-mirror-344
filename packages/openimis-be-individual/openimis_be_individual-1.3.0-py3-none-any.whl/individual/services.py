import logging
import json
import uuid
import pandas as pd
import concurrent.futures
import math
from pandas import DataFrame
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import transaction

from calculation.services import get_calculation_object
from core import filter_validity
from core.custom_filters import CustomFilterWizardStorage
from core.models import User
from core.services import BaseService
from core.signals import register_service_signal
from django.apps import apps
from django.utils.translation import gettext as _
from django.db.models import Q, OuterRef, Subquery, Count
from individual.apps import IndividualConfig
from individual.models import (
    Individual,
    IndividualDataSource,
    GroupIndividual,
    Group,
    IndividualDataUploadRecords,
    IndividualDataSourceUpload
)
from individual.utils import (
    load_dataframe,
    fetch_summary_of_valid_items,
    fetch_summary_of_broken_items
)
from individual.validation import (
    IndividualValidation,
    IndividualDataSourceValidation,
    GroupIndividualValidation,
    GroupValidation, CrateGroupAndMoveIndividualValidation
)
from core.services.utils import check_authentication as check_authentication, output_exception, output_result_success, \
    model_representation
from location.models import Location, LocationManager
from tasks_management.models import Task
from tasks_management.services import UpdateCheckerLogicServiceMixin, CreateCheckerLogicServiceMixin, \
    crud_business_data_builder, DeleteCheckerLogicServiceMixin
from workflow.systems.base import WorkflowHandler

logger = logging.getLogger(__name__)


class IndividualService(BaseService, UpdateCheckerLogicServiceMixin, DeleteCheckerLogicServiceMixin):
    @register_service_signal('individual_service.create')
    def create(self, obj_data):
        return super().create(obj_data)

    def create_update_task(self, obj_data):
        self._update_json_ext(obj_data)
        return super().create_update_task(obj_data)

    @register_service_signal('individual_service.update')
    def update(self, obj_data):
        self._update_json_ext(obj_data)
        return super().update(obj_data)

    @register_service_signal('individual_service.delete')
    def delete(self, obj_data):
        return super().delete(obj_data)

    @register_service_signal('individual_service.undo_delete')
    @check_authentication
    def undo_delete(self, obj_data):
        try:
            with transaction.atomic():
                self.validation_class.validate_undo_delete(obj_data)
                obj_ = self.OBJECT_TYPE.objects.filter(id=obj_data['id']).first()
                obj_.is_deleted = False
                obj_.save(user=self.user.user)
                return {
                    "success": True,
                    "message": "Ok",
                    "detail": "Undo Delete",
                }
        except Exception as exc:
            return output_exception(model_name=self.OBJECT_TYPE.__name__, method="undo_delete", exception=exc)

    @register_service_signal('individual_service.select_individuals_to_benefit_plan')
    def select_individuals_to_benefit_plan(self, custom_filters, benefit_plan_id, status, user):
        individual_query = Individual.objects.filter(is_deleted=False)
        subquery = GroupIndividual.objects.filter(
            individual=OuterRef('pk')
        ).exclude(
            is_deleted=True
        ).values('individual')
        individual_query_with_filters = CustomFilterWizardStorage.build_custom_filters_queryset(
            "individual",
            "Individual",
            custom_filters,
            individual_query,
        )
        individual_query_with_filters = individual_query_with_filters.filter(~Q(pk__in=Subquery(subquery))).distinct()
        if benefit_plan_id:
            individuals_assigned_to_selected_programme = individual_query_with_filters. \
                filter(is_deleted=False, beneficiary__benefit_plan_id=benefit_plan_id)
            individuals_not_assigned_to_selected_programme = individual_query_with_filters.exclude(
                id__in=individuals_assigned_to_selected_programme.values_list('id', flat=True)
            )
            output = {
                "individuals_assigned_to_selected_programme": individuals_assigned_to_selected_programme,
                "individuals_not_assigned_to_selected_programme": individuals_not_assigned_to_selected_programme,
                "individual_query_with_filters": individual_query_with_filters,
                "benefit_plan_id": benefit_plan_id,
                "status": status,
                "user": user,
            }
            return output
        return None

    @register_service_signal('individual_service.create_accept_enrolment_task')
    def create_accept_enrolment_task(self, individual_queryset, benefit_plan_id):
        pass

    def _update_json_ext(self, obj_data):
        if not obj_data or 'json_ext' not in obj_data or 'location_id' not in obj_data:
            return

        json_ext = obj_data['json_ext']
        if not json_ext:
            return

        location_id = obj_data['location_id']
        if location_id:
            location = Location.objects.get(id=location_id)
            json_ext['location_str'] = str(location)
        else:
            json_ext['location_str'] = None

        obj_data['json_ext'] = json_ext

    OBJECT_TYPE = Individual

    def __init__(self, user, validation_class=IndividualValidation):
        super().__init__(user, validation_class)


class IndividualDataSourceService(BaseService):
    @register_service_signal('individual_data_source_service.create')
    def create(self, obj_data):
        return super().create(obj_data)

    @register_service_signal('individual_data_source_service.update')
    def update(self, obj_data):
        return super().update(obj_data)

    @register_service_signal('individual_data_source_service.delete')
    def delete(self, obj_data):
        return super().delete(obj_data)

    OBJECT_TYPE = IndividualDataSource

    def __init__(self, user, validation_class=IndividualDataSourceValidation):
        super().__init__(user, validation_class)


class GroupService(
    BaseService,
    CreateCheckerLogicServiceMixin,
    UpdateCheckerLogicServiceMixin,
    DeleteCheckerLogicServiceMixin
):
    OBJECT_TYPE = Group

    def __init__(self, user, validation_class=GroupValidation):
        super().__init__(user, validation_class)

    @check_authentication
    @register_service_signal('group_service.create')
    def create(self, obj_data):
        try:
            with transaction.atomic():
                individuals_data = obj_data.pop('individuals_data', None)
                result = super().create(obj_data)
                group_id = result.get('data', {}).get('id')

                if not group_id:
                    return result

                if individuals_data:
                    individual_ids = [data["individual_id"] for data in individuals_data]
                    self._update_group_json_ext(group_id, individual_ids)
                    for data in individuals_data:
                        obj_data = {
                            'group_id': group_id,
                            'individual_id': data.get("individual_id"),
                            'role': data.get("role"),
                            'recipient_type': data.get("recipient_type")
                        }
                        service = GroupIndividualService(self.user)
                        service.create(obj_data)
                return result
        except Exception as exc:
            return output_exception(model_name=self.OBJECT_TYPE.__name__, method="create", exception=exc)

    @check_authentication
    @register_service_signal('group_service.update')
    def update(self, obj_data):
        try:
            with transaction.atomic():
                individuals_data = obj_data.pop('individuals_data', None)
                result = super().update(obj_data)

                if not individuals_data:
                    return result

                group_id = obj_data['id']
                assigned_individuals_ids = \
                    GroupIndividual.objects.filter(group_id=group_id).values_list('individual_id', flat=True)

                service = GroupIndividualService(self.user)
                individual_ids = [data['individual_id'] for data in individuals_data]
                group = self._update_group_json_ext(group_id, individual_ids)

                for individual_id in assigned_individuals_ids:
                    if str(individual_id) not in individual_ids:
                        group_individual = GroupIndividual.objects.get(group_id=group_id, individual_id=individual_id)
                        service.delete({'id': group_individual.id})

                for data in individuals_data:
                    if uuid.UUID(data["individual_id"]) not in assigned_individuals_ids:
                        obj_data = {
                            'group_id': group_id,
                            'individual_id': data.get("individual_id"),
                            'role': data.get("role"),
                            'recipient_type': data.get("recipient_type")
                        }
                        service.create(obj_data)

                dict_repr = model_representation(group)
                return output_result_success(dict_representation=dict_repr)
        except Exception as exc:
            return output_exception(model_name=self.OBJECT_TYPE.__name__, method="update", exception=exc)

    @register_service_signal('group_service.delete')
    def delete(self, obj_data):
        # if there ever was a requirement to undo group delete, remember to use members from json_ext, you will avoid
        # adding individuals that had been deleted from the group before group deletion
        with transaction.atomic():
            group_id = obj_data.get('id')
            group_individuals = GroupIndividual.objects.filter(group_id=group_id)
            for group_individual in group_individuals:
                # cant use .delete() on query since it will completely remove instances from db instead of marking
                # them as isDeleted
                group_individual.delete(user=self.user)
            return super().delete(obj_data)

    @transaction.atomic
    def _update_group_json_ext(self, group_id, individual_ids):
        # it makes sure GroupIndividual .save() won't add each individual separately to group json_ext
        # because their ids will be already there
        group = Group.objects.get(id=group_id)
        group_members = {
            str(individual.id): f"{individual.first_name} {individual.last_name}"
            for individual in Individual.objects.filter(id__in=individual_ids)
        }
        group.json_ext["members"] = group_members
        group.save(user=self.user.user)
        return group

    @register_service_signal('group_service.select_groups_to_benefit_plan')
    def select_groups_to_benefit_plan(self, custom_filters, benefit_plan_id, status, user):
        group_query = Group.objects.filter(is_deleted=False)
        # criteria will be based on head of the group
        group_query_with_filters = CustomFilterWizardStorage.build_custom_filters_queryset(
            "individual",
            "Group",
            custom_filters,
            group_query,
        )
        if benefit_plan_id:
            groups_assigned_to_selected_programme = group_query_with_filters. \
                filter(is_deleted=False, groupbeneficiary__benefit_plan_id=benefit_plan_id)
            groups_not_assigned_to_selected_programme = group_query_with_filters.exclude(
                id__in=groups_assigned_to_selected_programme.values_list('id', flat=True)
            )
            output = {
                "groups_assigned_to_selected_programme": groups_assigned_to_selected_programme,
                "groups_not_assigned_to_selected_programme": groups_not_assigned_to_selected_programme,
                "group_query_with_filters": group_query_with_filters,
                "benefit_plan_id": benefit_plan_id,
                "status": status,
                "user": user,
            }
            return output
        return None


class CreateGroupAndMoveIndividualService(CreateCheckerLogicServiceMixin):
    OBJECT_TYPE = Group

    def __init__(self, user, validation_class=CrateGroupAndMoveIndividualValidation):
        self.user = user
        self.validation_class = validation_class

    @check_authentication
    @register_service_signal('create_group_and_move_individual.create')
    def create(self, obj_data):
        try:
            with transaction.atomic():
                self.validation_class.validate_create_group_and_move_individual(self.user, **obj_data)
                group_individual_id = obj_data.pop('group_individual_id')
                group = GroupService(self.user).create(obj_data)
                # return group if it has errors
                if not group['data']:
                    return group
                group_individual = GroupIndividual.objects.filter(id=group_individual_id).first()
                group_id = group['data']['id']
                service = GroupIndividualService(self.user)
                service.update({
                    'group_id': group_id, "id": group_individual_id, "role": group_individual.role
                })
                group_and_individuals_message = {**group, 'detail': group_individual_id}
                return group_and_individuals_message
        except Exception as exc:
            return output_exception(model_name=self.OBJECT_TYPE.__name__, method="create", exception=exc)

    def _business_data_serializer(self, data):
        def serialize(key, value):
            if key == 'group_individual_id':
                group_individual = GroupIndividual.objects.get(id=value)
                return f'{group_individual.individual.first_name} {group_individual.individual.last_name}'
            return value

        serialized_data = crud_business_data_builder(data, serialize)
        # TODO change to group code
        serialized_data['incoming_data']["id"] = 'NEW_GROUP'
        return serialized_data


class GroupIndividualService(BaseService, UpdateCheckerLogicServiceMixin):
    OBJECT_TYPE = GroupIndividual

    def __init__(self, user, validation_class=GroupIndividualValidation):
        super().__init__(user, validation_class)

    @register_service_signal('groupindividual_service.create')
    def create(self, obj_data):
        return super().create(obj_data)

    @check_authentication
    @register_service_signal('groupindividual_service.update')
    def update(self, obj_data):
        try:
            with transaction.atomic():
                group_individual_id = obj_data.get('id')
                incoming_group_id = obj_data.get('group_id')
                group_individual = GroupIndividual.objects.filter(id=group_individual_id, is_deleted=False).first()
                if not group_individual:
                    raise ValueError(f"no GroupIndividual found with this id {group_individual_id}")

                if str(group_individual.group.id) == str(incoming_group_id):
                    return super().update(obj_data)

                obj_data.pop('id', None)
                obj_data.pop('recipient_type', None)
                obj_data.pop('role', None)
                result = self.create(obj_data)
                self.delete({'id': group_individual_id})
                return result
        except Exception as exc:
            return output_exception(model_name=self.OBJECT_TYPE.__name__, method="update", exception=exc)

    @register_service_signal('groupindividual_service.delete')
    def delete(self, obj_data):
        return super().delete(obj_data)

    def _business_data_serializer(self, data):
        def serialize(key, value):
            if key == 'id':
                group_individual = GroupIndividual.objects.get(id=value)
                return f'{group_individual.individual.first_name} {group_individual.individual.last_name}'
            if key == 'group_id':
                group = Group.objects.get(id=value)
                return group.code
            return value

        serialized_data = crud_business_data_builder(data, serialize)
        return serialized_data


class GroupAndGroupIndividualAlignmentService:
    """
        Service used in overridden .save() of GroupIndividual model.
    """

    def __init__(self, user):
        self.user = user

    def handle_head_change(self, group_individual_id, role, group_id):
        """
            Method used for making sure that during head change, the old one is set to default role.
        """
        if role == GroupIndividual.Role.HEAD:
            self._change_head(group_individual_id, group_id)

    def handle_primary_recipient_change(self, group_individual_id, recipient_type, group_id):
        """
            Method used for making sure that during primary recipient change, the old one is set to default role.
        """
        if recipient_type == GroupIndividual.RecipientType.PRIMARY:
            self._change_primary(group_individual_id, group_id)

    def update_json_ext_for_group(self, group):
        """
        This method ensures that json_ext of a group is up-to-date with its roles and members.
        """
        group_individuals = GroupIndividual.objects.filter(group_id=group.id, is_deleted=False)
        head = group_individuals.filter(role=GroupIndividual.Role.HEAD).first()
        primary = group_individuals.filter(recipient_type=GroupIndividual.RecipientType.PRIMARY).first()
        secondary = group_individuals.filter(recipient_type=GroupIndividual.RecipientType.SECONDARY).first()

        group_members = {
            str(individual.individual.id): f"{individual.individual.first_name} {individual.individual.last_name}"
            for individual in group_individuals
        }

        head_str = f'{head.individual.first_name} {head.individual.last_name}' if head else None
        head_id = str(head.individual.id) if head else None
        head_json_ext = head.individual.json_ext if head and head.individual.json_ext else {}

        primary_str = f'{primary.individual.first_name} {primary.individual.last_name}' if primary else None
        primary_id = str(primary.individual.id) if primary else None

        secondary_str = f'{secondary.individual.first_name} {secondary.individual.last_name}' if secondary else None
        secondary_id = str(secondary.individual.id) if secondary else None

        changes_to_save = {}
        json_ext_minus_keys = {k: v for k, v in group.json_ext.items() if k not in [
            "members", "head", "head_id", "primary_recipient",
            "primary_recipient_id", "secondary_recipient", "secondary_recipient_id"
        ]}

        if json_ext_minus_keys != head_json_ext:
            all_keys = set(head_json_ext.keys()).union(json_ext_minus_keys.keys())
            for key in all_keys:
                value = head_json_ext.get(key)
                if value is None and key in group.json_ext:
                    del group.json_ext[key]
                else:
                    group.json_ext[key] = value

        current_members = group.json_ext.get("members", {})
        additional_members = {k: v for k, v in group_members.items() if k not in current_members}
        remove_members = {k: v for k, v in current_members.items() if k not in group_members}
        updated_members = {**current_members, **additional_members}
        for member_id in remove_members:
            updated_members.pop(member_id, None)

        if current_members != updated_members:
            changes_to_save["members"] = updated_members

        if group.json_ext.get("head") != head_str:
            changes_to_save["head"] = head_str

        if group.json_ext.get("head_id") != head_id:
            changes_to_save["head_id"] = head_id

        if group.json_ext.get("primary_recipient") != primary_str:
            changes_to_save["primary_recipient"] = primary_str

        if group.json_ext.get("primary_recipient_id") != primary_id:
            changes_to_save["primary_recipient_id"] = primary_id

        if group.json_ext.get("secondary_recipient") != secondary_str:
            changes_to_save["secondary_recipient"] = secondary_str

        if group.json_ext.get("secondary_recipient_id") != secondary_id:
            changes_to_save["secondary_recipient_id"] = secondary_id

        if changes_to_save:
            group.json_ext.update(changes_to_save)
            group.save(update_fields=['json_ext'], user=self.user)

    def handle_assure_primary_recipient_in_group(self, group, recipient_type):
        """
            Making sure that group has a head.
        """
        if recipient_type == GroupIndividual.RecipientType.PRIMARY:
            return
        self._assure_primary_recipient_in_group(group)

    def ensure_location_consistent(self, group, individual, role):
        if group.location_id == individual.location_id:
            return

        if role == GroupIndividual.Role.HEAD and group.location_id is None:
            group.location_id = individual.location_id
            group.save(user=self.user.user)
        else:
            individual.location_id = group.location_id
            individual.save(user=self.user.user)


    def _assure_primary_recipient_in_group(self, group):
        group_individuals = GroupIndividual.objects.filter(group=group, is_deleted=False)
        primary_exists = group_individuals.filter(recipient_type=GroupIndividual.RecipientType.PRIMARY).exists()
        head_exists = group_individuals.filter(role=GroupIndividual.Role.HEAD).exists()

        if primary_exists:
            return

        new_primary = group_individuals.first()

        if not new_primary:
            return

        new_primary.recipient_type = GroupIndividual.RecipientType.PRIMARY
        if not head_exists:
            new_primary.role = GroupIndividual.Role.HEAD
        new_primary.save(user=self.user.user)

    def _change_head(self, group_individual_id, group_id):
        heads_queryset = GroupIndividual.objects.filter(group_id=group_id, role=GroupIndividual.Role.HEAD)
        old_head = heads_queryset.exclude(id=group_individual_id).first()

        if not old_head:
            return

        old_head.role = None
        old_head.save(user=self.user.user)

    def _change_primary(self, group_individual_id, group_id):
        primaries_queryset = GroupIndividual.objects.filter(
            group_id=group_id, recipient_type=GroupIndividual.RecipientType.PRIMARY
        )
        old_primary = primaries_queryset.exclude(id=group_individual_id).first()

        if not old_primary:
            return

        old_primary.recipient_type = None
        old_primary.save(user=self.user.user)


class IndividualImportService:
    import_loaders = {
        # .csv
        'text/csv': lambda f: pd.read_csv(f),
        # .xlsx
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': lambda f: pd.read_excel(f),
        # .xls
        'application/vnd.ms-excel': lambda f: pd.read_excel(f),
        # .ods
        'application/vnd.oasis.opendocument.spreadsheet': lambda f: pd.read_excel(f),
    }

    def __init__(self, user):
        super().__init__()
        self.user = user

    @register_service_signal('individual.import_individuals')
    def import_individuals(self,
                           import_file: InMemoryUploadedFile,
                           workflow: WorkflowHandler,
                           group_aggregation_column: str):
        upload = self._save_sources(import_file)
        self._create_individual_data_upload_records(workflow, upload, group_aggregation_column)
        self._trigger_workflow(workflow, upload)
        return {'success': True, 'data': {'upload_uuid': upload.uuid}}

    @transaction.atomic
    def _save_sources(self, import_file):
        # Method separated as workflow execution must be independent of the atomic transaction.
        upload = self._create_upload_entry(import_file.name)
        dataframe = self._load_import_file(import_file)
        self._validate_dataframe(dataframe)
        self._save_data_source(dataframe, upload)
        return upload

    @transaction.atomic
    def _create_individual_data_upload_records(self, workflow, upload, group_aggregation_column):
        record = IndividualDataUploadRecords(
            data_upload=upload,
            workflow=workflow.name,
            json_ext={"group_aggregation_column": group_aggregation_column}
        )
        record.save(user=self.user.user)

    def validate_import_individuals(self, upload_id: uuid, individual_sources):
        dataframe = load_dataframe(individual_sources)
        validated_dataframe, invalid_items = self._validate_possible_individuals(
            dataframe,
            upload_id
        )
        return {'success': True, 'data': validated_dataframe, 'summary_invalid_items': invalid_items}

    def synchronize_data_for_reporting(self, upload_id: uuid):
        if 'opensearch_reports' in apps.app_configs:
            from individual.documents import IndividualDocument

            individuals = Individual.objects.filter(individualdatasource__upload=upload_id)
            if not individuals:
                return

            IndividualDocument().update(individuals, 'index')

    @staticmethod
    def process_chunk(
        chunk,
        properties,
        unique_validations,
        loc_name_code_district_ids_from_db,
        user_allowed_loc_ids,
        duplicate_village_name_code_tuples,
    ):
        validated_dataframe = []
        check_location = 'location_name' in chunk.columns

        for _, row in chunk.iterrows():
            field_validation = {'row': row.to_dict(), 'validations': {}}
            for field, field_properties in properties.items():

                # Validation Calculation
                if "validationCalculation" in field_properties and field in row:
                    field_validation['validations'][field] = IndividualImportService._handle_validation_calculation(row, field, field_properties)

                # Uniqueness Check
                if "uniqueness" in field_properties and field in row:
                    field_validation['validations'][f'{field}_uniqueness'] = IndividualImportService._handle_uniqueness(row, field, unique_validations)

            if 'location_name' in chunk.columns:
                field_validation['validations']['location_name'] = (
                    IndividualImportService._validate_location(
                        row.location_name,
                        row.location_code,
                        loc_name_code_district_ids_from_db,
                        user_allowed_loc_ids,
                        duplicate_village_name_code_tuples,
                    )
                )

            validated_dataframe.append(field_validation)

        return validated_dataframe

    def _validate_possible_individuals(self, dataframe: DataFrame, upload_id: uuid):
        schema_dict = json.loads(IndividualConfig.individual_schema)
        properties = schema_dict.get("properties", {})

        unique_fields = [field for field, props in properties.items() if "uniqueness" in props]
        unique_validations = {}
        if unique_fields:
            unique_validations = {
                field: dataframe[field].duplicated(keep=False) 
                for field in unique_fields
            }

        check_location = 'location_name' in dataframe.columns
        if check_location:
            # Issue a single DB query instead of per row for efficiency
            loc_name_code_district_ids_from_db = self._query_location_district_ids(dataframe)
            user_allowed_loc_ids = LocationManager().get_allowed_ids(self.user)
            duplicate_village_name_code_tuples = self._query_duplicate_village_name_code()
        else:
            loc_name_code_district_ids_from_db = None
            user_allowed_loc_ids = None
            duplicate_village_name_code_tuples = None

        # TODO: Use ProcessPoolExecutor after resolving django dependency loading issue
        validated_dataframe = IndividualImportService.process_chunk(
            dataframe,
            properties,
            unique_validations,
            loc_name_code_district_ids_from_db,
            user_allowed_loc_ids,
            duplicate_village_name_code_tuples,
        )

        self.save_validation_error_in_data_source_bulk(validated_dataframe)
        invalid_items = fetch_summary_of_broken_items(upload_id)
        return validated_dataframe, invalid_items

    @staticmethod
    def _query_location_district_ids(df):
        unique_tuples = df[['location_name', 'location_code']].drop_duplicates()
        query = Q()
        for _, row in unique_tuples.iterrows():
            query |= Q(name=row['location_name'], code=row['location_code'])
        locations = Location.objects.filter(type="V", *filter_validity()).filter(query)
        return {(loc.name, loc.code): loc.parent.parent.id for loc in locations}

    @staticmethod
    def _query_duplicate_village_name_code():
        return (
            Location.objects
            .filter(type="V", *filter_validity())
            .values('name', 'code')
            .annotate(name_count=Count('id'))
            .filter(name_count__gt=1)
            .values_list('name', 'code')
        )

    @staticmethod
    def _validate_location(
        location_name,
        location_code,
        loc_name_code_district_ids_from_db,
        user_allowed_loc_ids,
        duplicate_village_name_code_tuples
    ):
        result = {
            'field_name': 'location_name',
        }
        if (pd.isna(location_name) or location_name == "") and (pd.isna(location_code) or location_code == ""):
            result['success'] = True
        elif loc_name_code_district_ids_from_db is None and user_allowed_loc_ids is None:
            result['success'] = True
        elif (location_name, location_code) not in loc_name_code_district_ids_from_db:
            result['success'] = False
            result['note'] = f"Location with name '{location_name}' and code '{location_code}' is not valid. Please check the spelling against the list of locations in the system."
        elif (location_name, location_code) in duplicate_village_name_code_tuples:
            result['success'] = False
            result['note'] = f"Location with name '{location_name}' and code '{location_code}' is ambiguous, because there are more than one location with this name and code found in the system."
        elif loc_name_code_district_ids_from_db[(location_name, location_code)] not in user_allowed_loc_ids:
            result['success'] = False
            result['note'] = f"Location with name '{location_name}' and code '{location_code}' is outside the current user's location permissions."
        else:
            result['success'] = True
        return result


    @staticmethod
    def _handle_uniqueness(row, field, unique_validations):
        success = not unique_validations[field].loc[row.name]
        result = {
            "success": success,
            "field_name": field,
        }
        if not success:
            result["note"] = f"'{field}' Field value '{row[field]}' is duplicated"
        return result


    @staticmethod
    def _handle_validation_calculation(row, field, field_properties):
        validation_calculation = field_properties.get("validationCalculation", {}).get("name")
        if not validation_calculation:
            raise ValueError("Missing validation name")
        calculation_uuid = IndividualConfig.validation_calculation_uuid
        calculation = get_calculation_object(calculation_uuid)
        result_row = calculation.calculate_if_active_for_object(
            validation_calculation,
            calculation_uuid,
            field_name=field,
            field_value=row[field],
        )
        return result_row

    def _create_upload_entry(self, filename):
        upload = IndividualDataSourceUpload(source_name=filename, source_type='individual import')
        upload.save(username=self.user.login_name)
        return upload

    def _validate_dataframe(self, dataframe: pd.DataFrame):
        if dataframe is None:
            raise ValueError("Unknown error while loading import file")
        if dataframe.empty:
            raise ValueError("Import file is empty")

    def _load_import_file(self, import_file) -> pd.DataFrame:
        if import_file.content_type not in self.import_loaders:
            raise ValueError("Unsupported content type: {}".format(import_file.content_type))

        return self.import_loaders[import_file.content_type](import_file)

    def _save_data_source(self, dataframe: pd.DataFrame, upload: IndividualDataSourceUpload):
        data_source_objects = []
        
        for _, row in dataframe.iterrows():
            ds = IndividualDataSource(
                upload=upload,
                json_ext=json.loads(row.to_json()),
                validations={},
                user_created=self.user,
                user_updated=self.user,
                uuid=uuid.uuid4()
            )
            data_source_objects.append(ds)

        IndividualDataSource.objects.bulk_create(data_source_objects)

    def _trigger_workflow(self,
                          workflow: WorkflowHandler,
                          upload: IndividualDataSourceUpload):
        try:
            # Before the run in order to avoid racing conditions
            upload.status = IndividualDataSourceUpload.Status.TRIGGERED
            upload.save(username=self.user.login_name)

            result = workflow.run({
                # Core user UUID required
                'user_uuid': str(User.objects.get(username=self.user.login_name).id),
                'upload_uuid': str(upload.uuid),
            })

            # Conditions are safety measure for workflows. Usually handles like PythonHandler or LightningHandler
            #  should follow this pattern but return type is not determined in workflow.run abstract.
            if result and isinstance(result, dict) and result.get('success') is False:
                raise ValueError(result.get('message', 'Unexpected error during the workflow execution'))
        except ValueError as e:
            upload.status = IndividualDataSourceUpload.Status.FAIL
            upload.error = {'workflow': str(e)}
            upload.save(username=self.user.login_name)
            return upload

    def save_validation_error_in_data_source_bulk(self, validated_dataframe):
        data_sources_to_update = []

        for field_validation in validated_dataframe:
            row = field_validation['row']
            error_fields = []

            for key, value in field_validation['validations'].items():
                if not value.get('success', False):
                    error_fields.append({
                        "field_name": value.get('field_name'),
                        "note": value.get('note')
                    })

            data_sources_to_update.append(
                IndividualDataSource(
                    id=row['id'],
                    validations={'validation_errors': error_fields}
                )
            )

        if data_sources_to_update:
            IndividualDataSource.objects.bulk_update(data_sources_to_update, ['validations'])

    def create_task_with_importing_valid_items(self, upload_id: uuid):
        if IndividualConfig.enable_maker_checker_for_individual_upload:
            IndividualTaskCreatorService(self.user) \
                .create_task_with_importing_valid_items(upload_id)
        else:
            record = IndividualDataUploadRecords.objects.get(
                data_upload_id=upload_id,
                is_deleted=False
            )
            from individual.signals.on_validation_import_valid_items import IndividualItemsImportTaskCompletionEvent
            IndividualItemsImportTaskCompletionEvent(
                IndividualConfig.validation_import_valid_items_workflow,
                record,
                record.data_upload.id,
                self.user
            ).run_workflow()

    def create_task_with_update_valid_items(self, upload_id: uuid):
        # Resolve automatically if maker-checker not enabled
        if IndividualConfig.enable_maker_checker_for_individual_update:
            IndividualTaskCreatorService(self.user) \
                .create_task_with_update_valid_items(upload_id)
        else:
            record = IndividualDataUploadRecords.objects.get(
                data_upload_id=upload_id,
                is_deleted=False
            )
            from individual.signals.on_validation_import_valid_items import IndividualItemsUploadTaskCompletionEvent
            IndividualItemsUploadTaskCompletionEvent(
                IndividualConfig.validation_upload_valid_items_workflow,
                record,
                record.data_upload.id,
                self.user
            ).run_workflow()

class IndividualTaskCreatorService:

    def __init__(self, user):
        self.user = user

    def create_task_with_importing_valid_items(self, upload_id: uuid):
        self._create_task(upload_id, IndividualConfig.validation_import_valid_items)

    def create_task_with_update_valid_items(self, upload_id: uuid):
        self._create_task(upload_id, IndividualConfig.validation_upload_valid_items)

    @register_service_signal('individual.update_task')
    @transaction.atomic()
    def _create_task(self, upload_id, business_event):
        from tasks_management.services import TaskService
        from tasks_management.apps import TasksManagementConfig
        from tasks_management.models import Task
        upload_record = IndividualDataUploadRecords.objects.get(
            data_upload_id=upload_id,
            is_deleted=False
        )
        json_ext = {
            'source_name': upload_record.data_upload.source_name,
            'workflow': upload_record.workflow,
            'percentage_of_invalid_items': self.__calculate_percentage_of_invalid_items(upload_id),
            'data_upload_id': str(upload_id),
            'group_aggregation_column':
                upload_record.json_ext.get('group_aggregation_column')
                if isinstance(upload_record.json_ext, dict)
                else None,
        }
        TaskService(self.user).create({
            'source': 'import_valid_items',
            'entity': upload_record,
            'status': Task.Status.RECEIVED,
            'executor_action_event': TasksManagementConfig.default_executor_event,
            'business_event': business_event,
            'json_ext': json_ext
        })

        data_upload = upload_record.data_upload
        data_upload.status = IndividualDataSourceUpload.Status.WAITING_FOR_VERIFICATION
        data_upload.save(user=self.user.user)

    def __calculate_percentage_of_invalid_items(self, upload_id):
        number_of_valid_items = len(fetch_summary_of_valid_items(upload_id))
        number_of_invalid_items = len(fetch_summary_of_broken_items(upload_id))
        total_items = number_of_invalid_items + number_of_valid_items

        if total_items == 0:
            percentage_of_invalid_items = 0
        else:
            percentage_of_invalid_items = (number_of_invalid_items / total_items) * 100

        percentage_of_invalid_items = round(percentage_of_invalid_items, 2)
        return percentage_of_invalid_items
