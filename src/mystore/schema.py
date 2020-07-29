import graphene

import accounts.schema
import profiles.schema
import shopping.schema
import order.schema

class Query(
    accounts.schema.Query,
    profiles.schema.Query,
    shopping.schema.Query,
    order.schema.Query,
    graphene.ObjectType
): pass

class Mutation(
    accounts.schema.Mutation,
    profiles.schema.Mutation,
    shopping.schema.Mutation,
    order.schema.Mutation,
    graphene.ObjectType
): pass

schema = graphene.Schema(query=Query, mutation=Mutation)