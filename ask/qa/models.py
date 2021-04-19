from django.db import models
from django.conf import settings
from django.db import models


class QuestionManager(models.Manager):                                          
    def new(self):
        return self.order_by('-id') 

    def popular(self):
        return self.order_by('-rating')


class Question(models.Model):
    def get_url(self):
        return '/question/'+str(self.id)+'/'
        
    title = models.CharField(max_length=255)
    text = models.TextField()
    added_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='likes_set')
    objects = QuestionManager()

class Answer(models.Model):
    text = models.TextField()                                                   
    added_at = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE) 
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)     
