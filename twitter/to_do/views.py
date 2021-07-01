from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import NewTweet, Comment
from .forms import TweetForm, CommentForm
from django.urls import reverse_lazy
from django.views.generic import (
    DetailView,
    DeleteView,
)



def home(request):
    tweet_list = NewTweet.objects.all()
    content = {'tweet_list': tweet_list}
    print(tweet_list)
    return render(request, 'to_do/home.html', content)


@login_required()
def create_tweet(request):
    form = TweetForm()
    if request.method == "POST":
        form = TweetForm(data=request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('home')

    return render(request, 'to_do/create.html', {'tweet_form': form})


@login_required()
def comment_tweet(request):
    comment_form = TweetForm()
    if request.method == "POST":
        form = TweetForm(data=request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('home')

    return render(request, 'to_do/retrieve.html', {'comment_form': comment_form})


def search(request):
    if request.method == 'POST':
        searched = request.POST['searched']
        venues = NewTweet.objects.filter(tweet__contains=searched)
        return render(request, 'to_do/search.html', {'searched': searched, 'venues': venues})
    else:
        return render(request, 'to_do/search.html', {})


@login_required()
def retrieve_tweet(request, tweet_id):
    try:
        tweet = NewTweet.objects.get(id=tweet_id)
    except NewTweet.DoesNotExist:
        return HttpResponse('Object not found')
    return render(request, 'to_do/retrieve.html', {'tweet': tweet})


# @login_required()
# def tweet_detail(request, pk):
#     context = {}
#     tweet = NewTweet.objects.get(id=pk)
#     context['tweet'] = tweet
#
#     if request.POST:
#         comment_form = CommentForm(request.POST)
#         if comment_form.is_valid():
#             new_comment = comment_form.save(commit=False)
#             new_comment.author = request.user
#             new_comment.tweet = context['tweet']
#             new_comment.save()
#
#     comments = Comment.objects.filter(tweet=context['tweet'])
#     context['comments'] = comments
#     return render(request, 'tweet_detail.html', context)

class TweetDetailView(LoginRequiredMixin, DetailView):

    def get(self, request, pk, date_added=None):
        tweet = NewTweet.objects.get(pk=pk)
        form = CommentForm()
        comments = Comment.objects.filter(tweet=tweet).order_by(-date_added)
        context = {
            'tweet': tweet,
            'form': form,
            'comments': comments,
        }
        return render(request, 'to_do/tweet_detail.html', context)

    def post(self, request, pk, date_added=None):
        tweet = NewTweet.objects.get(pk=pk)
        form = CommentForm(request.POST)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.tweet = tweet
            new_comment.save()

        comments = Comment.objects.filter(tweet=tweet).order_by(-date_added)
        context = {
            'tweet': tweet,
            'form': form,
            'comments': comments,
        }
        return render(request, 'to_do/tweet_detail.html', context)


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'to_do/comment_delete.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('tweet-detail', kwargs={'pk': pk})

    def test_funk(self):
        comment = self.get_object()
        return self.request.user == comment.author
