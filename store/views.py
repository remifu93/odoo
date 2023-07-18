from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import OrderSerializer, OrderCreateSerializer
from .models import Customer, OrderProduct, OrderLine, Order


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.all()

    def create(self, request):
        serializer = OrderCreateSerializer(data=request.data)
        # verifica si los datos del json estan bien si no devuelve un error
        serializer.is_valid(raise_exception=True)

        # Obtengo los datos del pedido ya validados previamente
        order_data = serializer.validated_data

        # Crea o actualiza el cliente si no se desea actualizar los datos podria utilizar create en lugar de update_or_create
        customer_data = order_data['customer']
        customer, _ = Customer.objects.update_or_create(
            companyName=customer_data['companyName'],
            defaults=customer_data
        )

        # Crea el pedido
        order = Order.objects.create(
            customer=customer,
            fiscal_position=order_data['fiscal_position']
        )

        # Inserta las lienas del pedido
        for order_line_data in order_data['orderLines']:
            order_product_data = order_line_data['orderProduct']

            order_product, _ = OrderProduct.objects.update_or_create(
                sku=order_product_data['sku'],
                defaults=order_product_data
            )

            OrderLine.objects.create(
                order=order,
                orderProduct=order_product,
                quantity=order_line_data['quantity'],
                unitPrice=order_line_data['unitPrice'],
            ).save()

        return Response(OrderSerializer(order).data, status=201)


