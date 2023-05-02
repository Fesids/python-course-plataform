from django import forms
from .models import Course, Comment


class CourseCreateForm(forms.ModelForm):

    class Meta:
        model = Course
        fields = ['course_title', 'description', 'price', 'image', 'thumbnail', 'category']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']


class UpdateCommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['body']
