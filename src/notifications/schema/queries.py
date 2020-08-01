import graphene
from graphene_django.filter import DjangoFilterConnectionField

from .nodes import NotificationNode

class NotificationQuery(graphene.ObjectType):
    notification = graphene.relay.Node.Field(NotificationNode)
    notifications = DjangoFilterConnectionField(NotificationNode)
