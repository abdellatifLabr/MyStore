import graphene
from graphene_django.types import DjangoObjectType

from ..models import Order, OrderItem, Address, DiscountCode

class OrderNode(DjangoObjectType):
    pk = graphene.Int(source='pk')
    total = graphene.Int(source='total')

    class Meta:
        model = Order
        filter_fields = ('id',)
        interfaces = (graphene.relay.Node,)

class OrderItemNode(DjangoObjectType):
    pk = graphene.Int(source='pk')
    cost = graphene.Int(source='cost')

    class Meta:
        model = OrderItem
        filter_fields = ('id',)
        interfaces = (graphene.relay.Node,)

class AddressNode(DjangoObjectType):
    pk = graphene.Int(source='pk')

    class Meta:
        model = Address
        filter_fields = ('id',)
        interfaces = (graphene.relay.Node,)

class DiscountCodeNode(DjangoObjectType):
    pk = graphene.Int(source='pk')
    expired = graphene.Boolean(source='expired')

    class Meta:
        model = DiscountCode
        filter_fields = {
            'code': ['exact']
        }
        interfaces = (graphene.relay.Node,)