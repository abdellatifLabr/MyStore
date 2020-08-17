import graphene
from graphene_django.filter import DjangoFilterConnectionField

from .nodes import (
    StoreNode,
    VisitNode,
    SubscriptionNode,
    RecruitmentRequestNode,
    ProductNode,
    PriceNode,
    CartProductNode,
)

class StoreQuery(graphene.ObjectType):
    store = graphene.relay.Node.Field(StoreNode)
    stores = DjangoFilterConnectionField(StoreNode)

class VisitQuery(graphene.ObjectType):
    visit = graphene.relay.Node.Field(VisitNode)
    visits = DjangoFilterConnectionField(VisitNode)

class SubscriptionQuery(graphene.ObjectType):
    subscription = graphene.relay.Node.Field(SubscriptionNode)
    subscriptions = DjangoFilterConnectionField(SubscriptionNode)

class RecruitmentRequestQuery(graphene.ObjectType):
    recruitment_request = graphene.relay.Node.Field(RecruitmentRequestNode)
    recruitment_requests = DjangoFilterConnectionField(RecruitmentRequestNode)

class ProductQuery(graphene.ObjectType):
    product = graphene.relay.Node.Field(ProductNode)
    products = DjangoFilterConnectionField(ProductNode)

class PriceQuery(graphene.ObjectType):
    price = graphene.relay.Node.Field(PriceNode)
    prices = DjangoFilterConnectionField(PriceNode)

class CartProductQuery(graphene.ObjectType):
    cart_product = graphene.relay.Node.Field(CartProductNode)
    cart_products = DjangoFilterConnectionField(CartProductNode)