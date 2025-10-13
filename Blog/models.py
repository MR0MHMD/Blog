# from django.db.models.signals import post_delete, pre_save
# from django.dispatch import receiver
import os
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django_jalali.db import models as jmodels
from django.urls import reverse
from django_resized import ResizedImageField
from django.template.defaultfilters import slugify


# Create your models here.
# managers

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = '0', 'Draft'
        PUBLISHED = '1', 'Published'
        REJECTED = '-1', 'Rejected'

    CATEGORY_CHOICES = (
        ('تکنولوژی', "تکنولوژی"),
        ('زبان برنامه نویسی', "زبان برنامه نویسی"),
        ('هوش مصنوعی', "هوش مصنوعی"),
        ('بلاکچین', "بلاکچین"),
        ('سایر', "سایر"),
    )

    # Data
    title = models.CharField(max_length=250, verbose_name='عنوان')
    description = models.TextField(verbose_name='توضیحات')
    slug = models.SlugField(max_length=250, )
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT, verbose_name="وضعیت")
    reading_time = models.PositiveIntegerField(verbose_name="زمان مطالعه")
    category = models.CharField(choices=CATEGORY_CHOICES, default="سایر")
    # Date
    publish = jmodels.jDateTimeField(default=timezone.now, verbose_name="تاریخ انتشار")
    created = jmodels.jDateTimeField(auto_now_add=True)
    updated = jmodels.jDateTimeField(auto_now=True)
    # Relationships
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_posts', verbose_name='نویسدنده')

    object = jmodels.jManager()
    published = PublishedManager()

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]
        verbose_name = "پست"
        verbose_name_plural = "پست ها"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.id])


class Ticket(models.Model):
    subject = models.CharField(verbose_name="موضوع")
    message = models.TextField(verbose_name="پیام")
    name = models.CharField(max_length=250, verbose_name='نام')
    email = models.EmailField(verbose_name='ایمیل')
    phone = models.CharField(max_length=11, verbose_name="شماره تماس")

    class Meta:
        verbose_name = "تیکت"
        verbose_name_plural = "تیکت ها"

    def __str__(self):
        return self.name


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='نظر')
    name = models.CharField(max_length=250, verbose_name='نام')
    body = models.TextField(verbose_name="متن نظر")
    created = jmodels.jDateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated = jmodels.jDateTimeField(auto_now=True, verbose_name="آخرین ویرایش")
    active = models.BooleanField(default=True, verbose_name="وضعیت")

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['created']),
        ]
        verbose_name = "نظر"
        verbose_name_plural = "نظرات"

    def __str__(self):
        return f"{self.name} : {self.post}"


def post_image_upload_to(instance, filename):
    return f"post_images/{instance.post.author}/{filename}"


class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images', verbose_name='پست')
    image_file = ResizedImageField(upload_to=post_image_upload_to, size=(500, 500), quality=75, crop=['middle', 'center'], verbose_name='تصویر')
    title = models.CharField(max_length=250, verbose_name='عنوان', blank=True)
    description = models.TextField(verbose_name='توضیحات', blank=True)
    created = jmodels.jDateTimeField(auto_now_add=True)

    def __str__(self):
        return os.path.basename(self.image_file.name) if self.image_file else self.title

    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['created']),
        ]
        verbose_name = "تصویر"
        verbose_name_plural = "تصاویر"


class Account(models.Model):
    user = models.OneToOneField(User, related_name="account", on_delete=models.CASCADE)
    date_of_birth = jmodels.jDateField(null=True, blank=True, verbose_name="تاریخ تولد")
    bio = models.TextField(verbose_name='بیوگرافی', blank=True, null=True)
    photo = ResizedImageField(upload_to='profile_image', size=(500, 500), quality=60,
                              crop=['middle', 'center'], verbose_name='تصویر', blank=True, null=True)
    job = models.CharField(max_length=250, verbose_name='شغل', blank=True, null=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "اکانت"
        verbose_name_plural = "اکانت ها"
