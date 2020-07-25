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
        profileForm = ProfileForm(kwargs, instance=profile)

        if profileForm.is_valid():
            profileForm.save()
            return UpdateProfileMutation(profile=profile, success=True)
        
        return UpdateProfileMutation(profile=None, success=False, errors=profileForm.errors.get_json_data())
