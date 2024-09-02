from django.shortcuts import get_object_or_404, render, redirect
from orders.models import Order
from .models import Restaurant, MenuItem
from .forms import MenuItemForm, RestaurantForm
from django.contrib.auth.decorators import login_required

@login_required
def owner_dashboard(request):
    """View for the restaurant owner's dashboard, displaying and creating restaurants, and listing orders."""
    user = request.user
    
    # Get all restaurants owned by the user
    restaurants = Restaurant.objects.filter(owner=user)
    
    # Get all orders related to the owner's restaurants
    orders = Order.objects.filter(items__restaurant__in=restaurants).distinct()

    if request.method == 'POST':
        form = RestaurantForm(request.POST)
        if form.is_valid():
            restaurant = form.save(commit=False)
            restaurant.owner = user
            restaurant.save()
            return redirect('owner_dashboard')  # Redirect back to the dashboard
    else:
        form = RestaurantForm()

    return render(request, 'restaurants/restaurant_owner_dashboard.html', {
        'user': user,
        'restaurants': restaurants,
        'orders': orders,
        'form': form,
    })

@login_required
def restaurant_detail(request, pk):
    """View to display details of a specific restaurant and manage its menu."""
    restaurant = get_object_or_404(Restaurant, pk=pk, owner=request.user)
    menu_items = MenuItem.objects.filter(restaurant=restaurant)

    if request.method == 'POST':
        if 'delete_item' in request.POST:
            item_id = request.POST.get('delete_item')
            MenuItem.objects.filter(id=item_id).delete()
            return redirect('restaurant_detail', pk=pk)
        else:
            form = MenuItemForm(request.POST)
            if form.is_valid():
                menu_item = form.save(commit=False)
                menu_item.restaurant = restaurant
                menu_item.save()
                return redirect('restaurant_detail', pk=pk)
    else:
        form = MenuItemForm()

    return render(request, 'restaurants/restaurant_detail.html', {
        'restaurant': restaurant,
        'menu_items': menu_items,
        'form': form,
    })

@login_required
def restaurant_menu(request, pk):
    """View to display a restaurant's menu and handle item selection."""
    restaurant = get_object_or_404(Restaurant, pk=pk)
    menu_items = MenuItem.objects.filter(restaurant=restaurant)

    # Initialize the cart if it doesn't exist
    cart = request.session.get('cart', {})

    if request.method == 'POST':
        if 'item_id' in request.POST:
            item_id = request.POST.get('item_id')
            if item_id:
                cart[item_id] = cart.get(item_id, 0) + 1  
                request.session['cart'] = cart
        elif 'delete_item' in request.POST:
            item_id = request.POST.get('delete_item')
            if item_id in cart:
                del cart[item_id]
                request.session['cart'] = cart 

   
    cart_items = []
    total_price = 0
    for item_id, quantity in cart.items():
        item_id_int = int(item_id)
        item = MenuItem.objects.get(id=item_id_int)
        item_total_price = item.price * quantity
        cart_items.append({'item': item, 'quantity': quantity, 'item_total_price': item_total_price})
        total_price += item_total_price

    return render(request, 'restaurants/restaurant_menu.html', {
        'restaurant': restaurant,
        'menu_items': menu_items,
        'cart_items': cart_items,  
        'total_price': total_price,  
    })

@login_required
def manage_menu(request, pk):
    """View to manage menu items for a restaurant."""
    restaurant = get_object_or_404(Restaurant, pk=pk, owner=request.user)
    menu_items = MenuItem.objects.filter(restaurant=restaurant)

    if request.method == 'POST':
        if 'delete_item' in request.POST:
            item_id = request.POST.get('delete_item')
            MenuItem.objects.filter(id=item_id).delete()
            return redirect('manage_menu', pk=pk)
        else:
            form = MenuItemForm(request.POST)
            if form.is_valid():
                menu_item = form.save(commit=False)
                menu_item.restaurant = restaurant
                menu_item.save()
                return redirect('manage_menu', pk=pk)
    else:
        form = MenuItemForm()  

    return render(request, 'restaurants/manage_menu.html', {
        'restaurant': restaurant,
        'menu_items': menu_items,
        'form': form,
    })