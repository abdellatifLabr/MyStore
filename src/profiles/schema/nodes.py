import graphene
from graphene_django.types import DjangoObjectType

from ..models import Profile

class ProfileNode(DjangoObjectType):
    pk = graphene.Int(source='pk')
    
    class Meta:
        model = Profile
        filter_fields = ('id',)
        interfaces = (graphene.relay.Node,)
    
