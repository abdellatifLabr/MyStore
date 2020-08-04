import uuid

def build_store_logo_path(instance, filename):
    return f'img/store/logo/{uuid.uuid4()}_{filename}'

def build_store_cover_path(instance, filename):
    return f'img/store/cover/{uuid.uuid4()}_{filename}'

def build_product_picture_path(instance, filename):
    return f'img/product/{instance.id}/{uuid.uuid4()}_{filename}'
    