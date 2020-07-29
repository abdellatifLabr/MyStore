import graphene
from graphql_auth.types import ExpectedErrorType
from graphql_jwt.decorators import login_required
from graphene_file_upload.scalars import Upload

from ..models import Profile
from ..forms import ProfileForm
from .nodes import ProfileNode

class UpdateProfileMutation(graphene.relay.ClientIDMutation):
    class Input:
        bio = graphene.String()
        phone = graphene.String()
        picture = Upload()
    
    profile = graphene.Field(ProfileNode)
    success = graphene.Boolean()
    errors = graphene.Field(ExpectedErrorType)

    @login_required
    def mutate_and_get_payload(self, info, **kwargs):
        profile = Profile.objects.get(user=info.context.user)
        profile_form = ProfileForm(kwargs, instance=profile)

        if not profile_form.is_valid():
            return UpdateProfileMutation(success=False, errors=profile_form.errors.get_json_data())

        profile_form.save()
        return UpdateProfileMutation(profile=profile, success=True)
