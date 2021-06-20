from django.contrib import admin
from .models import Category, Question, Questionare, QuestionareQuestion

admin.site.register(Category)
admin.site.register(Question)
admin.site.register(Questionare)
admin.site.register(QuestionareQuestion)

# Register your models here.
