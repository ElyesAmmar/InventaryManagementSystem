from django.shortcuts import render, get_list_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import Product
from .serializers import ProductSerializer
from django.core.paginator import Paginator,EmptyPage



@api_view(['GET', 'POST'])
def products(request):
    if request.method == 'GET':
        # products = Product.objects.all()
        products = Product.objects.select_related('category').all()
        category_name = request.query_params.get('category')
        to_price = request.query_params.get('to-price')
        search = request.query_params.get('search')
        ordering = request.query_params.get('ordering')
        perpage = request.query_params.get('perpage', default=5)
        page = request.query_params.get('page', default=1)
        if category_name:
            products = products.filter(category__name=category_name)
        if to_price:
            products = products.filter(price__lte=to_price)
        if search:
            products = products.filter(name__icontains=search)
        if ordering:
            ordering_fields = ordering.split(',')
            products = products.order_by(*ordering_fields)
        paginator = Paginator(products, per_page=perpage)
        try:
            products = paginator.page(number=page)
        except EmptyPage:
            products = []
        serialized_product = ProductSerializer(products, many=True)
        return Response(serialized_product.data)
    if request.method == 'POST':
        serialized_product = ProductSerializer(data= request.data)
        serialized_product.is_valid(raise_exception=True)
        serialized_product.save()
        return Response(serialized_product.data, status= status.HTTP_201_CREATED)

@api_view(['GET', 'PUT', 'DELETE'])
def single_product(request, id):
    # product = get_list_or_404(Product, pk=id)
    try:
        product = Product.objects.get(pk=id)
        if request.method == 'DELETE':
            product.delete()
            return Response({'msg':'deleting product success'}, status= status.HTTP_200_OK)
        
        serialized_product = ProductSerializer(product)
        if request.method == 'GET':
            return Response(serialized_product.data, status= status.HTTP_200_OK)
        if request.method == 'PUT':
            serializer = ProductSerializer(product, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status= status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response('product not found', status= status.HTTP_404_NOT_FOUND)
