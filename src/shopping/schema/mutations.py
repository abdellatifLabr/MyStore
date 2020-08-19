import graphene
from graphql_auth.types import ExpectedErrorType
from graphql_jwt.decorators import login_required
from graphene_file_upload.scalars import Upload

from core.constants import Messages

from ..models import (
    Store,
    StoreLogo,
    StoreCover,
    Visit,
    Subscription,
    RecruitmentRequest,
    Product,
    ProductPicture,
    Price,
    CartProduct,
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
    CartProductNode,
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
    def mutate_and_get_payload(self, info, logo=None, cover=None, **kwargs):
        store = Store(user=info.context.user)
        store_form = StoreForm(kwargs, instance=store)

        if not store_form.is_valid():
            return CreateStoreMutation(store=None, success=False, errors=store_form.errors.get_json_data())

        if logo is not None:
            store.logo = StoreLogo.objects.create(original=logo)
        
        if cover is not None:
            store.cover = StoreCover.objects.create(original=cover)

        store_form.save()
        return CreateStoreMutation(store=store, success=True)    

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
    def mutate_and_get_payload(self, info, id=None, logo=None, cover=None, **kwargs):
        store = Store.objects.get(pk=id)

        is_owner = store.user == info.context.user
        has_permission = is_owner

        if not has_permission:
            return UpdateStoreMutation(success=False, errors=[Messages.NO_PERMISSION])

        update_store_form = UpdateStoreForm(kwargs, instance=store)

        if not update_store_form.is_valid():
            return UpdateStoreMutation(success=False, errors=update_store_form.errors.get_json_data())

        if logo is not None:
            if store.logo is None:
                store.logo = StoreLogo.objects.create(original=logo)
            else:
                store.logo.original = logo
        
        if cover is not None:
            if store.cover is None:
                store.cover = StoreCover.objects.create(original=cover)
            else:
                store.cover.original = cover

        store = update_store_form.save(commit=False)
        store.save()
        return UpdateStoreMutation(store=store, success=True)
        
class DeleteStoreMutation(graphene.relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)
    
    success = graphene.Boolean()

    @login_required
    def mutate_and_get_payload(self, info, id=None, **kwargs):
        store = Store.objects.get(pk=id)

        if not store.user == info.context.user:
            return DeleteStoreMutation(success=False, errors=[Messages.NO_PERMISSION])

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
        store = Store.objects.get(pk=store_id)
        sub = Subscription.objects.create(user=info.context.user, store=store)
        # notifiy the store owner
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
            return CreateRecruitmentRequestMutation(success=False, errors=[Messages.NO_PERMISSION])
        
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
            return UpdateRecruitmentRequestMutation(success=False, errors=[Messages.NO_PERMISSION])
        
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
            return DeleteRecruitmentRequestMutation(success=False, errors=[Messages.NO_PERMISSION])
        
        recruitment_request.delete()
        return DeleteRecruitmentRequestMutation(success=True)


class CreateProductMutation(graphene.relay.ClientIDMutation):
    class Input:
        name = graphene.String(required=True)
        description = graphene.String(required=True)
        pictures = graphene.List(Upload, required=True)
        price_value = graphene.Int(required=True)
        price_currency = graphene.String(required=True)
        store_id = graphene.ID(required=True)
    
    product = graphene.Field(ProductNode)
    success = graphene.Boolean()
    errors = graphene.Field(ExpectedErrorType)

    @login_required
    def mutate_and_get_payload(self, info, store_id=None, price_value=None, price_currency=None, pictures=None, **kwargs):
        store = Store.objects.get(pk=store_id)

        is_owner = info.context.user == store.user
        is_worker = info.context.user in store.workers.iterator()
        has_permission = is_worker or is_owner

        if not has_permission:
            return CreateProductMutation(success=False, errors=[Messages.NO_PERMISSION])

        product = Product(store=store)
        product_form = ProductForm(kwargs, instance=product)

        if not product_form.is_valid():
            return CreateProductMutation(product=None, success=False, errors=product_form.errors.get_json_data())
        
        if pictures is not None:
            for picture in pictures:
                product.pictures.add(ProductPicture.objects.create(original=picture))
        
        price = Price.objects.create(value=price_value, currency=price_currency)
        product.price = price

        product_form.save()
        return CreateProductMutation(product=product, success=True)

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
    def mutate_and_get_payload(self, info, id=None, picture=None, **kwargs):
        product = Product.objects.get(pk=id)

        is_worker = info.context.user in product.store.workers.iterator()
        is_owner = info.context.user == product.store.user
        has_permission = is_owner or is_worker

        if not has_permission:
            return UpdateProductMutation(success=False, errors=[Messages.NO_PERMISSION])

        update_product_form = UpdateProductForm(kwargs, instance=product)

        if not update_product_form.is_valid():
            return UpdateProductMutation(success=False, errors=update_product_form.errors.get_json_data())
        
        if picture is not None:
            product.picture.original = picture
        
        product = update_product_form.save(commit=False)
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
            return DeleteProductMutation(success=False, errors=[Messages.NO_PERMISSION])

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
            return CreatePriceMutation(success=False, errors=[Messages.NO_PERMISSION])

        price = Price()
        price_form = PriceForm(kwargs, instance=price)

        if not price_form.is_valid():
            return CreatePriceMutation(success=False, errors=price_form.errors.get_json_data())

        price_form.save()
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
            return UpdatePriceMutation(success=False, errors=[Messages.NO_PERMISSION])

        update_price_form = UpdatePriceForm(kwargs, instance=price)

        if update_price_form.is_valid():
            return UpdatePriceMutation(success=False, errors=update_price_form.errors.get_json_data())
            
        price = update_price_form.save(commit=False)
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
            return DeletePriceMutation(success=False, errors=[Messages.NO_PERMISSION])

        price.delete()
        return DeletePriceMutation(success=True)


class CreateCartProductMutation(graphene.relay.ClientIDMutation):
    class Input:
        product_id = graphene.ID(required=True)
    
    cart_product = graphene.Field(CartProductNode)
    success = graphene.Boolean()

    @login_required
    def mutate_and_get_payload(self, info, product_id=None, **kwargs):
        cart_product = CartProduct.objects.create(user=info.context.user, product_id=product_id)
        return CreateCartProductMutation(success=True, cart_product=cart_product)

class UpdateCartProductMutation(graphene.relay.ClientIDMutation):
    class Input:
        cart_product_id = graphene.ID(required=True)
        quantity = graphene.Int()
    
    cart_product = graphene.Field(CartProductNode)
    success = graphene.Boolean() 

    @login_required
    def mutate_and_get_payload(self, info, cart_product_id, **kwargs):
        cart_product = CartProduct.objects.get(pk=cart_product_id)

        is_owner = info.context.user == cart_product.user
        has_permission = is_owner

        if not has_permission:
            return UpdateCartProductMutation(success=False, errors=[Messages.NO_PERMISSION])
        
        for field, value in kwargs.items():
            setattr(cart_product, field, value)
        
        cart_product.save()
        return UpdateCartProductMutation(success=True, cart_product=cart_product)

class DeleteCartProductMutation(graphene.relay.ClientIDMutation):
    class Input:
        product_id = graphene.ID(required=True)
    
    success = graphene.Boolean()

    @login_required
    def mutate_and_get_payload(self, info, product_id=None, **kwargs):
        cart_product = CartProduct.objects.get(user=info.context.user, product_id=product_id)
        cart_product.delete()
        return DeleteCartProductMutation(success=True)

class DeleteAllCartProductsMutation(graphene.relay.ClientIDMutation):
    class Input:
        pass

    success = graphene.Boolean()

    @login_required
    def mutate_and_get_payload(self, info, **kwargs):
        cart_products = CartProduct.objects.filter(user=info.context.user)

        for cart_product in cart_products:
            cart_product.delete()
        
        return DeleteAllCartProductsMutation(success=True)