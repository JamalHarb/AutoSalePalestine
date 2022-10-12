from multiprocessing import context
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from . import models
from django.core import serializers

# Create your views here.
def index(request):
    models.create_cities()
    context = {
        'cities': models.get_all_cities()
    }
    return render(request, 'login_index.html', context)

def check_register(request):
    reg_errors = models.register_errors(request)
    if reg_errors:
        for value in reg_errors.values():
            messages.error(request, value)
        return redirect('/')
    models.register(request)
    return redirect('/dashboard')

def check_login(request):
    log_errors = models.login_errors(request)
    if log_errors:
        for value in log_errors.values():
            messages.error(request, value)
        return redirect('/')
    models.login(request)
    return redirect('/dashboard')

def logout(request):
    request.session.clear()
    return redirect('/')

def dashboard(request):
    try:
        print(models.get_searched_cars(request))
        context = {
            'cities': models.get_all_cities(),
            'manufacturers': models.get_all_manufacturers(),
            'models': models.get_all_models(),
            'sources': models.get_all_sources(),
            'cars': models.get_searched_cars(request),
            'min_year': models.year_limits()[0],
            'max_year': models.year_limits()[1],
        }
    except:
        print('except')
        context = {
            'cities': models.get_all_cities(),
            'manufacturers': models.get_all_manufacturers(),
            'models': models.get_all_models(),
            'sources': models.get_all_sources(),
            'cars': [],
            'min_year': models.year_limits()[0],
            'max_year': models.year_limits()[1],
        }
    # if 'search_result' in request.session:
    #     context['cars'] = request.session['search_result']
    return render(request, 'dashboard.html', context)

def my_cars(request):
    user = models.get_logged_user(request)
    context = {
        'cars': user.advertised_cars.all()
    }
    return render(request, 'my_cars.html', context)

def add_car(request):
    context = {
        'cities': models.get_all_cities(),
        'manufacturers': models.get_all_manufacturers(),
        'models': models.get_all_models(),
        'sources': models.get_all_sources(),
        'min_year': models.year_limits()[0],
        'max_year': models.year_limits()[1],
    }
    return render(request, 'add_car.html', context)

def create_car(request):
    models.create_car(request)
    return redirect('/my_cars')

def view_car(request, id):
    context = {
        'car': models.get_car(id)
    }
    return render(request, 'view_car.html', context)

def edit_car(request, id):
    context = {
        'cities': models.get_all_cities(),
        'manufacturers': models.get_all_manufacturers(),
        'models': models.get_all_models(),
        'sources': models.get_all_sources(),
        'min_year': models.year_limits()[0],
        'max_year': models.year_limits()[1],
        'car': models.get_car(id),
    }
    return render(request, 'edit_car.html', context)

def update_car(request, id):
    models.update_car(request, id)
    return redirect(f'/car/{id}/view')

def goback(request, id):
    return redirect(f'/car/{id}/view')

def delete_car(request, id):
    car = models.get_car(id)
    car.delete()
    return redirect('/my_cars')

def search_car(request):
    request.session['search_result'] = serializers.serialize("json", models.get_searched_cars(request))
    print(request.session['search_result'])
    return redirect('/dashboard')