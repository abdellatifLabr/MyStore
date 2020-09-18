import graphene
from graphql_auth.types import ExpectedErrorType
from graphql_jwt.decorators import login_required
from graphene_file_upload.scalars import Upload
from djmoney.money import Money

from core.constants import Messages

from ..models import (
    Store,
    StoreLogo,
    StoreCover,
    Visit,
    Subscription,
    RecruitmentRequest,
    Product,
    Rating,
    ProductPicture,
    Cart,
    CartProduct,
)

from ..forms import (
    StoreForm,
    UpdateStoreForm,
    ProductForm,
    UpdateProductForm,
)

from .nodes import (
    StoreNode,
    VisitNode,
    SubscriptionNode,
    RecruitmentRequestNode,
    ProductNode,
    RatingNode,
    ProductPictureNode,
    CartNode,
    CartProductNode,
)

class CreateStoreMutation(graphene.relay.ClientIDMutation):
    class Input:
        name = graphene.String(required=True)
        description = graphene.String(required=True)
        logo = Upload()
        cover = Upload()
        closed = graphene.Boolean(default_value=False)
        shipping = graphene.Decimal(required=True)
    
    store = graphene.Field(StoreNode)
    success = graphene.Boolean()
    errors = graphene.Field(ExpectedErrorType)

    @login_required
    def mutate_and_get_payload(self, info, logo=None, cover=None, shipping=None, **kwargs):
        store = Store(user=info.context.user)
        store_form = StoreForm(kwargs, instance=store)

        if not store_form.is_valid():
            return CreateStoreMutation(store=None, success=False, errors=store_form.errors.get_json_data())

        store.logo = StoreLogo.objects.create()
        store.cover = StoreCover.objects.create()

        if shipping is not None:
            store.shipping = Money(shipping, 'USD')

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
        shipping = graphene.Decimal()
        closed = graphene.Boolean()
    
    store = graphene.Field(StoreNode)
    success = graphene.Boolean()
    errors = graphene.Field(ExpectedErrorType)

    @login_required
    def mutate_and_get_payload(self, info, id=None, logo=None, cover=None, shipping=None, **kwargs):
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
                store.logo.save()
        
        if cover is not None:
            if store.cover is None:
                store.cover = StoreCover.objects.create(original=cover)
            else:
                store.cover.original = cover
                store.cover.save()
            
        if shipping is not None:
            store.shipping = Money(shipping, 'USD')

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
        quantity = graphene.Int()
        price = graphene.Decimal(required=True)
        store_id = graphene.ID(required=True)
    
    product = graphene.Field(ProductNode)
    success = graphene.Boolean()
    errors = graphene.Field(ExpectedErrorType)

    @login_required
    def mutate_and_get_payload(self, info, store_id=None, price=None, pictures=None, **kwargs):
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
        
        if price is not None:
            product.price = Money(price, 'USD')

        product_form.save()
        
        if pictures is not None:
            for picture in pictures:
                product.pictures.add(ProductPicture.objects.create(original=picture))
        
        return CreateProductMutation(product=product, success=True)

class UpdateProductMutation(graphene.relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)
        name = graphene.String()
        description = graphene.String()
        pictures = graphene.List(Upload)
        price = graphene.Decimal()
        quantity = graphene.Int()
        rating = graphene.Float()
    
    product = graphene.Field(ProductNode)
    success = graphene.Boolean()
    errors = graphene.Field(ExpectedErrorType)

    @login_required
    def mutate_and_get_payload(self, info, id=None, pictures=None, price=None, rating=None, **kwargs):
        product = Product.objects.get(pk=id)

        is_worker = info.context.user in product.store.workers.iterator()
        is_owner = info.context.user == product.store.user
        has_permission = is_owner or is_worker

        if not has_permission:
            return UpdateProductMutation(success=False, errors=[Messages.NO_PERMISSION])

        update_product_form = UpdateProductForm(kwargs)

        if not update_product_form.is_valid():
            return UpdateProductMutation(success=False, errors=update_product_form.errors.get_json_data())
        
        if pictures is not None:
            for picture in pictures:
                product.picture.original = picture
        
        if price is not None:
            product.price = Money(price, 'USD')
        
        if rating is not None:
            _rating, created = Rating.objects.get_or_create(user=info.context.user, product_id=id)
            _rating.value = rating
            _rating.save()
        
        for field, value in kwargs.items():
            if value:
                setattr(product, field, value)

        product.save()
        return UpdateProductMutation(product=product, success=True)
        
class DeleteProductMutation(graphene.relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)
    
    success = graphene.Boolean()
    errors = graphene.Field(ExpectedErrorType)

    @login_required
    def mutate_and_get_payload(self, info, id=None, **kwargs):
        product = Product.objects.get(pk=id)

        is_worker = info.context.user in product.store.workers.iterator()
        is_owner = info.context.user == product.store.user
        has_permission = is_owner or is_worker

        if not has_permission:
            return DeleteProductMutation(success=False, errors=[Messages.NO_PERMISSION])

        product.delete()
        return DeleteProductMutation(success=True)


class CreateRatingMutation(graphene.relay.ClientIDMutation):
    class Input:
        product_id = graphene.ID(required=True)
        value = graphene.Float(required=True)
    
    rating = graphene.Field(RatingNode)
    success = graphene.Boolean()
    errors = graphene.Field(ExpectedErrorType)

    @login_required
    def mutate_and_get_payload(self, info, **kwargs):
        product_id = kwargs.get('product_id')
        value = kwargs.get('value')

        rating, created = Rating.objects.get_or_create(user=info.context.user, product_id=product_id)
        rating.value = value
        rating.save()

        return CreateRatingMutation(rating=rating, success=True)


class CreateProductPictureMutation(graphene.relay.ClientIDMutation):
    class Input:
        product_id = graphene.ID(required=True)
        picture = Upload(required=True)
    
    success = graphene.Boolean()
    product_picture = graphene.Field(ProductPictureNode)

    @login_required
    def mutate_and_get_payload(self, info, product_id=None, picture=None, **kwargs):
        product = Product.objects.get(pk=product_id)
        product_picture = ProductPicture.objects.create(original=picture)
        product.pictures.add(product_picture)
        return CreateProductPictureMutation(success=True, product_picture=product_picture)
    
class UpdateProductPictureMutation(graphene.relay.ClientIDMutation):
    class Input:
        product_picture_id = graphene.ID(required=True)
        picture = Upload(required=True)
    
    success = graphene.Boolean()
    picture = graphene.Field(ProductPictureNode)

    @login_required
    def mutate_and_get_payload(self, info, product_picture_id=None, picture=None, **kwargs):
        product_picture = ProductPicture.objects.get(pk=product_picture_id)
        product_picture.original = picture
        return UpdateProductPictureMutation(success=True, product_picture=product_picture)

class DeleteProductPictureMutation(graphene.relay.ClientIDMutation):
    class Input:
        product_picture_id = graphene.ID(required=True)
    
    success = graphene.Boolean()

    @login_required
    def mutate_and_get_payload(self, info, product_picture_id=None, **kwargs):
        product_picture = ProductPicture.objects.get(pk=product_picture_id)
        product_picture.delete()
        return DeleteProductPictureMutation(success=True)


class DeleteCartMutation(graphene.relay.ClientIDMutation):
    class Input:
        cart_id = graphene.ID(required=True)
    
    cart = graphene.Field(CartNode)
    success = graphene.Boolean()
    
    @login_required
    def mutate_and_get_payload(self, info, **kwargs):
        cart_id = kwargs.get('cart_id', None)

        cart = Cart.objects.get(pk=cart_id)
        cart.delete()
        return DeleteCartMutation(success=True, cart=cart)


class CreateCartProductMutation(graphene.relay.ClientIDMutation):
    class Input:
        product_id = graphene.ID(required=True)
    
    cart_product = graphene.Field(CartProductNode)
    cart = graphene.Field(CartNode)
    is_new_cart = graphene.Boolean()
    success = graphene.Boolean()

    @login_required
    def mutate_and_get_payload(self, info, product_id=None, **kwargs):
        product = Product.objects.get(pk=product_id)
        cart, created = Cart.objects.get_or_create(user=info.context.user, store=product.store)
        cart_product = CartProduct.objects.create(product_id=product_id, cart=cart, user=info.context.user)
        return CreateCartProductMutation(success=True, cart_product=cart_product, is_new_cart=created, cart=cart)

class UpdateCartProductMutation(graphene.relay.ClientIDMutation):
    class Input:
        cart_product_id = graphene.ID(required=True)
        quantity = graphene.Int()
    
    cart_product = graphene.Field(CartProductNode)
    cart = graphene.Field(CartNode)
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
        return UpdateCartProductMutation(success=True, cart_product=cart_product, cart=cart_product.cart)

class DeleteCartProductMutation(graphene.relay.ClientIDMutation):
    class Input:
        cart_product_id = graphene.ID(required=True)
    
    cart = graphene.Field(CartNode)
    is_last_item = graphene.Boolean()
    success = graphene.Boolean()
    errors = graphene.Field(ExpectedErrorType)

    @login_required
    def mutate_and_get_payload(self, info, cart_product_id=None, **kwargs):
        cart_product = CartProduct.objects.get(pk=cart_product_id)

        is_owner = info.context.user == cart_product.user
        has_permission = is_owner

        if not has_permission:
            return DeleteCartProductMutation(success=False, errors=[Messages.NO_PERMISSION])

        cart_product.delete()

        is_last_item = False
        if cart_product.cart.cart_products.count() == 0:
            cart_product.cart.delete()
            is_last_item = True

        return DeleteCartProductMutation(success=True, is_last_item=is_last_item, cart=cart_product.cart)
