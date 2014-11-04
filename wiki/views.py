from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.core.paginator import Paginator, EmptyPage
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from wiki.models import Article, Revision
from wiki.forms import EditForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages

def view_article(request, slug):
    try:
        article = Article.objects.get(slug=slug)
    except Article.DoesNotExist:
        return redirect('/%s/edit' % slug)
    return render_to_response('wiki/article.html', {'article': article}, context_instance=RequestContext(request))


@login_required
def edit_article(request, slug):
    try:
        article = Article.objects.get(slug=slug)
        initial_text = article.current_revision.text
        initial_comment = ''
    except Article.DoesNotExist:
        article = Article(slug=slug, title=slug)
        initial_text = ''
        initial_comment = 'Creating new article'

    form = EditForm(request.POST or None, initial={'text': initial_text, 'comment': initial_comment})
    if form.is_valid():
        # Need to save this first, so the revision can have a valid article field
        article.save()

        # Get text and comment from the form
        revision = form.save(commit=False)
        # Auto generate the rest
        revision.article = article
        revision.user = request.user
        # And save
        revision.save()

        # Now update the article's current revision
        article.current_revision = revision
        article.save()

        return redirect(article)
    return render_to_response('wiki/edit.html', 
                                { 
                                    'form': form, 
                                    'article': article
                                },
                                context_instance=RequestContext(request))


def article_history(request, slug):
    article = get_object_or_404(Article, slug=slug)
    revision_list = Revision.objects.filter(article=article)
    return render_to_response('wiki/article_history.html', {
                                    'article': article,
                                    'revision_list': revision_list
                                },
                                context_instance=RequestContext(request))


def create_account(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()

            # Now want to log in
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            new_user = authenticate(username=username, password=password)
            login(request, new_user)

            messages.success(request, 'Successfully created account %s' % username)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render_to_response('registration/createaccount.html', {'form': form}, context_instance=RequestContext(request))


def get_search_results(request):
    """
    Search for an article by title
    """
    
    query = request.GET.get('q', '')
    page = request.GET.get('page', 1)

    results = Article.objects.filter(Q(title__icontains=query))
    pages = Paginator(results, 5)

    try:
        returned_page = pages.page(page)
    except EmptyPage:
        returned_page = pages.page(1)

    return render_to_response('wiki/search_results.html',
                                {'page_obj': returned_page,
                                 'object_list': returned_page.object_list,
                                 'search': query})