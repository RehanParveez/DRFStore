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
