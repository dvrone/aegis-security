from django.shortcuts import render

def home(request):
    planned_projects = [
        {"name": "Aegis Vault", "description": "Secure password and secrets manager."},
        {"name": "Aegis Auth", "description": "Self-hosted authentication & 2FA toolkit."},
        {"name": "Aegis Notes", "description": "Encrypted note-taking app."},
        {"name": "Aegis Encrypt", "description": "File encryption utility."},
        {"name": "Aegis Scan", "description": "Vulnerability scanning tool."},
        {"name": "Aegis OSINT", "description": "Open-source intelligence gathering toolkit."},
    ]
    return render(request, "core/home.html", {"planned_projects": planned_projects})