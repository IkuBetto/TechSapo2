from django.db import models
from django.utils import timezone
from datetime import datetime
# Create your models here.
class Users(models.Model):
    name = models.CharField(max_length=20)
    tel = models.CharField(max_length=20)
    department = models.CharField(max_length=10)
    position = models.CharField(max_length=10)
    email = models.CharField(max_length=30)
    user_id = models.CharField(max_length=10)
    password = models.CharField(max_length=10)
    created_at = models.DateTimeField(default=datetime.now)
    update_at = models.DateTimeField(auto_now=True)

class Clients(models.Model):
	clients_name = models.CharField(max_length=20)
	company_id = models.CharField(max_length=30)
	clients_mail = models.CharField(max_length=30)
	tel = models.CharField(max_length=20)
	web_site_link = models.CharField(max_length=50)
	# sales_user_id = models.IntegerField()
	stage_id = models.IntegerField()
	accuracy = models.CharField(max_length=100)
	industry = models.CharField(max_length=10)
	annual_revenue = models.IntegerField()
	address = models.CharField(max_length=50)
	memo1 = models.CharField(max_length=2000)
	memo2 = models.CharField(max_length=2000)
	created_at = models.DateTimeField(default=datetime.now)
	update_at = models.DateTimeField(auto_now=True)

class Connection(models.Model):
	clients_name = models.CharField(max_length=20)
	company_id = models.CharField(max_length=30)
	clients_mail = models.CharField(max_length=30)
	tel = models.CharField(max_length=20)
	web_site_link = models.CharField(max_length=50)
	# sales_user_id = models.IntegerField()
	stage_id = models.IntegerField()
	accuracy = models.CharField(max_length=100)
	industry = models.CharField(max_length=10)
	annual_revenue = models.IntegerField()
	address = models.CharField(max_length=50)
	memo1 = models.CharField(max_length=2000)
	memo2 = models.CharField(max_length=2000)
	created_at = models.DateTimeField(default=datetime.now)
	update_at = models.DateTimeField(auto_now=True)

class Admin_users(models.Model):
	name = models.CharField(max_length=10)
	tel = models.CharField(max_length=20)
	department = models.CharField(max_length=10)
	position = models.CharField(max_length=10)
	email = models.CharField(max_length=30)
	user_id = models.CharField(max_length=10)
	password = models.CharField(max_length=10)
	created_at = models.DateTimeField(default=datetime.now)
	update_at = models.DateTimeField(auto_now=True)

class Business_talk(models.Model):
	name = models.CharField(max_length=30)
	company_id = models.IntegerField()
	tel = models.CharField(max_length=15)
	mail = models.CharField(max_length=30)
	client_representive = models.CharField(max_length=10)
	web_site_link = models.CharField(max_length=50)
	# estimated_value = models.IntegerField()
	date = models.DateField()
	stage_id = models.IntegerField()
	accuracy = models.CharField(max_length=100)
	next_step = models.CharField(max_length=100)
	content = models.CharField(max_length=5000)
	memo1 = models.CharField(max_length=2000)
	memo2 = models.CharField(max_length=2000)
	created_at = models.DateTimeField(default=datetime.now)
	update_at = models.DateTimeField(auto_now=True)
	complete = models.IntegerField()

class Company(models.Model):
	name = models.CharField(max_length=30)
	mail = models.CharField(max_length=30)
	tel = models.CharField(max_length=30)
	web_site_link = models.CharField(max_length=30)
	#number_of_employee = models.IntegerField()
	industry = models.CharField(max_length=10)
	#annual_revenue = models.IntegerField()
	address = models.CharField(max_length=50)
	created_at = models.DateTimeField(default=datetime.now)
	update_at = models.DateTimeField(auto_now=True)

class mail_password(models.Model):
	mail = models.CharField(max_length=30)
	password = models.CharField(max_length=30)
	user_index = models.IntegerField()

class Client_stage(models.Model):
	stage = models.CharField(max_length=30)

class Business_talk_stage(models.Model):
	stage = models.CharField(max_length=30)
