import graphene

import accounts.schema
import profiles.schema

class Query(
    accounts.schema.Query,
    profiles.schema.Query,
    graphene.ObjectType
): pass

class Mutation(
    accounts.schema.Mutation,
    profiles.schema.Mutation,
    graphene.ObjectType
): pass

schema = graphene.Schema(query=Query, mutation=Mutation)