# Food Ordering Project

This is a Django-based web application that allows users to order food from various restaurants. The application supports multiple user roles, including Customers, Restaurant Owners, and Delivery Personnel, each with their own set of functionalities.


## Features

- **User Registration and Authentication**:
  - Users can sign up and log in as Customers, Restaurant Owners, or Delivery Personnel.
  
- **Role-Based Dashboards**:
  - Each user role has access to a unique dashboard:
    - **Customers**: Browse restaurants, manage cart, place orders, and track order status.
    - **Restaurant Owners**: Manage restaurant details, menu items, and view orders.
    - **Delivery Personnel**: View available delivery tasks and update delivery status.
  
- **Order Management**:
  - Restaurant Owners can manage and track orders.
  - Customers can place orders and track their status.
  - Delivery Personnel can accept and manage deliveries.

- **Restaurant Management**:
  - Restaurant Owners can add, edit, and delete menu items.
  - View and manage orders placed by customers.

## Tech Stack

- **Backend**: Django, Python
- **Frontend**: HTML, CSS
- **Database**: SQLite (default, can be replaced with PostgreSQL/MySQL)
- **Version Control**: Git, GitHub

### Prerequisites

- Python 3.x
- Django
- Git
