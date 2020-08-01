import graphene
from graphene_django.types import DjangoObjectType

from ..models import Notification

class NotificationNode(DjangoObjectType):
    class Meta:
        model = Notification
        filter_fields = ('id', 'user')
        interfaces = (graphene.relay.Node,)
