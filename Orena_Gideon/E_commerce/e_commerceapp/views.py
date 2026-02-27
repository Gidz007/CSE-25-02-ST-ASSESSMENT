"""
Views for the e_commerceapp module.
contains product management,and user_related operations.
"""

from django.shortcuts import render, redirect
from e_commerceapp.models import Product

# Create your views here.


def index(request):
    """
    A view handling product entry, display and calculations.
    A form for entry, a table for dispaly and cards for calcualated outputs.
    """

    # Initialise the error and success box.
    error = None
    success = None
    field_errors = {}  # Field-specific errors for highlighting inputs.

    # Check for success message from URL parameters
    if request.GET.get('success'):
        success = request.GET.get('success').replace('%20', ' ')
    
    # Check for error message from URL parameters
    if request.GET.get('error'):
        error = request.GET.get('error').replace('%20', ' ')

    if request.method == "POST":
        # Check if the "clear" button was clicked
        if "clear" in request.POST:
            # Reset error and success messages
            error = None
            success = None
            field_errors = {}
        else:

            data = request.POST

            # Extract form data.
            name = data.get("name")
            category = data.get("category")
            price = data.get("price")
            quantity = data.get("quantity")
            color = data.get("color")
            image = request.FILES.get("image")

            # Start validation.
            errors = []
            if not name or not name.replace(" ", "").isalpha():
                field_errors["name"] = "Product name is required and must contain only letters."
                errors.append("Product name is required and must contain only letters.")
            if not category or not category.replace(" ", "").isalpha():
                field_errors["category"] = "Category is required and must contain only letters."
                errors.append("Category is required and must contain only letters.")
            if not price or not price.isdigit() or int(price) <= 0:
                field_errors["price"] = "Price must be a positive number."
                errors.append("Price must be a positive number.")
            if not quantity or not quantity.isdigit() or int(quantity) < 0:
                field_errors["quantity"] = "Quantity must be a non-negative number."
                errors.append("Quantity must be a non-negative number.")
            if not color or not color.replace(" ", "").isalpha():
                field_errors["color"] = "Color is required and must contain only letters."
                errors.append("Color is required and must contain only letters.")

            # If there are errors, return them to
            if errors:
                error = " | ".join(errors)

            else:
                # Save the product to database.
                product = Product(
                    name=name,
                    category=category,
                    price=int(price),
                    quantity=int(quantity),
                    color=color,
                    image=image,
                )

                # Save the product instance to the database.
                product.save()

                # Set a success message.
                success = f"Product '{name}' has been added successfully!"

                # redirecting after proper submission of the product.
                return redirect(f"/?success={success.replace(' ', '%20')}")

    # Fetch all products from the database
    products = Product.objects.all().order_by("-id")

    # Dashboard data calculations.
    # Total revenue.
    total_revenue = sum(product.price * product.quantity for product in products)
    # Expected revenue (assume it is one per product ).
    expected_revenue = sum(product.price for product in products)
    # Capital in stock.
    capital_in_stock = sum(
        product.price * product.quantity for product in products if product.quantity > 0
    )
    # number of products out of stock.
    out_of_stock = products.filter(quantity=0).count()
    # Use a context to pass the products table in the tampate.

    # pass the products, error, field_errors and dashboard caluculations to the template.
    context = {
        "all_products": products,
        "error": error,
        "success": success,
        "field_errors": field_errors,
        "dashboard": {
            "total_revenue": total_revenue,
            "expected_revenue": expected_revenue,
            "capital_in_stock": capital_in_stock,
            "out_of_stock": out_of_stock,
        },
    }

    return render(request, "index.html", context)


def delete_product(request, product_id):
    """
    A view to delete a product permanently from the database.
    """
    try:
        product = Product.objects.get(id=product_id)
        product_name = product.name
        product.delete()
        # Set success message for deletion
        return redirect(f"/?success={product_name}%20deleted%20successfully!")
    except Product.DoesNotExist:
        # Set error message if product doesn't exist
        return redirect(f"/?error=Product%20not%20found!")


def edit_product(request, product_id):
    """
    A view to edit an existing product.
    """
    try:
        product = Product.objects.get(id=product_id)
        
        if request.method == "POST":
            # Handle form submission for editing
            data = request.POST
            
            # Extract form data.
            name = data.get("name")
            category = data.get("category")
            price = data.get("price")
            quantity = data.get("quantity")
            color = data.get("color")
            image = request.FILES.get("image")
            
            # Validation
            errors = []
            if not name or not name.replace(" ", "").isalpha():
                errors.append("Product name is required and must contain only letters.")
            if not category or not category.replace(" ", "").isalpha():
                errors.append("Category is required and must contain only letters.")
            if not price or not price.isdigit() or int(price) <= 0:
                errors.append("Price must be a positive number.")
            if not quantity or not quantity.isdigit() or int(quantity) < 0:
                errors.append("Quantity must be a non-negative number.")
            if not color or not color.replace(" ", "").isalpha():
                errors.append("Color is required and must contain only letters.")
            
            if errors:
                error = " | ".join(errors)
                return render(request, "edit_product.html", {
                    "product": product,
                    "error": error,
                    "name": name,
                    "category": category,
                    "price": price,
                    "quantity": quantity,
                    "color": color,
                })
            
            # Update product
            product.name = name
            product.category = category
            product.price = int(price)
            product.quantity = int(quantity)
            product.color = color
            if image:
                product.image = image
            
            product.save()
            return redirect(f"/?success={name}%20updated%20successfully!")
        
        # GET request - show edit form
        return render(request, "edit_product.html", {"product": product})
        
    except Product.DoesNotExist:
        return redirect(f"/?error=Product%20not%20found!")


###################################
## Testing view.
def testing(request):
    return render(request, "testing.html")
