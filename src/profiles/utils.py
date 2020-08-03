import uuid

def build_avatar_path(instance, filename):
    return f'img/profile/{uuid.uuid4()}_{filename}'