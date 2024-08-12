from django.urls import path
from . import views

# URL patterns for the application
urlpatterns = [
    # Route for the core view displaying the list of all employees
    path('', views.core, name='core'),

    # Route for viewing and editing a single employee's data, identified by primary key
    path('singledata/<int:pk>/', views.single_data, name='singledata'),

    # Route for adding a new employee
    path('adddata', views.add_data, name='adddata'),

    # Route for deleting an employee, identified by primary key
    path('deletedata/<int:pk>/', views.delete_row, name='deletedata'),

    # Route for user registration
    path('signup', views.signup, name='signup'),

    # Route for user login
    path('login', views.login_user, name='login'),

    # Route for user logout
    path('logout', views.logout_user, name='logout'),
]
