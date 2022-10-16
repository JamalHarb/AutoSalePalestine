from multiprocessing import context
import re
from django.http import JsonResponse
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from . import models
from django.core import serializers
import json

# Create your views here.


def comment(request, id):
    c_id = request.POST['c_id']
    models.Reply.objects.create(
        reply=request.POST['comment'], request_id=id, user_id=request.session['user_id'])
    context = {
        'lastCars': models.Car.objects.all().order_by('-id')[:5],
    }
    return redirect('/car/'+c_id+'/posts')


def post(request, id):
    models.Request.objects.create(
        request=request.POST['post'], user_id=request.session['user_id'], car_id=id)
    context = {
        'lastCars': models.Car.objects.all().order_by('-id')[:5],
    }
    return redirect('/my_request', id)


def deleteRequest(request, id):
    m = models.Request.objects.get(id=id)
    m.delete()
    return redirect('/my_request')


def deleteComment(request, id):
    c_id = request.POST['c_id']
    c = models.Reply.objects.get(id=id)
    c.delete()
    return redirect('/car/'+c_id+'/posts')


def car_posts(request, id):
    context = {
        'lastCars': models.Car.objects.all().order_by('-id')[:5],
        'car': models.Car.objects.get(id=id),
        'posts': models.Request.objects.filter(car_id=id, user_id=request.session['user_id']),
        'post1': models.Request.objects.filter(car_id=id),
        'comm': models.Reply.objects.all(),
    }
    return render(request, 'posts.html', context)


def request(request, id):
    context = {
        'lastCars': models.Car.objects.all().order_by('-id')[:5],
        'car': models.Car.objects.get(id=id),
    }
    return render(request, 'requestcar.html', context)


def my_request(request):
    print(request.session['user_id'], '*/'*20)
    context = {
        'car': models.Car.objects.all(),
        'myreq': models.Request.objects.filter(user=request.session['user_id']),
        'lastCars': models.Car.objects.all().order_by('-id')[:5],
    }
    return render(request, 'myrequest.html', context)


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
        return redirect('/log/reg')
    models.register(request)
    return redirect('/dashboard')


def check_login(request):
    log_errors = models.login_errors(request)
    if log_errors:
        for value in log_errors.values():
            messages.error(request, value)
        return redirect('/log/reg')
    models.login(request)
    return redirect('/dashboard')


def logout(request):
    request.session.clear()
    return redirect('/dashboard')


def dashboard(request):
<<<<<<< HEAD
    try:
        print(models.get_searched_cars(request))
        context = {
            'cities': models.get_all_cities(),
            'manufacturers': models.get_all_manufacturers(),
            'models': models.get_all_models(),
            'sources': models.get_all_sources(),
            'min_year': models.year_limits()[0],
            'max_year': models.year_limits()[1],
            'lastCars': models.Car.objects.all().order_by('-id')[:5],
            'colors': models.Colors.objects.all(),
        }
    except:
        if 'user_id' in request.session:
            print('except')
            context = {
                'cities': models.get_all_cities(),
                'manufacturers': models.get_all_manufacturers(),
                'models': models.get_all_models(),
                'sources': models.get_all_sources(),
                'min_year': models.year_limits()[0],
                'max_year': models.year_limits()[1],
                'lastCars': models.Car.objects.all().order_by('-id')[:5],
                'colors': models.Colors.objects.all(),
            }
        else:
            context = {
                'cities': models.get_all_cities(),
                'manufacturers': models.get_all_manufacturers(),
                'models': models.get_all_models(),
                'sources': models.get_all_sources(),
                'min_year': models.year_limits()[0],
                'max_year': models.year_limits()[1],
                'lastCars': models.Car.objects.all().order_by('-id')[:5],
                'colors': models.Colors.objects.all(),
            }
=======
    # print(models.get_searched_cars(request))
    context = {
        'cities': models.get_all_cities(),
        'manufacturers': models.get_all_manufacturers(),
        'models': models.get_all_models(),
        'sources': models.get_all_sources(),
        'min_year': models.year_limits()[0],
        'max_year': models.year_limits()[1],
    }
    # print('context read')
>>>>>>> 8ae64b5dc29444a820c90b4f6800b45c3f4c5fbc
    # if 'search_result' in request.session:
    #     print('context read')
    #     context['search_cars'] = request.session['search_cars']
    #     context['search_models'] = request.session['search_models']
    return render(request, 'dashboard.html', context)


""" """ """ """ """ """ """ """ """  """ """ """ """ """ """ """ """ """


def addCity(request):
    city1 = models.City.objects.all()
    print(request.POST['city'])
    for city in city1:
        if request.POST['city'] == '' or request.POST['city'] == city.name:
            return redirect('/123')
    city = models.City.objects.create(name=request.POST['city'])
    city.save()
    return redirect('/123')


def addManufacturer(request):
    manufacturer1 = models.Manufacturer.objects.all()
    print(request.POST['Manufacturer'])
    for manufacturer in manufacturer1:
        if request.POST['Manufacturer'] == '' or request.POST['Manufacturer'] == manufacturer.manufacturer:
            return redirect('/123')
    m = models.Manufacturer.objects.create(
        manufacturer=request.POST['Manufacturer'])
    m.save()
    return redirect('/123')


def addPowerSource(request):
    Ps = models.PowerSource.objects.all()
    print(request.POST['PowerSource'])
    for source in Ps:
        if request.POST['PowerSource'] == '' or request.POST['PowerSource'] == source.source:
            return redirect('/123')
    m = models.PowerSource.objects.create(source=request.POST['PowerSource'])
    m.save()
    return redirect('/123')


def addModel(request):
    mo = models.CarModel.objects.all()
    print(request.POST['Model'])
    for model in mo:
        if request.POST['Model'] == '' or request.POST['Model'] == model.model:
            return redirect('/123')
    m = models.CarModel.objects.create(
        manufacturer_id=request.POST['Manufacturer'], model=request.POST['Model'])
    m.save()
    return redirect('/123')


def addColor(request):
    color1 = models.Colors.objects.all()
    print(request.POST['color'])
    for color in color1:
        if request.POST['color'] == '' or request.POST['color'] == color.color_name:
            return redirect('/123')
    color = models.Colors.objects.create(color_name=request.POST['color'])
    color.save()
    return redirect('/123')


def deleteCity(request, id):
    city = models.City.objects.get(id=id)
    city.delete()
    return redirect('/123')


def deleteColor(request, id):
    color = models.Colors.objects.get(id=id)
    color.delete()
    return JsonResponse({'success': True, 'message': 'Delete', 'id': id})


def deleteManufacturer(request, id):
    m = models.Manufacturer.objects.get(id=id)
    m.delete()
    return redirect('/123')


def deleteModel(request, id):
    m = models.CarModel.objects.get(id=id)
    m.delete()
    return JsonResponse({'success': True, 'message': 'Delete', 'id': id})


def deletePowerSource(request, id):
    s = models.PowerSource.objects.get(id=id)
    s.delete()
    return redirect('/123')


""" """ """ """ """ """ """ """ """ """ """  """ """ """ """ """ """ """ """ """ """ """


def admin(request):
    context = {
        'cities': models.City.objects.all(),
        'color': models.Colors.objects.all(),
        'Manufacturer': models.Manufacturer.objects.all(),
        'model': models.CarModel.objects.all(),
        'Ps': models.PowerSource.objects.all(),
        'users': models.User.objects.all(),
    }
    return render(request, 'admin.html', context)


""" """ """ """ """ """ """ """ """  """ """ """ """ """ """ """ """ """


def my_cars(request):
    user = models.get_logged_user(request)
    context = {
        'cars': user.advertised_cars.all(),
        'lastCars': models.Car.objects.all().order_by('-id')[:5],
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
        'colors': models.Colors.objects.all(),
        'lastCars': models.Car.objects.all().order_by('-id')[:5],

    }
    return render(request, 'add_car.html', context)


def create_car(request):
    models.create_car(request)
    return redirect('/my_cars')


def view_car(request, id):
    context = {
        'car': models.get_car(id),
        'lastCars': models.Car.objects.all().order_by('-id')[:5],
        'users': models.User.objects.all(),
        'cars': models.Car.objects.all(),
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
        'colors': models.Colors.objects.all(),
        'lastCars': models.Car.objects.all().order_by('-id')[:5],

    }
    return render(request, 'edit_car.html', context)

def search_car(request):
    print('+'*80)
    print('searching cars')
    cars_qs = models.get_searched_cars(request)
    print('resulting query set:')
    print(cars_qs)
    print('+'*80)
    cars = []
    for car in cars_qs:
        item = [car.id, car.model.model, car.model.manufacturer.manufacturer, car.advertiser.first_name, car.year, car.price, car.color]
        cars.append(item)
    request.session['cars'] = cars
    request.session['search_performed'] = True
    return redirect('/dashboard')

def update_car(request, id):
    car_errors = models.car_errors_without_image(request)
    if car_errors:
        for value in car_errors.values():
            messages.error(request, value)
        return redirect(f'/car/{id}/edit')
    models.update_car(request, id)
    return redirect(f'/car/{id}/view')


def goback(request, id):
    return redirect(f'/car/{id}/view')


def delete_car(request, id):
    car = models.get_car(id)
    car.delete()
    return JsonResponse({'success': True, 'message': 'Delete', 'id': id})

<<<<<<< HEAD

def about_us(request):
    context = {
        'lastCars': models.Car.objects.all().order_by('-id')[:5],
    }
    return render(request, 'about_us.html', context)


def contact_us(request):
    context = {
        'lastCars': models.Car.objects.all().order_by('-id')[:5],
    }
    return render(request, 'contact_us.html', context)
=======
def search_car(request):
    # request.session['search_result'] = serializers.serialize("json", models.get_searched_cars(request))
    request.session['search_result'] = list(models.get_searched_cars(request).values('id', 'model'))
    print('session')
    print(request.session['search_result'])
    car_id_list = []
    model_id_list = []
    for dict in request.session['search_result']:
        car_id_list.append(dict['id'])
        model_id_list.append(dict['model'])
    cars = []
    _models = []
    for id in car_id_list:
        cars.append(models.get_car(id))
    for model_id in model_id_list:
        _models.append(models.get_car_model_by_id(model_id))
    request.session['search_cars'] = serializers.serialize("json", cars)
    request.session['search_models'] = serializers.serialize("json", _models)
    print('second session')
    print(request.session['search_models'])
    print('cars and models lists')
    print(cars, _models)
    return redirect('/dashboard')
>>>>>>> 8ae64b5dc29444a820c90b4f6800b45c3f4c5fbc
