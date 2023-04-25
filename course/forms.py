from django import forms
from .models import Course


class CourseCreateForm(forms.ModelForm):

    class Meta:
        model = Course
        fields = ['course_title', 'description', 'price', 'image', 'thumbnail', 'category']