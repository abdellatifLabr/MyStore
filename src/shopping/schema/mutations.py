import graphene
from graphql_auth.types import ExpectedErrorType
from graphql_jwt.decorators import login_required
from graphene_file_upload.scalars import Upload

from ..models import (
    Store,
    Visit,
    Subscription,
    RecruitmentRequest,
    Product,
    Price,
    Cart,
)

from ..forms import (
    StoreForm,
    UpdateStoreForm,
    ProductForm,
    UpdateProductForm,
    PriceForm,
    UpdatePriceForm,
)

from .nodes import (
    StoreNode,
    VisitNode,
    SubscriptionNode,
    RecruitmentRequestNode,
    ProductNode,
    PriceNode,
    CartNode,
)

class CreateStoreMutation(graphene.relay.ClientIDMutation):
    class Input:
        name = graphene.String(required=True)
        description = graphene.String(required=True)
        logo = Upload()
        cover = Upload()
        closed = graphene.Boolean(default_value=False)
    
    store = graphene.Field(StoreNode)
    success = graphene.Boolean()
    errors = graphene.Field(ExpectedErrorType)

    @login_required
    def mutate_and_get_payload(self, info, **kwargs):
        store = Store(user=info.context.user)
        storeForm = StoreForm(kwargs, instance=store)

        if storeForm.is_valid():
            storeForm.save()
            return CreateStoreMutation(store=store, success=True)
        
        return CreateStoreMutation(store=None, success=False, errors=storeForm.errors.get_json_data())

class UpdateStoreMutation(graphene.relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)
        name = graphene.String()
        description = graphene.String()
        logo = Upload()
        cover = Upload()
        workers = graphene.List(graphene.ID)
        closed = graphene.Boolean()
    
    store = graphene.Field(StoreNode)
    success = graphene.Boolean()
    errors = graphene.Field(ExpectedErrorType)

    @login_required
    def mutate_and_get_payload(self, info, id=None, **kwargs):
        store = Store.objects.get(pk=id)

        is_owner = store.user == info.context.user
        has_permission = is_owner

        if not has_permission:
            raise PermissionError('You don\'t have the permission to perform this action')

        updateStoreForm = UpdateStoreForm(kwargs, instance=store)

        if not updateStoreForm.is_valid():
            return UpdateStoreMutation(success=False, errors=updateStoreForm.errors.get_json_data())

        updateStoreForm.save()
        return UpdateStoreMutation(store=store, success=True)
        
class DeleteStoreMutation(graphene.relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)
    
    success = graphene.Boolean()

    @login_required
    def mutate_and_get_payload(self, info, id=None, **kwargs):
        store = Store.objects.get(pk=id)
        if not store.user == info.context.user:
            raise PermissionError('You don\'t have the permission to perform this action')

        store.delete()
        return DeleteStoreMutation(success=True)


class CreateVisitMutation(graphene.relay.ClientIDMutation):
    class Input:
        store_id = graphene.ID(required=True)
    
    visit = graphene.Field(VisitNode)
    success = graphene.Boolean()

    @login_required
    def mutate_and_get_payload(self, info, store_id=None, **kwargs):
        visit = Visit.objects.create(user=info.context.user, store_id=store_id)
        return CreateVisitMutation(visit=visit, success=True)


class CreateSubscriptionMutation(graphene.relay.ClientIDMutation):
    class Input:
        store_id = graphene.ID(required=True)
    
    subscription = graphene.Field(SubscriptionNode)
    success = graphene.Boolean()

    @login_required
    def mutate_and_get_payload(self, info, store_id=None, **kwargs):
        sub = Subscription.objects.create(user=info.context.user, store_id=store_id)
        return CreateSubscriptionMutation(subscription=sub, success=True)

class DeleteSubscriptionMutation(graphene.relay.ClientIDMutation):
    class Input:
        subscription_id = graphene.ID(required=True)
    
    success = graphene.Boolean()

    @login_required
    def mutate_and_get_payload(self, info, subscription_id=None, **kwargs):
        sub = Subscription.objects.get(pk=subscription_id)
        sub.delete()
        return DeleteSubscriptionMutation(success=True)


class CreateRecruitmentRequestMutation(graphene.relay.ClientIDMutation):
    class Input:
        user_id = graphene.ID(required=True)
        store_id = graphene.ID(required=True)

    recruitment_request = graphene.Field(RecruitmentRequestNode)
    success = graphene.Boolean()

    @login_required
    def mutate_and_get_payload(self, info, **kwargs):
        store = Store.objects.get(pk=kwargs.get('store_id'))

        if not store.user == info.context.user:
            raise PermissionError('You don\'t have the permission to perform this action')
        
        recruitment_request = RecruitmentRequest.objects.create(**kwargs)
        return CreateRecruitmentRequestMutation(recruitment_request=recruitment_request, success=True)

class UpdateRecruitmentRequestMutation(graphene.relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)
        accepted = graphene.Boolean()

    recruitment_request = graphene.Field(RecruitmentRequestNode)
    success = graphene.Boolean()

    @login_required
    def mutate_and_get_payload(self, info, id=None, accepted=None, **kwargs):
        recruitment_request = RecruitmentRequest.objects.get(pk=id)

        is_owner = info.context.user == recruitment_request.user
        has_permission = is_owner

        if not has_permission:
            raise PermissionError('You don\'t have the permission to perform this action')
        
        if accepted:
            recruitment_request.accepted = True
            # send request accepted notification
        else:
            # send request declined notifiation
            pass

        return UpdateRecruitmentRequestMutation(recruitment_request=recruitment_request, success=True)

class DeleteRecruitmentRequestMutation(graphene.relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    @login_required
    def mutate_and_get_payload(self, info, id=None, **kwargs):
        recruitment_request = RecruitmentRequest.objects.get(pk=id)

        if not recruitment_request.store.user == info.context.user:
            raise PermissionError('You don\'t have the permission to perform this action')
        
        recruitment_request.delete()
        return DeleteRecruitmentRequestMutation(success=True)


class CreateProductMutation(graphene.relay.ClientIDMutation):
    class Input:
        name = graphene.String(required=True)
        description = graphene.String(required=True)
        picture = Upload(required=True)
        store_id = graphene.ID(required=True)
    
    product = graphene.Field(ProductNode)
    success = graphene.Boolean()
    errors = graphene.Field(ExpectedErrorType)

    @login_required
    def mutate_and_get_payload(self, info, sotre_id=None, **kwargs):
        store = Store.objects.get(pk=store_id)

        is_owner = info.context.user == store.user
        is_worker = info.context.user in store.workers.iterator()
        has_permission = is_worker or is_owner

        if not has_permission:
            raise PermissionError('You don\'t have the permission to perform this action')

        product = Product(store=store)
        productForm = ProductForm(kwargs, instance=product)

        if productForm.is_valid():
            productForm.save()
            return CreateProductMutation(product=product, success=True)
        
        return CreateProductMutation(product=None, success=False, errors=productForm.errors.get_json_data())

class UpdateProductMutation(graphene.relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)
        name = graphene.String()
        description = graphene.String()
        picture = Upload()
    
    product = graphene.Field(ProductNode)
    success = graphene.Boolean()
    errors = graphene.Field(ExpectedErrorType)

    @login_required
    def mutate_and_get_payload(self, info, id=None, **kwargs):
        product = Product.objects.get(pk=id)

        is_worker = info.context.user in product.store.workers.iterator()
        is_owner = info.context.user == product.store.user
        has_permission = is_owner or is_worker

        if not has_permission:
            raise PermissionError('You don\'t have the permission to perform this action')

        updateProductForm = UpdateProductForm(kwargs, instance=product)

        if not updateProductForm.is_valid():
            return UpdateProductMutation(success=False, errors=updateProductForm.errors.get_json_data())
        
        product = updateProductForm.save(commit=False)
        product.save(update_fields=list(kwargs.keys()))
        return UpdateProductMutation(product=product, success=True)
        
class DeleteProductMutation(graphene.relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)
    
    success = graphene.Boolean()

    @login_required
    def mutate_and_get_payload(self, info, id=None, **kwargs):
        product = Product.objects.get(pk=id)

        is_worker = info.context.user in product.store.workers
        is_owner = info.context.user == product.store.user
        has_permission = is_owner or is_worker

        if not has_permission:
            raise PermissionError('You don\'t have the permission to perform this action')

        product.delete()
        return DeleteProductMutation(success=True)


class CreatePriceMutation(graphene.relay.ClientIDMutation):
    class Input:
        value = graphene.Float(required=True)
        value_currency = graphene.String(required=True)
        product_id = graphene.ID(required=True)
    
    price = graphene.Field(PriceNode)
    success = graphene.Boolean()
    errors = graphene.Field(ExpectedErrorType)

    @login_required
    def mutate_and_get_payload(self, info, product_id=None, **kwargs):
        product = Product.objects.get(pk=product_id)

        is_worker = info.context.user in product.store.workers.iterator()
        is_owner = info.context.user == product.store.user
        has_permission = is_owner or is_worker

        if not has_permission:
            raise PermissionError('You don\'t have the permission to perform this action')

        price = Price()
        priceForm = PriceForm(kwargs, instance=price)

        if not priceForm.is_valid():
            return CreatePriceMutation(success=False, errors=priceForm.errors.get_json_data())

        priceForm.save()
        return CreatePriceMutation(price=price, success=True)      

class UpdatePriceMutation(graphene.relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)
        value = graphene.Float()
        value_currency = graphene.String()
    
    price = graphene.Field(PriceNode)
    success = graphene.Boolean()
    errors = graphene.Field(ExpectedErrorType)

    @login_required
    def mutate_and_get_payload(self, info, id=None, **kwargs):
        price = Price.objects.get(pk=id)

        is_worker = info.context.user in price.product.store.workers
        is_owner = info.context.user == price.product.store.user
        has_permission = is_owner or is_worker

        if not has_permission:
            raise PermissionError('You don\'t have the permission to perform this action')

        updatePriceForm = UpdatePriceForm(kwargs, instance=price)

        if updatePriceForm.is_valid():
            return UpdatePriceMutation(success=False, errors=updatePriceForm.errors.get_json_data())
            
        price = updatePriceForm.save(commit=False)
        price.save(update_fields=list(kwargs.keys()))
        return UpdatePriceMutation(price=price, success=True)     

class DeletePriceMutation(graphene.relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)
    
    success = graphene.Boolean()

    @login_required
    def mutate_and_get_payload(self, info, id=None, **kwargs):
        price = Price.objects.get(pk=id)

        is_worker = info.context.user in price.product.store.workers
        is_owner = info.context.user == price.product.store.user
        has_permission = is_owner or is_worker

        if not has_permission:
            raise PermissionError('You don\'t have the permission to perform this action')

        price.delete()
        return DeletePriceMutation(success=True)


class AddProductToCartMutation(graphene.relay.ClientIDMutation):
    class Input:
        product_id = graphene.ID(required=True)
    
    success = graphene.Boolean()

    @login_required
    def mutate_and_get_payload(self, info, product_id, **kwargs):
        cart = Cart.objects.get(user=info.context.user)
        product = Product.objects.get(pk=product_id)
        cart.products.add(product)
        cart.save()
        return AddProductToCartMutation(success=True)

class RemoveProductFromCartMutation(graphene.relay.ClientIDMutation):
    class Input:
        product_id = graphene.ID(required=True)
    
    success = graphene.Boolean()

    @login_required
    def mutate_and_get_payload(self, info, product_id, **kwargs):
        cart = Cart.objects.get(user=info.context.user)
        product = Product.objects.get(pk=product_id)
        cart.products.remove(product)
        cart.save()
        return RemoveProductFromCartMutation(success=True)
