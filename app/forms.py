from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from app.models import Question, Tag, Answer
from datetime import datetime


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(min_length=3, widget=forms.PasswordInput)


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(min_length=3, widget=forms.PasswordInput)
    password_confirmation = forms.CharField(min_length=3, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        password = self.cleaned_data['password']
        password_confirmation = self.cleaned_data['password_confirmation']
        if password != password_confirmation:
            raise ValidationError('Пароль и его подтверждение не совпадают')

    def save(self, **kwargs):
        self.cleaned_data.pop('password_confirmation')
        return User.objects.create_user(**self.cleaned_data)


class AskForm(forms.ModelForm):
    title = forms.CharField(min_length=3)
    content = forms.TextInput()
    tags = forms.CharField()

    class Meta:
        model = Question
        fields = ['title', 'content', 'tags']

    def save_ask(self, user):
        q = Question(user=user,
                     title=self.cleaned_data['title'],
                     content=self.cleaned_data['content'],
                     dt=datetime.now())
        q.save()
        tags = self.cleaned_data['tags'].split()
        for tag in tags:
            t = Tag(question=q, tag=tag.strip())
            t.save()


class AnswerForm(forms.ModelForm):
    content = forms.TextInput()

    class Meta:
        model = Answer
        fields = ['content']

    def save_answer(self, user, question):
        a = Answer(question=question,
                   user=user,
                   content=self.cleaned_data['content'],
                   dt=datetime.now(),
                   is_correct=False)
        a.save()
