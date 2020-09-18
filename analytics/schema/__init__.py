import graphene

from .queries import AnalyticsQuery

class Query(
    AnalyticsQuery,
    graphene.ObjectType
): pass

class Mutation(graphene.ObjectType):
    pass
