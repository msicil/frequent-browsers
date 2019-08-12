import graphene

import frequentbrowsers.schema


class Query(frequentbrowsers.schema.Query, graphene.ObjectType):
    pass


class Mutation(frequentbrowsers.schema.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
