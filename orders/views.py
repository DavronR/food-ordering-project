from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Order
from restaurants.models import MenuItem
from .forms import OrderForm
from django.contrib import messages



def home(request):
    return render(request, 'orders/home.html')


@login_required
def customer_dashboard(request):
    """View for displaying the customer's order history."""
    orders = Order.objects.filter(customer=request.user)
    return render(request, 'orders/customer_dashboard.html', {'orders': orders})

@login_required
def cart(request):
    """View for displaying and managing the user's cart."""
    if 'cart' not in request.session:
        request.session['cart'] = {}
    
    cart = request.session['cart']
    items = []
    total_price = 0

    for item_id, quantity in cart.items():
        menu_item = get_object_or_404(MenuItem, id=item_id)
        items.append({'item': menu_item, 'quantity': quantity})
        total_price += menu_item.price * quantity
    
    return render(request, 'orders/cart.html', {'items': items, 'total_price': total_price})

@login_required
def add_to_cart(request, item_id):
    """View to add a menu item to the cart."""
    menu_item = get_object_or_404(MenuItem, id=item_id)
    
    cart = request.session.get('cart', {})
    if str(item_id) in cart:
        cart[str(item_id)] += 1
    else:
        cart[str(item_id)] = 1
    
    request.session['cart'] = cart
    messages.success(request, f"{menu_item.name} added to cart.")
    return redirect('cart')

@login_required
def remove_from_cart(request, item_id):
    """View to remove a menu item from the cart."""
    cart = request.session.get('cart', {})
    if str(item_id) in cart:
        del cart[str(item_id)]
        request.session['cart'] = cart
        messages.success(request, "Item removed from cart.")
    
    return redirect('cart')

@login_required
def place_order(request):
    """View to place an order from the items in the cart."""
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "Your cart is empty.")
        return redirect('cart')

    items = []
    total_price = 0

    for item_id, quantity in cart.items():
        menu_item = get_object_or_404(MenuItem, id=item_id)
        items.append(menu_item)
        total_price += menu_item.price * quantity

    order = Order.objects.create(customer=request.user, total_price=total_price)
    order.items.set(items)
    order.save()

    # Clear the cart after placing the order
    del request.session['cart']

    messages.success(request, "Your order has been placed successfully!")
    return redirect('order_success', order_id=order.id)

@login_required
def order_success(request, order_id):
    """View to display a success message after an order is placed."""
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    return render(request, 'orders/order_success.html', {'order': order})

@login_required
def delivery_personnel_dashboard(request):
    """View for displaying available orders and ongoing deliveries for delivery personnel."""
    available_orders = Order.objects.filter(status='Received')  # Orders available for pickup
    ongoing_deliveries = Order.objects.filter(delivery_personnel=request.user, status='picked up')  # Ongoing deliveries
    
    return render(request, 'orders/delivery_personnel_dashboard.html', {
        'available_orders': available_orders,
        'ongoing_deliveries': ongoing_deliveries
    })


@login_required
def pick_order(request, order_id):
    """View for delivery personnel to pick up an order."""
    order = get_object_or_404(Order, id=order_id, status='Received')

    if request.method == 'POST':
        order.status = 'picked up'  
        order.delivery_personnel = request.user  
        order.save()
        messages.success(request, f"Order #{order.id} has been picked up.")
        return redirect('delivery_personnel_dashboard')

    return render(request, 'orders/delivery_personnel_dashboard.html')

@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    total_price = 0
    items = []

    # Calculate total price and gather items
    for item_id, quantity in cart.items():
        item = MenuItem.objects.get(id=int(item_id))
        item_total = item.price * quantity
        items.append({'item': item, 'quantity': quantity, 'item_total': item_total})
        total_price += item_total

    if request.method == 'POST':
        # Create an Order instance
        order = Order.objects.create(customer=request.user, total_price=total_price)
        # Add the items to the order
        for item in items:
            order.items.add(item['item'])

        # Clear the cart after successful checkout
        del request.session['cart']
        return redirect('order_success', order_id=order.id)

    return render(request, 'orders/checkout.html', {
        'items': items,
        'total_price': total_price,
    })
    
@login_required
def order_success(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'orders/order_success.html', {'order': order})