from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django import forms
from .models import TestCategory, Test, Question, AnswerChoice

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput, label="Повторите пароль")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_email(self):
        email = self.cleaned_data['email']
        if not email.endswith('@mpt.ru'):
            raise ValidationError('Почта должна быть на домене mpt.ru')
        return email

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')

        if password and password2 and password != password2:
            raise ValidationError('Пароли не совпадают')
        return password2


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        labels = {
            'username': 'Имя пользователя',
            'email': 'Электронная почта'
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if not email.endswith('@mpt.ru'):
            raise ValidationError('Почта должна быть на домене mpt.ru')
        return email



class TestCategoryForm(forms.ModelForm):
    class Meta:
        model = TestCategory
        fields = ['name', 'slug', 'description']

class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['name', 'category', 'duration']
class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['choices'] = forms.ModelMultipleChoiceField(
            queryset=AnswerChoice.objects.all(),
            widget=forms.CheckboxSelectMultiple,
            required=False
        )


class AnswerChoiceForm(forms.ModelForm):
    class Meta:
        model = AnswerChoice
        fields = ['text', 'question', 'is_correct']

    def clean_is_correct(self):
        is_correct = self.cleaned_data.get('is_correct')
        question = self.cleaned_data.get('question')
        if is_correct:
            existing_correct = AnswerChoice.objects.filter(question=question, is_correct=True).exists()
            if existing_correct:
                raise ValidationError('Только один ответ может быть правильным для этого вопроса.')
        return is_correct
