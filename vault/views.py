from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import VaultEntryForm
from .models import VaultEntry


@login_required
def entry_list(request):
    entries = VaultEntry.objects.filter(owner=request.user)
    return render(request, "vault/entry_list.html", {"entries": entries})


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
