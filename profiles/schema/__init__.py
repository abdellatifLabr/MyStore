import graphene

from .queries import ProfileQuery
from .mutations import UpdateProfileMutation

class Query(
    ProfileQuery,
    graphene.ObjectType
): pass

class Mutation(graphene.ObjectType):
    update_profile = UpdateProfileMutation.Field()
