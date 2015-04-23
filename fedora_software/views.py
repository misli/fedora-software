from django.shortcuts import render
from django.views.generic import TemplateView

from .models import FeaturedApp

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self):
        return {
            'featured_app': FeaturedApp.objects.order_by('?').first(),
        }

class AppView(TemplateView):
    template_name = 'app.html'

class SearchView(TemplateView):
    template_name = 'search.html'

class CategoryView(TemplateView):
    template_name = 'category.html'

class FaqView(TemplateView):
    template_name = 'faq.html'
