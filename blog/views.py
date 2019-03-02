from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.http import HttpResponse
from .models import Post

# I'm not using this function based view to print the post but the class based.


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)


# Here I'll be using class_based views to display our post on the home page
"""
the ListView class by default is looking for a template called 'blog/post_list' which is the generic
view convention and the variable that is looking for to loop over is called 'object_list'.
By using the convention we will only need to set one attributes which is the 'model' that we want
to work with and if we want to we can add the 'ordering' variable for proper ordering of the posts.
"""


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'       # <app>/<model>_<viewtype>.html ==> default
    context_object_name = 'posts'          # object_list ==> default
    ordering = ['-date_posted']            # This shows the latest post at the top
    paginate_by = 10


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        # We are overwriting the order_by attribute by calling it as a method
        return Post.objects.filter(author=user).order_by('-date_posted')


# This is the view for the individual post which will be handled by DetailView

class PostDetailView(DetailView):
    model = Post


# The create view handle the creation of new post
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    """
    If I did not provide a template for the updateview, it will automatically use the CreateView
    template by default.
    """
    template_name = 'blog/post_update.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# The UserPassesTestMixin run this test_func() to check if the user meet a certain condition
    def test_func(self):
        """ This get_object() is a function of the UpdateView that get the exact post that we are
         currently updating """
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
