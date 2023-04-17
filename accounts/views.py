from django.shortcuts import render, get_object_or_404, redirect
from .models import CustomUser, ConfirmString,Profile
from django.urls import reverse
from .forms import UserProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,authenticate
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.views import View
from django.core.mail import EmailMultiAlternatives
import datetime
import hashlib
from django.http import HttpResponse


def index(request):
    render(request,'jongah/index.html')


class LoginView(View):
    def get(self, request):
        return render(request, 'account/login.html')

    def post(self, request):

        if request.session.get('is_login',None):
            return render(request,'jongah/index.html',locals())
        if request.method == 'POST':
            username_or_email = request.POST.get('username_or_email')
            user = CustomUser.objects.get(name=username_or_email)
            profile = Profile.objects.get(user=user)
            password = request.POST.get('password')
            message = '请检查填写的内容!'

            try:
                if '@' in username_or_email:
                    user = CustomUser.objects.get(email=username_or_email)
                else:
                    user = CustomUser.objects.get(name=username_or_email)
            except:
                message = '用户不存在！'
                return render(request, 'account/login.html', locals())

            if not user.has_confirmed:
                message = '该用户还未经过邮件确认!'
                return render(request, 'account/login.html', locals())

            if user.password == self.hash_code(password):

                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                return redirect('accounts:user_center',username=username_or_email)
            else:
                message = '密码不正确！'
                return render(request, 'account/login.html', locals())
        return render(request, 'account/login.html')

    def hash_code(self, s, salt='jongahlove'):
        h = hashlib.sha256()
        s += salt
        h.update(s.encode())
        return h.hexdigest()


class RegisterView(View):
    def get(self, request):
        return render(request, 'account/register.html')

    def post(self, request):
        message = "请检查填写内容!"
        if request.method == 'POST':
            email = request.POST.get('email')
            username = request.POST.get('username')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')

            if password1 != password2:
                message = "两次输入密码不同!"
                return render(request, 'account/register.html', locals())
            else:
                same_name_user = CustomUser.objects.filter(name=username)
                if same_name_user:
                    message = '用户名已经存在!'
                    return render(request, 'account/register.html', locals())
                same_email_user = CustomUser.objects.filter(email=email)
                if same_email_user:
                    message = '该邮箱已经被注册了！'
                    return render(request, 'account/register.html', locals())

                password_1 = self.hash_code(password1)
                new_user = CustomUser.objects.create(
                    name=username, email=email, password=password_1
                )
                new_user_profile = Profile.objects.create(user=new_user)

                code = self.make_confirm_string(new_user)
                self.send_email(email, code)

                message = '请前往邮箱确认!'
                return render(request, 'account/login.html', locals())

        return render(request, 'account/register.html', locals())

    def hash_code(self, s, salt='jongahlove'):
        h = hashlib.sha256()
        s += salt
        h.update(s.encode())
        return h.hexdigest()

    def make_confirm_string(self, user):
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        code = self.hash_code(user.name, now)
        ConfirmString.objects.create(code=code, user=user)
        return code

    def send_email(self, email, code):
        subject = '来自www.jongah.love的注册确认邮件'
        text_content = '''
        感谢注册www.jongah.love，这里是宗亚夫妇分享站点，专注于宗亚夫妇俩人日常活动的分享！\
        如果你看到这条消息，说明你的邮箱服务器不提供HTML链接功能，请联系管理员
        '''
        html_content = '''
                            <p>感谢注册<a href="http://{}/confirm/?code={}" target=blank>www.jongah.love</a>，\
                            这里是宗亚夫妇分享站点，专注于宗亚夫妇俩人日常活动的分享！</p>
                            <p>请点击站点链接完成注册确认！</p>
                            <p>此链接有效期为{}天！</p>
                            '''.format('127.0.0.1:8001', code, settings.CONFIRM_DAYS)
        msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()


class ConfirmView(View):
    def get(self, request):
        code = request.GET.get('code', None)
        message = ''
        try:
            confirm = ConfirmString.objects.get(code=code)
        except:
            message = '无效的确认请求!'
            return render(request, 'account/confirm.html', locals())


class ConfirmView(View):
    def get(self, request):
        code = request.GET.get('code', None)
        message = ''
        try:
            confirm = ConfirmString.objects.get(code=code)
        except:
            message = '无效的确认请求!'
            return render(request, 'account/confirm.html', locals())

        c_time = confirm.c_time.replace(tzinfo=None)
        now = datetime.datetime.now()
        if now > c_time + datetime.timedelta(settings.CONFIRM_DAYS):
            confirm.user.delete()
            message = '您的邮件已经过期!请重新注册!'
            return render(request, 'account/confirm.html', locals())
        else:
            confirm.user.has_confirmed = True
            confirm.user.save()
            confirm.delete()
            message = '感谢确认,请使用账户登录!'
            return render(request, 'account/confirm.html', locals())

class PasswordForgetView(View):
    def get(self,request):
        return render(request,'account/password_reset.html')

class LoggoutView(View):
    def get(self,request):
        request.session.flush()
        return redirect('accounts:login')

# @login_required
def user_center(request,username):
    if username:
        user = CustomUser.objects.get(name=username)
        profile = Profile.objects.get(user=user)
        return render(request,'account/user_center.html',locals())
    return render(request, 'jongah/index.html',locals())


# @login_required
def edit_profile(request,user_name):
    user = CustomUser.objects.get(name=user_name)
    user_profile = Profile.objects.get(user=user)
    if request.method == 'POST':
        user_profile_form = UserProfileForm(request.POST)
        if user_profile_form.is_valid():
            nickname = request.POST.get('nickname')
            sex = request.POST.get('sex')
            introduction = request.POST.get('introduction')
            user_profile.nickname = nickname
            user_profile.sex = sex
            user_profile.introduction = introduction
            user_profile.save()
            return redirect('accounts:user_center',username=user_name)
    else:
        user_profile_form = UserProfileForm()
    return render(request,'account/edit.html',locals())

def cover(request,user_name):
    if request.method == 'POST':
        user = get_object_or_404(CustomUser, name=user_name)
        cover = request.FILES.get('cover_file')
        cover_name = request.POST.get('cover_name')

        # 获取 FileSystemStorage 对象
        fs = FileSystemStorage(location=settings.MEDIA_ROOT)

        # 保存头像文件到媒体文件夹
        saved_file = fs.save(cover_name, cover)

        # 更新用户个人资料中的头像文件路径
        user.profile.cover = saved_file
        user.profile.save()

        return HttpResponse('封面上传成功！')

def avatar(request,user_name):
    if request.method == 'POST':
        user = get_object_or_404(CustomUser, name=user_name)
        avatar = request.FILES.get('avatar_file')
        avatar_name = request.POST.get('avatar_name')

        # 获取 FileSystemStorage 对象
        fs = FileSystemStorage(location=settings.MEDIA_ROOT)

        # 保存头像文件到媒体文件夹
        saved_file = fs.save(avatar_name, avatar)

        # 更新用户个人资料中的头像文件路径
        user.profile.photo = saved_file
        user.profile.save()

        return HttpResponse('头像上传成功！')
