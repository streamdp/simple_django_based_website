from django.shortcuts import render, get_object_or_404                          
from django.views.decorators.http import require_GET, require_POST 
from django.http import HttpResponse,  Http404, HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage                                    
from qa.models import Question, Answer
from qa.forms import AskForm, AnswerForm


def test(request, *args, **kwargs):
     return render(request, 'qa/posts.html')
#    return HttpResponse('OK')


@require_GET
def get_new_questions(request):
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
def get_most_popular(request):
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


def get_question(request, id):
    try:
        question = Question.objects.get(id=id)
    except Question.DoesNotExist:
        raise Http404
    answers = Answer.objects.filter(question=question.id)
          
    if request.method == "POST":
        form = AnswerForm(request.POST, question)
        if form.is_valid():
            answer = form.save()
            url = question.get_url()
            return HttpResponseRedirect(url)
    else:
        form = AnswerForm()

    return render(request, 'qa/question.html', {
        'question' : question,
        'answers': answers,
        'form': form
        })


def add_question(request):
    if request.method == "POST":
        form = AskForm(request.POST)
        if form.is_valid():
            question = form.save()
            url = question.get_url()
            return HttpResponseRedirect(url)
    else:
        form = AskForm()
    return render(request, 'qa/add_question.html', {
        'form': form
    })
