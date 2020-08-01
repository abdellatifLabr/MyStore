import graphene

from .queries import NotificationQuery

class Query(
    NotificationQuery,
    graphene.ObjectType
): pass

class Mutation(graphene.ObjectType):
    pass
