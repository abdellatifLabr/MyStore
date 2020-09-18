import graphene
from graphene_django.filter import DjangoFilterConnectionField
from graphql_jwt.decorators import login_required

from .nodes import ProfileNode
from ..models import Profile

class ProfileQuery(graphene.ObjectType):
    profile = graphene.relay.Node.Field(ProfileNode)
    my_profile = graphene.Field(ProfileNode)
    profiles = DjangoFilterConnectionField(ProfileNode)

    @login_required
    def resolve_my_profile(self, info, **kwargs):
        return Profile.objects.get(user=info.context.user)
