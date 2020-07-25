import graphene
from graphene_django.filter import DjangoFilterConnectionField

from .nodes import ProfileNode

class ProfileQuery(graphene.ObjectType):
    profile = graphene.relay.Node.Field(ProfileNode)
    profiles = DjangoFilterConnectionField(ProfileNode)
