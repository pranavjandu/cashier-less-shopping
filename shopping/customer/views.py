import json
from django.db.models.fields import DecimalField
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import *
from django.http import JsonResponse
from .utils import cartData

def mainpage(request):
    '''
    For logging users in
    '''
    if request.method == "POST":
        type = request.POST.get('type')
        if type=="login":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user=authenticate(request,username=username,password=password)  #django default authentication
            if user is not None:
                login(request,user)
                return redirect('customerhomepage')
            else: 
                messages.error(request,"Wrong Credentials! Please Try again")
        elif type=="register":
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            try:   #creating Customer object
                user=CustomUser.objects.create_user(username=username,password=password,email=email,user_type=3)
                user.customer.name=username #adding name to instructor object
                user.save()
                messages.success(request," Signup successfull ")
                return redirect('loginpage')
            except:
                messages.error(request," Error occured. Please Try again!")
                return redirect('loginpage')
    return render(request, 'login.html')   


def dashboard(request):
    if (request.user.is_authenticated)==False:
        return redirect('loginpage')

    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'cartItems':cartItems}
    return render(request, 'index.html', context)   

def logoutuser(request):
    '''
    for logging user out and redirecting to login-page
    '''
    logout(request)
    return redirect('loginpage')

def scanner(request):
    if (request.user.is_authenticated)==False:
        return redirect('loginpage')

    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'cartItems':cartItems}
    return render(request,'scanner.html', context)

def cart(request):
    if (request.user.is_authenticated)==False:
        return redirect('loginpage')

    data = cartData(request)

    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'cartItems':cartItems, 'order':order, 'items':items}
    return render(request,'cart.html', context)


def addtocart(request):
    product = request.GET.get('productid', None)
    action = request.GET.get('action')
    data = {
        'added': Product.objects.filter(id=product).exists()
    }
    if (Product.objects.filter(id=product).exists()):
        customer = request.user.customer
        product = Product.objects.get(id=product)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

        if action == 'add':
            orderItem.quantity = (orderItem.quantity + 1)
        elif action == 'remove':
            orderItem.quantity = (orderItem.quantity - 1)

        orderItem.save()
        if orderItem.quantity <= 0:
            orderItem.delete()

    return JsonResponse(data)


def checkout(request):
    if (request.user.is_authenticated)==False:
        return redirect('loginpage')
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    order.complete = True
    order.save()
    orderid = order.id
    context = {'cartItems':cartItems, 'order':order, 'items':items, 'orderid': orderid}
    return render(request, 'checkout.html', context)


def loginGuard(request):
    '''
    For logging users in
    '''
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)  #django default authentication
        if user is not None:
            login(request,user)
            if user.user_type=='2' or user.user_type=='1':
                return redirect('guardHome')
            else:
                messages.error(request," Wrong Credentials! Please Try again or contact your administrator")
        else:
            messages.info(request," Wrong Credentials! Please Try again or contact your administrator")

    return render(request,'guard/login.html')

def scanGuard(request):
    if (request.user.is_authenticated)==False:
        return redirect('guardlogin')

    return render(request,'guard/scanner.html')


def getdetailsGuard(request):
    orderid = request.GET.get('orderid', None)
    data = {
        'added': Order.objects.filter(id=orderid).exists()
    }
    if (Order.objects.filter(id=orderid).exists()):
        request.session['currentOrder'] = orderid
    return JsonResponse(data)


def verifyGuard(request):
    if (request.user.is_authenticated)==False:
        return redirect('guardlogin')

    orderid = request.session['currentOrder']
    order = Order.objects.get(id=orderid)
    if order==None:
        return redirect('guardHome')
    else:
        customer = order.customer
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items

    context =  {'cartItems':cartItems ,'order':order, 'items':items}
    return render(request, 'guard/verify.html', context)

def logoutGuard(request):
    logout(request)
    return redirect('guardlogin')


def verified(request):
    if request.method=='GET':
        orderid = request.GET.get('order')
        orderid = int(orderid)
        order = Order.objects.get(id=orderid)
        order.verified = True
        order.save()
        del request.session['currentOrder']
    return redirect('guardHome')

def raiseIssue(request):
    if request.method=='GET':
        orderid = request.GET.get('order')
        orderid = int(orderid)
        order = Order.objects.get(id=orderid)
        order.issueRaised = True
        order.save()
        del request.session['currentOrder']
    return redirect('guardHome')