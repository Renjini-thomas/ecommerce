from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from .forms import ProductForm
from .models import Products, Cart,CartItem


def home(request):
    product = Products.objects.all()
    return render(request, "home.html",{'product':product})
def crud(request):
    product = Products.objects.all()
    return render(request, "crud_page.html",{'product':product})
# def cart(request):
#     return render(request, "cart_detail.html")
def payments(request):
    return render(request,"payments.html")
# def products(request):
#     product = Products.objects.all()
#     return render(request,"products.html",{'product': product})
def products(request):
    """Display all products on the products page."""
    product_list = Products.objects.all()
    context = {
        'product': product_list
    }
    return render(request, 'products.html', context)

def view_details(request, id):
    # Retrieve the product using the default 'id' field
    product = get_object_or_404(Products, id=id)
    context = {'product': product}
    return render(request, 'view_details.html', context)
def add_p(request):
    if request.method == 'POST':
        pf = ProductForm(request.POST,request.FILES)
        if pf.is_valid():
            pf.save()
            messages.success(request,"successfully added a product")
    pf = ProductForm()
    return render(request,'add_p.html',{'form':pf})

def edit_p(request,product_id):
    product = get_object_or_404(Products,id=product_id)
    if request.method == 'POST':
        pf = ProductForm(request.POST,request.FILES,instance=product)
        if pf.is_valid():
            pf.save()
            return redirect('home')
    pf = ProductForm(instance=product)
    return render(request,'edit_p.html',{'form':pf})

def delete_p(request,id):
    product = Products.objects.get(id=id)
    product.delete()
    return redirect('crud')

def signin(request):
    if request.method == 'POST':
        uname = request.POST['username']
        password1 = request.POST['password1']
        user = authenticate(username=uname,password=password1)
        if user is not None:
            login(request,user)
            fname = user.first_name
            lname = user.last_name
            return render(request, 'user_dashboard.html',{'fname':fname,'lname':lname})
        else:
            messages.error(request,'invalid credentials')
            return redirect('signin')
    return render(request,'signin.html')

def signup(request):
    if request.method == 'POST':
        uname = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password2 = request.POST['password2']

        myuser = User.objects.create_user(username=uname,email=email,password=password2)
        myuser.first_name=fname
        myuser.last_name = lname
        myuser.save()
        return redirect('signin')
    return render(request,'signup.html')


def _cart_id(request):
    """Generate a unique cart ID for each session."""
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_to_cart(request, product_id):
    """Add a product to the cart."""
    product = get_object_or_404(Products, id=product_id)
    cart_id = _cart_id(request)
    cart, created = Cart.objects.get_or_create(cart_id=cart_id)

    cart_item, created = CartItem.objects.get_or_create(product=product, cart=cart)
    if created:  # If this is a new cart item
        cart_item.quantity = 1
    else:
        cart_item.quantity += 1  # Increment quantity for existing items
    cart_item.save()
    return redirect('cart_detail')



def remove_from_cart(request, product_id):
    """Remove a product from the cart."""
    cart_id = _cart_id(request)
    cart = get_object_or_404(Cart, cart_id=cart_id)
    product = get_object_or_404(Products, id=product_id)
    cart_item = CartItem.objects.filter(product=product, cart=cart).first()
    if cart_item:
        cart_item.delete()
    return redirect('cart_detail')


def update_cart(request, product_id):
    """Update the quantity of a product in the cart."""
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart_id = _cart_id(request)
        cart = get_object_or_404(Cart, cart_id=cart_id)
        product = get_object_or_404(Products, id=product_id)
        cart_item, created = CartItem.objects.get_or_create(product=product, cart=cart)
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()
    return redirect('cart_detail')


def cart_detail(request):
    """Display the cart and its items."""
    cart_id = _cart_id(request)
    cart = get_object_or_404(Cart, cart_id=cart_id)
    cart_items = CartItem.objects.filter(cart=cart, active=True)
    total = sum(item.sub_total() for item in cart_items)
    return render(request, 'cart_detail.html', {'cart_items': cart_items, 'total': total})