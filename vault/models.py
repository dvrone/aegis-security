from django.conf import settings
from django.db import models

from .fields import EncryptedCharField


class VaultEntry(models.Model):
    CATEGORY_CHOICES = [
        ("general", "General"),
        ("social", "Social"),
        ("banking", "Banking"),
        ("work", "Work"),
        ("email", "Email"),
        ("shopping", "Shopping"),
    ]

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="vault_entries"
    )
    title = models.CharField(max_length=100)
    username = models.CharField(max_length=150, blank=True)
    password = EncryptedCharField()
    url = models.URLField(blank=True)
    notes = EncryptedCharField(blank=True, default="")
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, default="general"
    )
    is_favorite = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-is_favorite", "title"]

    def __str__(self):
        return f"{self.title} ({self.owner.username})"
