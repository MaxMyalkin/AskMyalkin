import os
from django import forms
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.forms import ModelForm, Form, IntegerField, forms, Field
from django.forms.models import fields_for_model
from django.http import HttpResponse
from djangosphinx.models import SphinxSearch


def rel(*x):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)


class Tag(models.Model):
    text = models.CharField(max_length=15)

class Question(models.Model):
    title = models.CharField(max_length = 100)
    body = models.CharField(max_length = 1000)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField()
    rating = models.IntegerField()
    counter = models.IntegerField()
    file = models.FileField(upload_to='uploads', null=True , blank=True)
    search = SphinxSearch(weights={'title': 100, 'body': 80})
    tags = models.ManyToManyField(Tag, null=True , blank=True)

class Answer(models.Model):
    body = models.CharField(max_length = 1000)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    date = models.DateTimeField()
    correct = models.BooleanField()
    rating = models.IntegerField()
    search = SphinxSearch(weights={'body': 100})

class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = ['body','question', 'author']

class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['title','body','author', 'file']

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    rating = models.IntegerField()
    User.profile = property(lambda u : UserProfile.objects.get(user=u)[0])


class CommentAns(models.Model):
    body = models.CharField(max_length = 200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    main = models.ForeignKey(Answer, on_delete=models.CASCADE)
    date = models.DateTimeField()

class CommentQuest(models.Model):
    body = models.CharField(max_length = 200)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    main = models.ForeignKey(Question, on_delete=models.CASCADE)
    date = models.DateTimeField()

class LikeQuest(models.Model):
    type = models.BooleanField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    main = models.ForeignKey(Question, on_delete=models.CASCADE)


class LikeAns(models.Model):
    type = models.BooleanField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    main = models.ForeignKey(Answer, on_delete=models.CASCADE)


class CommentQForm(ModelForm):
    class Meta:
        model = CommentQuest
        fields = ['body','author','main']

class CommentAForm(ModelForm):
    class Meta:
        model = CommentAns
        fields = ['body','author','main']
