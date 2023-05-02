from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import TemplateResponseMixin, View
from django.views import generic
from django.views.generic import ListView
from django.db.models import Q
from django.utils.text import slugify
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Course, Comment
from .forms import CourseCreateForm, CommentForm, UpdateCommentForm


class CourseGenericMixin(TemplateResponseMixin,View):
    model = Course

class CourseDetail(generic.DetailView, CourseGenericMixin):
    #model = Course
    course = None
    comment = None
    comments = None
    template_name = "course/manage/course_detail.html"

    def get_formset(self, request, data=None):
        return CommentForm(data=data)

    def dispatch(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        self.course = get_object_or_404(Course, id=pk)
        self.comments = Comment.objects.filter(course=self.course, active=True)
        return super().dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        form = self.get_formset(request)
        return self.render_to_response({
            "course": self.course,
            "form": form,
            "comments": self.comments
        })

    def post(self, request, *args, **kwargs):
        form = self.get_formset(request, request.POST)

        if form.is_valid():
            self.comment = form.save(commit=False)
            self.comment.username = request.user.username
            self.comment.email = request.user.email
            self.comment.course = self.course
            self.comment.comment_author = request.user

            self.comment.save()
            return redirect("detail_course", pk=self.course.pk)
        return self.render_to_response({
            "added": True
        })
class CourseDelete(generic.DeleteView, CourseGenericMixin):
    template_name = "course/manage/course_delete.html"
    context_object_name = 'course'
    success_url = reverse_lazy("")
    course = None

    def dispatch(self, request, *args, **kwargs):
        id = kwargs.get('id')
        self.course = get_object_or_404(Course, id=id)
        return super().dispatch(request, id)

    def get(self, request, *args, **kwargs):
        return self.render_to_response({
            "course": self.course
        })

    def post(self, request, *args, **kwargs):
        id = kwargs.get("id")
        course_to_delete = Course.objects.filter(id=id, course_author=request.user)

        if course_to_delete:
            course_to_delete.delete()
            redirect("own_course_list")

        return self.render_to_response({
            "course": course_to_delete
        })


class CourseUpdate(generic.UpdateView, CourseGenericMixin):
    template_name = "course/manage/course_update.html"
    fields = ['image', 'course_title','description', 'price', 'category']
    success_url = reverse_lazy("own_course_list")


class OwnCourseList(CourseGenericMixin):
    template_name = 'course/manage/own_course_list.html'
    own_course_list = None

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        self.own_course_list = Course.objects.filter(course_author=user)
        return super().dispatch(request)

    def get(self, request, *args, **kwargs):
        return self.render_to_response({
            "own_course_list": self.own_course_list
        })


class CreateCourse(CourseGenericMixin):
    template_name = 'course/manage/course_create.html'

    def get_formset(self, data=None, files=None):
        return CourseCreateForm(data=data, files=files)

    def get(self, request, format=None):
        form = self.get_formset()
        return self.render_to_response({
            "form": form
        })

    def post(self, request, *args, **kwargs):
        form = self.get_formset(request.POST, request.FILES)
        if form.is_valid():
            form.instance.course_author = request.user
            form.instance.slug = slugify(form.cleaned_data['course_title'])
            form.save()
            return redirect("own_course_list")
        return self.render_to_response({
            "form": form
        })

class SearchCourse(CourseGenericMixin):

    template_name = 'search/search.html'
    courses = None

    def get(self, request, *args, **kwargs):

        self.courses = Course.objects.all()

        return self.render_to_response({
            "courses": self.courses
        })


class CourseSearchList(TemplateResponseMixin, View):
    model = Course
    template_name = "search/course_search_list.html"
    results = None

    def dispatch(self, request, *args, **kwargs):

        query = request.GET.get('search')
        if query == '':
            query = 'a'

        self.results = Course.objects.filter(
            Q(course_title__icontains=query) | Q(course_author__username__icontains=query)
            | Q(category__name__icontains=query)
        )

        return self.render_to_response({
            "query": query,
            "results": self.results
        })


class EnrollStudent(CourseGenericMixin):
    template_name = 'course/enroll/enroll_course.html'
    course = None

    def dispatch(self, request, *args, **kwargs):
        id = kwargs.get("id")
        self.course = get_object_or_404(Course, id=id)

        return super().dispatch(request, id)

    def get(self, request, *args, **kwargs):
        return self.render_to_response({
            "course": self.course
        })

    def post(self, request, *args, **kwargs):
        course = self.course
        course.students.add(request.user)

        if (request.user in course.students.all()):
         return redirect('courses_you_are_enroll')
        return self.render_to_response({
            "enrolled": True
        })


class UnrollStudents(CourseGenericMixin):
    template_name = 'course/enroll/unroll_course.html'
    course = None

    def dispatch(self, request, *args, **kwargs):
        id = kwargs.get("id")
        self.course = get_object_or_404(Course, id=id)
        return super(UnrollStudents, self).dispatch(request, id)

    def get(self, request, *args, **kwargs):
        return self.render_to_response({
            "course": self.course
        })

    def post(self, request, *args, **kwargs):
        try:
            self.course.students.remove(request.user)
            return redirect("courses_you_are_enroll")

        except:
            raise AssertionError("failed to unrolled current user")




class CourseYouAreEnroll(CourseGenericMixin):
    template_name = 'course/manage/courses_you_are_enroll.html'
    courses = None

    def dispatch(self, request, *args, **kwargs):
        self.courses = Course.objects.filter(students=request.user)
        return super().dispatch(request)

    def get(self, request, *args, **kwargs):

        return self.render_to_response({
            "courses": self.courses
        })


## Comment views


class UpdateComment(CourseGenericMixin):

    template_name = 'comment/manage/update_comment.html'
    course = None
    comment = None

    def get_formset(self, data=None):
        return UpdateCommentForm(data=data, instance=self.comment)

    def dispatch(self, request, *args, **kwargs):
        course_id = kwargs.get("course_id")
        comment_id = kwargs.get("comment_id")
        self.course = get_object_or_404(Course, id=course_id)
        self.comment = get_object_or_404(Comment, course=self.course, id=comment_id)
        return super().dispatch(request, kwargs)

    def get(self, request, *args, **kwargs):
        form = self.get_formset()
        return self.render_to_response({
            "comment": self.comment,
            "form": form
        })

    def post(self, request, *args, **kwargs):
        form = self.get_formset(request.POST)
        if form.is_valid():
            form.save()
            return redirect("detail_course", pk=self.course.pk)

        return self.render_to_response({
            "form": form
        })


class DeleteComment(CourseGenericMixin):
    template_name = 'comment/manage/delete_comment.html'
    course = None
    comment = None

    def dispatch(self, request, *args, **kwargs):
        course_id = kwargs.get("course_id")
        comment_id = kwargs.get("comment_id")
        self.course = get_object_or_404(Course, id=course_id)
        self.comment = get_object_or_404(Comment, course=self.course, id=comment_id)
        return super().dispatch(request, kwargs)

    def get(self, request, *args, **kwargs):
        return self.render_to_response({
            "comment": self.comment
        })

    def post(self, request, *args, **kwargs):
        id = kwargs.get("comment_id")
        comment_to_delete = self.comment

        if comment_to_delete:
            comment_to_delete.delete()
            return redirect("detail_course", pk=self.course.pk)
        return self.render_to_response({
            "deleted": True
        })

