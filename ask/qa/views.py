from django.shortcuts import render
from django.shortcuts import render, get_object_or_404                          
from django.views.decorators.http import require_GET 
# Create your views here.
from django.http import HttpResponse 
from django.core.paginator import Paginator                                     



def test(request, *args, **kwargs):
    return HttpResponse('OK')


@require_GET
def new_questions(request):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'qa/posts.html', {
        'post':
         post,
    })


from django.core.paginator import Paginator
def post_list_all(request):
    posts = Post.objects.filter(is_published=True)
    limit = request.GET.get('limit', 10)
    page = request.GET.get('page', 1)
    paginator = Paginator(posts, limit)
    paginator.baseurl = '/qa/all_posts/?page='
    page = paginator.page(page) # Page
    return render(request, 'qa/posts.html', {
           'posts': page.object_list,
           'paginator': paginator, 'page': page,
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

