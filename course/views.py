from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import TemplateResponseMixin, View
from django.views import generic
from django.views.generic import ListView
from django.db.models import Q
from django.utils.text import slugify
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Course


class CourseGenericMixin(View):
    model = Course


class SearchCourse(TemplateResponseMixin, CourseGenericMixin):
    template_name = 'search/search.html'
    courses = None

    def get(self, request, *args, **kwargs):

        self.courses = Course.objects.all()

        return self.render_to_response({
            "courses": self.courses
        })


class CourseSearchList(TemplateResponseMixin, View):
    template_name = "search/course_search_list.html"
    results = None

    def dispatch(self, request, *args, **kwargs):

        query = request.GET.get('search')
        if query == '':
            query = None

        self.results = Course.objects.filter(
            Q(course_title__icontains=query) | Q(course_author__username__icontains=query)
            | Q(category__name__icontains=query)
        )

        return self.render_to_response({
            "query": query,
            "results": self.results
        })
