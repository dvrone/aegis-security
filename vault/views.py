from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import VaultEntryForm
from .models import VaultEntry
from .utils import generate_password


@login_required
def entry_list(request):
    entries = VaultEntry.objects.filter(owner=request.user)

    query = request.GET.get("q", "").strip()
    category = request.GET.get("category", "")
    favorites_only = request.GET.get("favorites") == "1"

    if query:
        entries = entries.filter(
            Q(title__icontains=query)
            | Q(username__icontains=query)
            | Q(url__icontains=query)
        )
    if category:
        entries = entries.filter(category=category)
    if favorites_only:
        entries = entries.filter(is_favorite=True)

    context = {
        "entries": entries,
        "query": query,
        "selected_category": category,
        "favorites_only": favorites_only,
        "categories": VaultEntry.CATEGORY_CHOICES,
    }
    return render(request, "vault/entry_list.html", context)


@login_required
def entry_create(request):
    if request.method == "POST":
        form = VaultEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.owner = request.user
            entry.save()
            return redirect("vault:entry_list")
    else:
        form = VaultEntryForm()
    return render(request, "vault/entry_form.html", {"form": form, "action": "Add"})


@login_required
def entry_edit(request, pk):
    entry = get_object_or_404(VaultEntry, pk=pk, owner=request.user)
    if request.method == "POST":
        form = VaultEntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            return redirect("vault:entry_list")
    else:
        form = VaultEntryForm(instance=entry)
    return render(request, "vault/entry_form.html", {"form": form, "action": "Edit"})


@login_required
def entry_delete(request, pk):
    entry = get_object_or_404(VaultEntry, pk=pk, owner=request.user)
    if request.method == "POST":
        entry.delete()
        return redirect("vault:entry_list")
    return render(request, "vault/entry_confirm_delete.html", {"entry": entry})


@login_required
def generate_password_view(request):
    length = int(request.GET.get("length", 16))
    length = max(6, min(length, 64))  # clamp to a sane range

    use_upper = request.GET.get("upper", "true") == "true"
    use_lower = request.GET.get("lower", "true") == "true"
    use_digits = request.GET.get("digits", "true") == "true"
    use_symbols = request.GET.get("symbols", "true") == "true"

    try:
        password = generate_password(
            length, use_upper, use_lower, use_digits, use_symbols
        )
    except ValueError as e:
        return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"password": password})
