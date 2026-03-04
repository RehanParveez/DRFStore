## Some Imp Concepts which are used in the Viewsets of DRF

## Overriding get_queryset():

the concept of overriding with get_queryset is like:
-- instead of using the default way like Model.objects.all(), here model is the one we are using, so we can customize what data should be returned depending on some condition we are using.

for example:

. if user is staff -> then return all the data,
. and if the user is the normal user -> then return only their own related data

so this helps in filtering data betterly based on:

. logged in user
. ownership like who owns what
. role, like what role someone has

and also this is very useful because:

. it controls which user can see what data.
. so get_queryset() method acts like a central filtering system for the whole viewset being used.


## get_object() Use:

the concept of the get_object() method is like:
-- it returns a single particular object based on its id (pk) which is being used.

for example:

in stores/5/
here 5 is the primary key (pk).

so get_object() method helps in:

. picking the specific object
. applying of the queryset filtering
. applying of the permission checking

so instead of using -> Store.objects.get(pk=pk), its better to do -> self.get_object()

so get_object() method is better bcz it provides a:

. custom queryset logic,
. permissions logic,
. and the custom filtering logic

due to these point the get_object() is the safer way of getting a single object from the data.


## get_serializer() Use:

the concept of get_serializer() method use is:

it returns the instance of the serializer with proper context, 

like instead of writing the:

ProductSerializer(products, many=True) -> in the action decorator, it better to use -> self.get_serializer(products, many=True)

-- and why this?

bcz this is according to the -> get_serializer_class() which we use to override it,

 and also using this helps in:

. adding the context of the request automatically,
. it also supports in the dynamic selection of the serializer which offers better control.


## Why use get_queryset(), get_object(), get_serializer() instead of the Model.objects logic in the Viewsets?

the point is if we directly use:

Product.objects.filter(..)

then in this situation we bypass the custom filtering logic, like we are:

. bypassing the user-based restrictions,
. we are bypassing the serializer context,
. and also we can break permissions logic which is used for applying restrictions.

but instead of all of this when we use:

. self.get_queryset() method,
. self.get_object() method,
. self.get_serializer() method,

then in this case everything is according to better practice like:

. the correct override logic,
. the correct user filtering logic,
. the correct permissions logic,
. the correct dynamic serializer class logic being used.

so this is better practice even according to the drf design practice as well.


## Using the get_queryset() method + the has_object_permission() method logic together:

this is quite important point while using viewsets due to various points like:

# using only the get_queryset() method:

see this helps in identifying like, which user can see what kind of data?

for example:
the user 1 sees only the products of their own store.

but this doesnt give us the control of like:

. who can edit what?
. who can delete what?

# uing only the has_object_permission() method:

this helps in mainly controlling like what the user can do on the given particular object, like oepration such as:

. update
. delete

but it does not  give the filtering logic properly like in the list views for example.

but if we use both these together, then:

. this gives us the multi level security.
. the get_queryset() method gives the -> visibility level security means a user can see what kind of data,
. the has_object_permission() method gives the -> instance level security means a user for example can edit/delete a specific object in the present data or not?

so using both these together gives multi level security as:

. a user cannot see others data,
. a user cannot modify others data,
. and a one main point about multi level security is like even if someone forgets to use the get_queryset() method in a custom action decorator method , then the object permission logic still gives protection.

thats why bottom line is using the get_queryset() method + the has_object_permissions method together give the strong safety and the best architecture.


## the use of @action(detail=True) vs @action(detail=False) in the @action decorator:

-- first of all the action decorator is used in the viewsets of the drf in order to add the extra logic, like any custom logic to add and it can about filtering according to a certain condition for instance.

now what is the meaning of detail=true and detail=false inside the action decorator.

# detail=True

this simply means:

. a action works on a specific object rather than working on the full general level.
. in case of detail=true we also need to use a pk in the url like when accessing that particular actions endpoint.

example:

stores/5/product_count/

here the store id = 5

-- so this means this is used when:

. we want to work on one object,
. like counting the products inside a specific category,
. or even calculating the total inventory capacity of a given specific store

so detail=true means -> single object level operation.

# detail=False

this simply means:

. a action decoraotr method works on the full general level like a full list and not on any specific object.
. in this we do not require any pk, like while accessing the url endpoint of the specific action being performed.

example:

products/low_stock/

this will return all the low stock products, according to applied condition like in my case i did quantity__lt = 5.

so in simple terms the detail=false is mainly used when we are:

. running query on the full dataset,
. we are using filtering logic across all the objects,
. like the most expensive products,
. and low stock products,
. or even total products count overall in the database.

so the detail=false means -> filtering logic on the whole data.


## Using F Expressions + Aggregate + Sum + Count + Annotate 

the simple explantion about all these is following:

# F Expressions
. the F expressions we use like when we want to do the calculations directly in our database instead of separate logic in python, means like these let us give the reference to a specific field of our model while writing a query, like a price or quantity field. so this we can use for multiplying, adding, and even comparing the fields of ours across the rows.

# Aggregate
. the aggregate functionality part offers us various methods like Sum or Count, and these we can use to combine the multiple rows of our into one value.

-- for example like doing the sum of all the product values, or like counting how many related objects exist in our data.

# Annotate
. the annotate functionality part is mainly used like to add a temproary calculated field in the each object present in the queryset. so simply it does not change our database rather it allows us to perform a operation and get desired result, like a extra info.

 -- like for example the number of products the each store has, and we can do all of this directly in the queryset.


# example of using F expressions and the Sum operation:

total = store.products.aggregate(total_inventory=Sum(F('price') * F('quantity')))

so here in this example,
. F('price') * F('quantity') part calculates the total value of our each product,
. and the Sum(..) part adds the all those values in order to get the total inventory value in our specific store.
. one more thing this i used in the inventory method with detail=True, which is like used if we want the any total value for a specific store, not all stores but a specific store.

# example of using annotate and Count:

stores = self.get_queryset().annotate(product_count=Count('products'))

and here in this example:

. the annotate(product_count=Count('products')) part is adding a temporary field which is product_count to the each store,
. and then the Count('products') part is being used for counting like how many products belong to the each store,
. and this i used in the strpro_count method which has the detail=False, again bcz we want the count of products for all the stores, not just one.


## Use of Nested Serializers:

. the Nested serializers are mainly used when like we want to show the data of the related objects inside a serialized output of the parent objects. So thats why it helps in avoiding the making of multiple api calls and also it helps in keeping the related info together.

-- And in this project, i added two basic serializers first with limited data output like:

. ProductSerializer1 –> this serializer only contains the main fields of the product model like id, name, price, and the quantity.
. StoreSerializer1 –> and this serializer only contains the main store model fields like id, name, and the city.
. then after the addition of these two serializer, now the main serializers like:

# Now in StoreSerializers:
. products = ProductSerializer1(many = True, read_only=True) -> so this means the products of the store are nwo nested.
. owner = UsersSerializers(read_only=True) -> and htis means the information of the store owner is nested here.
. product_count -> and also this is the annotated field which i used earlier like to show how many products are in the store.

# Now in ProductsSerializers:
store = StoreSerializer1(read_only = True) -> this means the details of hte store are now nested inside the product.
category = CategorySerializers(read_only = True) -> and this line menas the details of the category are nwo nested in the product.

. So by doing all of this now when i will try to fetch the data related to the store or a product, i will get the related objects information automatically like without even writing the extra queries logic.

## Select_Related:

. the select_related is the orm method of django which is used like when we mainly want to get the foreign key relationship or the one to one related objects and  all of this is done in the same query by using the sql join logic.

. And it also helps to reduce the extra queries like when we try to access the single related objects in the data, and so this makes the api working faster.

## Prefetch_Related:

. the prefetch_related is the orm method in django which is used like when we want to get the reverse of the foreign key or the many to many related objects and this happens in the separate query.

. Also the prefetch_related method helps in avoiding the  running of the more than one queries for every object like it at once gathers all the related objects together, so thats why.


## Now updating the get_queryset with select_related and the prefetch_related methods:

. Now while using the nested serializers, like its important to use better database queries means in order to avoid the n+1 query problem, which means like when i get the related objects for every row again and again so this makes all the process very slow.

. so to avoid this problem i updated the get queryset methods in all the viewsets like:

# In StoresViewset:

def get_queryset(self):
    users = self.request.user
    queryset1 = Store.objects.select_related('owner').prefetch_related('products')
    if users.is_staff:
        return queryset1
    return queryset1.filter(owner=users)

. the select_related('owner') part is about -> like by using the sql join, trying to get the related owner data in the same query.
. the prefetch_related('products') part is about -> trying to get all the products of every store properly.
. so here i mainly used it bcz it helped in supporting the nesting the ProductsSerializers1 inside the main StoreSerializers.

# In CategoryViewset:

def get_queryset(self):
    users = self.request.user
    queryset1 = Category.objects.prefetch_related('products__store', 'products__category')
    if users.is_staff:
        return queryset1
    return queryset1.filter(products__store__owner=users)

. In this viewset i used the prefetch_related('products__store', 'products__category') method part and this is helping -> in trying to properly get all the products of a category alongside its stores and other categories.

# In ProductsViewset:

def get_queryset(self):
    users = self.request.user
    queryset1 = Product.objects.select_related('store', 'category', 'store__owner')
    if users.is_staff:
        return queryset1
    return queryset1.filter(store__owner=users)

. In this viewset i again used the select_related('store', 'category', 'store__owner') method part -> to join the tables of the store, category, and of the store owner in order to reduce the queries when i properly needed to serialize the products.

# Updating the Action Decorator:

. So after adding hte nested serializers, i updated two of the action decorator methods like to use the related objects obtained from the prefetched and the selected queries rather writing extra query logic.

-- Products of a store (products_store in StoresViewset):

store = self.get_object()
serializer = ProductsSerializers(store.products.all(), many=True)

. now here the store.products.all() part is using the prefetch_related('products') which were obtained from the get_queryset and so this is a better way.

-- Products of a category (products_category in CategoryViewset):

category = self.get_object()
serializer = ProductsSerializers(category.products.all(), many=True)

. now here similarly like above the category.products.all() part is using the prefetch_related('products__store', 'products__category') properly collected at once and so this reduced the process of accessing the database again and again.


## Adding the Validation Logic in the Serializers:

# Validation:
. First of all the validation is simply about checking and analysing the data we are trying to send in the request and also before we save it to the present database.

. As i studied in drf like most of the validation logic is used in the serializer classes, means by validating the data here, this makes sure that we are only sending the right and safe data to the database.

-- And also we can do validation mainly in two ways:

. Field-level validation -> this is about checking only the single value of field by using the methods like validate_ and the fieldname().

. Object-level validation -> and this is about checking the use of multiple fields together and this is done by using the validate method and in the parenthesis of this method the parameters are(self, and the other one we can name as we want).

The validation which i practiced today is related to:

# Store Validation:
in the StoreSerializer1, i added the simple logic of validation and practiced it using the perform create() method inside the storeviewset and it about functionality like:

. the owner of the store automatically gets assign to the user who is making the request,
. and this means whenever a store is created, we dont need the one using facilty to send the owner by himself in detail rather this will be handled in the backend itself.

. furhter this is imp. bcz we want to handle the control properly like its imp to avoid if someone assigns a store to the different user.

. and in the practice i used simpler store serializer which is StoreSerializer1, used it for the create-update actions, and in the main store serializer which is StoreSerializers, used it for the read operations only and which were like as i nested the data, counting the products and also the information of the owner for example.

# Product Validation:
Then in the ProductSerializer1, i added both the field level and the object level validations like:
-- the field level:

def validate_price(self, value):
    if value <= 0:
        raise serializers.ValidationError('the price should be greater than zero')
    return value

def validate_quantity(self, value):
    if value < 0:
        raise serializers.ValidationError('the quantity cannot be zero')
    return value

. so these are the field level validations, to make sure the both fields are correct according to the validation.
. Like in the first condition, the price should be positive means greater than one, and in the second condition it is the quantity cannot be negative, and similar to the price condition it is also like the count of product should be greater than zero. 

-- Object-level validation:

def validate(self, data):
    store = data.get('store')
    category = data.get('category')
    name = data.get('name')
    user = self.context['request'].user

    if not store.is_active:
        raise serializers.ValidationError('store is not active')

    if store.owner != user:
        raise serializers.ValidationError('the store owner can only add the product')

    if category.store != store:
        raise serializers.ValidationError('the category should be related to the store')

    if Product.objects.filter(store=store, name=name).exists():
        raise serializers.ValidationError('the product already exists in this store')
    return data

. And here simialrly i tried to check multiple conditions at once like:

. The store should be active before adding products,
. And only the owner of the store can add products to it,
. Then the category should belong to the store in which the products are,
. and the last one which is like the product name should be unique in the same store, means every store name should be different.

# Category Validation:

Then in the CategorySerializer1, i added the logic of validation to make sure that only the user can create the categories in their related store, not anyone else:

def validate(self, data):
    store = data.get('store')
    user = self.context['request'].user

    if store.owner != user:
        raise serializers.ValidationError("You are not the owner of this store")
    return data

. So here this method is making sure that those users cannot create the categories for stores to which they dont belong.

## Use of Nested Serializers and the Read-only Fields:
And outisde this validation logic like related to the write operations as create, update, partial update, etc as yesterday i learnt about the use of nested serializers like in StoreSerializers added the products and the owner logic and in the ProductsSerializers added the store, category logic, for example:

products = ProductSerializer1(many=True, read_only=True)
owner = UsersSerializers(read_only=True)

. so these serializers which are nested they were only displaying the related data without allowing the one handling data liek the cleint to modify it.

-- For example, when we view a store, then we can see all the products and the owner details but bcz its read only so the handler which is client he cannot change any of these.

so this is how here the read only and hte write only operations are working

# Error Problem:
after trying to fix the error for a hour or so, like using gpt for fixing the error, and trying other was but it was telling to check the access of the serilazer like are you accessing the serializer which has validation checks or maybe your validation method is not being called, in the end the real error was which is super easy yet i could not solve it, and then the thought came like i was trying to create the product from the admin panel, so while the validation logic was in the api, but i was not using it to create the product, adn other validation checks like quantity, active store, different product in the same store, etc. so this was the error. in the end now tried checking all the validation methods and they are working according to the logic.

## Use of get_serializer_class() method:

# get_serializer_class()

The important point is normally in drf while using the ModelViewSet we usually use only the one serializer class like:

serializer_class = ProductsSerializers

And while coming to the functionality this same serializers is used for all the important actions like:
. The same serializer is used for GET action,
. The same serializer is used for POST action,
. The same serializer is used for PUT action,
. And also the same serializer is used for PATCH action

but like as i practiced yesterday the two different level serializers like for the nested information display and for the validation logic, so in the real world scenarios once should use the different serializers for different actions.

Like for example:

. when we create a product or update it, we should use the validation logic,
. And in cases when we are only retrieving a product, like getting it, then we sshould use serializers with the nested details like information of store, information of the category.

And in these cases the get_serializer_class() method is mainly used.

# Example from this project:
def get_serializer_class(self):
    if self.action in ['create', 'update', 'partial_update']:
        return ProductSerializer1 
    return ProductsSerializers

so this method simply means like:

if the request is about the actions of:
. POST (create)
. PUT (update)
. PATCH (partial_update)

 then i used the ProductSerializer1 which has the validation logic and for the actions like:

. GET list
. GET retrieve
i used the ProductsSerializers, which has mainly the nested information logic part.


## Parsers Concept in DRF:

So in this project, after using the validation logic and the nested serializers, i studied and practiced about the concept of Parsers in drf which is basically about understanding like before reaching the serializer in use how the incoming request data is processed.

# Parsers
And according to the official documentation of the drf, the parsers are mainly responsible for handling the incoming request body and then converting it into a data structure like dictionaries of Python and which are then can be accessed by using the request.data.

this means, when a handler like client sends a request to the api:

like the raw http request -> then the parser in use processes it -> then it converts it into the data of python -> and then it can be used as request.data

and if we dont use parsers then the serializer in use wont receive any data properly.

The commonly used parsers which also are used by default in drf, are:

. JSONParser
. FormParser
. MultiPartParser

By default means hese are enabled automatically and we can override these as well.

And also here each parser works depending on the Content-Type header which is handler/client sending, like:

. application/json related logic -> is handled by the JSONParser,
. application/x-www-form-urlencoded related logic -> is handled by the FormParser,
. and the multipart/form-data related logic -> is handled by the MultiPartParser

-- so If a request is sent by a content type which is not supported by the view being used then error like:
415 Unsupported Media Type occurs.


## Practice of parsers in this project:

After studying parsers i practiced parsers like firstly i added the image field in the product model in order to upload the image.

image = models.ImageField(upload_to='products/', null=True, blank=True)

after this ran the migrations, and then as uploading the image requires the media handling, so added related commands in the settings file:

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

after this in the project level urls.py file added the command:

 + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

and this setup is about making sure that the uploaded images get stored properly and can be used.


-- Then in order To handle the image uploads used parsers in the ProductsViewset as:

from rest_framework.parsers import FormParser, JSONParser, MultiPartParser

and then added parser_class as:
parser_classes = [FormParser, JSONParser, MultiPartParser]

Now out of these all parsers the:

. The FormParser is about handling the submission of form whic is by standard,
. The JSONParser is about handling the requests related to JSON data,
. And the MultiPartParser is about handling the image/file uploading by using (multipart/form-data).

-- Then i tested all these like first by uploading the images for some products again by using MultiPartParser and the offcourse FormParser for submitted the post form.

Then practiced the parser of JSONParser alone, in order to understand how this parser gives the restriction behavior.

parser_classes = [JSONParser]

after this the api was gonna accept only the -> Content-Type: application/json, so when i attempted to submit the data in the browser using the form data and the multipart form it gave the error of:

415 Unsupported Media Type -> and this occured bcz i was sending the request as multipart/form-data -> but the view was only allowing the application/json -> so this is why the request was being rejected, and after this switching to the raw JSON format, the request was working.


## Use of Middlewares:

The Middleware in django/drf is like a way to handle the logic of requests and responses at global level of any project like even before they reach our view or after the view returns a response to us.

so basically middleware classes are those that is placed b/w the handler/client request and then the response to it of the server.

After studying the middlewares concept from the documentation and gpt as well, so the thing is middlewares can be used for the tasks like authentication, logging, or like checking the performance of the system, and even can be used for updating the cycle of the request/response of objects.

And in this project, the three middleware classes are used and practiced like:

1. Block Middleware:

The BlockMiddleware is used firstly at the global level and it helps in stopping the inactive users from accessing the API.

from django.http import JsonResponse

class BlockMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and not request.user.is_active:
            return JsonResponse({'error': 'account is inactive'}, status=403)
        return self.get_response(request)

now here is the logic of:

. user = request.user -> which is about getting the current user of our to make the request for any action,
. now if the user.is_authenticated -> part is checking whether the user is logged in, 
. then not user.is_active -> part is about checking whether the users account is vurrently not active,
. so if the both of these conditions are true, then the middleware will quickly return the response of error like a 403 Forbidden response.
. and finally the logic of return self.get_response(request) -> is being used for checking like if the user is active.

# How it works then in the project:

so mainly this process is like:

when the user is inactive -> then the request action is stopped quickly like immediately, so in this case,

. The viewset logic is never going to be performed/carried out, 
. then the database being used it will be never accessed,
. and also it directly returns a 403 response.

2. Request Middleware:

The RequestMiddleware is the one middleware which is designed in the system, in auch a way, like the task is to return and then also it will display the simple information about the each and every request being present.

class RequestMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        if not user.is_authenticated:
           user = None  
        method = request.method
        path = request.path
        response = self.get_response(request)
        status = response.status_code

        print(f'{user} | {method} | {path} | status: {status}')
        return response

now here,
-- user = request.user -> part is being used to get the user who is making the request, now If the user is not authenticated, then we give it the value of None.

. method -> this part here is the HTTP method having actions like(GET, POST, PUT, DELETE) of the request,
. path -> part here is refering to the path of url which is being accessed,
. now response = self.get_response(request) -> part is mainly about executing the view and then getting a response from it,
. then status = response.status_code -> this part is being used for the HTTP status of the response we are getting like ->  200, 404, 500.
. And now the print statement will show like who did what according to the logic and it will use the response status.
 

3. Response Middleware:

The ResponseMiddleware is the middleware which is calculating like how much time the every request will take to execute itself, so:

import time

class ResponseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        duration = time.time() - start_time
        print(request.path, 'in', duration, 'sec')
        return response

now here the,
. start_time = time.time() -> part will calculate the time of start and it will happen before processing the request,
. response = self.get_response(request) -> now this part will execute our view and it will get the response from it,
. duration = time.time() - start_time -> then this part will calculate the amount of time the request took beofre completing,
. print(request.path, 'in', duration, 'sec') -> further this part will simply show/give the path and the duration of the request and response and the duration is going to be in seconds.
. return response -> and finally this part will simply return the given response.


## Use of Testing in Django/DRF:

The concept of testing in django/drf is basically like a way to check if our code and the APIs are working properly. So main use of testing is like instead of manually calling our APIs every time and then checking them if they are returning the correct data or not, so instead of doing all of this we can write our tests which could do this automatically.

And in django/drf, we can write our own made tests for our APIs by using the APITestCase class which is provided by the drf itself.

Now after creating our tests when we run them, then:

. The django will first create a temporary test database,
. Then it will run all the code which is present inside our test methods.
. Then it will check the output of the code relevant to what we expect.
. And then finally it will delete the test database which was created at the start.

So the main thing is this help us to quickly verify our given API logic, and this too without really affecting our original database.

Now while studying about the testing, the first thing was the method of setup for the product api tests is important so this simply means:

Like before testing our APIs, we first need some data in the database so we can use it. So thats why in start we use the setUp() method in our test class.

So in setUp() method i created different kind of data like related to:

# Users:
self.user1 = User.objects.create_user(username='user1', email='user1@test.com', password='pass12312')
self.user2 = User.objects.create_user(username='user2', email='user2@test.com', password='pass12312')
self.staff_user = User.objects.create_user(username='admin', email='admin@test.com', password='pass12312', is_staff=True)

. here user1 and the user2 are the normal users,
. and the staff_user here is a staff/admin user and who has the control like who can see all products, and whom not.

# Stores:
self.store1 = Store.objects.create(name="Store1", city="CityA", owner=self.user1)
self.store2 = Store.objects.create(name="Store2", city="CityB", owner=self.user2)

Now here the each store present it belongs to a particular user.

# Categories:
self.category1 = Category.objects.create(name="Category1", store=self.store1)
self.category2 = Category.objects.create(name="Category2", store=self.store2)

And then here all the categories are linked with the stores.

# Products:
self.product1 = Product.objects.create(name="Product1", price=100, quantity=3, store=self.store1, category=self.category1)
self.product2 = Product.objects.create(name="Product2", price=500, quantity=10, store=self.store2, category=self.category2)

And here the products simply belong to a store and the category.

also for testing here the product1 has a low quantity of 3, so this is helpful for testing logic like low stock filtering.


# Now the API tests:

1. test_user_data

firstly this test is about checking like if a normal user can see only their products or not.

so here what is happening? like first its:

. authenticating as the user1.
. then its calling the GET API which has path of -> /stores/api/v1/products/.
. so on running it checks like whether the response status is 200 OK which simply means success,
and the Check happens like the users can only see their own products.

2. test_owner_create

Next this test is about checking whether a owner of store can create a new product or not?

in this first it will:

authenticate as user1,
then it will send a POST request to path of -> /stores/api/v1/products/ with the data of product,
also it will verify like whether the status of response is 201  which means success like the product is created,
and lastly it will check that the total number of products is inc. by 1.

3. test_low_stock

Next this test is about checking the low stock products in the API.

In this test it will:

first again authenticate as the user1,
then call the GET API with path of -> /stores/api/v1/products/low_stock/,
then it is verifying that the status of response is 200 OK which is success,
it will check that the products only with the low quantity are shown.

4. test_staff_control

Lastly this test is about checking like if a staff/admin user can see all the products, without the fact of like to which store it belongs.

This test will again simply:

. authenticate as the staff_user,
. then it will Call GET with the path of -> /stores/api/v1/products/,
. next it will verify the point that status of response is 200 OK, meaning success.
. and lastly it will simply check like whether the response has all the given products or not.

