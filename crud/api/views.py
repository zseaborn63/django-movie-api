from django.forms import modelform_factory
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from movie.models import Movie
import json

# Create your views here.

@csrf_exempt
def api_movie_list_create(request):
    if request.POST:
        title = request.POST.get('title')
        Movie.objects.create(title=title)
        return HttpResponse(json.dumps({"message": "Success!"}), content_type='application/json')
    if request.method == 'PUT':
        # create an object and redirect to detail page
        modelform = modelform_factory(Movie)
        form = modelform(request.PUT)
        if form.is_valid():
            form.save()
        return redirect('restview')
    all_movies = Movie.objects.all()
    data = [{'id': movie.id, 'title': movie.title} for movie in all_movies]
    data = json.dumps(data)
    return HttpResponse(data, content_type="application/json")

@csrf_exempt
def api_movie_detail(request, pk):
    if request.method == 'DELETE':
        # delete an object and send a confirmation response
        Movie.objects.get(id=pk).delete()
        return HttpResponse(json.dumps({"message": "Success!"}), content_type='application/json')
    if request.method == 'PUT':
        # create an object and redirect to detail page
        modelform = modelform_factory(Movie)
        form = modelform(request.PUT)
        if form.is_valid():
            form.save()
        return redirect('restview')
    movie = Movie.objects.get(id=pk)
    serialized_tweet = json.dumps({'id': movie.id, 'title': movie.title})
    return HttpResponse(serialized_tweet, content_type='application/json')