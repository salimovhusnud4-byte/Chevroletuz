from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Car, HighlightCar


def index(request):
    cars = Car.objects.filter(is_active=True)
    highlights = HighlightCar.objects.filter(is_active=True).select_related('car')
    return render(request, 'main/index.html', {
        'cars': cars,
        'highlights': highlights,
    })


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('main:admin_panel')
            return redirect('main:index')
        else:
            messages.error(request, "Foydalanuvchi nomi yoki parol noto'g'ri!")
    return render(request, 'main/login.html')


def user_logout(request):
    logout(request)
    return redirect('main:index')


def register(request):
    return render(request, 'main/register.html')


def is_admin(user):
    return user.is_authenticated and user.is_staff


@user_passes_test(is_admin, login_url='main:login')
def admin_panel(request):
    cars = Car.objects.all()
    highlights = HighlightCar.objects.all().select_related('car')
    discount_count = cars.filter(has_discount=True).count()
    return render(request, 'main/admin_panel.html', {
        'cars': cars,
        'highlights': highlights,
        'discount_count': discount_count,
    })


@user_passes_test(is_admin, login_url='main:login')
def car_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        image_url = request.POST.get('image_url')
        price = request.POST.get('price')
        discount_text = request.POST.get('discount_text', '')
        has_discount = request.POST.get('has_discount') == 'on'
        engine = request.POST.get('engine', '')
        power = request.POST.get('power', '')
        transmission = request.POST.get('transmission', '')
        description = request.POST.get('description', '')

        Car.objects.create(
            name=name,
            image_url=image_url,
            price=price,
            discount_text=discount_text,
            has_discount=has_discount,
            engine=engine,
            power=power,
            transmission=transmission,
            description=description,
        )
        messages.success(request, f"'{name}' muvaffaqiyatli qo'shildi!")
        return redirect('main:admin_panel')
    return render(request, 'main/car_form.html', {'action': 'add'})


@user_passes_test(is_admin, login_url='main:login')
def car_edit(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    if request.method == 'POST':
        car.name = request.POST.get('name')
        car.image_url = request.POST.get('image_url')
        car.price = request.POST.get('price')
        car.discount_text = request.POST.get('discount_text', '')
        car.has_discount = request.POST.get('has_discount') == 'on'
        car.engine = request.POST.get('engine', '')
        car.power = request.POST.get('power', '')
        car.transmission = request.POST.get('transmission', '')
        car.description = request.POST.get('description', '')
        car.is_active = request.POST.get('is_active') == 'on'
        car.save()
        messages.success(request, f"'{car.name}' muvaffaqiyatli yangilandi!")
        return redirect('main:admin_panel')
    return render(request, 'main/car_form.html', {'action': 'edit', 'car': car})


@user_passes_test(is_admin, login_url='main:login')
def car_delete(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    if request.method == 'POST':
        name = car.name
        car.delete()
        messages.success(request, f"'{name}' o'chirildi!")
    return redirect('main:admin_panel')


@user_passes_test(is_admin, login_url='main:login')
def car_toggle_discount(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    car.has_discount = not car.has_discount
    car.save()
    status = "chegirmaga qo'shildi" if car.has_discount else "chegirmadan olib tashlandi"
    messages.success(request, f"'{car.name}' {status}!")
    return redirect('main:admin_panel')


@user_passes_test(is_admin, login_url='main:login')
def highlight_add(request):
    cars = Car.objects.filter(is_active=True)
    if request.method == 'POST':
        car_id = request.POST.get('car')
        tab_title = request.POST.get('tab_title')
        description = request.POST.get('description')
        order = request.POST.get('order', 0)
        car = get_object_or_404(Car, id=car_id)
        HighlightCar.objects.create(
            car=car,
            tab_title=tab_title,
            description=description,
            order=order,
        )
        messages.success(request, f"Yangilik bo'limi qo'shildi!")
        return redirect('main:admin_panel')
    return render(request, 'main/highlight_form.html', {'cars': cars, 'action': 'add'})


@user_passes_test(is_admin, login_url='main:login')
def highlight_edit(request, highlight_id):
    highlight = get_object_or_404(HighlightCar, id=highlight_id)
    cars = Car.objects.filter(is_active=True)
    if request.method == 'POST':
        car_id = request.POST.get('car')
        highlight.car = get_object_or_404(Car, id=car_id)
        highlight.tab_title = request.POST.get('tab_title')
        highlight.description = request.POST.get('description')
        highlight.order = request.POST.get('order', 0)
        highlight.is_active = request.POST.get('is_active') == 'on'
        highlight.save()
        messages.success(request, "Yangilik bo'limi yangilandi!")
        return redirect('main:admin_panel')
    return render(request, 'main/highlight_form.html', {
        'highlight': highlight,
        'cars': cars,
        'action': 'edit',
    })


@user_passes_test(is_admin, login_url='main:login')
def highlight_delete(request, highlight_id):
    highlight = get_object_or_404(HighlightCar, id=highlight_id)
    if request.method == 'POST':
        highlight.delete()
        messages.success(request, "Yangilik bo'limi o'chirildi!")
    return redirect('main:admin_panel')
