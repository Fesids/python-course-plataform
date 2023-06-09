from django.db import models
from django.urls import reverse
from django.core.files import File
from django.conf import settings


from io import BytesIO
from PIL import Image


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField()

    def __str__(self):
        return self.name


class Course(models.Model):
    course_title = models.CharField(max_length=244)
    course_author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='course_author',
                                      on_delete=models.CASCADE, null=True, default='')
    slug = models.CharField(auto_created=course_title, max_length=255)
    description = models.CharField(max_length=244)
    price = models.FloatField()
    image = models.ImageField(upload_to="uploads/books", blank=True, null=True, default=" ")
    thumbnail = models.ImageField(upload_to="uploads/books", blank=True, null=True, default=" ")
    category = models.ForeignKey(Category, related_name="course_category",
                                 on_delete=models.CASCADE)
    students = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='students_joined',
                                      blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta():
        ordering = ('-created_at',)

    def __str__(self):
        return self.course_title

    def get_url(self):
        return reverse('course_detail', args=[self.id])

    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO
        img.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name=image.name)

        return thumbnail

    def get_image(self):
        if self.image:
            return 'http://127.0.0.1:8000'+self.image.url
        return ''

    def get_thumbnail(self):
        if self.thumbnail:
            return 'http://127.0.0.1:8000'+self.thumbnail.url

        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()

                return 'http://127.0.0.1:8000'+self.thumbnail.url

            else:
                return ''

class Comment(models.Model):
    course = models.ForeignKey(Course, related_name='comments', on_delete=models.CASCADE)
    comment_author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user',
                                       on_delete=models.CASCADE)
    username = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['createdAt']

    def __str__(self):
        return f'Comment by {self.username} on {self.course}'





