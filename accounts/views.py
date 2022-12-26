from django.shortcuts import render, get_object_or_404, redirect
from .models import CustomUser, ConfirmString,Profile
from django.urls import reverse
from django.conf import settings
from django.views import View
from django.core.mail import EmailMultiAlternatives
import datetime
import hashlib


class LoginView(View):
    def get(self, request):
        return render(request, 'account/login.html')

    def post(self, request):
        if request.session.get('is_login',None):
            return render(request,'jongah/index.html')
        if request.method == 'POST':
            username_or_email = request.POST.get('username_or_email')
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
                return redirect(reverse('couple:index'))
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
        return render(request,'jongah/index.html')

def user_settings(request,username):
    if username:

        user = CustomUser.objects.get(name=username)
        profile = Profile.objects.get(user=user)
        return render(request,'account/user_center.html',locals())
    return render(request, 'account/edit.html',locals())

class UserEditView(View):

    def get(self,request,user_name):
        return render(request,'account/edit.html',locals())

    def post(self,request,user_name):
        # try:
        user = CustomUser.objects.get(name=user_name)
        nickname = request.POST.get('nickname', None)
        sex = request.POST.get('sex', None)
        introduction = request.POST.get('desc', None)
        profile = Profile.objects.filter(user=user)[0]
        if profile:
            profile.nickname = nickname
            profile.sex = sex
            profile.introduction = introduction
            profile.save()
        else:
            profile = Profile.objects.create(user=user,nickname=nickname,
                                  sex=sex,introduction=introduction)
            return render(request, 'account/user_center.html',locals())

        return render(request,'account/user_center.html',locals())

def modify_photo(request):
    pass
