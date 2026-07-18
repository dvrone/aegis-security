from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import SignUpForm


def home(request):
    planned_projects = [
        {"name": "Aegis Vault", "description": "Secure password and secrets manager."},
        {
            "name": "Aegis Auth",
            "description": "Self-hosted authentication & 2FA toolkit.",
        },
        {"name": "Aegis Notes", "description": "Encrypted note-taking app."},
        {"name": "Aegis Encrypt", "description": "File encryption utility."},
        {"name": "Aegis Scan", "description": "Vulnerability scanning tool."},
        {
            "name": "Aegis OSINT",
            "description": "Open-source intelligence gathering toolkit.",
        },
    ]
    return render(request, "core/home.html", {"planned_projects": planned_projects})


def register(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")
    else:
        form = SignUpForm()
    return render(request, "core/register.html", {"form": form})


@login_required
def dashboard(request):
    return render(request, "core/dashboard.html")
