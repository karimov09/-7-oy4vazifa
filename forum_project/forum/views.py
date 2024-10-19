from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Topic, Comment
from .forms import TopicForm, CommentForm
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages


@login_required
def create_topic(request):
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.created_by = request.user
            topic.save()
            return redirect('topic_detail', pk=topic.pk)
    else:
        form = TopicForm()
    return render(request, 'create_topic.html', {'form': form})

@login_required
def update_topic(request, pk):
    topic = get_object_or_404(Topic, pk=pk)
    if request.method == 'POST':
        form = TopicForm(request.POST, instance=topic)
        if form.is_valid():
            form.save()
            return redirect('forum:topic_detail', pk=pk)
    else:
        form = TopicForm(instance=topic)
    return render(request, 'update_topic.html', {'form': form})



def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Ro'yxatdan o'tish muvaffaqiyatli bo'ldi!")
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Login muvaffaqiyatli amalga oshirildi!")
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    messages.success(request, "Logout muvaffaqiyatli amalga oshirildi!")
    return redirect('index')



def home(request):
    topics = Topic.objects.all()
    return render(request, 'home.html', {'topics': topics})

def topic_detail(request, pk):
    topic = get_object_or_404(Topic, pk=pk)
    comments = topic.comments.all()
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.topic = topic
            comment.created_by = request.user
            comment.save()
            return redirect('topic_detail', pk=pk)
    else:
        comment_form = CommentForm()
    return render(request, 'topic_detail.html', {'topic': topic, 'comments': comments, 'comment_form': comment_form})
