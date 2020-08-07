from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)

from .forms import AddPostForm, UpdatePostForm
from .models import Post, Category


class PostsListView(ListView):
    model = Post
    template_name = 'blog/posts_list.html'
    context_object_name = 'posts'
    paginate_by = 1

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.GET.get('category')
        queryset = queryset.filter(category_id=category)
        return queryset


class PostDetailsView(DetailView):
    model = Post
    template_name = 'blog/post_details.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_has_permission'] = self.request.user.is_authenticated and self.get_object(self.get_queryset()).user == self.request.user
        return context


class ViewsMixin:
    def get_success_url(self):
        return self.object.get_absolute_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_form'] = self.get_form(self.get_form_class())
        return context


class UserHasPermissionMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.get_object(self.get_queryset()).user == self.request.user



class AddPostView(LoginRequiredMixin, ViewsMixin, CreateView):
    model = Post
    template_name = 'blog/add_post.html'
    form_class = AddPostForm

    def form_valid(self, form):
        user = self.request.user
        post = form.save(commit=False)
        post.user = user
        post.save()
        return redirect(post.get_absolute_url())


class UpdatePostView(UserHasPermissionMixin, ViewsMixin, UpdateView):
    model = Post
    template_name = 'blog/update_post.html'
    form_class = UpdatePostForm
    context_object_name = 'post'



class DeletePostView(UserHasPermissionMixin, DeleteView):
    model = Post
    template_name = 'blog/delete_post.html'
    success_url = reverse_lazy('home-page')


class CategoriesListView(ListView):
    model = Category
    template_name = 'blog/index.html'
    context_object_name = 'categories_list'
