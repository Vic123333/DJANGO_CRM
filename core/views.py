from django.shortcuts import render, get_object_or_404, redirect
from .models import EmployeeList
from .forms import EditForm, AddDataForm, RegisterForm, LoginForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def core(request):
    """
    Renders a list of all employees.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered HTML response displaying employee data.
    """
    employees = EmployeeList.objects.all()
    context = {
        'employees': employees
    }
    return render(request, 'data.html', context)

@login_required(login_url='login')
def single_data(request, pk):
    """
    Renders and handles form submission for editing a single employee's data.

    Args:
        request (HttpRequest): The HTTP request object.
        pk (int): The primary key of the employee to be edited.

    Returns:
        HttpResponse: Rendered HTML response with form for editing employee data.
    """
    if request.method == 'POST':
        form = EditForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            name = data['name']
            job = data['job']
            favorite_color = data['favorite_color']
            
            # Retrieve the employee object or return a 404 error if not found
            employee = get_object_or_404(EmployeeList, pk=pk)

            # Use existing values if no new values are provided
            if name == '':
                name = employee.name
            if job == '':
                job = employee.job
            if favorite_color == '':
                favorite_color = employee.favorite_color

            # Update the employee's data
            EmployeeList.objects.filter(pk=pk).update(
                name=name,
                job=job,
                favorite_color=favorite_color
            )

            return redirect('core')

    # Initialize form for GET request
    form = EditForm()

    # Retrieve the employee object for pre-filling the form
    employee = get_object_or_404(EmployeeList, pk=pk)

    context = {
        'form': form,
        'employees': employee
    }

    # Set placeholders in the form fields to existing employee data
    form.fields['name'].widget.attrs.update({
        'placeholder': employee.name,
    })
    form.fields['job'].widget.attrs.update({
        'placeholder': employee.job,
    })
    form.fields['favorite_color'].widget.attrs.update({
        'placeholder': employee.favorite_color,
    })

    return render(request, 'singledata.html', context)

@login_required(login_url='login')
def add_data(request):
    """
    Renders and handles form submission for adding a new employee.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered HTML response with form for adding a new employee.
    """
    if request.method == 'POST':
        form = AddDataForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('core')
    
    # Initialize form for GET request
    form = AddDataForm()
    context = {
        'form': form
    }

    # Set placeholders in the form fields
    form.fields['name'].widget.attrs.update({
        'placeholder': 'name',
    })
    form.fields['job'].widget.attrs.update({
        'placeholder': 'job',
    })
    form.fields['favorite_color'].widget.attrs.update({
        'placeholder': 'favorite color',
    })

    return render(request, 'adddata.html', context)

@login_required(login_url='login')
def delete_row(request, pk):
    """
    Handles deletion of an employee record.

    Args:
        request (HttpRequest): The HTTP request object.
        pk (int): The primary key of the employee to be deleted.

    Returns:
        HttpResponse: Redirects to the core view after deletion.
    """
    if request.method == 'POST':
        # Retrieve and delete the employee object or return a 404 error if not found
        employee = get_object_or_404(EmployeeList, pk=pk)
        employee.delete()
        
    return redirect('core')

@login_required(login_url='login')
def update_form_fields(form):
    """
    Helper function to update the widget attributes of the form fields.

    Args:
        form (Form): The form object whose fields need to be updated.
    """
    field_classes = 'bg-white rounded-full placeholder-gray-900 shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline hover:placeholder-gray-300'
    
    # List of fields to update with the specified CSS class
    fields_to_update = ['username', 'password1', 'password2', 'email']
    
    for field in fields_to_update:
        form.fields[field].widget.attrs.update({
            'class': field_classes
        })


def signup(request):
    """
    Handles user registration and renders the signup form.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered HTML response with the signup form or redirects after successful registration.
    """
    if request.method == 'GET':
        form = RegisterForm()  # Initialize the form for GET requests
        form = form.visible_fields()[:4]
        context = {
            'form': form,
        }

        return render(request, 'signup.html', context)
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)  # Bind POST data to the form

        if form.is_valid():  # Validate the form
            user = form.save()  # Save the new user
            login(request, user)  # Log the user in
            messages.success(request, 'Registration successful!')  # Add a success message
            return redirect('core')  # Redirect to a success page or home page
        form = form.visible_fields()[:4]
        # If form is invalid, render the form with errors
        context = {
            'form': form,
        }
        return render(request, 'signup.html', context)


def login_user(request):
    """
    Handles user login and renders the login form.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Rendered HTML response with the login form or redirects after successful login.
    """
    if request.method == 'GET':
        form = LoginForm()
        context = {'form': form}
        return render(request, 'login.html', context)

    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            username = data['username']
            password = data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f'Login successful! Hello {username}')
                return redirect('core')
            else:
                messages.error(request, 'Wrong Password or Username')
                return redirect('login')
        else:
            # Form is not valid, re-render the login page with form errors
            context = {'form': form}
            return render(request, 'login.html', context)

@login_required(login_url='login')
def logout_user(request):
    """
    Logs out the user and redirects to the core view.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Redirects to the core view after logout.
    """
    logout(request)
    messages.success(request, 'Logout successful!')
    return redirect('core')
