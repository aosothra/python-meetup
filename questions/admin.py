from django.contrib import admin

from questions.models import Question

# Register your models here.
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    pass
