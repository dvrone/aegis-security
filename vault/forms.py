from django import forms

from .models import VaultEntry


class VaultEntryForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(render_value=True))

    class Meta:
        model = VaultEntry
        fields = [
            "title",
            "username",
            "password",
            "url",
            "notes",
            "category",
            "is_favorite",
        ]
        widgets = {
            "notes": forms.Textarea(attrs={"rows": 3}),
        }
