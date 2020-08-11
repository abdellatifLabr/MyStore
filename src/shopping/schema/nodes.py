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
    Price, 
    Cart,
)
from graphql_auth.schema import UserNode

class StoreNode(DjangoObjectType):
    pk = graphene.Int(source='pk')
    workers = graphene.List(UserNode)

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

class StoreCoverNode(DjangoObjectType):
    mobile = graphene.String()

    class Meta:
        model = StoreCover
    
    def resolve_original(self, info, **kwargs):
        return info.context.build_absolute_uri(self.original.url)

    def resolve_mobile(self, info, **kwargs):
        return info.context.build_absolute_uri(self.mobile.url)
    
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
    
    class Meta:
        model = Product
        filter_fields = ('id',)
        interfaces = (graphene.relay.Node,)

class ProductPictureNode(DjangoObjectType):
    class Meta:
        model = ProductPicture
    
    def resolve_original(self, info, **kwargs):
        return info.context.build_absolute_uri(self.original.url)

class PriceNode(DjangoObjectType):
    pk = graphene.Int(source='pk')
    
    class Meta:
        model = Price
        filter_fields = ('id',)
        interfaces = (graphene.relay.Node,)

class CartNode(DjangoObjectType):
    pk = graphene.Int(source='pk')
    products = graphene.List(ProductNode)

    def resolve_products(self, info, **kwargs):
        return self.products.all()

    class Meta:
        model = Cart
        filter_fields = ('id', 'user')
        interfaces = (graphene.relay.Node,)
