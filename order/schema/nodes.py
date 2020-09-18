import graphene
from graphene_django.types import DjangoObjectType

from ..models import Order, OrderItem, Address, DiscountCode
from graphql_auth.schema import UserNode

class OrderNode(DjangoObjectType):
    pk = graphene.Int(source='pk')
    total = graphene.String(source='total')
    user = graphene.Field(UserNode)

    def resolve_user(self, info, **kwargs):
        return self.user

    class Meta:
        model = Order
        filter_fields = {
            'store__id': ['exact']
        }
        interfaces = (graphene.relay.Node,)

class OrderItemNode(DjangoObjectType):
    pk = graphene.Int(source='pk')
    cost = graphene.String(source='cost')

    class Meta:
        model = OrderItem
        filter_fields = ('id',)
        interfaces = (graphene.relay.Node,)

class AddressNode(DjangoObjectType):
    pk = graphene.Int(source='pk')
    formatted = graphene.String(source='formatted')
    country_name = graphene.String()

    def resolve_country_name(self, info, **kwargs):
        return self.country.name

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
            'code': ['exact'],
            'store__id': ['exact']
        }
        interfaces = (graphene.relay.Node,)