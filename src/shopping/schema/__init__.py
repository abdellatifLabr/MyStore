import graphene

from .queries import (
    StoreQuery,
    VisitQuery,
    SubscriptionQuery,
    RecruitmentRequestQuery,
    ProductQuery,
    PriceQuery,
    CartQuery,
    CartProductQuery,
)

from .mutations import (
    CreateStoreMutation,
    UpdateStoreMutation,
    DeleteStoreMutation,

    CreateVisitMutation,

    CreateSubscriptionMutation,
    DeleteSubscriptionMutation,

    CreateRecruitmentRequestMutation,
    UpdateRecruitmentRequestMutation,
    DeleteRecruitmentRequestMutation,

    CreateProductMutation,
    UpdateProductMutation,
    DeleteProductMutation,

    CreatePriceMutation,
    UpdatePriceMutation,
    DeletePriceMutation,

    CreateCartMutation,
    DeleteCartMutation,

    CreateCartProductMutation,
    UpdateCartProductMutation,
    DeleteCartProductMutation,
)

class Query(
    StoreQuery,
    VisitQuery,
    SubscriptionQuery,
    RecruitmentRequestQuery,
    ProductQuery,
    PriceQuery,
    CartQuery,
    CartProductQuery,
    graphene.ObjectType
): pass

class Mutation(graphene.ObjectType):
    create_store = CreateStoreMutation.Field()
    update_store = UpdateStoreMutation.Field()
    delete_store = DeleteStoreMutation.Field()

    create_visit = CreateVisitMutation.Field()

    create_subscription = CreateSubscriptionMutation.Field()
    delete_subscription = DeleteSubscriptionMutation.Field()

    create_recruitment_request = CreateRecruitmentRequestMutation.Field()
    update_recruitment_request = UpdateRecruitmentRequestMutation.Field()
    delete_recruitment_request = DeleteRecruitmentRequestMutation.Field()

    create_product = CreateProductMutation.Field()
    update_product = UpdateProductMutation.Field()
    delete_product = DeleteProductMutation.Field()

    create_price = CreatePriceMutation.Field()
    update_price = UpdatePriceMutation.Field()
    delete_price = DeletePriceMutation.Field()

    create_cart = CreateCartMutation.Field()
    delete_cart = DeleteCartMutation.Field()

    create_cart_product = CreateCartProductMutation.Field()
    update_cart_product = UpdateCartProductMutation.Field()
    delete_cart_product = DeleteCartProductMutation.Field()
