from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
import random

def sex_choice():
    sex = ['男','女']
    return random.choice(sex)

def photo_choice():
    photo_url = ['image/default/photo/1.png',
                 'image/default/photo/2.png',
                 'image/default/photo/3.png',
                 'image/default/photo/4.png',
                 'image/default/photo/5.png',
                 'image/default/photo/6.png',
                 'image/default/photo/7.png',
                 'image/default/photo/8.png',
                 'image/default/photo/9.png',
                 'image/default/photo/10.png',]
    return random.choice(photo_url)

def intro_choice():
    intro = ['孤单就是这样一种东西：没有觉察到就不存在，而一旦觉察，它便如影随形',
             '当你意识到自己是个谦虚的人的时候，你马上就已经不是个谦虚的人了',
             '淡蓝色，并不是我的最爱，却是我最难忘的',
             '好想好想见你一面，直到想遍了你不在身边的每个日日夜夜',
             '我从来不知道什么叫淑女，更不装，我活的随意',
             '没有一种生命的轮回是命中注定的，就像，隔夜的狂欢',
             '相信你只是怕伤害我，而不是骗我',
             '没有人天生是好脾气，只是在乎的东西多了，也就不得不收起了负面的自己',
             '爱上一个人的时候，总会有点害怕，怕得到他，怕失掉他',
             '孤独，是给你思考自己的时间']
    return random.choice(intro)


class CustomUser(models.Model):
    name = models.CharField(max_length=128, unique=True,verbose_name='用户名')
    password = models.CharField(max_length=256,verbose_name='密码')
    email = models.EmailField(unique=True,verbose_name='邮箱')
    last_login = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name='最后登录时间')
    is_active = models.BooleanField(default=True,verbose_name='是否激活')
    c_time = models.DateTimeField(auto_now_add=True,verbose_name='注册时间')
    has_confirmed = models.BooleanField(default=False,verbose_name='确认时间')

    class Meta:
        ordering = ['-c_time']
        verbose_name = verbose_name_plural = '身份'

    def __str__(self):
        return self.name

def upload_to(instance,filename):
    return f'image/users/{instance.user.name}/{filename}'

class Profile(models.Model):

    sex_choice = (
        ('male','男'),
        ('female','女'),
    )

    nickname = models.CharField(max_length=128,verbose_name='昵称',blank=True)
    user = models.OneToOneField('CustomUser', on_delete=models.CASCADE, verbose_name='用户')
    sex = models.CharField(max_length=255,verbose_name='性别',blank=True,choices=sex_choice)
    introduction = models.TextField(max_length=1000,blank=True,verbose_name='简介',default=intro_choice)
    photo = models.ImageField(upload_to=upload_to, blank=True,verbose_name='头像',default=photo_choice)
    cover = models.ImageField(upload_to=upload_to,blank=True,verbose_name='封面')

    class Meta:
        verbose_name = verbose_name_plural = '资料'

    def __str__(self):
        return "{}的个人资料".format(self.user.name)

    def photo_url(self):
        if self.photo and hasattr(self.photo,'url'):
            return self.photo.url
        else:
            return f'/media/image/default/photo/{random.randint(1,10)}.png'




class ConfirmString(models.Model):
    code = models.CharField(max_length=256,verbose_name='确认码')
    user = models.OneToOneField('CustomUser', on_delete=models.CASCADE,verbose_name='用户')
    c_time = models.DateTimeField(auto_now_add=True,verbose_name='确认时间')

    class Meta:
        ordering = ['-c_time']
        verbose_name = verbose_name_plural = '确认码'

    def __str__(self):
        return self.user.name + ': ' + self.code


