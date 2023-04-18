from django.contrib import admin
from .models import Question, Choice

class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3
class QuestionAdmin(admin.ModelAdmin):
    fields = ["timstamp",  "question_text"]
    inlines = [ChoiceInline]
    list_display = ("question_text", "timstamp", "is_recently")
    list_filter = ["timstamp"]
    search_fields = ["question_text"]
    
admin.site.register(Question, QuestionAdmin)
