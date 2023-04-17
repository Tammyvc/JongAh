from django.db import models
from django.conf import settings
from tinymce.models import HTMLField
from accounts.models import CustomUser
import datetime


class Category(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )

    name = models.CharField(max_length=50, verbose_name='名称')
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS, verbose_name='状态')
    is_nav = models.BooleanField(default=False, verbose_name='是否为导航')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='作者', on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    slug = models.SlugField(max_length=250,blank=True)


    class Meta:
        verbose_name = verbose_name_plural = '分类'

    def get_absolute_url(self):
        from django.urls import reverse
        if self.slug == 'we-get-married':
            return reverse('couple:wgm_video')
        elif self.slug == 'half-drama-half-you':
            return reverse('couple:category_detail',args=(self.slug,))
        elif self.slug == 'jongah-fellow':
            return reverse('couple:category_detail',args=(self.slug,))

        return reverse('couple:wgm_video')


    def __str__(self):
        return self.name


class Tag(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )

    name = models.CharField(max_length=25, verbose_name='名称')
    status = models.PositiveIntegerField(default=STATUS_NORMAL,
                                         choices=STATUS_ITEMS, verbose_name='状态')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='作者', on_delete=models.CASCADE)  # 级联删除
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = verbose_name_plural = '标签'

    def __str__(self):
        return self.name


class Post(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_DRAFT = 2
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
        (STATUS_DRAFT, '草稿'),
    )

    def get_upload_path(self, filename):
        # 获取帖子标题，并将其转换为文件名格式（去除空格和特殊字符）
        title = self.title.replace(' ', '_').replace('-', '_')
        filename = filename.replace(' ', '_').replace('-', '_')
        # 返回完整的上传路径
        return 'thumbnail/image/posts/{}/{}/{}'.format(title, datetime.date.today().strftime('%Y%m%d'), filename)


    title = models.CharField(max_length=255,verbose_name='标题')
    desc = models.CharField(max_length=1024,blank=True,verbose_name='摘要')
    content = HTMLField(verbose_name='正文',help_text='正文必须用MarkDown格式')
    status = models.PositiveIntegerField(default=STATUS_NORMAL,choices=STATUS_ITEMS,verbose_name='状态')
    image = models.ImageField(upload_to=get_upload_path,blank=True,null=True,verbose_name='图片')

    category = models.ForeignKey(Category,verbose_name='分类',on_delete=models.CASCADE,related_name='post')
    tags = models.ManyToManyField(Tag,verbose_name='标签')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name='作者',on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    likes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    slug = models.SlugField(max_length=250,blank=True)

    class Meta:
        verbose_name = verbose_name_plural = '文章'
        ordering = ['-id']

    def __str__(self):
        return self.title


    def get_absolute_url(self):
        from django.urls import reverse
        if self.category.slug == 'we-get-married':
            return reverse('couple:wgm_video_detail',args=(self.slug,))
        elif self.category.slug == 'half-drama-half-you' or self.category.slug == 'jongah-fellow':
            return reverse('couple:post_detail',args=(self.category.slug,self.slug))



class Comment(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = (
        (STATUS_NORMAL, '正常'),
        (STATUS_DELETE, '删除'),
    )
    target = models.ForeignKey(Post,verbose_name='评论目标',on_delete=models.CASCADE,related_name='comment')
    comment_user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,verbose_name='评论者',null=True)
    content = models.CharField(max_length=2000,verbose_name='内容')
    nickname = models.CharField(max_length=50,verbose_name='昵称')
    email = models.EmailField(verbose_name='邮箱')
    status = models.PositiveIntegerField(default=STATUS_NORMAL,choices=STATUS_ITEMS,verbose_name='状态')
    created_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')

    class Meta:
        verbose_name = verbose_name_plural = '评论'


class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,blank=True,verbose_name='用户')
    post = models.ForeignKey(Post, on_delete=models.CASCADE,verbose_name='帖子')

    class Meta:
        verbose_name = verbose_name_plural = '点赞'
