from django.contrib import admin
from .models import Course, Category
# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {"slug": ('name',)}

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    search_fields = ['course_title', 'course_author', 'slug', 'description', 'price', 'category']
    list_display = ['course_title', 'course_author', 'slug', 'description', 'price', 'category']
    prepopulated_fields = {'slug':('course_title',)}
