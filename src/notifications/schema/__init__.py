import graphene

from .queries import NotificationQuery, NotificationTypeQuery

class Query(
    NotificationQuery,
    NotificationTypeQuery,
    graphene.ObjectType
): pass

class Mutation(graphene.ObjectType):
    pass
