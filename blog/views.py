from django.http import FileResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required

import datetime
from datetime import timedelta

from .models import Post, Reply
from .forms import PostForm, ReplyForm

# from reply.models import Reply
# from reply.forms import ReplyForm

# Create your views here.
@login_required(login_url='user:index')
def blog_view(request):
    postlist = Post.objects.all()
    paginator = Paginator(postlist, 10)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('blog:blog')
    else:
        form = PostForm()
    return render(request, 'blog.html', {'posts':posts, 'form': form})

@login_required(login_url='/')
def blogdt_view(request, post_id):
    post = Post.objects.prefetch_related('reply_set').get(id=post_id)
    replyForm = ReplyForm()
    response = render(request, 'blog-details.html', {'post':post, 'replyForm':replyForm})
    
    expire_date, now = datetime.datetime.now(), datetime.datetime.now()
    expire_date += timedelta(days=1)
    expire_date = expire_date.replace(hour=0, minute=0, second=0, microsecond=0)
    expire_date -= now
    max_age = expire_date.total_seconds()
    
    cookie_value = request.COOKIES.get('hitblog', '_')

    if f'_{post_id}_' not in cookie_value:
        cookie_value += f'{post_id}_'
        response.set_cookie('hitblog', value=cookie_value, max_age=max_age, httponly=True)
        post.view_count += 1
        post.save()
    return response

@login_required(login_url='/') 
def create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            post = form.save(commit=False)
            post.author_id = request.user.id  # Set the author ID
            post.save()
            return redirect('blog:blog')
    else:
        form = PostForm(user=request.user)
    return render(request, 'create.html', {'form': form})

@login_required(login_url='/')
def delete(request, post_id):
    post = Post.objects.get(id=post_id)
    post.delete()
    return redirect('blog:blog')

@login_required(login_url='/')
def edit(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == "POST":
        postForm = PostForm(request.POST, request.FILES, instance=post)
        if postForm.is_valid():
            postForm.save()
            return redirect('blog:blogdt', post_id)
    else:
        postForm = PostForm(instance=post, initial={
            'title': post.title,
            'content': post.content,
            'file': post.file,
        })
        postForm.fields['file'].required = False
    return render(request, 'change_create.html', {'form':postForm, 'post':post})

def download_file(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    file_path = post.file.path
    return FileResponse(open(file_path, 'rb'), as_attachment=True)

@login_required(login_url='/')
def delete_comment(request, post_id, com_id):
    my_com = Reply.objects.get(id=com_id)
    my_com.delete()
    return redirect('/blog/'+str(post_id))

@login_required(login_url='/')
def edit_comment(request, post_id, com_id):
    post = Post.objects.prefetch_related('reply_set').get(id=post_id)
    comment = get_object_or_404(Reply, id=com_id)
    if request.method == "POST":
        replyForm = ReplyForm(request.POST, instance=comment)
        if replyForm.is_valid():
            comment = replyForm.save()
            return redirect('blog:blogdt', post_id)
    else:
        replyForm = ReplyForm(instance=comment)
    return render(request, 'comment_edit.html', {'post':post, 'comment':comment})