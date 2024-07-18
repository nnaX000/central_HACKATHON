from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm
from django.http import JsonResponse

def posthome(request):
    sort_by = request.GET.get('sort', 'date')
    category = request.GET.get('category', 'latest')
    
    if category == 'my_posts':
        posts = Post.objects.filter(author=request.user)
    elif category == 'liked_posts':
        posts = Post.objects.filter(likes=request.user)
    else:
        posts = Post.objects.all()
    
    if sort_by == 'likes':
        posts = sorted(posts, key=lambda post: post.total_likes, reverse=True)
    else:
        posts = posts.order_by('-date_posted')
    
    return render(request, 'posthome.html', {'posts': posts, 'sort_by': sort_by, 'category': category})

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posthome')
    else:
        form = PostForm()
    return render(request, 'post_form.html', {'form': form})

@login_required
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('posthome')
    else:
        form = PostForm(instance=post)
    return render(request, 'post_form.html', {'form': form})


@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user == post.author:
        post.delete()
    return redirect('posthome')


@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'liked': liked,
            'total_likes': post.likes.count(),
        })
    return redirect('posthome')

# @login_required
# def bookmark_post(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     if post.bookmarks.filter(id=request.user.id).exists():
#         post.bookmarks.remove(request.user)
#     else:
#         post.bookmarks.add(request.user)
#     return redirect('posthome')

# @login_required
# def bookmarked_posts(request):
#     user = request.user
#     posts = Post.objects.filter(bookmarks=user).order_by('-date_posted')
#     return render(request, 'bookmarked_posts.html', {'posts': posts})

@login_required
def user_posts(request):
    user = request.user
    posts = Post.objects.filter(author=user).order_by('-date_posted')
    return render(request, 'user_posts.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'post_detail.html', {'post': post})
