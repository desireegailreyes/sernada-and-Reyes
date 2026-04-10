from django.shortcuts import render, redirect
from .models import Product, Cart, CartItem
from django.contrib.auth.decorators import login_required

def home(request):
    products = Product.objects.all()
    return render(request, 'pharmacy/home.html', {'products': products})


@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        item.quantity += 1
    item.save()

    return redirect('cart')


@login_required
def cart(request):
    cart = Cart.objects.get(user=request.user)
    items = CartItem.objects.filter(cart=cart)

    total = sum(item.product.price * item.quantity for item in items)

    return render(request, 'pharmacy/cart.html', {'items': items, 'total': total})


@login_required
def checkout(request):
    cart = Cart.objects.get(user=request.user)
    items = CartItem.objects.filter(cart=cart)

    if request.method == "POST":
        items.delete()
        return redirect('home')

    return render(request, 'pharmacy/checkout.html', {'items': items})