import uuid

def build_avatar_path(instance, filename):
    return f'img/profile/avatar/{uuid.uuid4()}_{filename}'