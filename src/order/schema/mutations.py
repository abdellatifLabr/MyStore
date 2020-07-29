import graphene
from graphql_jwt.decorators import login_required
from graphql_auth.types import ExpectedErrorType

from core.constants import Messages
from ..models import Order, OrderItem, Address, DiscountCode
from shopping.models import Store, Product
from ..forms import AddressForm, UpdateAddressForm, DiscountCodeForm, UpdateDiscountCodeForm
from .nodes import OrderNode, OrderItemNode, AddressNode, DiscountCodeNode

class CreateAddressMutation(graphene.relay.ClientIDMutation):
    class Input:
        country = graphene.String(required=True)
        city = graphene.String(required=True)
        street = graphene.String(required=True)
        postal_code = graphene.String(required=True)
    
    address = graphene.Field(AddressNode)
    success = graphene.Boolean()
    errors = graphene.Field(ExpectedErrorType)

    @login_required
    def mutate_and_get_payload(self, info, **kwargs):
        address = Address(user=info.context.user)
        address_form = AddressForm(kwargs, instance=address)

        if not address_form.is_valid():
            return CreateAddressMutation(success=False, errors=address_form.errors.get_json_data())
        
        address_form.save()
        return CreateAddressMutation(address=address, success=True)

class UpdateAddressMutation(graphene.relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)     
        country = graphene.String()
        city = graphene.String()
        street = graphene.String()
        postal_code = graphene.String()

    address = graphene.Field(AddressNode)
    success = graphene.Boolean()
    errors = graphene.Field(ExpectedErrorType)
    
    @login_required
    def mutate_and_get_payload(self, info, id=None, **kwargs):
        address = Address.objects.get(pk=id)

        is_owner = info.context.user == address.user
        has_permission = is_owner

        if not has_permission:
            return UpdateAddressMutation(success=False, errors=[Messages.NO_PERMISSION])

        update_address_form = UpdateAddressForm(kwargs, instance=address)

        if not update_address_form.is_valid():
            return CreateAddressMutation(success=False, errors=update_address_form.errors.get_json_data())
        
        address = update_address_form.save(commit=False)
        address.save(update_fields=list(kwargs.keys()))
        return UpdateAddressMutation(address=address, success=True)

class DeleteAddressMutation(graphene.relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)
    
    success = graphene.Boolean()

    @login_required
    def mutate_and_get_payload(self, info, id=None, **kwargs):
        address = Address.objects.get(pk=id)

        is_owner = info.context.user == address.user
        has_permission = is_owner

        if not has_permission:
            return DeleteAddressMutation(success=False, errors=[Messages.NO_PERMISSION])
            
        address.delete()
        return DeleteAddressMutation(success=False)


class CreateDiscountCodeMutation(graphene.relay.ClientIDMutation):
    class Input:
        code = graphene.String(required=True)
        value = graphene.String(required=True)
        expiry = graphene.DateTime(required=True)
        store_id = graphene.ID(required=True)
    
    discount_code = graphene.Field(DiscountCodeNode)
    success = graphene.Boolean()
    errors = graphene.Field(ExpectedErrorType)

    @login_required
    def mutate_and_get_payload(self, info, **kwargs):
        store = Store.objects.get(pk=store_id)

        is_owner = info.context.user == store.user
        is_worker = info.context.user in store.workers.iterator()
        has_permission = is_owner or is_worker

        if not has_permission:
            raise PermissionError('You don\'t have the permission to perform this action')
        
        discount_code = DiscountCode(user=info.context.user, store=store)
        discount_code_form = DiscountCodeForm(kwargs, instance=discount_code)

        if not discount_code_form.is_valid():
            return CreateDiscountCodeMutation(success=False, errors=discount_code_form.errors.get_json_data())
        
        discount_code_form.save()
        return CreateDiscountCodeMutation(discount_code=discount_code, success=True)

class UpdateDiscountCodeMutation(graphene.relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)     
        code = graphene.String()
        value = graphene.String()
        expiry = graphene.DateTime()

    discount_code = graphene.Field(DiscountCodeNode)
    success = graphene.Boolean()
    errors = graphene.Field(ExpectedErrorType)
    
    @login_required
    def mutate_and_get_payload(self, info, id=None, **kwargs):
        discount_code = DiscountCode.objects.get(pk=id)

        is_owner = info.context.user == discount_code.store.user
        is_worker = info.context.user in discount_code.store.workers.iterator()
        has_permission = (is_owner or is_worker) and not discount_code.expired

        if not has_permission:
            return UpdateDiscountCodeMutation(success=False, errors=[Messages.NO_PERMISSION])

        update_discount_code_form = UpdateDiscountCodeForm(kwargs, instance=discount_code)

        if not update_discount_code_form.is_valid():
            return UpdateDiscountCodeMutation(success=False, errors=update_discount_code_form.errors.get_json_data())
        
        discount_code = update_discount_code_form.save(commit=False)
        discount_code.save(update_fields=list(kwargs.keys()))
        return UpdateAddressMutation(discount_code=discount_code, success=True)

class DeleteDiscountCodeMutation(graphene.relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)
    
    success = graphene.Boolean()

    @login_required
    def mutate_and_get_payload(self, info, id=None, **kwargs):
        discount_code = DiscountCode.objects.get(pk=id)

        is_owner = info.context.user == discount_code.store.user
        is_worker = info.context.user in discount_code.store.workers.iterator()
        has_permission = is_owner

        if not has_permission:
            return DeleteDiscountCodeMutation(success=False, errors=[Messages.NO_PERMISSION])
            
        discount_code.delete()
        return DeleteDiscountCodeMutation(success=False)


class CreateOrderMutation(graphene.relay.ClientIDMutation):
    class Input:
        shipping_address_id = graphene.ID(required=True) 
        billing_address_id = graphene.ID(required=True)
        discount_code_id = graphene.ID(required=True)
    
    order = graphene.Field(OrderNode)
    success = graphene.Boolean()

    def mutate_and_get_payload(self, info, **kwargs):
        shipping_address = Address.objects.get(pk=kwargs.get('shipping_address_id'))
        billing_address = Address.objects.get(pk=kwargs.get('billing_address_id'))
        discount_code_id = DiscountCode.objects.get(pk=kwargs.get('discount_code_id'))

        is_owner = info.context.user == shipping_address.user and info.context.user == billing_address.user
        has_permission = is_owner

        if not has_permission:
            raise PermissionError('You don\'t have the permission to perform this action')
            
        order = Order.objects.create(
            user=info.context.user,
            shipping_address=shipping_address,
            billing_address=billing_address,
            discount_code=discount_code
        )
        return CreateOrderMutation(order=order, success=True)

class UpdateOrderMutation(graphene.relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)
        done = graphene.Boolean(default_value=False)
        shipping_address_id = graphene.ID() 
        billing_address_id = graphene.ID()
        discount_code_id = graphene.ID()
    
    order = graphene.Field(OrderNode)
    success = graphene.Boolean()

    def mutate_and_get_payload(self, info, id=None, **kwargs):
        order = Order.objects.get(pk=id)

        is_owner = info.context.user == order.user
        has_permission = is_owner

        if not has_permission:
            return UpdateOrderMutation(success=False, errors=[Messages.NO_PERMISSION])
            
        for field, value in kwargs.items():
            setattr(order, field, value)
        
        order.save()
        return CreateOrderMutation(order=order, success=True)

class DeleteOrderMutation(graphene.relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate_and_get_payload(self, info, id=None, **kwargs):
        order = Order.objects.get(pk=id)

        is_owner = info.context.user == order.user
        has_permission = is_owner and not order.done

        if not has_permission:
            return DeleteOrderMutation(success=False, errors=[Messages.NO_PERMISSION])

        order.delete()
        return DeleteOrderMutation(success=True)


class CreateOrderItemMutation(graphene.relay.ClientIDMutation):
    class Input:
        quantity = graphene.Int(required=True)
        product_id = graphene.ID(required=True)
        order_id = graphene.ID(required=True)
    
    order_item = graphene.Field(OrderItemNode)
    success = graphene.Boolean()
    errors = graphene.Field(ExpectedErrorType)

    def mutate_and_get_payload(self, info, **kwargs):
        product = Product.objects.get(pk=kwargs.get('product_id'))
        order = Order.objects.get(pk=kwargs.get('order_id'))

        is_owner = info.context.user == order.user
        has_permission = is_owner and not order.done

        if not has_permission:
            return CreateOrderItemMutation(success=False, errors=[Messages.NO_PERMISSION])

        order_item = OrderItem.objects.create(order=order, product=product, quantity=quantity)
        return CreateOrderMutation(order_item=order_item, success=True)

class UpdateOrderItemMutation(graphene.relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)
        quantity = graphene.Int()

    order_item = graphene.Field(OrderItemNode)
    success = graphene.Boolean()

    def mutate_and_get_payload(self, info, id=None, **kwargs):
        order_item = OrderItem.objects.get(pk=id)

        is_owner = info.context.user == order_item.order.user
        has_permission = is_owner and not order_item.order.done

        if not has_permission:
            return UpdateOrderItemMutation(success=False, errors=[Messages.NO_PERMISSION])

        for field, value in kwargs.items():
            setattr(order_item, field, value)
        
        order_item.save()
        return UpdateOrderItemMutation(order_item=order_item, success=True)

class DeleteOrderItemMutation(graphene.relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate_and_get_payload(self, info, id=None, **kwargs):
        order_item = OrderItem.objects.get(pk=id)

        is_owner = info.context.user == order_item.order.user
        has_permission = is_owner and not order_item.order.done

        if not has_permission:
            return DeleteOrderItemMutation(success=False, errors=[Messages.NO_PERMISSION])

        order_item.delete()
        return DeleteOrderItemMutation(success=True)


