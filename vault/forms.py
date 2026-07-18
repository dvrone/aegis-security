from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Field, Layout, Submit
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False  # we'll keep the <form> tag in the template
        self.helper.layout = Layout(
            Field("title"),
            Field("username"),
            Field("password"),
            HTML("""
                <div class="mt-2 mb-3 d-flex gap-2 align-items-center">
                    <input type="range" min="8" max="32" value="16" id="gen-length" class="form-range" style="max-width: 150px;">
                    <span id="gen-length-label">16</span>
                    <button type="button" id="gen-btn" class="btn btn-sm btn-outline-secondary">
                        <i class="bi bi-shuffle"></i> Generate
                    </button>
                </div>
                <div class="progress mb-3" style="height: 6px;">
                    <div id="strength-bar" class="progress-bar" role="progressbar" style="width: 0%;"></div>
                </div>
                <small id="strength-label" class="text-muted d-block mb-3"></small>
            """),
            Field("url"),
            Field("notes"),
            Field("category"),
            Field("is_favorite"),
        )
