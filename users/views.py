from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect

from orders.models import Order
from restaurants.models import Restaurant
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required

import logging

logger = logging.getLogger(__name__)

from django.contrib.auth.models import Group

def create_groups():
    for role in ['Customer', 'Restaurant Owner', 'Delivery Personnel']:
        Group.objects.get_or_create(name=role)

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # Ensure the necessary groups exist
            create_groups()

            user = form.save()
            role = form.cleaned_data.get('role')  # No need to lower() here
            group = Group.objects.get(name=role)
            user.groups.add(group)
            user.save()

            user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password1'))
            if user:
                login(request, user)
                if role == 'Customer':
                    return redirect('customer_dashboard')
                elif role == 'Restaurant Owner':
                    return redirect('restaurant_owner_dashboard')
                elif role == 'Delivery Personnel':
                    return redirect('delivery_personnel_dashboard')
                else:
                    messages.error(request, f"No dashboard available for the role '{role}'.")
                    return redirect('home')
        else:
            print("Form errors:", form.errors)
            messages.error(request, "Form is not valid. Please check the entered data.")
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/register.html', {'form': form})




@login_required
def profile(request):
    """View to display and edit the user's profile."""
    return render(request, 'users/profile.html', {'user': request.user})

import logging

logger = logging.getLogger(__name__)

def custom_login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            # Check and log user groups
            user_groups = user.groups.values_list('name', flat=True)
            logger.info(f"User Groups: {list(user_groups)}")
            
            # Redirect based on user role
            if user.groups.filter(name='customer').exists():
                return redirect('customer_dashboard')
            elif user.groups.filter(name='restaurant_owner').exists():
                return redirect('restaurant_owner_dashboard')
            elif user.groups.filter(name='delivery_personnel').exists():
                return redirect('delivery_personnel_dashboard')
            else:
                logger.error("No valid group found for user; redirecting to home.")
                return redirect('home')  # Fallback to home if no specific role found
        else:
            logger.error("Invalid login attempt.")
            return render(request, 'users/login.html', {'error': 'Invalid username or password.'})
    else:
        return render(request, 'users/login.html')
    
@login_required
def customer_dashboard(request):
    """View for the customer dashboard displaying profile data, available restaurants, and their orders."""
    user = request.user
    orders = Order.objects.filter(customer=user)  # Retrieve all orders placed by the logged-in customer
    restaurants = Restaurant.objects.all()  # Fetch all available restaurants
    
    return render(request, 'users/customer_dashboard.html', {
        'user': user,
        'orders': orders,
        'restaurants': restaurants,
    })
    

@login_required
def delivery_personnel_dashboard(request):
    """View for displaying available orders and ongoing deliveries for delivery personnel."""
    available_orders = Order.objects.filter(status='Received')  # Orders available for pickup
    ongoing_deliveries = Order.objects.filter(delivery_personnel=request.user, status='Picked Up')  # Ongoing deliveries
    
    return render(request, 'users/delivery_personnel_dashboard.html', {
        'available_orders': available_orders,
        'ongoing_deliveries': ongoing_deliveries
    })  

@login_required
def delivery_personnel_profile(request):
    """View to display the delivery personnel's profile and their deliveries."""
    deliveries = Order.objects.filter(delivery_personnel=request.user)
    return render(request, 'users/delivery_personnel_profile.html', {
        'user': request.user,
        'deliveries': deliveries
    })