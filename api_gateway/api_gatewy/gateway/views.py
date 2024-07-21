from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import requests

# Create your views here.
@api_view(['POST'])
def signup(request):
    data = request.data
    response = requests.post("http://127.0.0.1:8001/signup/", data=data)
    try:
        return Response(response.json(), status=response.status_code)
    except ValueError:
        return Response(response.text, status=response.status_code)


@api_view(['POST'])
def login(request):
    data = request.data
    response = requests.post("http://127.0.0.1:8001/login/", data=data)
    try:
        return Response(response.json(), status=response.status_code)
    except ValueError:
        return Response(response.text, status=response.status_code)


@api_view(['GET', 'DELETE', "PUT","PATCH"])
def getAndDeleteProfile(request, pk):
    if request.method == "GET":
        response = requests.get(f"http://127.0.0.1:8001/users/{pk}/")
    elif request.method == "DELETE":
        response = requests.delete(f"http://127.0.0.1:8001/users/delete/{pk}/")
    elif request.method == "PATCH":
        response = requests.delete(f"http://127.0.0.1:8001/users/edit/{pk}/")
    else:
        data = request.data
        response = requests.put(f"http://127.0.0.1:8001/users/update/{pk}/", data=data)

    try:
        return Response(response.json(), status=response.status_code)
    except ValueError:
        return Response(response.text, status=response.status_code)



@api_view(['GET'])
def listings(request):
    response = requests.get("http://127.0.0.1:8003/products/")
    try:
        return Response(response.json(), status=response.status_code)
    except ValueError:
        return Response(response.text, status=response.status_code)
    

@api_view(['POST'])
def listings_add(request):
    data = request.data
    response = requests.post("http://127.0.0.1:8003/products/add/", data=data)
    try:
        return Response(response.json(), status=response.status_code)
    except ValueError:
        return Response(response.text, status=response.status_code)


@api_view(['GET', 'DELETE', "PUT"])
def listings_details(request, pk):
    if request.method == "GET":
        response = requests.get(f"http://127.0.0.1:8003/products/{pk}/")
    elif request.method == "DELETE":
        response = requests.delete(f"http://127.0.0.1:8003/products/{pk}/")
    else:
        data = request.data
        response = requests.put(f"http://127.0.0.1:8003/products/{pk}/", data=data)

    try:
        return Response(response.json(), status=response.status_code)
    except ValueError:
        return Response(response.text, status=response.status_code)
    

@api_view(['GET'])
def shops(request):
    response = requests.get("http://127.0.0.1:8003/shops/")
    try:
        return Response(response.json(), status=response.status_code)
    except ValueError:
        return Response(response.text, status=response.status_code)
    

@api_view(['POST'])
def shops_add(request):
    data = request.data
    response = requests.post("http://127.0.0.1:8003/shops/add/", data=data)
    try:
        return Response(response.json(), status=response.status_code)
    except ValueError:
        return Response(response.text, status=response.status_code)


@api_view(['GET', 'DELETE', "PUT", "PATCH"])
def shops_details(request, pk):
    if request.method == "GET":
        response = requests.get(f"http://127.0.0.1:8003/shops/{pk}/")
    elif request.method == "DELETE":
        response = requests.delete(f"http://127.0.0.1:8003/shops/{pk}/")
    else:
        data = request.data
        response = requests.patch(f"http://127.0.0.1:8003/shops/{pk}/", data=data)

    try:
        return Response(response.json(), status=response.status_code)
    except ValueError:
        return Response(response.text, status=response.status_code)
    

@api_view(['GET'])
def orders(request):
    response = requests.get("http://127.0.0.1:8002/api/order-list/")
    try:
        return Response(response.json(), status=response.status_code)
    except ValueError:
        return Response(response.text, status=response.status_code)
    

@api_view(['POST'])
def orders_add(request):
    data = request.data
    response = requests.post("http://127.0.0.1:8002/api/orders/", data=data)
    try:
        return Response(response.json(), status=response.status_code)
    except ValueError:
        return Response(response.text, status=response.status_code)
    

@api_view(['GET', 'DELETE', "PUT", "PATCH"])
def order_details(request, pk):
    if request.method == "GET":
        response = requests.get(f"http://127.0.0.1:8002/api/orders/{pk}/")
    elif request.method == "DELETE":
        response = requests.delete(f"http://127.0.0.1:8002/api/orders/{pk}/")
    elif request.method == "PUT":
        data = request.data
        response = requests.put(f"http://127.0.0.1:8002/api/orders/{pk}/", data=data)
    else:
        data = request.data
        response = requests.put(f"http://127.0.0.1:8002/api/orders/{pk}/", data=data)

    try:
        return Response(response.json(), status=response.status_code)
    except ValueError:
        return Response(response.text, status=response.status_code)
    

@api_view(['GET'])
def deliveries(request):
    response = requests.get("http://127.0.0.1:8006/api/deliver/")
    try:
        return Response(response.json(), status=response.status_code)
    except ValueError:
        return Response(response.text, status=response.status_code)
    


@api_view(['GET', "PUT"])
def delivery_details(request, pk):
    if request.method == "GET":
        response = requests.get(f"http://127.0.0.1:8006/api/update/{pk}/")
    elif request.method == "PUT":
        data = request.data
        response = requests.put(f"http://127.0.0.1:8006/api/update/{pk}/", data=data)

    try:
        return Response(response.json(), status=response.status_code)
    except ValueError:
        return Response(response.text, status=response.status_code)