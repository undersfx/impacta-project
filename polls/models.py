import datetime

from django.forms import ModelForm
from django.utils import timezone
from django.db import models
from django.contrib import admin


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published", default=timezone.now)

    def __str__(self):
        return self.question_text

    @admin.display(boolean=True, ordering="pub_date", description="Published recently?")
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ["question_text"]


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
