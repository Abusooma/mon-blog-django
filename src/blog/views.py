from datetime import date

from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from django import forms
from .models import BlogPost


class IndexView(ListView):
    model = BlogPost
    template_name = 'blog/index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            return queryset
        return queryset.filter(published=True)


class PostView(DetailView):
    model = BlogPost
    template_name = 'blog/blogpost.html'
    context_object_name = 'post'


@method_decorator(login_required, name='dispatch')
class CreatePostView(CreateView):
    model = BlogPost
    fields = ['title', 'content', 'published', 'author', 'create_on', 'thumbnail']
    template_name = 'blog/create_post.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['create_on'].widget = forms.SelectDateWidget(years=range(2020, 2026))
        form.fields['author'].initial = self.request.user
        form.fields['create_on'].initial = date.today()
        return form


class UpdatePostView(UpdateView):
    model = BlogPost
    fields = ['title', 'content', 'published', 'author', 'create_on', 'thumbnail']
    template_name = 'blog/update_post.html'

    def get_success_url(self):
        return reverse('blog:postview', kwargs={'slug': self.object.slug})

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['create_on'].widget = forms.SelectDateWidget(years=range(2020, 2026))
        return form


class DeletePostView(DeleteView):
    model = BlogPost
    template_name = 'blog/delete_post.html'
    context_object_name = 'post'
    success_url = reverse_lazy('home')




"""def index(request):
    if request.user.is_authenticated:
        posts = BlogPost.objects.all()
    else:
        posts = BlogPost.objects.filter(published=True)

    return render(request, 'blog/index.html', {'posts': posts})"""

"""def post_view(request, slug):
    post = BlogPost.objects.get(slug=slug)
    return render(request, 'blog/blogpost.html', {'post': post})"""


"""def create_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            form.instance.author = request.user
            form.save()
    else:
        form = BlogPostForm(initial={'create_on': date.today(), 'author': request.user})
        form.fields['create_on'].widget = forms.SelectDateWidget(
            years=range(2010, 2030)
        )
    return render(request, 'blog/create_post.html', {'form': form})"""


