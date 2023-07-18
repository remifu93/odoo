from rest_framework import serializers
from .models import Customer, OrderProduct, OrderLine, Order


class CustomerSerializer(serializers.ModelSerializer):
    """ Serializador para comprador """
    class Meta:
        model = Customer
        fields = '__all__'


class OrderProductSerializer(serializers.ModelSerializer):
    """ Serializador de un producto de la orden """
    class Meta:
        model = OrderProduct
        fields = '__all__'


class OrderLineSerializer(serializers.ModelSerializer):
    """ Serializador para linea o producto de una orden"""
    orderProduct = OrderProductSerializer()

    class Meta:
        model = OrderLine
        fields = ['orderProduct', 'quantity', 'unitPrice']


class OrderSerializer(serializers.ModelSerializer):
    """ Serializador para Pedidos """
    customer = CustomerSerializer()
    orderLines = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id', 'customer', 'orderLines', 'fiscal_position']

    def get_orderLines(self, obj):
        queryset = obj.order_lines.all()
        return OrderLineSerializer(queryset, many=True).data


class OrderCreateSerializer(serializers.Serializer):
    """ Serializador para Crear Pedidos """

    customer = CustomerSerializer()
    orderLines = OrderLineSerializer(many=True)
    fiscal_position = serializers.CharField()

