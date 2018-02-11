from django.db import models
from django.utils import timezone
from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Product(models.Model):
	seller = models.ForeignKey('auth.User')
	name = models.CharField(max_length=200, default = "")
	Cas = models.IntegerField(default = 0)
	grade=models.CharField(max_length=30, default = "")
	quantity=models.IntegerField(default = 0)
	added_date = models.DateTimeField(
			blank=True, null=True)

	def add(self):
		self.added_date = timezone.now()
		self.save()

	def __str__(self):
		return self.name

## Can't use tagging as component a b will be considered as 2 different components.

class Mainproduct(models.Model):
	seller = models.CharField(max_length = 200, default="")
	name = models.CharField(max_length = 200)
	components = models.TextField(default="")
	company_name = models.CharField(max_length = 200, default="")
	country = models.CharField(max_length = 200, default="")
	company_type = models.CharField(max_length = 200, default="")
	added_date = models.DateTimeField(
			blank=True, null=True)

	def add(self):
		self.added_date = timezone.now()
		self.save()

	def __str__(self):
		return self.name

class Api(models.Model):
	name = models.CharField(max_length = 200)
	mainproduct = models.ForeignKey(Mainproduct, on_delete=models.CASCADE, default="")

	def __str__(self):
		return self.name

class impurity(models.Model):
	av_choices=(
		('IP','IP'),
		('EP','EP'),
		('USP','USP'),
		)

	name = models.CharField(max_length=200, default="")
	Cas = models.IntegerField()
	grade=models.CharField(max_length=3,choices=av_choices)
	quantity=models.IntegerField()
	added_date = models.DateTimeField(
			blank=True, null=True)

	def add(self):
		self.added_date = timezone.now()
		self.save()

	def __str__(self):
		return self.name

class Profile(models.Model):
	av_choices=(
		('Manufacturer','Manufacturer'),
		('Trader','Trader'),
		)	
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	email_confirmed = models.BooleanField(default=False)
	email = models.EmailField(max_length=254, default = "")
	company_name = models.CharField(max_length=100, default="")
	company_type = models.CharField(max_length=12, choices = av_choices, default = "")
	phone_no = models.IntegerField(default = 0)
	
@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)
	instance.profile.save()


class ProductAvailability(models.Model):
	name = models.CharField(max_length=100, default = "")
	email = models.EmailField(max_length=254, default = "")
	company_name = models.CharField(max_length=100, default="")
	phone_no = models.IntegerField(default = 0)
	product_name = models.CharField(max_length=100, default = "")
	Cas = models.IntegerField(default = 0)
	grade=models.CharField(max_length=30, default = "")
	quantity=models.IntegerField(default=0)
	added_date = models.DateTimeField(
			blank=True, null=True)

	def add(self):
		self.added_date = timezone.now()
		self.save()

	def __str__(self):
		return self.name


class ImpurityAvailability(models.Model):
	name = models.CharField(max_length=100, default = "")
	email = models.EmailField(max_length=254, default = "")
	company_name = models.CharField(max_length=100, default="")
	phone_no = models.IntegerField(default = 0)
	impurity_name = models.CharField(max_length=100, default = "")
	Cas = models.IntegerField(default = 0)
	grade=models.CharField(max_length=30, default = "")
	quantity=models.IntegerField(default = 0)
	added_date = models.DateTimeField(
			blank=True, null=True)

	def add(self):
		self.added_date = timezone.now()
		self.save()

	def __str__(self):
		return self.name
