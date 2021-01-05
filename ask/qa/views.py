from django.shortcuts import render, get_object_or_404                          
from django.views.decorators.http import require_GET 
# Create your views here.
from django.http import HttpResponse 
from django.core.paginator import Paginator                                     
from qa.models import Question, Answer


def test(request, *args, **kwargs):
     return render(request, 'qa/posts.html')
#    return HttpResponse('OK')


@require_GET
def new_questions(request):
    questions = Question.objects.new()
    limit = request.GET.get('limit', 10)
    page = request.GET.get('page', 1)
    paginator = Paginator(questions, limit)
    paginator.baseurl = '/?page=' 
    page = paginator.page(page)
    return render(request, 'qa/questions.html', {
        'questions' : page.object_list,
        'paginator' : paginator,
        'page' : page,
    })


def paginate(request, qs):
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
    paginator = Paginator(qs, limit)
    try:
        page = paginator.page(page)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return page

