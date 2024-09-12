from django.contrib import admin

from .models import Question, Choice


admin.site.site_title = "Polls Admin"
admin.site.site_header = "Polls Administração"
admin.site.index_title = "Polls Administração"


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    list_display = ["question_text", "pub_date", "was_published_recently"]
    list_filter = ["pub_date"]
    search_fields = ["question_text"]

    # fields = ["pub_date", "question_text"]
    fieldsets = [
        (None, {"fields": ["question_text"]})
    ]
    inlines = [ChoiceInline]

admin.site.register(Question, QuestionAdmin)
