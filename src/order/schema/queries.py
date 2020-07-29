import graphene
from graphene_django.filter import DjangoFilterConnectionField

from .nodes import OrderNode, OrderItemNode, AddressNode, DiscountCodeNode

class OrderQuery(graphene.ObjectType):
    order = graphene.relay.Node.Field(OrderNode)
    orders = DjangoFilterConnectionField(OrderNode)

class OrderItemQuery(graphene.ObjectType):
    order_item = graphene.relay.Node.Field(OrderItemNode)
    order_items = DjangoFilterConnectionField(OrderItemNode)

class AddressQuery(graphene.ObjectType):
    address = graphene.relay.Node.Field(AddressNode)
    addresses = DjangoFilterConnectionField(AddressNode)

class DiscountCodeQuery(graphene.ObjectType):
    discount_code = graphene.relay.Node.Field(DiscountCodeNode)
    discount_codes = DjangoFilterConnectionField(DiscountCodeNode)
