from django.http import HttpResponse
from django.shortcuts import render
from .models import Books

def home_view(request, *args, **kwargs):
   return HttpResponse("<h1>Hello World!</h1>")


def book_detail_view(request, book_id, *args, **kwargs):
   obj = Books.objects.get(id=book_id)
   return HttpResponse(f"Kitap Ad1: {obj.name} Yazar1: {obj.author}")
