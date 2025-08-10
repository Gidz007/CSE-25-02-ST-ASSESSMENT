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

    # Initialise the error and the success box.
    error = None
    success = None
    field_errors = {}  # Field-spefific errors for highlighting inputs.

    if request.method == "POST":
        # Check if the "clear" button was clicked
        if "clear" in request.POST:
            # Reset error and success messages
            error = None
            success = None
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
            if not name or not name.isalpha():
                errors.append("Product name is required and must contain only letters.")
            if not category or not category.isalpha():
                errors.append("Category is required and must contain only letters.")
            if not price or not price.isdigit() or int(price) <= 0:
                errors.append("Price must be a positive number.")
            if not quantity or not quantity.isdigit() or int(quantity) < 0:
                errors.append("Quantity must be a non-negative number.")
            if not color or not color.isalpha():
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

                # redirecting after propersubmission of the product.
                return redirect("/")

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

    # pass the products, error and dashboard caluculations to the template.
    context = {
        "all_products": products,
        "error": error,
        "success": success,
        "dashboard": {
            "total_revenue": total_revenue,
            "expected_revenue": expected_revenue,
            "capital_in_stock": capital_in_stock,
            "out_of_stock": out_of_stock,
        },
    }

    return render(request, "index.html", context)


###################################
## Testing view.
def testing(request):
    return render(request, "testing.html")
