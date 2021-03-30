from django.urls import path
from . import views
urlpatterns = [
	path('', views.index),
	path('create_user', views.create_user),
	path('login', views.login),
	path('books', views.books), 	
	path('logout', views.logout),
	path('add_book', views.add_book),
	path('books/<int:book_id>', views.book_bio, name="book_bio"),
	path('books/<int:book_id>/edit', views.edit, name="edit"),
	path('books/<int:book_id>/delete', views.delete, name="delete"),
	path('favorites/<int:book_id>', views.favorites, name="add_favorites"),
	path('remove_fav/<int:book_id>', views.remove_fav, name="remove_fav"),
]