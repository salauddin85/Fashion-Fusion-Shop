    


from rest_framework.decorators import action
from decimal import Decimal
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from .models import PurchaseModel,PurchaseCartModel
from Purchase.serialaizers  import PurchaseSerializer,PurchaseProductSerialaizer
from cloth_product.models import Product
from auth_app.models import Account
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from rest_framework.exceptions import PermissionDenied


class PurchaseProductView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, id):
        print(id)
        if not id:
            return Response({'error': "No product id found"}, status=status.HTTP_400_BAD_REQUEST)

        product = get_object_or_404(Product, id=id)
        try:
            requested_user = Account.objects.get(user=request.user)
        except Account.DoesNotExist:
            return Response({'error': "No Account Match"}, status=status.HTTP_400_BAD_REQUEST)

        # Debugging: Print user and product details
        print(f"Request User: {request.user}")
        print(f"Requested User: {requested_user}")
        print(f"Product: {product}")

        # Check if user is authenticated
        if not request.user.is_authenticated:
            raise PermissionDenied("User is not authenticated")

        if requested_user.balance >= product.price and product.quantity > 0:
            requested_user.balance -= product.price
            product.quantity -= 1
            requested_user.save()
            product.save()

            # Email Part
            email_subject = "Purchase Confirmation"
            email_body = render_to_string("purchase_email.html", {
                'user': request.user,
                'price': product.price,
                'product': product,
                'balance': requested_user.balance
            })
            email = EmailMultiAlternatives(email_subject, '', to=[request.user.email])
            email.attach_alternative(email_body, 'text/html')
            email.send()

            # Create purchase record
            PurchaseModel.objects.create(
                user=request.user,
                product=product,
            )
            return Response({'success': "Purchase completed successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({'error': "Insufficient balance or product quantity"}, status=status.HTTP_400_BAD_REQUEST)





class PurchaseCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request,price):
        
        try:
            requested_user = Account.objects.get(user=request.user)
        except Account.DoesNotExist:
            return Response({'error': "No Account Match"}, status=status.HTTP_400_BAD_REQUEST)

       
        print(f"Requested User: {requested_user}")
       

        # Check if user is authenticated
        if not request.user.is_authenticated:
            raise PermissionDenied("User is not authenticated")
        price = Decimal(price)

        if requested_user.balance >= price:
            requested_user.balance-=price
            requested_user.save()
            

            # Email Part
            email_subject = "Purchase Confirmation"
            email_body = render_to_string("cartpurchase_email.html", {
                'user': request.user,
                'balance': requested_user.balance
            })
            email = EmailMultiAlternatives(email_subject, '', to=[request.user.email])
            email.attach_alternative(email_body, 'text/html')
            email.send()

            # Create purchase record
            PurchaseCartModel.objects.create(
                user=request.user,
                

            )
            return Response({'success': "Purchase completed successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({'error': "Insufficient balance or product quantity"}, status=status.HTTP_400_BAD_REQUEST)





class PurchaseProductallView(viewsets.ModelViewSet):
    queryset = PurchaseModel.objects.all()
    serializer_class =PurchaseProductSerialaizer
