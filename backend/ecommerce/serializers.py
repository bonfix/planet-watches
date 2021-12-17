from rest_framework import serializers

from ecommerce.models import Product
import logging;

logger = logging.getLogger(__name__)


class GenericSerializer(serializers.ModelSerializer):
    class Meta:
        model = None
        fields = '__all__'


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'image', 'price', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    name = serializers.CharField(max_length=255, required=False)
    price = serializers.DecimalField(max_digits=6, decimal_places=2, required=False)
    quantity = serializers.IntegerField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'quantity']

    def validate(self, data):
        # check if enough products in stock
        try:
            item_id = data.get('id', 0)
            product = Product.objects.get(pk=item_id)
        except:
            raise serializers.ValidationError(
                {'error_code': "ITEM_NOT_FOUND",
                 'error_message': f"Sorry, an ordered item was not found: Item ID - {item_id}"}
            )
        quantity_requested = data.get('quantity', 0)
        if product.quantity < quantity_requested:
            raise serializers.ValidationError(
                {'error_code': "INSUFFICIENT_STOCK",
                 'error_message': "Sorry, we do not have sufficient stock for the item: " + product.name}
            )
        # set the ordered quantity
        product.quantity = quantity_requested
        return product