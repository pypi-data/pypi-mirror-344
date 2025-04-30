import graphene
from django.utils.translation import gettext as _
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ValidationError
from django.db.models import Q

from core.gql.gql_mutations.base_mutation import BaseHistoryModelCreateMutationMixin, BaseMutation, \
    BaseHistoryModelUpdateMutationMixin, BaseHistoryModelDeleteMutationMixin
from core.schema import OpenIMISMutation
from invoice.apps import InvoiceConfig
from invoice.gql.input_types import CreateBillEventType, UpdateBillEventType
from invoice.models import BillEvent, BillEventMutation


class CreateBillEventMutation(BaseHistoryModelCreateMutationMixin, BaseMutation):
    _mutation_class = "CreateBillEventMutation"
    _mutation_module = "invoice"
    _model = BillEvent

    @classmethod
    def _mutate(cls, user, **data):
        client_mutation_id = data.get("client_mutation_id")
        if "client_mutation_id" in data:
            data.pop('client_mutation_id')
        if "client_mutation_label" in data:
            data.pop('client_mutation_label')
        p = cls.create_object(user=user, object_data=data)
        if p:
            BillEventMutation.object_mutated(
                user,
                client_mutation_id=client_mutation_id,
                bill_event=p
            )

    @classmethod
    def _validate_mutation(cls, user, **data):
        if type(user) is AnonymousUser or not user.id or not user.has_perms(
                InvoiceConfig.gql_bill_event_create_message_perms):
            raise PermissionError("Unauthorized")

    class Input(CreateBillEventType):
        pass


class DeleteUserBillEventMutation(BaseHistoryModelDeleteMutationMixin, BaseMutation):
    _mutation_class = "DeleteUserBillEventMutation"
    _mutation_module = "invoice"
    _model = BillEvent

    @classmethod
    def _validate_mutation(cls, user, **data):
        if type(user) is AnonymousUser or not user.id or not user.has_perms(
                InvoiceConfig.gql_bill_event_delete_my_message_perms):
            raise PermissionError("Unauthorized")

        objs_ = cls._model.objects.filter(id=data['uuids'])
        not_created_by_user = objs_.filter(~Q(user_created=user))
        if not_created_by_user.exists():
            raise PermissionError(
                _(F"User is not creator of bill events: %(events)s, events can't be deleted.")
                % {'events': str(not_created_by_user.values_list('uuid', flat=True))}
            )

    class Input(OpenIMISMutation.Input):
        uuids = graphene.List(graphene.UUID)
