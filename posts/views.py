from urllib import request
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from .models import Post
from .forms import PostForm
from cloudinary.forms import cl_init_js_callbacks
# Create your views here.


def index(request):
    if request.method == 'POST':
        form = PostForm(request.POST,request.FILES)

        if form.is_valid():

            form.save()

            return HttpResponseRedirect('/')

        else:
            return HttpResponseRedirect(form.erros.as_json())

    posts = Post.objects.all().order_by('-created_at')[:20]
    return render(request, 'posts.html',
                  {'posts': posts})
def delete(request, post_id):
    post = Post.objects.get(id = post_id)
    post.delete()
    return HttpResponseRedirect('/')

def edit(request, post_id):
    post = Post.objects.get(id = post_id)

    if request.method == 'POST':
       form = PostForm(request.POST, request.FILES, instance=post)
       if form.is_valid():
           form.save()
           return HttpResponseRedirect('/')
       else:
            return HttpResponse("not valid")
    
    form = PostForm
    
    return render(request, 'edit.html',
                   {'post':post, 'form':form } 
    )


def like(request, post_id):
    post= Post.objects.get(id = post_id)
    post.like += 1
    post.save()
    return HttpResponseRedirect('/')


