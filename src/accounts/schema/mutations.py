import graphene
from graphql_jwt.decorators import login_required
from graphql_auth.types import ExpectedErrorType
from django.contrib.auth import get_user_model

from ..forms import UpdateUserForm

class UpdateUserMutation(graphene.relay.ClientIDMutation):
    class Input:
        username = graphene.String()
        email = graphene.String()
        first_name = graphene.String()
        last_name = graphene.String()
    
    success = graphene.Boolean()
    errors = graphene.Field(ExpectedErrorType)
    
    @login_required
    def mutate_and_get_payload(self, info, **kwargs):
        user = info.context.user
        user_update_form = UpdateUserForm(kwargs, instance=user)

        if not user_update_form.is_valid():
            return UpdateUserMutation(success=False, errors=user_update_form.errors.get_json_data())
        
        user = user_update_form.save(commit=False)
        fields_to_update = list(filter(lambda field: kwargs[field] is not None, kwargs.keys()))
        user.save(update_fields=fields_to_update)
        return UpdateUserMutation(success=True)
