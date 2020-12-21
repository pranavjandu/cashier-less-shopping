from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.db.models.signals import post_save
from django.dispatch import receiver

class Customer(models.Model):
    readonly_fields = ('id',)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id) +". "+ self.user.username

class Product(models.Model):
    readonly_fields = ('id',)
    title = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=2, max_digits=100, default=0.00)
    image = models.ImageField(null=True, blank = True)

    def __str__(self):
        return str(self.id) +". "+ self.title

class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=CASCADE)
    products = models.ManyToManyField(Product)
    total = models.DecimalField(decimal_places=2, max_digits=100, default=0.00)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.customer.save()