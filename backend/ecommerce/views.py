from django.shortcuts import render
from django.template.loader import render_to_string
from rest_framework import viewsets, generics, permissions, status
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response

from bonfix_utils.utils import util_send_email
from ecommerce import apps
from ecommerce.models import Product, Order, OrderProducts
from ecommerce.serializers import GenericSerializer, ProductsSerializer, OrderSerializer


class GeneralViewSet(viewsets.ModelViewSet):
    @property
    def model(self):
        self.kwargs.setdefault('app_label', "backend")
        app_label = str(self.kwargs['app_label'])
        return apps.get_model(app_label=app_label, model_name=str(self.kwargs['model_name']))

    def get_queryset(self):
        # model = self.kwargs.get('model')
        model = self.model
        return model.objects.all()

    def get_serializer_class(self):
        # GenericSerializer.Meta.model = self.kwargs.get('model')
        GenericSerializer.Meta.model = self.model
        return GenericSerializer


class ProductsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows products to be viewed
    """
    permission_classes = [permissions.AllowAny]
    queryset = Product.objects.all()
    serializer_class = ProductsSerializer


class OrderViewSet(RetrieveAPIView):
    """
    API endpoint that allows products to be ordered
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        # create an order
        order = Order.objects.create(user=request.user, cost=0)
        for product in serializer.validated_data:
            # add order items
            OrderProducts.objects.create(product=product, order=order,
                                         price=product.price, quantity=product.quantity)
            order.cost += product.price
        # save the value of the cost
        order.save()
        self.mail_order(order, serializer.validated_data, request.user)

        status_code = status.HTTP_200_OK

        return Response({"message": f"Order #{order.id} successful, check your email for the details."},
                        status=status_code)

    def mail_order(self, order: Order, products: Product, user):
        # create msg
        name = user.email.split('@')[0]
        plain_message = render_to_string('order_email_template_plain.html', {
            'user': user,
            'name': name,
            'products': products,
            'products': products,
            'order': order
        })
        html_message = render_to_string('order_email_template.html', {
            'user': user,
            'name': name,
            'products': products,
            'products': products,
            'order': order
        })
        subject = "Planet Watches Order"
        util_send_email(subject, [user.email], plain_message, html_message)
