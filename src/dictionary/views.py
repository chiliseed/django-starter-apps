from django.forms import ModelForm
from django.urls import reverse

from dictionary.models import Word
from django.shortcuts import redirect, render


def index(request):
    words = Word.objects.order_by("-id").all()[:10]
    return render(request, "dictionary/list.html", {"words": words})


class WordForm(ModelForm):
    class Meta:
        model = Word
        fields = ("value", "description")


def add(request):
    if request.method == "POST":
        form = WordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("dictionary:list"))
    else:
        form = WordForm()

    return render(request, "dictionary/add.html", {"form": form})
