import graphene
from graphene_django.filter import DjangoFilterConnectionField

from .nodes import AnalyticsNode

class AnalyticsQuery(graphene.ObjectType):
    analytics = graphene.relay.Node.Field(AnalyticsNode)
