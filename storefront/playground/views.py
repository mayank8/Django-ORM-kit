from typing import Collection
from django.db.models.expressions import Col
from django.db.models.fields import DecimalField
from django.shortcuts import render
from django.http import HttpResponse
from store.models import Customer, Order, OrderItem, Product, Collection
from django.db.models import Q, F, Value, Func, ExpressionWrapper
from django.db.models.aggregates import Count, Avg, Min, Max
from django.contrib.contenttypes.models import ContentType
from store.models import Product
from tags.models import TaggedItem

from django.db import connection

from django.db import transaction #used to create autonomous transactions
# Create your views here.

@transaction.atomic() #this will make the fn atomic
def say_hello(request):
    #https://docs.djangoproject.com/en/3.2/ref/models/querysets/
    #product = Product.objects.get(pk=1)
    #product = Product.objects.filter(unit_price = 1)
    #product = Product.objects.filter(unit_price__gt = 1) #greaterthan lt-lessthan
    #title__startswith last_update__year = 2021
    #query_set = Product.objects.filter(unit_price__range = (20,30)) this will return query set

    #product = Product.objects.order_by('unit_price')[0] this will return a single object
    #product = Product.objects.latest('unit_price') 

    #query_set = Product.objects.all()[0:5] #fetch first 5
    #query_set = OrderItem.objects.values_list('id','title') #query only specified fileds. __ will find the join condition column
    #query_set = Product.objects.only('id','title') #same as above

    #query_set = Product.objects.select_related('collection').all() #used to load collection in inner join

    #query_set = Product.objects.prefetch_related('promotions').select_related('collection').all() #this will create 2 queries with innerjoins and make a single queryset

    #query_set = Order.objects.select_related('customer').prefetch_related('orderitem_set')[:5] #2 innerjoins between tables and fetch first 5 rows
    #query_set = Product.objects.filter(Q(inventory__lt=10) | Q(unit_price__lt=20)) # | for or operator, & - for and ~ for not
    #return render(request, 'hello.html', {'name' : 'Mayanks', 'products' : list(query_set)})
    
    #Annotate is used to create a new column or derive a new col
    #query_set = Customer.objects.annotate(  fullname = Func(F('first_name'), Value(' '), F('last_name'), function='CONCAT') )
    #concat('first_name', Value(' '), 'last_name') this could also be used as above example. we wrap value(' ') because django thinks ' ' is a column
    #return render(request, 'hello.html', {'name' : 'Mayanks', 'products' : list(query_set)})

    #grouping
    #query_set = Customer.objects.annotate(order_count = Count('order')) find number of orders for each customer

    #Aggregate fns
    #result = Product.objects.aggregate(count = Count('id'), min_price = Min('unit_price'))
    #return render(request, 'hello.html', {'name' : 'Mayanks', 'result' : result})

    #creating expression.. type casting
    #discounted_price = ExpressionWrapper(F('unit_price'), * 0.8, output_field=DecimalField())
    #query_set = Product.objects.annotate(discounted_price)

    #we created a function on taggeditem model to fetch teggeditem for product
    #query_set = TaggedItem.objects.get_tags_for(Product, 1)

    #caching
    query_set = Product.objects.all()[:5]
    #list(query_set) this query will be evaluated and fetch data from db
    #list(query_set) as we've already evalusted this data is stored in cache and will be fetched from there

    #inserting a new row in table collection
    '''collection = Collection()
    collection.title = 'Video Games'
    collection.featured_product = Product(pk=1)
    collection.save()'''

    #updating a collection
    #Collection.objects.filter(pk=11).update(featured_product = None)

    #delete a collection
    '''collection = Collection(pk=11)
    collection.delete()'''

    #atomic trn block
    '''with transaction.atomic():
        order = Order()
        order.customer_id = 1
        order.save()

        item = OrderItem()
        item.order=order
        item.product_id = 1
        item.quantity = 1
        item.unit_price = 10
        item.save()'''

    #execute raw sql queries 2 ways
    '''with connection.cursor() as c:
        c.callproc('get_cust', [1,2,a]) #calling a procedure
        c.execute('insert into store values(1,abc')'''
    #query_set = Product.objects.raw('select * from store_products')


    return render(request, 'hello.html', {'name' : 'Mayanks', 'products' : list(query_set)})