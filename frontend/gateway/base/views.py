from django.shortcuts import render,HttpResponse,redirect
import json
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from django.contrib import messages
import requests
from .forms import *
from .models import *
from django.urls import reverse
from datetime import datetime
from collections import *
from django.core.cache import cache


# Create your views here.


@csrf_exempt
def login(request):
     
    message=''
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')


        url = 'http://127.0.0.1:8000/auth/login/'
        body ={
        "username":username,
        "password": password
        }

        # Make the POST request
        response = requests.post('http://127.0.0.1:8000/auth/login/', json=body)

        # Check the status code of the response
        if response.status_code == 201 or response.status_code == 200:
            print('Success:', response.json())
            user_id=response.json()['user']['id']
            message='Success'
            cache.set('isAuth',True, timeout=60 * 15)
            cache.set('userid',user_id, timeout=60 * 15)
            if UserModel.objects.filter(id=1):
                user=UserModel.objects.get(id=1)
                user.user_id=user_id
                user.email=' '
                user.password=password
                user.save()
            else:
                user=UserModel.objects.create(
                    user_id=user_id,
                    password=password,
                    email=''
                )
            return redirect(reverse('home', args=[user_id]))
        else:
            print('Failed:', response.status_code)


    return render(request, 'login.html',{'message':message})

@csrf_exempt
def register(request):
    message=''
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        email=request.POST.get('email')

        url = 'http://127.0.0.1:8000/auth/signup/'
        body ={
        "username":username,
        "email":email,
        "password": password
        }

        # Make the POST request
        response = requests.post(url, json=body)

        # Check the status code of the response
        if response.status_code>= 200:
            print('Success:', response.json())
            user_id=response.json()['user']['id']
            message='Success'
            return redirect(login)
        else:
            print('Failed:', response.status_code, response.text)
            message='Failed:'+ str(response.status_code)


    return render(request, 'register.html',{'message':message})


def home(request,user_id):
    isAuth=cache.get('isAuth',default=False)
    id=cache.get('userid',default=-1)
    print('Auth cache data:',isAuth,id)
    if isAuth==False or id==-1:
        return redirect(login)
    
    api_url = "http://127.0.0.1:8000/listings/"
    data=[]
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        
    except requests.exceptions.RequestException as e:
        print('error')

    context={
        'data':data,
        'id':id#------------------------
        }

    return render(request, 'index.html',context)

@csrf_exempt
def profile(request,user_id):
    isAuth=cache.get('isAuth',default=False)
    id=cache.get('userid',default=-1)
    print('Auth cache data:',isAuth,id)
    if isAuth==False or id==-1:
        return redirect(login)
    

    url = f'http://127.0.0.1:8000/auth/users/{user_id}'
    response = requests.get(url)
    message=''
    data={}
    if request.method == "POST":
        fullname=request.POST.get('fullname')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        dob=request.POST.get('birthdate')

        print([fullname,email,phone,email])
        body=defaultdict(str)

        if fullname:
            body['full_name']=fullname
        else:
            body['full_name']=response.json()['full_name']

        if email:
            body['email']=email
        else:
            body['email']=response.json()['email']

        if phone:
            body['phone']=phone
        else:
            body['phone']=response.json()['phone']

        if dob:
            dob_date = datetime.strptime(dob, '%Y-%m-%d')
            dob_str = dob_date.strftime('%Y-%m-%d') 
            body['date_of_birth']=dob_str
        else:
            body['date_of_birth']=response.json()['date_of_birth']

        body['created']=datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print('edit body',body)


        update_response = requests.put(f'http://127.0.0.1:8000/auth/users/{user_id}/', json=body)
        if update_response.status_code == 201 or update_response.status_code == 200:
            print('Success:', update_response.json())
            message='Success'
            return redirect(reverse('profile', args=[user_id]))
        else:
            print('Failed:', update_response.status_code)

    if response.status_code == 201 or response.status_code == 200:
        print('Success:', response.json())
        data=response.json()
        user_id=response.json()['user']['id']
    else:
        print('Failed:', response.status_code)
        

    context={
        "id":id,
        "data":data,
        "message":message
    }
    return render(request, 'profile.html',context)
        
def dashboard(request,user_id):
    isAuth=cache.get('isAuth',default=False)
    id=cache.get('userid',default=-1)
    print('Auth cache data:',isAuth,id)
    if isAuth==False or id==-1:
        return redirect(login)

    api_url = f"http://127.0.0.1:8000/orders"
    shop_url= f"http://127.0.0.1:8000/shops"
    product_url= f"http://127.0.0.1:8000/listings"
    delivery_url= f"http://127.0.0.1:8000/deliveries"
    context={'data':[]}
    try:
        response = requests.get(api_url)
        shop_response=requests.get(shop_url)
        products_response=requests.get(product_url)
        deliveries_response=requests.get(delivery_url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        shop_response.raise_for_status()
        products_response.raise_for_status()
        deliveries_response.raise_for_status()
        res = response.json()
        list=shop_response.json()
        deliv=deliveries_response.json()
        prod=products_response.json()

        print(deliv)
        orders=[]
        shops=[]
        products=[]
        deliveries=[]

        for item in res['orders']:
            if item["user_id"]==user_id:
                orders.append(item)
        

        for item in list:
            if item["created_by"]==user_id:
                shops.append(item)

        for item in deliv:
            for item2 in orders:
                if item["order_id"]==item2["id"]:
                    deliveries.append(item)

        for item in prod:
            for shop in shops:
                if item["shop_id"]==shop["id"]:
                    products.append(item)

            

        context={
            'id':id,
            'orders':orders,
            'shops':shops,
            'products':products,
            'deliveries':deliveries,
            'order_tally':len(orders),
            'shop_tally':len(shops),
            'product_tally':len(products),
            'delivery_tally':len(deliveries)
        }
    except requests.exceptions.RequestException as e:
        print('error')
    return render(request, 'user_dashboard.html',context)


def contact(request):
    id=cache.get('userid',default=-1)
    return render(request, 'contact.html',{'id':id})

def about(request):
    id=cache.get('userid',default=-1)
    return render(request, 'about.html',{'id':1})

def product(request,user_id):
    isAuth=cache.get('isAuth',default=False)
    id=cache.get('userid',default=-1)
    print('Auth cache data:',isAuth,id)
    if isAuth==False or id==-1:
        return redirect(login)
    
    api_url = "http://127.0.0.1:8000/api/products/"
    context={'data':[]}
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        context={'data':data}
    except requests.exceptions.RequestException as e:
        print('error')
    return render(request, 'products.html',context)

def product_detail(request,product_id):
    isAuth=cache.get('isAuth',default=False)
    id=cache.get('userid',default=-1)
    print('Auth cache data:',isAuth,id)
    if isAuth==False or id==-1:
        return redirect(login)
    
    api_url = f"http://127.0.0.1:8000/listings/{product_id}"
    context={'data':{}}
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        
    except requests.exceptions.RequestException as e:
        print('error')
    context={
        'id':id,
        'data':data
    }
    return render(request, 'product_detail.html',context)


@csrf_exempt
def products_add(request):
    isAuth=cache.get('isAuth',default=False)
    id=cache.get('userid',default=-1)
    print('Auth cache data:',isAuth,id)
    if isAuth==False or id==-1:
        return redirect(login)
    message=''
    shop_list=requests.get("http://127.0.0.1:8000/shops").json()
    shops=[]

    for item in shop_list:
        if item['created_by']==id:
            shops.append(item)


    if request.method=='POST':
        name=request.POST.get('name')
        description=request.POST.get('description')
        price=request.POST.get('price')
        stock=request.POST.get('stock')
        shopid=request.POST.get('shopid')


        url = 'http://127.0.0.1:8000/listings/add/'
        body ={
            "name": name,
            "description": description,
            "price": price,
            "stock_quantity": stock,
            "shop_id": shopid
        }

        # Make the POST request
        response = requests.post(url, json=body)

        # Check the status code of the response
        if response.status_code == 201:
            print('Success:', response.json())
            user_id=response.json()['user']['id']
            message='Success'
            return redirect(login)
        else:
            print('Failed:', response.status_code, response.text)
            message='Failed:'+ str(response.status_code)+ response.text

    context={
        'id':id,
        'shops':shops,
    }
    return render(request, 'product_add.html',context)

@csrf_exempt
def products_edit(request):
    isAuth=cache.get('isAuth',default=False)
    id=cache.get('userid',default=-1)
    print('Auth cache data:',isAuth,id)
    if isAuth==False or id==-1:
        return redirect(login)

    message=''
    shop_list=requests.get("http://127.0.0.1:8000/shops").json()
    product_list=requests.get("http://127.0.0.1:8000/listings").json()
    shops=[]
    products=[]

    for item in shop_list:
        if item['created_by']==id:
            shops.append(item)
    
    for item in product_list:
        for shop in shops:
            if item["shop_id"]==shop["id"]:
                products.append(item)

    data={}
    if request.method == "POST":
        productid=request.POST.get('product')
        name=request.POST.get('name')
        description=request.POST.get('description')
        price=request.POST.get('price')
        stock=request.POST.get('stock')
        shopid=request.POST.get('shopid')

        url = f'http://127.0.0.1:8000/listings/{productid}/'
        response = requests.get(url)

        body=defaultdict(str)

        if name:
            body['name']=name
        else:
            body['name']=response.json()['name']

        if description:
            body['description']=description
        else:
            body['description']=response.json()['description']

        if price:
            body['price']=int(price)
        else:
            body['price']=response.json()['price']

        if stock:
            body['stock_quantity']=int(stock)
        else:
            body['stock_quantity']=response.json()['stock_quantity']

        if shopid:
            body['shop_id']=int(shopid)
        else:
            body['shop_id']=response.json()['shop_id']


        print('edit body',body)


        update_response = requests.put(f'http://127.0.0.1:8000/listings/{productid}/', json=body)
        if update_response.status_code == 201 or update_response.status_code == 200:
            print('Success:', update_response.json())
            message='Success'
            return redirect(reverse('product_edit'))
        else:
            print('Failed:', update_response.status_code)

    context={
        "id":id,
        "shops":shops,
        "products":products,

    }
    return render(request, 'product_edit.html',context)

def shop(request):
    isAuth=cache.get('isAuth',default=False)
    id=cache.get('userid',default=-1)
    print('Auth cache data:',isAuth,id)
    if isAuth==False or id==-1:
        return redirect(login)
    

    api_url = f"http://127.0.0.1:8000/shops"
    context={'data':[]}
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        
    except requests.exceptions.RequestException as e:
        print('error')

    context={
        'id':id,
        'data':data
        }
    return render(request, 'shop.html',context)

@csrf_exempt
def shop_add(request):
    isAuth=cache.get('isAuth',default=False)
    id=cache.get('userid',default=-1)
    print('Auth cache data:',isAuth,id)
    if isAuth==False or id==-1:
        return redirect(login)
    
    message=''
    if request.method=='POST':
        userid=id
        name=request.POST.get('name')
        location=request.POST.get('location')
        created=request.POST.get('created')


        url = 'http://127.0.0.1:8000/shops/add/'
        body =    {
        "created_by": userid,
        "name": name,
        "location": location,
        "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        # Make the POST request
        response = requests.post(url, json=body)

        # Check the status code of the response
        if response.status_code == 201 or response.status_code == 200:
            print('Success:', response.json())  
        else:
            print('Failed:', response.status_code, response.text)

    context={
        'id':id,
    }

    return render(request, 'shop_add.html',context)


def shop_detail(request,shop_id):
    isAuth=cache.get('isAuth',default=False)
    id=cache.get('userid',default=-1)
    print('Auth cache data:',isAuth,id)
    if isAuth==False or id==-1:
        return redirect(login)
    
    api_url = f"http://127.0.0.1:8000/shops/{shop_id}"
    context={'data':{}}
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        
    except requests.exceptions.RequestException as e:
        print('error')
    context={
        'id':id,
        'data':data
        }
    return render(request, 'shop_detail.html',context)

@csrf_exempt
def shop_delete(request):
    isAuth=cache.get('isAuth',default=False)
    id=cache.get('userid',default=-1)
    print('Auth cache data:',isAuth,id)

    if isAuth==False or id==-1:
        return redirect(login)
    
    shop_list=requests.get("http://127.0.0.1:8000/shops").json()
    shops=[]

    for item in shop_list:
        if item['created_by']==id:
            shops.append(item)

    if request.method=='POST':

        shopid=request.POST.get('shopid')
        url = f'http://127.0.0.1:8000/shops/{shopid}/'

        # Make the POST request
        response = requests.delete(url)

        # Check the status code of the response
        if response.status_code == 201 or response.status_code == 200:
            print('Success:', response.json())  
        else:
            print('Failed:', response.status_code, response.text)

    context={
        'id':id,
        'shops':shops
    }

    return render(request, 'shop_delete.html',context)

@csrf_exempt
def product_delete(request):
    isAuth=cache.get('isAuth',default=False)
    id=cache.get('userid',default=-1)
    print('Auth cache data:',isAuth,id)
    if isAuth==False or id==-1:
        return redirect(login)

    shop_list=requests.get("http://127.0.0.1:8000/shops").json()
    product_list=requests.get("http://127.0.0.1:8000/listings").json()
    shops=[]
    products=[]

    for item in shop_list:
        if item['created_by']==id:
            shops.append(item)
    
    for item in product_list:
        for shop in shops:
            if item["shop_id"]==shop["id"]:
                products.append(item)
    if request.method=='POST':

        productid=request.POST.get('productid')

        url = f'http://127.0.0.1:8000/listings/{productid}/'

        # Make the POST request
        response = requests.delete(url)

        # Check the status code of the response
        if response.status_code == 201 or response.status_code == 200:
            print('Success:', response.json())  
        else:
            print('Failed:', response.status_code, response.text)

    context={
        'id':id,
        'products':products
    }

    return render(request, 'product_delete.html',context)


def order(request,user_id):
    isAuth=cache.get('isAuth',default=False)
    id=cache.get('userid',default=-1)
    print('Auth cache data:',isAuth,id)
    if isAuth==False or id==-1:
        return redirect(login)
    
    api_url = f"http://127.0.0.1:8000/orders"
    context={'data':[]}
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        res = response.json()
        print(list)
        data=[]
        for item in res['orders']:
            if item["user_id"]==user_id:
                data.append(item)
        
    except requests.exceptions.RequestException as e:
        print('error')
    context={
        'id':id,
        'data':data
        }
    return render(request, 'order.html',context)

@csrf_exempt
def shop_edit(request):
    isAuth=cache.get('isAuth',default=False)
    id=cache.get('userid',default=-1)
    print('Auth cache data:',isAuth,id)
    if isAuth==False or id==-1:
        return redirect(login)

    message=''
    shop_list=requests.get("http://127.0.0.1:8000/shops").json()
    shops=[]

    for item in shop_list:
        if item['created_by']==id:
            shops.append(item)

    data={}
    if request.method == "POST":
        shopid=request.POST.get('shopid')
        name=request.POST.get('name')
        location=request.POST.get('location')

        url = f'http://127.0.0.1:8000/shops/{shopid}/'
        response = requests.get(url)

        body=defaultdict(str)
        print('shop',shopid)
        if name:
            body['name']=name
        else:
            body['name']=response.json()['name']

        if location:
            body['location']=location
        else:
            body['location']=response.json()['location']


        print('edit body',body)


        update_response = requests.put(f'http://127.0.0.1:8000/shops/{shopid}/', json=body)
        if update_response.status_code == 201 or update_response.status_code == 200:
            print('Success:', update_response.json())
            message='Success'
            return redirect(reverse('product_edit'))
        else:
            print('Failed:', update_response.status_code)

    context={
        "id":id,
        "shops":shops,

    }
    return render(request, 'shop_edit.html',context)

@csrf_exempt
def order_add(request):
    isAuth=cache.get('isAuth',default=False)
    id=cache.get('userid',default=-1)
    print('Auth cache data:',isAuth,id)
    if isAuth==False or id==-1:
        return redirect(login)
    
    message=''
    products=requests.get("http://127.0.0.1:8000/listings").json()
    if request.method=='POST':
        product=request.POST.get('product')
        address=request.POST.get('address')
        quantity=request.POST.get('quantity')
        created=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print('item id',product)
        url = 'http://127.0.0.1:8000/orders/add/'
        body = {
            "user_id": id,
            "listing_id": product,
            "delivery_provider": "ubber rides",
            "created_at": created,
            "quantity": quantity,
            "address": address,
            "delivery_method": "standard",
            "updated_at": "2024-07-19T15:55:03.858669Z",
            "status": "on_the_way"
        }

        # Make the POST request
        response = requests.post(url, json=body)

        # Check the status code of the response
        if response.status_code == 201:
            print('Success:', response.json())
        else:
            print('Failed:', response.status_code, response.text)

    context={
        'id':id,
        'products':products
    }

    return render(request, 'order_add.html',context)


def order_detail(request,order_id):
    isAuth=cache.get('isAuth',default=False)
    id=cache.get('userid',default=-1)
    print('Auth cache data:',isAuth,id)
    if isAuth==False or id==-1:
        return redirect(login)
    
    api_url = f"http://127.0.0.1:8000/orders/{order_id}"

    deliveries=requests.get(f'http://127.0.0.1:8000/deliveries/').json()


    delivery={}

    for d in deliveries:
        if d["order_id"]==order_id:
            delivery=d

    context={'data':{}}
    try:
        
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        
        product=requests.get(f'http://127.0.0.1:8000/listings/{data['order']['listing_id']}').json()
        print(product,data['order']['listing_id'])

        context={
            'id':id,
            'data':data['order'],
            'product':product,
            'delivery':delivery,
            'total':product['price']*data['order']['quantity']
        }
    except requests.exceptions.RequestException as e:
        print('error')
    return render(request, 'order_details.html',context)

@csrf_exempt
def order_delete(request,order_id):
    isAuth=cache.get('isAuth',default=False)
    id=cache.get('userid',default=-1)
    print('Auth cache data:',isAuth,id)

    if isAuth==False or id==-1:
        return redirect(login)
    
    deliveries=requests.get(f'http://127.0.0.1:8000/deliveries/').json()
    order=requests.get(f'http://127.0.0.1:8000/orders/{order_id}/').json()['order']
    delivery={}
    for d in deliveries:
        if d["order_id"]==order_id:
            delivery=d
    
    delivery_body={
        "order_id": d["order_id"],
        "delivery_status": "cancelled",
        "tracking_number": d["tracking_number"],
        "courier": d["courier"],
        "estimated_delivery_date": d["estimated_delivery_date"],
        "created_at": d["created_at"],
        "updated_at": d["updated_at"]
    }
    order_body={
        "user_id": order["user_id"],
        "listing_id": order["listing_id"],
        "delivery_provider": order["delivery_provider"],
        "created_at": order["created_at"],
        "quantity": order["quantity"],
        "address": order["address"],
        "delivery_method": order["delivery_method"],
        "updated_at": order["updated_at"],
        "status": "cancelled"
    }

    url = f'http://127.0.0.1:8000/orders/{order_id}/'

    response = requests.put(url,json=order_body)


    if response.status_code >= 200:
        print('Success ',response.status_code)  
        url = f'http://127.0.0.1:8000/deliveries/{d['id']}/'
        response = requests.put(url,json=delivery_body)
        if response.status_code >= 200:
            print('Complete ',response.status_code)  
        else:
            print('Failed:', response.status_code, response.text)
    else:
        print('Failed:', response.status_code, response.text)
    


    return redirect(reverse('home', args=[id]))



def logout(request):
    #cache operations
    cache.delete('isAuth')
    cache.delete('userid')
    return redirect(reverse('login'))