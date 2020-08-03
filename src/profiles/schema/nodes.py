import graphene
from graphene_django.types import DjangoObjectType

from ..models import Profile, Avatar

class ProfileNode(DjangoObjectType):
    pk = graphene.Int(source='pk')
    
    class Meta:
        model = Profile
        filter_fields = ('id',)
        interfaces = (graphene.relay.Node,)

class AvatarNode(DjangoObjectType):
    thumbnail = graphene.String()
    desktop = graphene.String()
    mobile = graphene.String()

    class Meta:
        model = Avatar
    
    def resolve_original(self, info, **kwargs):
        return info.context.build_absolute_uri(self.original.url)

    def resolve_thumbnail(self, info, **kwargs):
        return info.context.build_absolute_uri(self.thumbnail.url)
    
    def resolve_desktop(self, info, **kwargs):
        return info.context.build_absolute_uri(self.desktop.url)
    
    def resolve_mobile(self, info, **kwargs):
        return info.context.build_absolute_uri(self.mobile.url)
    
