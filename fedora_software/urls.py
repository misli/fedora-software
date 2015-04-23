from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns

from .views import HomeView, AppView, SearchView, CategoryView, FaqView

#from django.contrib import admin
#admin.autodiscover()

urlpatterns = i18n_patterns('',
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^apps/.*$', AppView.as_view(), name='app'),
    url(r'^search/.*$', SearchView.as_view(), name='search'),
    url(r'^category/.*$', CategoryView.as_view(), name='category'),
    url(r'^faq$', FaqView.as_view(), name='faq'),
)
