import graphene

from .queries import (
    StoreQuery,
    VisitQuery,
    SubscriptionQuery,
    RecruitmentRequestQuery,
    ProductQuery,
    RatingQuery,
    ProductPictureQuery,
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

    CreateProductPictureMutation,
    UpdateProductPictureMutation,
    DeleteProductPictureMutation,

    DeleteCartMutation,

    CreateCartProductMutation,
    UpdateCartProductMutation,
    DeleteCartProductMutation,

    CreateRatingMutation,
)

class Query(
    StoreQuery,
    VisitQuery,
    SubscriptionQuery,
    RecruitmentRequestQuery,
    ProductQuery,
    RatingQuery,
    ProductPictureQuery,
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

    create_product_picture = CreateProductPictureMutation.Field()
    update_product_picture = UpdateProductPictureMutation.Field()
    delete_product_picture = DeleteProductPictureMutation.Field()

    delete_cart = DeleteCartMutation.Field()

    create_cart_product = CreateCartProductMutation.Field()
    update_cart_product = UpdateCartProductMutation.Field()
    delete_cart_product = DeleteCartProductMutation.Field()

    create_rating_mutation = CreateRatingMutation.Field()
