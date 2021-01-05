from django.shortcuts import render, get_object_or_404                          
from django.views.decorators.http import require_GET 
# Create your views here.
from django.http import HttpResponse,  Http404
from django.core.paginator import Paginator, EmptyPage                                    
from qa.models import Question, Answer


def test(request, *args, **kwargs):
     return render(request, 'qa/posts.html')
#    return HttpResponse('OK')


@require_GET
def new_questions(request):
    questions = Question.objects.new()
    try:
        limit = int(request.GET.get('limit', 10))
    except ValueError:
        limit = 10
    if limit > 100:
        limit = 10
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        raise Http404
    paginator = Paginator(questions, limit)
    paginator.baseurl = '/?page=' 
    try:    
        page = paginator.page(page)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return render(request, 'qa/questions.html', {
        'questions' : page.object_list,
        'paginator' : paginator,
        'page' : page,
    })

@require_GET
def most_popular(request):
    questions = Question.objects.popular()
    try:
        limit = int(request.GET.get('limit', 10))
    except ValueError:
        limit = 10
    if limit > 100:
        limit = 10
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        raise Http404
    paginator = Paginator(questions, limit)
    paginator.baseurl = '/popular/?page=' 
    try:    
        page = paginator.page(page)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return render(request, 'qa/questions.html', {
        'questions' : page.object_list,
        'paginator' : paginator,
        'page' : page,
    })


@require_GET
def get_question(request, id):
    try:
		questions = Question.objects.filter(id=id)
    except Question.DoesNotExist:
		raise Http404
    return render(request, 'qa/questions.html', {
        'questions' : questions,
    })
