from django import forms
from qa.models import Question, Answer

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
        title = self.cleaned_data['title']
        text = self.cleaned_data['text']

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
        self.cleaned_data['author_id'] = 2
        question = Question(**self.cleaned_data)
        question.save()
        return question

        

class AnswerForm(forms.Form): 
    def __init__(self, *args, **kwargs):
        super(AnswerForm, self).__init__(*args, **kwargs)
        if len(args)>0:
            self._question = args[1]


    text = forms.CharField(label='Text of you answer',
        widget=forms.Textarea(attrs={'class':'form-control'}))
    question = forms.CharField(widget=forms.HiddenInput())
    
    def clean(self):
        text = self.cleaned_data['text']
        if not is_normal_text(text):
            raise forms.ValidationError(WARNING_TEXT, params={'value': text[:5] + '...',
                                                      'name_field': 'text'})
        if len(self.cleaned_data['text']) < 15:
             raise forms.ValidationError(WARNING_TEXT, params={'value': len(self.cleaned_data['text']),
                                                       'name_field': 'text'})
        return self.cleaned_data


    def save(self):
        self.cleaned_data['question'] = self._question
        self.cleaned_data['author_id'] = 2
        answer = Answer(**self.cleaned_data)
        answer.save()
        return answer
