import graphene
from graphene_django.filter import DjangoFilterConnectionField
from graphql_jwt.decorators import login_required

from .nodes import OrderNode, OrderItemNode, AddressNode, DiscountCodeNode
from ..models import Address

class OrderQuery(graphene.ObjectType):
    order = graphene.relay.Node.Field(OrderNode)
    orders = DjangoFilterConnectionField(OrderNode)

class OrderItemQuery(graphene.ObjectType):
    order_item = graphene.relay.Node.Field(OrderItemNode)
    order_items = DjangoFilterConnectionField(OrderItemNode)

class AddressQuery(graphene.ObjectType):
    address = graphene.relay.Node.Field(AddressNode)
    addresses = DjangoFilterConnectionField(AddressNode)
    my_addresses = DjangoFilterConnectionField(AddressNode)

    @login_required
    def resolve_my_addresses(self, info, **kwargs):
        return Address.objects.filter(user=info.context.user)

class DiscountCodeQuery(graphene.ObjectType):
    discount_code = graphene.relay.Node.Field(DiscountCodeNode)
    discount_codes = DjangoFilterConnectionField(DiscountCodeNode)
