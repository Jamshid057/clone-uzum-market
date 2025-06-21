from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, Order, OrderItem
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Yoki mavjudini top, yoki yarat
    order = Order.objects.filter(user=request.user, is_ordered=False).first()
    if not order:
        order = Order.objects.create(
            user=request.user,
            full_name="Temporary",
            address="",
            phone="",
            total_price=0,
            is_ordered=False
        )

    # Mahsulotni savatga qo‘shish
    order_item, created = OrderItem.objects.get_or_create(
        order=order,
        product=product,
        defaults={'quantity': 1, 'price': product.price}
    )
    if not created:
        order_item.quantity += 1
        order_item.save()

    return redirect('home')

@login_required
def cart(request):
    order = Order.objects.filter(user=request.user, is_ordered=False).first()
    return render(request, 'market/cart.html', {'order': order})

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

@login_required
def checkout(request):
    # Savatni session orqali olamiz (masalan, savat dict holatida saqlanadi)
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())
    total = sum(product.price * cart[str(product.id)] for product in products)

    if request.method == 'POST':
        full_name = request.POST['full_name']
        address = request.POST['address']
        phone = request.POST['phone']

        # Order yaratamiz
        order = Order.objects.create(
            user=request.user,
            full_name=full_name,
            address=address,
            phone=phone,
            total_price=total
        )

        # Har bir item uchun OrderItem
        for product in products:
            quantity = cart[str(product.id)]
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price
            )

        # Savatni tozalaymiz
        request.session['cart'] = {}
        messages.success(request, "Buyurtmangiz muvaffaqiyatli yakunlandi!")
        return redirect('home')

    return render(request, 'market/checkout.html', {
        'cart_items': [(product, cart[str(product.id)]) for product in products],
        'total': total
    })
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
