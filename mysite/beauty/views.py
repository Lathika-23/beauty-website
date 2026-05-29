from django.shortcuts import render, redirect, get_object_or_404
from decimal import Decimal
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User

from .forms import CustomUserCreationForm
from .models import Product, Category, ShippingAddress
from .cart import Cart
from .forms import ShippingForm

import ssl
import random

ssl._create_default_https_context = ssl._create_unverified_context


# Home Page
def index(request):
    return render(request, 'index.html')


def about(request):
    return render(request, 'about.html')


def cart(request):
    return render(request, 'cart.html')


# Product Page
def product(request):
    products = Product.objects.all()
    return render(request, 'product.html', {'products': products})


# Product Details
def productdetails(request, pk):
    product = get_object_or_404(Product, id=pk)
    return render(request, 'productdetails.html', {'product': product})


# Home View
def home_view(request):
    return render(request, 'home.html')


# Register
def register_view(request):

    if request.method == 'POST':

        form = CustomUserCreationForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(request, 'Account created successfully!')

            return redirect('login')

    else:

        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})


# Logout
def logout_view(request):

    logout(request)

    messages.info(request, 'Logged out successfully.')

    return redirect('login')


# Category
def category(request, foo):

    foo = foo.replace('-', ' ').strip()

    try:

        category = Category.objects.get(name__iexact=foo)

        products = Product.objects.filter(category=category)

        return render(request, 'category.html', {
            'products': products,
            'category': category
        })

    except Category.DoesNotExist:

        messages.success(request, "The category doesn't exist.")

        return redirect('index')


# Search
def search(request):

    if request.method == "POST":

        searched = request.POST.get('searched', '').strip()

        if searched == "":

            messages.warning(request, "Please enter a product name.")

            return render(request, "search.html", {})

        products = Product.objects.filter(
            Q(name__icontains=searched) |
            Q(description__icontains=searched)
        )

        if not products:

            messages.error(request, "No matching products found.")

            return render(request, "search.html", {})

        return render(request, "search.html", {
            'searched': products
        })

    return render(request, "search.html", {})


# Cart Summary
def cart_summary(request):

    cart = Cart(request)

    cart_products = cart.get_prods()

    quantities = cart.get_quants()

    product_data = []

    totals = 0

    for product in cart_products:

        quantity = quantities[str(product.id)]

        # PRICE
        if product.is_sale:
            price = product.sale_price
        else:
            price = product.price

        # PRODUCT TOTAL
        item_total = price * quantity

        # ADD TO GRAND TOTAL
        totals += item_total

        # STORE DATA
        product_data.append({
            'product': product,
            'quantity': quantity,
            'total': item_total,
        })

    context = {
        'product_data': product_data,
        'totals': totals,
    }

    return render(request, 'cart_summary.html', context)

# Add To Cart
def cart_add(request):

    cart = Cart(request)

    if request.POST.get('action') == 'post':

        product_id = int(request.POST.get('product_id'))

        product_qty = request.POST.get('product_qty')

        if product_qty == '':

            product_qty = 1

        product_qty = int(product_qty)

        product = get_object_or_404(Product, id=product_id)

        cart.add(product=product, quantity=product_qty)

        cart_quantity = cart.__len__()

        response = JsonResponse({'qty': cart_quantity})

        messages.success(request, "Product Added To Cart")

        return response


# Update Cart
def cart_update(request):

    if request.POST.get('action') == 'post':

        product_id = str(request.POST.get('product_id'))

        product_qty = int(request.POST.get('product_qty'))

        cart = request.session.get('session_key', {})

        cart[product_id] = product_qty

        request.session['session_key'] = cart

        request.session.modified = True

        return JsonResponse({
            'qty': product_qty
        })


# Delete Cart Item
def cart_delete(request):

    cart = Cart(request)

    if request.POST.get('action') == 'post':

        product_id = int(request.POST.get('product_id'))

        cart.delete(product=product_id)

        response = JsonResponse({
            'product': product_id
        })

        return response


# Login With OTP
def login_user(request):

    if request.method == "POST":

        username = request.POST.get('username')

        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

          otp = random.randint(100000, 999999)

          request.session['otp'] = str(otp)
          request.session['username'] = username
          request.session['user_id'] = user.id
          send_mail(
            subject='Your OTP Code',
            message=f'Your OTP is: {otp}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
          )

          return redirect('verify_otp')

        else:

            messages.error(request, "Invalid credentials.")

            return redirect('login')

    return render(request, 'login.html')


# Verify OTP
def verify_otp(request):

    if request.method == "POST":

        otp_entered = request.POST.get("otp")

        if otp_entered == request.session.get('otp'):

            user_id = request.session.get('user_id')
            user = User.objects.get(id=user_id)

            login(request, user)   # ✅ LOGIN HERE

            return redirect('home')

        else:
            messages.error(request, "Invalid OTP")

    return render(request, "otp_verify.html")


# Delight Page
def delight(request):
    return render(request, 'delight.html')


# Update Shipping Info
def update_info(request):

    shipping_user, created = ShippingAddress.objects.get_or_create(
        user=request.user
    )

    shipping_form = ShippingForm(
        request.POST or None,
        instance=shipping_user
    )

    if request.method == "POST":

        if shipping_form.is_valid():

            shipping_form.save()

            messages.success(request, "Shipping Info Updated")

            return redirect('checkout')

    return render(request, "update_info.html", {
        'shipping_form': shipping_form
    })


# Checkout
# Checkout
def checkout(request):

    cart = Cart(request)

    # GET PRODUCTS
    cart_products = cart.get_prods()

    # GET QUANTITIES
    quantities = cart.get_quants()

    # CALCULATE TOTALS
    totals = 0

    for product in cart_products:

        quantity = quantities[str(product.id)]

        if product.is_sale:
            price = product.sale_price
        else:
            price = product.price

        totals += price * quantity

    # LOGGED IN USER
    if request.user.is_authenticated:

        shipping_user, created = ShippingAddress.objects.get_or_create(
            user=request.user
        )

        shipping_form = ShippingForm(
            request.POST or None,
            instance=shipping_user
        )

    # GUEST USER
    else:

        shipping_form = ShippingForm(request.POST or None)

    context = {
        "cart_products": cart_products,
        "quantities": quantities,
        "totals": totals,
        "shipping_form": shipping_form
    }

    return render(request, "checkout.html", context)
# Order Page
def order(request):
    return render(request, 'order.html')