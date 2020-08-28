import graphene
from graphene_django.filter import DjangoFilterConnectionField
from graphql_jwt.decorators import login_required

from ..models import Cart, CartProduct, Store

from .nodes import (
    StoreNode,
    VisitNode,
    SubscriptionNode,
    RecruitmentRequestNode,
    ProductNode,
    PriceNode,
    CartNode,
    CartProductNode,
)

class StoreQuery(graphene.ObjectType):
    store = graphene.relay.Node.Field(StoreNode)
    stores = DjangoFilterConnectionField(StoreNode)
    my_stores = DjangoFilterConnectionField(StoreNode)

    @login_required
    def resolve_my_stores(self, info, **kwargs):
        return Store.objects.filter(user=info.context.user)

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

class CartQuery(graphene.ObjectType):
    cart = graphene.relay.Node.Field(CartNode)
    carts = DjangoFilterConnectionField(CartNode)

    @login_required
    def resolve_carts(self, info, **kwargs):
        return Cart.objects.filter(user=info.context.user)

class CartProductQuery(graphene.ObjectType):
    cart_product = graphene.relay.Node.Field(CartProductNode)
    cart_products = DjangoFilterConnectionField(CartProductNode)

    @login_required
    def resolve_cart_products(self, info, **kwargs):
        return CartProduct.objects.filter(user=info.context.user)