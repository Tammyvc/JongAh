from django.shortcuts import render, get_object_or_404,redirect
from .models import Post, Comment
from couple.models import Like,Category
from django.views import View
import markdown,qrcode,os
from accounts.models import Profile, CustomUser
from django.db.models import Q, F
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.http import JsonResponse
from django.db.models.functions import ExtractDay,ExtractYear,ExtractMonth
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt


def index(request):
    user_name = request.session.get('user_name')
    if user_name:
        user = CustomUser.objects.get(name=user_name)
    post_list = Post.objects.all()
    paginator = Paginator(post_list,10)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'jongah/index.html', locals())


def about(request):
    user_name = request.session.get('user_name')
    user = CustomUser.objects.get(name=user_name)
    return render(request, 'jongah/about.html', locals())


def contact(request):
    user_name = request.session.get('user_name')
    user = CustomUser.objects.get(name=user_name)
    return render(request, 'jongah/contact.html', locals())


class PostDetailView(View):

    def get(self, request, category_name,post_slug):
        post = Post.objects.get(slug=post_slug)
        # category = post.category.slug
        comment_list = Comment.objects.filter(target=post)
        post.views += 1
        post.save()
        user_name = request.session.get('user_name')
        if user_name:
            user = CustomUser.objects.get(name=user_name)

        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc', ])
        post.content = md.convert(post.content)

        post.toc = md.toc
        return render(request, f'jongah/{category_name}/{post_slug}.html', locals())

def category_detail(request,category_name):
    category = Category.objects.get(slug=category_name)
    posts = category.post.all()
    paginator = Paginator(posts,12)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request,f'jongah/{category_name}/{category_name}.html',locals())



def search(request):
    """搜索关键词"""
    keyword = request.GET.get('keyword', None)
    user_name = request.session.get('user_name')
    user = CustomUser.objects.get(name=user_name)
    if not keyword:
        post_list = Post.objects.all()
    else:
        # 包含查询的方法，用Q对象来组合复杂查询，title__icontains 他两个之间用的是双下划线（__）链接
        post_list = Post.objects.filter(
            Q(title__icontains=keyword) | Q(desc__icontains=keyword) | Q(content__icontains=keyword))
    paginator = Paginator(post_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'jongah/search_result.html', locals())


def like_post(request):
    if request.method == "POST":
        post_id = int(request.POST.get('post_id'))
        post = Post.objects.get(id=post_id)
        user_name = request.session['user_name']
        user = CustomUser.objects.get(name=user_name)
        print(user.name)
        try:
            like = Like.objects.get(user=user, post=post)
            like.delete()
            post.likes -= 1
            post.save()
            return JsonResponse({'status': 'error', 'message': 'You have already liked this post.'})
        except Like.DoesNotExist:
            Like.objects.create(user=user, post=post)
            post.likes += 1
            post.save()
            return JsonResponse({'status': 'ok', 'like_count': post.likes})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})


def comment_control(request):
    username = request.session['user_name']
    if username:
        comment_content = request.POST.get('comment_content')
        post_id = request.POST.get('post_id')
        comment_user = CustomUser.objects.get(name=username)
        # pid = request.POST.get('pid')
        comment_user_id = comment_user.id  # 获取当前用户的ID

        Comment.objects.create(content=comment_content,target_id=post_id,email=comment_user.email,
                               comment_user_id=comment_user_id)  # 将提交的数据保存到数据库中

        article = list(
            Comment.objects.values('id', 'content','target_id', 'comment_user_id',
                                   'created_time'))  # 以键值对的形式取出评论对象，并且转化为列表list类型

        return JsonResponse(article, safe=False)  # JsonResponse返回JSON字符串，自动序列化，如果不是字典类型，则需要添加safe参数为False
    else:
        return redirect('/login/')

def lastest_comments(request):
    comment_list = Comment.objects.order_by('-created_time')[:10]
    paginator = Paginator(comment_list,5)
    page = request.GET.get('page')
    comments = paginator.get_page(page)
    data = [{'comment':c.content,'user_name':c.comment_user.name,'comment_date':c.created_time} for c in comments]
    return JsonResponse({'comments':data,'has_previous':comments.has_previous(),'has_next':comments.has_next()})

def share_post(request,post_id):
    post = get_object_or_404(Post,id=post_id)
    post_created_year = post.created_time.strftime('%Y')
    post_created_month = post.created_time.strftime('%m')
    post_created_day = post.created_time.strftime('%d')
    share_url = request.build_absolute_uri(post.get_absolute_url())
    qr_code = qrcode.make(share_url)
    return render(request,'jongah/social/share_post.html',locals())

def wgm_video(request):
    videos = Post.objects.filter(category__slug='we-get-married')
    paginator = Paginator(videos,10)
    page = request.GET.get('page')
    try:
        videos = paginator.page(page)
    except PageNotAnInteger:
        videos = paginator.page(1)
    except EmptyPage:
        videos = paginator.page(paginator.num_pages)
    return render(request,'jongah/we-get-married/we-get-married.html',locals())

def wgm_video_detail(request,video_slug):
    video = Post.objects.get(slug=video_slug)
    category = video.category.slug
    wgm_video = video.category
    posts = wgm_video.post.all()

    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc', ])
    video.content = md.convert(video.content)

    video.toc = md.toc

    return render(request, f'jongah/{category}/{video_slug}.html', locals())

def latest_post(request):
    published = timezone.now() - timedelta(weeks=2)
    posts = Post.objects.filter(created_time__gte=published)
    return render(request,'jongah/latest_post.html',locals())

@csrf_exempt
def upload_image(request):
    if request.method == "POST":
        file_obj = request.FILES['file']
        file_name_suffix = file_obj.name.split(".")[-1]
        if file_name_suffix not in ["jpg", "png", "gif", "jpeg", ]:
            return JsonResponse({"message": "错误的文件格式"})

        upload_time = timezone.now()
        path = os.path.join(
            settings.MEDIA_ROOT,
            'image',
            'posts',
            str(upload_time.year),
            str(upload_time.month),
            str(upload_time.day),
        )
        # 如果没有这个路径则创建
        if not os.path.exists(path):
            os.makedirs(path)

        file_path = os.path.join(path, file_obj.name)

        file_url = f'{settings.MEDIA_URL}image/posts/{upload_time.year}/{upload_time.month}/{upload_time.day}/{file_obj.name}'

        if os.path.exists(file_path):
            return JsonResponse({
                "message": "文件已存在",
                'location': file_url
            })

        with open(file_path, 'wb+') as f:
            for chunk in file_obj.chunks():
                f.write(chunk)

        return JsonResponse({
            'message': '上传图片成功',
            'location': file_url
        })
    return JsonResponse({'detail': "错误的请求"})
