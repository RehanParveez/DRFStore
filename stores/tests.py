from rest_framework.test import APITestCase
from rest_framework import status
from accounts.models import User
from stores.models import Store, Category, Product

# Create your tests here.
class ProductAPITest(APITestCase):
    def setUp(self):
        # users
        self.user1 = User.objects.create_user(username='user1', email='user1@test.com', password='pass12312')
        self.user2 = User.objects.create_user(username='user2', email='user2@test.com', password='pass12312')
        self.staff_user = User.objects.create_user(username='admin', email='admin@test.com', password='pass12312', is_staff=True)
        
        # stores
        self.store1 = Store.objects.create(name="Store1", city="CityA", owner=self.user1)
        self.store2 = Store.objects.create(name="Store2", city="CityB", owner=self.user2)

        # categories
        self.category1 = Category.objects.create(name="Category1", store=self.store1)
        self.category2 = Category.objects.create(name="Category2", store=self.store2)

        # products
        self.product1 = Product.objects.create(name="Product1", price=100, quantity=3, store=self.store1, category=self.category1)
        self.product2 = Product.objects.create(name="Product2", price=500, quantity=10, store=self.store2, category=self.category2)
        
    def test_user_data(self):
        self.client.force_authenticate(user=self.user1)
        
        response = self.client.get("/stores/api/v1/products/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["name"], "Product1")
    
    def test_owner_create(self):
        self.client.force_authenticate(user=self.user1)
        
        data = {'name': 'NewProduct', 'price': 200, 'quantity': 8, 'store': self.store1.id, 'category': self.category1.id}
        response = self.client.post("/stores/api/v1/products/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 3)
        
    def test_low_stock(self):
        self.client.force_authenticate(user=self.user1)
        
        response = self.client.get("/stores/api/v1/products/low_stock/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Product1")
        
    def test_staff_control(self):
        self.client.force_authenticate(user=self.staff_user)
        
        response = self.client.get("/stores/api/v1/products/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)
        




