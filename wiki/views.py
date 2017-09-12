from django.shortcuts import redirect, render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from wiki.models import Article, Revision
from wiki.forms import EditForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

import difflib

from pygments import highlight
from pygments.lexers import DiffLexer
from pygments.formatters import HtmlFormatter

def view_article(request, slug):
    slug = slug.replace(' ', '-')
    try:
        article = Article.objects.get(slug=slug)
    except Article.DoesNotExist:
        return redirect('/%s/edit' % slug)
    return render(
        request,
        'wiki/article.html', 
        context = {'article': article}
    )


@login_required
def edit_article(request, slug):
    slug = slug.replace(' ', '-')
    try:
        article = Article.objects.get(slug=slug)
        initial_text = article.current_revision.text
        initial_comment = ''
        new_article = False
    except Article.DoesNotExist:
        article = Article(slug=slug, title=slug.replace('-', ' '))
        initial_text = ''
        initial_comment = 'Creating new article'
        new_article = True

    form = EditForm(request.POST or None, initial={'text': initial_text, 'comment': initial_comment})

    if form.is_valid():
        # Need to save this first, so the revision can have a valid article field
        article.save()

        # Get text and comment from the form
        revision = form.save(commit=False)
        # Auto generate the rest
        revision.article = article
        revision.user = request.user

        if not new_article:
            revision.parent = article.current_revision

        # And save
        revision.save()

        # Now update the article's current revision
        article.current_revision = revision
        article.save()

        return redirect(article)

    return render(
        request, 
        'wiki/edit.html',
        context = { 'form': form, 'article': article, 'new_article': new_article }
    )


def article_history(request, slug):
    slug = slug.replace(' ', '-')
    article = get_object_or_404(Article, slug=slug)
    revision_list = Revision.objects.filter(article=article)
    return render(
        request,
        'wiki/article_history.html', 
        context = { 'article': article, 'revision_list': revision_list }
    )


def diff(request, rev1id, rev2id):
    rev1 = Revision.objects.get(id=rev1id)
    rev2 = Revision.objects.get(id=rev2id)
    
    diff = difflib.unified_diff(a = rev1.text.split('\n'), b = rev2.text.split('\n'))
    diffText = ''.join(list(diff)[2:]) # skip first 2 lines (file names and dates)
    diffHtml = highlight( diffText, DiffLexer(), HtmlFormatter(cssclass='codehilite') )

    return render(
        request,
        'wiki/diff.html', 
        context = { 'rev1': rev1, 'rev2': rev2, 'diffHtml': diffHtml }
    )


def user_info(request, username):
    user = get_object_or_404(User, username=username)
    revision_list = Revision.objects.filter(user=user)
    return render(
        request,
        'wiki/user_info.html', 
        context = { 'user': user, 'revision_list': revision_list }
    )


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
    return render(
        request,
        'registration/createaccount.html',
        context = {'form': form}
    )


def get_search_results(request):
    """
    Search for an article by title
    """
    
    query = request.GET.get('q', '')
    page = request.GET.get('page', 1)

    results = Article.objects.filter(Q(title__icontains=query)).order_by('-current_revision')
    pages = Paginator(results, 6)

    try:
        returned_page = pages.page(page)
    except EmptyPage:
        returned_page = pages.page(1)

    return render(
        request,
        'wiki/search_results.html',
        context = { 'paginator': pages, 'page_obj': returned_page, 'object_list': returned_page.object_list, 'search': query }
    )