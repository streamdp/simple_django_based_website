from django import forms
from qa.models import Question, Answer
from django.contrib.auth.models import User

WARNING_TEXT = 'Enter meaningful %(name_field)s, please! You entered duplicate letters: %(value)s'


def is_normal_text(text):
    count = 0
    for i in text:
        if text.count(i) >= (len(text) / 4):
            count += 1
    if count > 10 or count == len(text):
        return False
    else:
        return True
        

class AskForm(forms.Form):
    title = forms.CharField(label='Title of you question',
        max_length=100, widget= forms.TextInput(attrs={'class':'form-control'}))
    text = forms.CharField(label='Text of you question',
        widget=forms.Textarea(attrs={'class':'form-control'}))

    def clean(self):
        self.cleaned_data['author_id'] = self._user.id
        title = self.cleaned_data['title'].lower()
        text = self.cleaned_data['text'].lower()

        if text == title:
            raise forms.ValidationError('Text in the fields must not match!')
        if not is_normal_text(title):
            raise forms.ValidationError(WARNING_TEXT, params={'value': title[:5] + '...',
                                                      'name_field': 'title'})
        if len(title) < 10:
            raise forms.ValidationError(WARNING_TEXT, params={'value': len(self.cleaned_data['title']),
                                                      'name_field': 'title'})
        if not is_normal_text(text):
            raise forms.ValidationError(WARNING_TEXT, params={'value': text[:5] + '...',
                                                      'name_field': 'text'})
        if len(self.cleaned_data['text']) < 15:
             raise forms.ValidationError(WARNING_TEXT, params={'value': len(self.cleaned_data['text']),
                                                       'name_field': 'text'})
        return self.cleaned_data


    def save(self):
        question = Question(**self.cleaned_data)
        question.save()
        return question
        

class AnswerForm(forms.Form):             
    text = forms.CharField(label='Text of you answer',
        widget=forms.Textarea(attrs={'class':'form-control'}))
    question = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    
    def clean(self):
        text = self.cleaned_data['text'].lower()
        if not is_normal_text(text):
            raise forms.ValidationError(WARNING_TEXT, params={'value': text[:5] + '...',
                                                      'name_field': 'text'})
        if len(self.cleaned_data['text']) < 15:
             raise forms.ValidationError(WARNING_TEXT, params={'value': len(self.cleaned_data['text']),
                                                       'name_field': 'text'})
        return self.cleaned_data


    def save(self):
        self.cleaned_data['question'] = self._question
        self.cleaned_data['author_id'] = self._user.id
        answer = Answer(**self.cleaned_data)
        answer.save()
        return answer


class SignUpForm(forms.Form):
    username = forms.CharField(label='Username',
        widget=forms.TextInput(attrs={'class':'form-control'}), max_length=20)
    email = forms.EmailField(label='Email',
        widget=forms.EmailInput(attrs={'class':'form-control'}))
    password = forms.CharField(label='Password',
        widget=forms.PasswordInput(attrs={'class':'form-control'}))


    def save(self):
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']      
        user = User.objects.create_user(username, email, password)
        user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(label='Username',
        widget=forms.TextInput(attrs={'class':'form-control'}), max_length=20)
    password = forms.CharField(label='Password',
        widget=forms.PasswordInput(attrs={'class':'form-control'}))

