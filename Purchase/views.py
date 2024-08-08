

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from .models import PurchaseModel
from .serialaizers import PurchaseSerializer
from cloth_product.models import Product
from auth_app.models import Account
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework.views import APIView

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


class PurchaseProductView(APIView):
    
    permission_classes = [IsAuthenticated]


    # PURCHASE PART:
    #jokon akjon user purchase korbe thokon akta post request asbe purchase ar jonno ajonno amra custom action use korlam amader moto  details false mane ata akta list action jeta kunu specific item ar jonno noy.
    def post(self, request,id):
        print("product",id)
        if not id:
            return Response({'error': "No product id found"}, status=status.HTTP_400_BAD_REQUEST)
  
        product = get_object_or_404(Product, id=id)
        print(product)

        try:
            requested_user = Account.objects.get(user=request.user)
        except Account.DoesNotExist:
            return Response({'error': "No Account Match"}, status=status.HTTP_400_BAD_REQUEST)

        print(requested_user.balance)
        if requested_user.balance >= product.price and product.quantity > 0:
            print(requested_user.balance)
            requested_user.balance -= product.price
            product.quantity -= 1
            print(product.quantity)
            requested_user.save()
            product.save()

            # EMAIL PART:

            email_subject = "Purchase Confirmations"
            email_body = render_to_string("purchase_email.html",{
                'user':request.user,
                'price':product.price,
                'product':product,
                'balance':requested_user.balance
            })
            email = EmailMultiAlternatives(email_subject,'',to = [request.user.email])
            email.attach_alternative(email_body,'text/html')
            email.send()

            
            # Create purchase record
            PurchaseModel.objects.create(
                user=request.user,
                product=product,
            )
            return Response({'success': "Purchase completed successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({'error': "Insufficient balance or product quantity"}, status=status.HTTP_400_BAD_REQUEST)