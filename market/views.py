from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, Order, OrderItem
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate

def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, 'market/home.html', {
        'products': products,
        'categories': categories,
    })

def products_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    categories = Category.objects.all()
    return render(request, 'market/home.html', {
        'products': products,
        'categories': categories,
        'selected_category': category.name,
    })

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'market/product_detail.html', {
        'product': product
    })

def add_to_cart(request, product_id):
    cart = request.session.get('cart', [])
    if product_id not in cart:
        cart.append(product_id)
    request.session['cart'] = cart
    return redirect('home')  # ← Savatga qo‘shgandan keyin home sahifaga qaytaradi


def view_cart(request):
    cart = request.session.get('cart', [])
    products = Product.objects.filter(id__in=cart)
    return render(request, 'market/cart.html', {
        'products': products
    })

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', [])
    if product_id in cart:
        cart.remove(product_id)
        request.session['cart'] = cart
    return redirect('view_cart')

def checkout(request):
    cart = request.session.get('cart', [])
    products = Product.objects.filter(id__in=cart)

    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        order = Order.objects.create(customer_name=name, phone=phone)

        for product in products:
            OrderItem.objects.create(order=order, product=product)

        request.session['cart'] = []  # savatni tozalaymiz
        return redirect('home')

    return render(request, 'market/checkout.html', {'products': products})

#Ro'yhattan o'tish
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'market/signup.html', {'form': form})

# Kirish
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'market/login.html', {'form': form})

# Chiqish
def logout_view(request):
    logout(request)
    return redirect('home')
