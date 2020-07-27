import graphene
from graphene_django.types import DjangoObjectType

from ..models import Store, Visit, Subscription, RecruitmentRequest, Product, Price, Cart
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
        filter_fields = ('id', 'user')
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
