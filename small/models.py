from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Group

from django.db.models.signals import post_save
from django.dispatch import receiver

from PIL import Image

"""
>>> user = User.objects.create_user(username="your_username", password="your_password")
>>> user.is_staff = True
>>> user.is_superuser = False
>>> user.save()
"""

class Customer(models.Model):
	user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
	profile_pic = models.ImageField(null=True, blank=True)
	bio = models.CharField(max_length=200, default="This is my Bio.")

	def save(self, *args, **kwargs):
		if self.profile_pic:
			super(Customer, self).save(*args,**kwargs) 
			img = Image.open(self.profile_pic.path)
			if img.height > 300 and img.width > 300:
				new_img_dim = (300, 300)
				img.thumbnail(new_img_dim)
				img.save(self.profile_pic.path, quality=20)
		else:
			super(Customer, self).save(*args,**kwargs)

	def __str__(self):
		if self.user:
			return self.user.username
		return f"beyouuser-{self.id}"


# SIGNALS
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	group = Group.objects.get(name="customer")
	instance.groups.add(group)
	if created:
		Customer.objects.create(user=instance)

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
	if not(created):
		instance.customer.save()




class Tag(models.Model):
	name = models.CharField(max_length=50, null=True)

	def __str__(self):
		return self.name

class Product(models.Model):
	name = models.CharField(max_length=150, null=True)
	price = models.FloatField(null=True)
	product_pic = models.ImageField(blank=True, null=True)
	tags = models.ManyToManyField(Tag)
	date_created = models.DateTimeField(auto_now_add=True)

	def save(self, *args, **kwargs):
		super(Product, self).save(*args,**kwargs)
		img = Image.open(self.product_pic.path)
		if img.height > 600 and img.width > 800:
			new_img_dim = (800, 600)
			img.thumbnail(new_img_dim)
			img.save(self.product_pic.path, quality=50)

	def __str__(self):
		return self.name


class Order(models.Model):
	STATUS = (
			('Pending', 'Pending'),
			('Delivered', 'Delivered'),
		)
	customer = models.ForeignKey(Customer, null=True, on_delete=models.CASCADE)
	product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE)
	date_created = models.DateTimeField(auto_now_add=True)
	status = models.CharField(max_length=30, null=True, choices=STATUS, default='Pending')

	def __str__(self):
		return f'buys {self.product.name}'



class Article(models.Model):
	author = models.ForeignKey(Customer, null=True, on_delete=models.CASCADE)
	title = models.CharField(max_length=100, null=True)
	content = models.TextField(null=True)
	like = models.IntegerField(null=True, default=20)

	def __str__(self):
		return self.title


