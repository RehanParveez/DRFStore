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

