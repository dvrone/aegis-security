from cryptography.fernet import Fernet
from django.conf import settings
from django.db import models


def get_fernet():
    return Fernet(settings.VAULT_ENCRYPTION_KEY.encode())


class EncryptedCharField(models.TextField):
    """Stores a CharField's value encrypted at rest using Fernet."""

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return get_fernet().decrypt(value.encode()).decode()

    def to_python(self, value):
        return value

    def get_prep_value(self, value):
        if value is None:
            return value
        if isinstance(value, bytes):
            value = value.decode()
        return get_fernet().encrypt(value.encode()).decode()
