from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from pos_api.serializers import ProductSerializer
from app_pos.models import Product
# from rest_framework.decorators import api_view

# Create your views here.
# @api_view(['GET'])
# def product_list(request):
#     data = Product.objects.all()
# we will use class based views
class ProductListCreateApiView(APIView):
    def get(self, request):
        try:
            data = Product.objects.all()
            serialized = ProductSerializer(data, many=True)
            context = {
                "status": status.HTTP_200_OK,
                "message": "Product List",
                "data": serialized.data
            }
            return Response(context, status=status.HTTP_200_OK)
        except:
            return Response({"message": "No data"}, status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request):
        try:
            data = request.data
            serialized = ProductSerializer(data=data)
            if serialized.is_valid():
                serialized.save()
                context = {
                    "status": status.HTTP_201_CREATED,
                    "message": "Product Created Successfully",
                    "data": serialized.data
                }
                return Response(context, status=status.HTTP_201_CREATED)
            else:
                context = {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "Something went wrong",
                    "data": serialized.errors
                }
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
        except:
            context = {
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Something went wrong"
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

class ProductDetailUpdateDeleteApiView(APIView):
    def get_object(self, request, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({"message": "Not found"}, status=status.HTTP_404_NOT_FOUND)
    
    def get(self, request, pk):
        instance = self.get_object(request, pk)
        serialized = ProductSerializer(instance)
        context = {
            "status": status.HTTP_200_OK,
            "message": "Product detail",
            "data": serialized.data
        }
        return Response(context, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        try:
            data = request.data # json request data
            instance = self.get_object(request, pk) # database's data
            serialized = ProductSerializer(instance=instance, data=data)
            if serialized.is_valid():
                serialized.save()
                context = {
                    "status": status.HTTP_201_CREATED,
                    "message": "Product Updated Successfully",
                    "data": serialized.data
                }
                return Response(context, status=status.HTTP_201_CREATED)
            else:
                context = {
                    "status": status.HTTP_400_BAD_REQUEST,
                    "message": "Something went wrong",
                    "data": serialized.errors
                }
                return Response(context, status=status.HTTP_400_BAD_REQUEST)
        except:
            context = {
                "status": status.HTTP_400_BAD_REQUEST,
                "message": "Something went wrong"
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk):
        instance = self.get_object(request, pk)
        instance.delete()
        context = {
            "status": status.HTTP_200_OK,
            "message": "Product deleted successfully"
        }
        return Response(context, status=status.HTTP_200_OK)