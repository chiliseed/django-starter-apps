from django.contrib import admin

from dictionary.models import Word


@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    fields = ("value", "description")
    list_display = ("id", "value", )
