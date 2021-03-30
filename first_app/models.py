from django.db import models
import re
from .models import *
import bcrypt

class UserManager(models.Manager):
	def basic_validator(self, postData):
		errors = {}
		
		if len(postData['first_name']) < 2:
			errors['first_name'] = "First name should be at least 2 characters."
		else: 
			FIRSTNAME_REGEX = re.compile(r'^[a-zA-Z]+$')
			if not FIRSTNAME_REGEX.match(postData['first_name']):
				errors['first_name'] = "First name must contain only letters."
		if len(postData['last_name']) < 2:
			errors['last_name'] = "Last name should be at least 2 characters."
		else:
			LASTNAME_REGEX = re.compile(r'^[a-zA-Z]+$')
			if not LASTNAME_REGEX.match(postData['last_name']):
				errors['last_name'] = "Last name must contain only letters."	
		if len(postData['email']) == 0:
			errors['email']	= "Email address required."
		else:
			EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
			if not EMAIL_REGEX.match(postData['email']):
				errors['email'] = "Invalid email address!"
		email = self.filter(email=postData['email'])
		if email:
			errors['email'] = "Email address already used."		
		if len(postData['password']) < 8:
			errors['password']	= "Password must be at least 8 characters."
		if postData['password'] != postData['confirmPassword']:
			errors['password'] = 'Passwords must match'
		return errors

	def login_validator(self, postData):
		errors = {}
		login_email = User.objects.filter(email=postData['login_email'])
		if len(login_email) > 0:
			if bcrypt.checkpw(postData['login_pass'].encode(),login_email[0].password.encode()):
				print("password matches")
			else:
				errors['login_email'] ='Password does not match'
		else:
			errors['login_email'] = 'User with that email does not exist'
		return errors

	def book_validator(self, postData):
		errors = {}
		
		if len(postData['title']) == 0:
			errors['title']	= "Title is required."
		if len(postData['description']) < 5:
			errors['description'] = "Description should be at least 5 characters."	 		
		# title = self.filter(title=postData['title'])
		# if postData['title'] 
		return errors


class User(models.Model):
	first_name= models.CharField(max_length=45)
	last_name= models.CharField(max_length=45)
	email= models.CharField(max_length=60)
	password=models.CharField(max_length=80)
	created_at= models.DateTimeField(auto_now_add = True)
	updated_at=models.DateTimeField(auto_now = True)
	objects = UserManager()
 	#liked_books= a list of books a given user likes
 	#books_uploaded = a list of books uploaded by a given user

class Book(models.Model):
	title = models.CharField(max_length=255)
	description = models.TextField(null=True)
	uploaded_by = models.ForeignKey(User, related_name="books_uploaded", on_delete = models.CASCADE)
		#User who uploaded a given book
	users_who_like = models.ManyToManyField(User, related_name="liked_books")
		#list of users who like a given books
	created_at= models.DateTimeField(auto_now_add = True)
	updated_at=models.DateTimeField(auto_now = True)
	objects = UserManager()

	def __repr__(self):
		return f"<Book: {self.title} ({self.id})>"