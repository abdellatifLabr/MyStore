import graphene
from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from django.contrib.contenttypes.models import ContentType

from ..models import Notification, NotificationType, NotificationSource

class ContentTypeNode(DjangoObjectType):
    class Meta:
        model = ContentType

class NotificationTypeNode(DjangoObjectType):
    pk = graphene.Int(source='pk')

    class Meta:
        model = NotificationType
        filter_fields = ('id',)
        interfaces = (graphene.relay.Node,)


class NotificationSourceNode(DjangoObjectType):
    content_type = graphene.Field(ContentTypeNode)

    class Meta:
        model = NotificationSource
        interfaces = (graphene.relay.Node,)


class NotificationNode(DjangoObjectType):
    pk = graphene.Int(source='pk')
    time_ago = graphene.String(source='time_ago')
    source = graphene.Field(NotificationSourceNode)

    def resolve_source(self, info, **kwargs):
        return self.source

    class Meta:
        model = Notification
        filter_fields = ('id', 'user')
        interfaces = (graphene.relay.Node,)
