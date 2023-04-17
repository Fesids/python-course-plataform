from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .models import CustomUserModel
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.views.generic.base import TemplateResponseMixin, View
# Create your views here.


class Home(TemplateView):
    template_name = "home.html"


class SignUp(TemplateResponseMixin, View):
    template_name = "registration/signup.html"
    user = None
    def get_formset(self, data=None):
        return CustomUserCreationForm(data=data)

    def get(self, request, format=None):
        form = self.get_formset()
        return self.render_to_response({
            "form": form
        })

    def post(self, request, format=None):
        user = request.POST
        form = self.get_formset(user)

        if form.is_valid():
            form.save()
            return redirect("login")
        return self.render_to_response({
            "form": form
        })