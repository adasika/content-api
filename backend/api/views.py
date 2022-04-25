from django.shortcuts import render
from django.views import generic
from .models import News 
from .tasks import get_google_news



class HomePageView(generic.ListView):
    get_google_news.delay()
    template_name = 'api/home.html'
    context_object_name = 'articles' 

    def get_queryset(self):
       print(News.objects.all())
       return News.objects.all()

