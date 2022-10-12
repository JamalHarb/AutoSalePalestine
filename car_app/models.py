from tkinter.tix import Tree
from django.db import models
import re
from datetime import datetime
from dateutil.relativedelta import relativedelta
import bcrypt
from django.contrib import messages
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class CityManager(models.Manager):
    def city_validator(self, postData):
        errors = {}
        if postData['city'] == 'None':
            errors['city'] = 'Choose city'
        return errors

class City(models.Model):
    name = models.CharField(max_length=10, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    objects = CityManager()

class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        if len(postData['first-name']) < 2:
            errors['first_name'] = 'First name should be at least 2 characters.'
        if len(postData['last-name']) < 2:
            errors['last_name'] = 'Last name should be at least 2 characters.'
        user_bday = datetime.strptime(postData['bday'], '%Y-%m-%d')
        if user_bday > datetime.today():
            errors['past'] = 'Birthday should be in the past!'
        if user_bday > datetime.today() - relativedelta(months=210):
            errors['age'] = 'You must be at least 17.5 years old!'
        if len(postData['bday']) < 10:
            errors['date'] = 'Enter your birthday.'
        if postData['city'] == 'None':
            errors['city'] = 'Choose city'
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = 'Invalid email address!'
        for user in User.objects.all():
            if postData['email'] == user.email:
                errors['unique_email'] = 'Email already exists!'
        if len(postData['password']) < 8:
            errors['password'] = 'Password should be at least 8 characters.'
        if postData['password'] != postData['confirm-password']:
            errors['confirm_password'] = 'Confirmed password does not match with password.'
        return errors
    
    def login_validator(self, postData):
        errors = {}
        user = User.objects.filter(email=postData['email'])
        if user:
            logged_user = user[0]
            if not bcrypt.checkpw(postData['password'].encode(), logged_user.password.encode()):
                errors['login'] = 'Invalid credentials!'
        else:
            errors['login'] = 'Invalid credentials!'
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    birthday = models.DateField()
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    city = models.ForeignKey(City, related_name='users', on_delete=models.CASCADE)

class PowerSourceManager(models.Manager):
    def power_source_validator(self, postData):
        errors = {}
        if postData['power-source'] == 'None':
            errors['power_source'] = 'Choose power source'
        return errors

class PowerSource(models.Model):
    source = models.CharField(max_length=8)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = PowerSourceManager()

class ManufacturerManager(models.Manager):
    def manufacturer_validator(self, postData):
        errors = {}
        if postData['manufacturer'] == 'None':
            errors['manufacturer'] = 'Choose manufacturer'
        return errors

class Manufacturer(models.Model):
    manufacturer = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ManufacturerManager()

class CarModelManager(models.Manager):
    def car_model_validator(self, postData):
        errors = {}
        if postData['car-model'] == 'None':
            errors['car_model'] = 'Choose car model'
        return errors

class CarModel(models.Model):
    model = models.CharField(max_length=45)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CarModelManager()
    manufacturer = models.ForeignKey(Manufacturer, related_name='car_models', on_delete=models.CASCADE)

class CarManager(models.Manager):
    def car_validator(self, postData):
        errors = {}
        if postData['color'] == 'None':
            errors['color'] = 'Choose color'
        if postData['year'] == 'None':
            errors['year'] = 'Choose year'
        elif postData['year'] < datetime.today().year-120:
            errors['year'] = 'Year cannot be earlier than 120 years ago'
        elif postData['year'] > datetime.today().year + 1:
            errors['year'] = f'Year cannot be later than {datetime.today().year + 1}'
        if postData['num-passengers'] == 'None':
            errors['num_passengers'] = 'Choose number of passengers'
        if postData['transmission'] == 'None':
            errors['transmission'] = 'Choose transmission'
        if postData['status'] == 'None':
            errors['status'] = 'Choose status'
        if len(postData['price']) < 1:
            errors['price'] = 'Specify price'
        errors['city'] = City.objects.city_validator(postData)['city']
        errors['power_source'] = PowerSource.objects.power_source_validator(postData)
        errors['car_model'] = CarModel.objects.car_model_validator(postData)
        return errors

class Car(models.Model):
    color = models.CharField(max_length=10, null=True)
    year = models.IntegerField(validators=[MinValueValidator(datetime.today().year-120), MaxValueValidator(datetime.today().year+1)])
    num_passengers = models.IntegerField(validators=[MinValueValidator(1)], null=True)
    transmission = models.CharField(max_length=9, null=True)
    status = models.CharField(max_length=4, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=8, null=True)
    bhp = models.IntegerField(null=True)
    features = models.TextField(null=True)
    photo = models.CharField(max_length=255, null=True)
    is_sold = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CarManager()
    advertiser = models.ForeignKey(User, related_name='advertised_cars', on_delete=models.CASCADE)
    city = models.ForeignKey(City, related_name='cars', on_delete=models.CASCADE)
    power_source = models.ForeignKey(PowerSource, related_name='cars', on_delete=models.CASCADE)
    model = models.ForeignKey(CarModel, related_name='cars', on_delete=models.CASCADE)

class RequestManager(models.Manager):
    def request_validator(postData):
        errors = {}
        if len(postData['request']) < 1:
            errors['request'] = 'Request cannot be empty'
        return errors

class Request(models.Model):
    request = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = RequestManager()
    user = models.ForeignKey(User, related_name='requests', on_delete=models.CASCADE)
    car = models.ForeignKey(Car, related_name='requests', on_delete=models.CASCADE)

class ReplyManager(models.Manager):
    def reply_validator(postData):
        errors = {}
        if len(postData['reply']) < 1:
            errors['reply'] = 'Reply cannot be empty'
        return errors

class Reply(models.Model):
    reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ReplyManager()
    request = models.ForeignKey(Request, related_name='replies', on_delete=models.CASCADE)

def create_cities():
    cities = ['Jenin', 'Tulkarm', 'Tubas', 'Nablus', 'Qalqilyah', 'Jericho', 'Salfit', 'Ramallah', 'Jerusalem', 'Bethlehem', 'Hebron', 'Gaza Strip']
    if City.objects.all().count() == 0:
        for city in cities:
            City.objects.create(name=city)
            if City.objects.all().count() == len(cities):
                some_city = City.objects.filter(name=city)[0]
                if some_city not in City.objects.all():
                    City.objects.create(name=city)

def get_all_cities():
    return City.objects.all()

def get_city(request):
    name = request.POST['city']
    return City.objects.get(name=name)

def all_users():
    return User.objects.all()

def register_errors(request):
    return User.objects.register_validator(request.POST)

def register(request):
    password = request.POST['password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    city_name = request.POST['city']
    city = City.objects.get(name=city_name)
    User.objects.create(
        first_name = request.POST['first-name'],
        last_name = request.POST['last-name'],
        birthday = request.POST['bday'],
        city = city,
        email = request.POST['email'],
        password = pw_hash
    )
    request.session['first_name'] = request.POST['first-name']
    request.session['email'] = request.POST['email']

def login_errors(request):
    return User.objects.login_validator(request.POST)

def login(request):
    user = User.objects.filter(email=request.POST['email'])
    logged_user = user[0]
    request.session['first_name'] = logged_user.first_name
    request.session['email'] = request.POST['email']

def get_logged_user(request):
    return User.objects.get(email=request.session['email'])

# def get_manu_model():
#     manu_model = {
#         'Mercedes Benz': ['GLA', 'CLS', 'S', 'C', 'E', 'G', 'GLS'],
#         'BMW': ['325', '525', '750iL'],
#         'VW': ['Golf', 'Passat', 'Jetta'],
#     }
#     return manu_model

def get_all_manufacturers():
    return Manufacturer.objects.all()

def get_manufacturer(request):
    return Manufacturer.objects.get(manufacturer=request.POST['manufacturer'])

def get_all_models():
    return CarModel.objects.all()

def get_car_model(request):
    return CarModel.objects.get(model=request.POST['model'], manufacturer=get_manufacturer(request))

def get_all_sources():
    return PowerSource.objects.all()

def get_power_source(requset):
    source = requset.POST['power-source']
    return PowerSource.objects.get(source=source)

def create_car(request):
    color = request.POST['color']
    year = request.POST['year']
    num_passengers = request.POST['num-passengers']
    transmission = request.POST['transmission']
    status = request.POST['status']
    price = request.POST['price']
    bhp = request.POST['bhp']
    features = request.POST['features']
    photo = request.POST['photo']
    advertiser = get_logged_user(request)
    city = get_city(request)
    power_source = get_power_source(request)
    model = get_car_model(request)
    
    Car.objects.create(
        color = color,
        year = year,
        num_passengers = num_passengers,
        transmission = transmission,
        status = status,
        price = price,
        bhp = bhp,
        features = features,
        photo = photo,
        advertiser = advertiser,
        city = city,
        power_source = power_source,
        model = model
    )

def get_car(id):
    return Car.objects.get(id=id)

def update_car(request, id):
    car = get_car(id)
    car.color = request.POST['color']
    car.year = request.POST['year']
    car.num_passengers = request.POST['num-passengers']
    car.transmission = request.POST['transmission']
    car.status = request.POST['status']
    car.price = request.POST['price']
    car.bhp = request.POST['bhp']
    car.features = request.POST['features']
    car.photo = request.POST['photo']
    car.city = get_city(request)
    car.power_source = get_power_source(request)
    car.model = get_car_model(request)
    car.save()

def get_searched_cars(request):
    user = get_logged_user(request)
    # return Car.objects.filter(color = request.POST['color']).filter(year = int(request.POST['year'])).filter(num_passengers = int(request.POST['num-passengers'])).filter(transmission = request.POST['transmission']).filter(status = request.POST['status']).filter(price = float(request.POST['price'])).filter(bhp = int(request.POST['bhp'])).filter(city = get_city(request)).filter(power_source = get_power_source(request)).filter(model = get_car_model(request))
    return Car.objects.filter(
        color = request.POST['color'],
        year = request.POST['year'],
        num_passengers = request.POST['num-passengers'],
        transmission = request.POST['transmission'],
        status = request.POST['status'],
        price = request.POST['price'],
        bhp = request.POST['bhp'],
        city = get_city(request),
        power_source = get_power_source(request),
        model = get_car_model(request)
    )

def year_limits():
    min_year = datetime.today().year-120
    max_year = datetime.today().year+1
    return [min_year, max_year]