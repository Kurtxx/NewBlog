from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post, Comment, Category
from .forms import CommentForm

# Create your views here.



def home(request):

    posts = Post.objects.all()

    context = {
        'posts': Post.objects.all(),
    }
    if 'search' in request.GET:
        search_term = request.GET['search']
        posts = Post.filter(text__icontains=search_term)
        
    return render(request, 'blog/home.html', context)




class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html' # <app>/model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 3




class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')




class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'




class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'post_category', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    template_name = 'blog/post_forms.html'




class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'post_category', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    template_name = 'blog/post_forms.html'




class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    template_name = 'blog/post_confirm_delete.html'




class KategoriaCreateView(LoginRequiredMixin, CreateView):
    model = Category
    fields = ['name']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    template_name = 'blog/AddCategory.html'


def CategoryDetail(request, slug):
    template_name = 'blog/category_detail.html'  # <app>/<model>_<viewtype>.html

    category = get_object_or_404(Category, slug=slug)
    post = Post.objects.filter(post_category=category)

    context = {
        'category': category,
        'posts': post,

    }
    return render(request, template_name, context)


#class CategoryDetail(ListView):
#    model = Post
#    model = Category
#    template_name = 'blog/category_detail.html'  # <app>/<model>_<viewtype>.html
#    context_object_name = 'posts'
#    paginate_by = 3

#    def get_queryset(self):
#        category = get_object_or_404(Category, slug=slug)
#        return Post.objects.filter(post_category=category)

@login_required
def AddComment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, f'Dodałeś Komentarz!')
            return redirect('post-detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/Addcomment.html', {'form': form})


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
