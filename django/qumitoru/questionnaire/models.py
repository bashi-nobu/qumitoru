from django.db import models
from account.models import User
# Create your models here.

class Category(models.Model):
    contents = models.CharField(max_length=20, null=False)
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.contents

class Question(models.Model):
    contents = models.CharField(max_length=40, null=False)
    scale_patarn = models.IntegerField(null=False, default=5)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

class Questionare(models.Model):
    name = models.CharField(max_length=40, null=False)
    is_active = models.BooleanField(null=False, default=False)
    question = models.ManyToManyField(Question, through='QuestionareQuestion')
    user = models.ForeignKey(User, on_delete=models.PROTECT)

class QuestionareQuestion(models.Model):
    questionare = models.ForeignKey(Questionare, on_delete=models.PROTECT)
    question = models.ForeignKey(Question, on_delete=models.PROTECT)

class QuestionareScore(models.Model):
    q1 = models.IntegerField(null=True)
    q2 = models.IntegerField(null=True)
    q3 = models.IntegerField(null=True)
    q4 = models.IntegerField(null=True)
    q5 = models.IntegerField(null=True)
    q6 = models.IntegerField(null=True)
    q7 = models.IntegerField(null=True)
    q8 = models.IntegerField(null=True)
    q9 = models.IntegerField(null=True)
    day_of_week = models.IntegerField(null=False)
    file_path = models.CharField(max_length=40, null=False)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    questionare = models.ForeignKey(Questionare, on_delete=models.PROTECT)
    take_at = models.DateField(null=False)
    is_finished = models.BooleanField(null=False, default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
