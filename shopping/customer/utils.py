import json
from .models import *


def cartData(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.get_cart_items
	else:
		cartItems = {}
		order = {}
		items = {}

	return {'cartItems':cartItems ,'order':order, 'items':items}