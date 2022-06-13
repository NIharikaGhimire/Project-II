from itertools import product
from traceback import print_tb
from django.shortcuts import redirect, render

from carts.views import _cart_id
from orders.models import Order


from .forms import RegistrationForm
from .models import Account
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
# from carts.views import _cart_id
from carts.models import Cart, CartItem
# import requests



# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]

            user = Account.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username, password=password)
            user.phone_number = phone_number
            user.save()
         
            messages.success(request,'Registration successful')
            return redirect(login)

    else:
        form = RegistrationForm()
    context={
        'form': form,
    }
    return render(request, 'accounts/register.html',context)

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
       
        user = auth.authenticate(email=email,password=password)
        
    
        print("Authenticated user", user)
        
        if user is not None:
            print(user is not None)
            try:
                # filter 
                cart = CartItem.objects.get(cart_id = _cart_id(request))
                print("Getting cart ",cart)

                print(cart)

                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                print(is_cart_item_exists,"IS cart existe")
                
                
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)
                   
                    for item in cart_item:
                        item.user = user
                        item.save()
            except:
              
                pass
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')

          

    return render(request, 'accounts/login.html')

@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request,'You are logged out!')
    return redirect('login')

@login_required(login_url = 'login')
def dashboard(request):
    orders = Order.objects.order_by('created_at').filter(user_id=request.user.id, is_ordered=True)
    orders_count = orders.count()
    context ={
        'orders_count': orders_count,
        }

    return render(request, 'accounts/dashboard.html', context)
