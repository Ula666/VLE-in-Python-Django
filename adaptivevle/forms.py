from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


from .models import *


# register
class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "password1", "password2"]


class AddTopicForm(forms.ModelForm):
    name = forms.CharField(label="Enter Topic Name", max_length=20)

    class Meta:
        model = Topic
        fields = ['name']


class AddVideoForm(forms.ModelForm):
    content = forms.CharField(label=" Add YouTube Video URL")

    class Meta:
        model = Material
        fields = ['name', 'content']


class AddPresentationForm(forms.ModelForm):
    content = forms.CharField(label=" Add Presentation URL")

    class Meta:
        model = Material
        fields = ['name', 'content']


class AddAudioForm(forms.ModelForm):
    name = forms.CharField(label=" Enter Audio name", max_length=20)
    file = forms.FileField(label="Select a file")

    class Meta:
        model = Material
        fields = ['name', 'file']


class AddTextForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['name', 'content']


class AddImageForm(forms.ModelForm):
    name = forms.CharField(label="Add Image Name", max_length=20)

    class Meta:
        model = Material
        fields = ['name', 'file']


class QuizForm(forms.ModelForm):
    name = forms.CharField(label="Add Quiz Name", max_length=50)
    description = forms.Textarea()

    class Meta:
        model = Quiz
        fields = ['name', 'description']


class QuizQuestionForm(forms.ModelForm):
    text = forms.CharField(label="Add Question", max_length=255)
    answer_1 = forms.CharField(label="Add Answer 1", max_length=255)
    answer_2 = forms.CharField(label="Add Answer 2", max_length=255)
    answer_3 = forms.CharField(label="Add Answer 3", max_length=255)
    answer_4 = forms.CharField(label="Add Answer 4", max_length=255)

    class Meta:
        model = QuizQuestion
        fields = ['text', 'answer_1', 'answer_2', 'answer_3', 'answer_4', 'correct']


class CommentForm(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Comment
        fields = ['message']
