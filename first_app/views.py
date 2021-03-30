from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
import bcrypt


def index(request):
	
	return render(request, "registration.html")

def create_user(request):
	if request.method == 'POST':
		errors = User.objects.basic_validator(request.POST)
		if errors:
			for key, value in errors.items():
				messages.error(request, value)
			print('error found')	
			return redirect('/')
		else:
			hashedpw = bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt()).decode()
			print(request.POST['password'])
			print(hashedpw)
			new_user = User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'], password= hashedpw)
			request.session['User'] = new_user.id
			return redirect('/books') 
	else: 
		redirect('/')

def login(request):
	if request.method == 'POST':
		errors = User.objects.login_validator(request.POST)
		if len(errors) > 0:
			for key, value in errors.items():
				messages.error(request, value)
			return redirect('/')
		else:
			logged_User = User.objects.get(email=request.POST['login_email'])
			request.session['User'] = logged_User.id
			print('password match')
			return redirect('/books')
	else:
		redirect('/')

def books(request):
	if 'User' in request.session:
		context = {
			"logged_User": User.objects.get(id=request.session['User']),
			"all_books": Book.objects.all(),
			}
		return render(request, 'main_page.html', context)
	else: 
		print('user must be logged in')
		return redirect('/')

def add_book(request):
	errors = User.objects.book_validator(request.POST)
	if len(errors) > 0:
		for key, value in errors.items():
			messages.error(request, value)
		print('error found')	
		return redirect('/books')
	else:
		one_user = User.objects.get(id=request.session['User'])
		new_book = Book.objects.create(title = request.POST['title'], description= request.POST['description'], uploaded_by= one_user)
		new_book.users_who_like.add(one_user)
		print("Book Added")
		return redirect('/books')

def book_bio(request, book_id):
	context = {
		"book": Book.objects.get(id=book_id),
		"user_in_session" : User.objects.get(id=request.session['User']),
		}
		
	return render(request,'book_bio.html',context)

def edit(request, book_id):
	book= Book.objects.get(id=book_id)
	book.description = request.POST['description']
	print('description updated')
	book.save()
	return redirect(f'/books/{book_id}')

def delete(request, book_id):
	delete_book = Book.objects.get(id=book_id).delete()
	return redirect('/books')

def favorites(request, book_id):
	one_user= User.objects.get(id=request.session['User'])
	book= Book.objects.get(id=book_id)
	one_user.liked_books.add(book)
	print("Book added to favorites")
	return redirect(f'/books/{book_id}')	

def remove_fav(request, book_id):
	one_user= User.objects.get(id=request.session['User'])
	book= Book.objects.get(id=book_id)
	one_user.liked_books.remove(book)
	
	return redirect(f'/books/{book_id}')

def logout(request):
	request.session.clear()
	return redirect('/')

