from django.views.generic import ListView, DetailView, DeleteView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from posts.models import Post, Status


class PostListView(ListView):
    template_name: str = "posts/list.html"
    model = Post


class PublishedPostListView(ListView):
    template_name: str = "posts/list.html"
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        published_status = Status.objects.get(name="published")
        context['post_list'] = Post.objects.filter(
                                    author=self.request.user
                                    ).filter(
                                        status=published_status).order_by(
                                            "created_on").reverse()
        return context


class DraftPostListView(ListView):
    template_name: str = "posts/list.html"
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pending_status = Status.objects.get(name="draft")
        context['post_list'] = Post.objects.filter(
                                    author=self.request.user
                                    ).filter(
                                        status=pending_status).order_by(
                                            "created_on").reverse()
        return context


class ArchivedPostListView(ListView):
    template_name: str = "posts/list.html"
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        archived_status = Status.objects.get(name="archived")
        context["post_list"] = Post.objects.filter(
                                    author=self.request.user
                                    ).filter(
                                        status=archived_status
                                        ).order_by("title")
        return context


class PostDetailView(DetailView):
    template_name: str="posts/detail.html"
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    template_name: str="posts/new.html"
    model = Post
    fields = ['title', 'subtitle', 'body']

    # Overwriting the form_valid function to set the author field as the user
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name: str="posts/edit.html"
    model = Post
    fields = ["title", "subtitle", "body"]

    # test_func validates the user is the author of the post to be able to manipulate it
    def test_func(self):
        post_obj = self.get_object()
        return post_obj.author == self.request.user


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name: str="posts/delete.html"
    model = Post
    success_url = reverse_lazy("list")

    def test_func(self):
        post_obj = self.get_object()
        return post_obj.author == self.request.user