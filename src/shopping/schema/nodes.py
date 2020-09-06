from decimal import Decimal

import graphene
from graphene_django.types import DjangoObjectType

from ..models import (
    Store, 
    StoreLogo,
    StoreCover,
    Visit, 
    Subscription, 
    RecruitmentRequest, 
    Product, 
    ProductPicture,
    Cart,
    CartProduct,
)
from graphql_auth.schema import UserNode

class StoreNode(DjangoObjectType):
    pk = graphene.Int(source='pk')
    workers = graphene.List(UserNode)
    user = graphene.Field(UserNode)
    shipping = graphene.String(source='shipping')

    def resolve_user(self, info, **kwargs):
        return self.user

    def resolve_workers(self, info, **kwargs):
        return self.workers.all()
    
    class Meta:
        model = Store
        filter_fields = ('id', 'user')
        interfaces = (graphene.relay.Node,)

class StoreLogoNode(DjangoObjectType):
    thumbnail = graphene.String()
    desktop = graphene.String()
    mobile = graphene.String()
    width = graphene.Int()
    height = graphene.Int()

    class Meta:
        model = StoreLogo
    
    def resolve_original(self, info, **kwargs):
        return info.context.build_absolute_uri(self.original.url)

    def resolve_thumbnail(self, info, **kwargs):
        return info.context.build_absolute_uri(self.thumbnail.url)
    
    def resolve_desktop(self, info, **kwargs):
        return info.context.build_absolute_uri(self.desktop.url)
    
    def resolve_mobile(self, info, **kwargs):
        return info.context.build_absolute_uri(self.mobile.url)
    
    def resolve_width(self, info, **kwargs):
        return self.original.width
    
    def resolve_height(self, info, **kwargs):
        return self.original.height

class StoreCoverNode(DjangoObjectType):
    mobile = graphene.String()
    width = graphene.Int()
    height = graphene.Int()

    class Meta:
        model = StoreCover
    
    def resolve_original(self, info, **kwargs):
        return info.context.build_absolute_uri(self.original.url)

    def resolve_mobile(self, info, **kwargs):
        return info.context.build_absolute_uri(self.mobile.url)
    
    def resolve_width(self, info, **kwargs):
        return self.original.width
    
    def resolve_height(self, info, **kwargs):
        return self.original.height
    
class VisitNode(DjangoObjectType):
    pk = graphene.Int(source='pk')
    
    class Meta:
        model = Visit
        filter_fields = ('id', 'user')
        interfaces = (graphene.relay.Node,)

class SubscriptionNode(DjangoObjectType):
    pk = graphene.Int(source='pk')
    
    class Meta:
        model = Subscription
        filter_fields = {
            'store__id': ['exact']
        }
        interfaces = (graphene.relay.Node,)

class RecruitmentRequestNode(DjangoObjectType):
    pk = graphene.Int(source='pk')
    
    class Meta:
        model = RecruitmentRequest
        filter_fields = ('id', 'user')
        interfaces = (graphene.relay.Node,)

class ProductNode(DjangoObjectType):
    pk = graphene.Int(source='pk')
    price = graphene.String(source='price')
    units_left = graphene.Int(source='units_left')
    
    class Meta:
        model = Product
        filter_fields = {
            'store__id': ['exact'],
            'name': ['icontains'],
            #'description': ['icontains']
        }
        interfaces = (graphene.relay.Node,)

class ProductPictureNode(DjangoObjectType):
    pk = graphene.Int(source='pk')
    width = graphene.Int()
    height = graphene.Int()

    class Meta:
        model = ProductPicture
        filter_fields = {
            'product__id': ['exact']
        }
        interfaces = (graphene.relay.Node,)
    
    def resolve_original(self, info, **kwargs):
        return info.context.build_absolute_uri(self.original.url)
    
    def resolve_width(self, info, **kwargs):
        return self.original.width
    
    def resolve_height(self, info, **kwargs):
        return self.original.height

class CartNode(DjangoObjectType):
    pk = graphene.Int(source='pk')
    total = graphene.String(source='total')

    class Meta:
        model = Cart
        filter_fields = {
            'user__id': ['exact']
        }
        interfaces = (graphene.relay.Node,)

class CartProductNode(DjangoObjectType):
    pk = graphene.Int(source='pk')
    cost = graphene.String(source='cost')

    class Meta:
        model = CartProduct
        filter_fields = {
            'cart__id': ['exact']
        }
        interfaces = (graphene.relay.Node,)
        