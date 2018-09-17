from django.shortcuts import render, redirect
from reddit_app.forms import UserForm, UserProfileInfoForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, Post, Comment

### POST VIEWS ##
def post_list(request): 
    # getting all posts
    posts = Post.objects.all()
    return render(request, 'reddit_app/post_list.html', {'posts': posts})

def post_detail(request, pk):
    # getting one post by id (pk)
    post = Post.objects.get(id=pk)
    return render(request, 'reddit_app/post_detail.html', {'post': post})

def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'reddit_app/post_form.html', {'form': form})

def post_edit(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'reddit_app/post_form.html', {'form': form})

def post_delete(request, pk):
    Post.objects.get(id=pk).delete()
    return redirect('post_list')



### COMMENTS VIEWS ###
def comment_list(request):
    comments = Comment.objects.all()
    return render(request, 'reddit_app/comment_list.html', {'comments': comments})

def comment_detail(request, pk):
    # getting one comment by id (pk)
    comment = Comment.objects.get(id=pk)
    return render(request, 'reddit_app/comment_detail.html', {'comment': comment})

def comment_create(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save()
            return redirect('comment_detail', pk=comment.pk)
    else:
        form = CommentForm()
    return render(request, 'reddit_app/comment_form.html', {'form': form})

def comment_edit(request, pk):
    comment = Comment.objects.get(pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save()
            return redirect('comment_detail', pk=comment.pk)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'reddit_app/comment_form.html', {'form': form})

def comment_delete(request, pk):
    Comment.objects.get(id=pk).delete()
    return redirect('comment_list')



### USER AUTH ###

def sendJson(request):
    users = list(User.objects.all().values('email', 'username'))
    return JsonResponse({'users': users})

def index(request):
    return render(request,'reddit_app/index.html')

@login_required
def special(request):
    return HttpResponse("You are logged in !")

@login_required
def user_logout(request):
    logout(request)
    return redirect('index')

def register(request):
    registered = False
    # if we are trying to create a user, not get a new user view
    if request.method == 'POST':
        # we are populating a Form object with data from our request body (username, email, password)
        user_form = UserForm(data=request.POST)
        # we are populating a Form object with data from our request body (profile_pic, portfolio_site)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']
            profile.save()
            registered = True

        else:
            print(user_form.errors,profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()
    return render(request, 'reddit_app/registration.html', {'user_form':user_form,'profile_form':profile_form,'registered':registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return redirect('index')
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print(f'They used username: {username} and password: {password}')
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'reddit_app/login.html', {})