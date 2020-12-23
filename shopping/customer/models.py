from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE
from django.db.models.signals import post_save
from django.dispatch import receiver

class CustomUser(AbstractUser):
    user_type_data=((1,"Manager"),(2,"Guard"),(3,"Customer"))
    user_type=models.CharField(default=1,choices=user_type_data,max_length=10)


class Manager(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=255,null=True,blank=True)
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    objects=models.Manager()

    def __str__(self):
        return self.name

class Guard(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=255,null=True,blank=True)
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    objects=models.Manager()

    def __str__(self):
        return self.name

class Customer(models.Model):
    id=models.AutoField(primary_key=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True,blank=True)
    objects=models.Manager()

    def __str__(self):
        return self.name

class Product(models.Model):
	id=models.AutoField(primary_key=True)
	name = models.CharField(max_length=200)
	price = models.FloatField()
	desc = models.TextField(blank=True,null=True)
	image = models.ImageField(null=True, blank=True)

	def __str__(self):
		return str(self.id)+". "+self.name

	@property
	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = ''
		return url

class Order(models.Model):
	id=models.AutoField(primary_key=True)
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False)
	transaction_id = models.CharField(max_length=100, null=True)

	def __str__(self):
		return str(self.id)
		
	@property
	def shipping(self):
		shipping = False
		orderitems = self.orderitem_set.all()
		for i in orderitems:
			if i.product.digital == False:
				shipping = True
		return shipping

	@property
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.get_total for item in orderitems])
		return total 

	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems])
		return total 

class OrderItem(models.Model):
	id=models.AutoField(primary_key=True)
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)

	@property
	def get_total(self):
		total = self.product.price * self.quantity
		return total

class BillingAddress(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	address = models.CharField(max_length=200, null=False)
	city = models.CharField(max_length=200, null=False)
	state = models.CharField(max_length=200, null=False)
	zipcode = models.CharField(max_length=200, null=False)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.customer.name


@receiver(post_save,sender=CustomUser)
def create_user_profile(sender,instance,created,**kwargs):
    '''
    For creating objects of user type from CustomUser object using django signals
    '''
    if created:
        if instance.user_type==1:
            Manager.objects.create(user=instance,name="admin")
        if instance.user_type==2:
            Guard.objects.create(user=instance)
        if instance.user_type==3:
            Customer.objects.create(user=instance)

@receiver(post_save,sender=CustomUser)
def save_user_profile(sender,instance,**kwargs):
    '''
    For saving objects of user type from CustomUser object using django signals
    '''
    if instance.user_type==1:
        instance.manager.save()
    if instance.user_type==2:
        instance.guard.save()
    if instance.user_type==3:
        instance.customer.save()