# Import Django's test tools and utilities
from django.test import TestCase, Client
from django.urls import reverse
from e_commerceapp.models import Product
from django.core.files.uploadedfile import SimpleUploadedFile

# Create your tests here.


# Create a test class for the view that handles the index page (product recording)
class IndexViewTests(TestCase):
    # Set up a test client and the URL for the view before each test
    def setUp(self):
        self.client = Client()  # Django's test client to simulate browser requests
        self.url = reverse(
            "index"
        )  # Gets the URL for the view named 'index' from urls.py

    # Test that a GET request to the index view returns a 200 OK and uses the correct template
    def test_get_request_renders_page(self):
        response = self.client.get(self.url)  # Send GET request to index view
        self.assertEqual(response.status_code, 200)  # Expect HTTP 200 (OK)
        self.assertTemplateUsed(
            response, "index.html"
        )  # Ensure 'index.html' was rendered

    # Test that a valid POST request actually creates a new Product object
    def test_post_valid_product_creates_product(self):
        # Create a fake image file to simulate uploading
        image = SimpleUploadedFile(
            "test.jpg", b"file_content", content_type="image/jpeg"
        )

        # Send POST request with valid data
        response = self.client.post(
            self.url,
            {
                "name": "Apple",
                "category": "Fruit",
                "price": "100",
                "quantity": "10",
                "color": "Red",
                "image": image,
            },
        )

        self.assertEqual(response.status_code, 302)  # Should redirect after success
        self.assertEqual(Product.objects.count(), 1)  # Confirm one product was created

    # Test that invalid POST data does not create a product and shows validation messages
    def test_post_invalid_product_shows_error(self):
        # Missing category, invalid numbers, invalid name/color
        response = self.client.post(
            self.url,
            {
                "name": "123",  # Should be letters only
                "category": "",  # Missing required field
                "price": "-50",  # Price must be positive
                "quantity": "-1",  # Quantity must be non-negative
                "color": "123",  # Should be letters only
            },
        )

        self.assertEqual(response.status_code, 200)  # Should reload form, not redirect
        self.assertContains(
            response, "Product name is required"
        )  # Should show an error message
        self.assertEqual(Product.objects.count(), 0)  # No product should be saved
