from django.shortcuts import render,get_list_or_404
from .models import Post
from django.views import View
import markdown,pygments
from accounts.models import Profile,CustomUser

def index(request):
    return render(request, 'jongah/index.html',{})

def about(request):
    return render(request, 'jongah/about.html',{})

def contact(request):
    return  render(request,'jongah/contact.html',{})

class PostDetailView(View):

    def get(self,request,wgm_id):
        post = Post.objects.get(id=wgm_id)
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',])
        post.content = md.convert(post.content)

        post.toc = md.toc


        return render(request,f'jongah/wgm/{wgm_id}.html',locals())
