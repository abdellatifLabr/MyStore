import graphene

from .queries import (
    OrderQuery,
    OrderItemQuery,
    AddressQuery,
    DiscountCodeQuery,
)

from .mutations import (
    CreateAddressMutation,
    UpdateAddressMutation,
    DeleteAddressMutation,

    CreateDiscountCodeMutation,
    UpdateDiscountCodeMutation,
    DeleteDiscountCodeMutation,

    CreateOrderMutation,
    UpdateOrderMutation,
    DeleteOrderMutation,

    CreateOrderItemMutation,
    UpdateOrderItemMutation,
    DeleteOrderItemMutation,
)

class Query(
    OrderQuery,
    OrderItemQuery,
    AddressQuery,
    DiscountCodeQuery,
    graphene.ObjectType
): pass

class Mutation(graphene.ObjectType):
    create_address = CreateAddressMutation.Field()
    update_address = UpdateAddressMutation.Field()
    delete_address = DeleteAddressMutation.Field()

    create_discount_code = CreateDiscountCodeMutation.Field()
    update_discount_code = UpdateDiscountCodeMutation.Field()
    delete_discount_code = DeleteDiscountCodeMutation.Field()

    create_order = CreateOrderMutation.Field()
    update_order = UpdateOrderMutation.Field()
    delete_order = DeleteOrderMutation.Field()

    create_order_item = CreateOrderItemMutation.Field()
    update_order_item = UpdateOrderItemMutation.Field()
    delete_order_item = DeleteOrderItemMutation.Field()
