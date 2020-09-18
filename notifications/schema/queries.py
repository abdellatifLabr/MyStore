import graphene
from graphene_django.filter import DjangoFilterConnectionField

from .nodes import NotificationNode, NotificationTypeNode, NotificationSourceNode

class NotificationQuery(graphene.ObjectType):
    notification = graphene.relay.Node.Field(NotificationNode)
    notifications = DjangoFilterConnectionField(NotificationNode)

class NotificationSourceQuery(graphene.ObjectType):
    notification_source = graphene.relay.node.Field(NotificationSourceNode)
    notification_sources = DjangoFilterConnectionField(NotificationSourceNode)

class NotificationTypeQuery(graphene.ObjectType):
    notification_type = graphene.relay.Node.Field(NotificationTypeNode)
    notification_types = DjangoFilterConnectionField(NotificationTypeNode)
