from django.forms import ModelForm
from django.shortcuts import redirect, render
from django.urls import reverse
import structlog

from dictionary.models import Word

logger = structlog.get_logger(__name__)


def index(request):
    words = Word.objects.order_by("-id").all()[:10]
    logger.info("showing latest words")
    return render(request, "dictionary/list.html", {"words": words})


class WordForm(ModelForm):
    class Meta:
        model = Word
        fields = ("value", "description")


def add(request):
    logger.info("accepted request to add a word")
    if request.method == "POST":
        form = WordForm(request.POST)
        if form.is_valid():
            word = form.save()
            logger.info("added new word", word=word.value)
            return redirect(reverse("dictionary:list"))
    else:
        form = WordForm()

    return render(request, "dictionary/add.html", {"form": form})
