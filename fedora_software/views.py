from django.shortcuts import render
from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = 'home.html'

class AppView(TemplateView):
    template_name = 'app.html'

class SearchView(TemplateView):
    template_name = 'search.html'

class CategoryView(TemplateView):
    template_name = 'category.html'

class FaqView(TemplateView):
    template_name = 'faq.html'
