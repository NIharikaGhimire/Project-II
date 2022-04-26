from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.http import HttpResponse
from carts.models import CartItem
from orders.models import Order
from.forms import OrderForm

# Create your views here.
def place_order(request, total = 0, quantity =0):
    current_user = request.user

    # if the cart count is less than or equal to 0 then redirect back to shop
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <=0:
        return redirect('store')

    grand_total = 0
    tax = 0
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (2 * total)/100
    grand_total = total + tax


    if request.method == 'POST':
        form = OrderForm(request.POST)

        if form.is_valid():
            # store all the billing info inside order table
            data = Order()
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address = form.cleaned_data['address']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            # Generate order number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d")  #2022/04/26
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()
            return redirect('checkout')

        else:
            return redirect('checkout')


