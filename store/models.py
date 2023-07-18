from django.db import models


class Customer(models.Model):
    """ Modelo para gestionar Compradores """
    additionalStreet = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255)
    companyName = models.CharField(max_length=255)
    country = models.CharField(max_length=2)
    customerType = models.CharField(max_length=255)
    email = models.EmailField()
    mobilePhone = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    postalCode = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    NIF = models.CharField(max_length=9)

    def __str__(self):
        return self.companyName


class OrderProduct(models.Model):
    """ Modelo para gestionar productos """
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=255)
    type = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Order(models.Model):
    """ Modelo para gestionar una orden """
    STATUS_CHOICES = [
        ('PRESUPUESTO', 'Presupuesto'),
        ('CONFIRMADO', 'Confirmado'),
        ('CANCELADO', 'Cancelado'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    fiscal_position = models.CharField(max_length=255)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='PRESUPUESTO')

    def __str__(self):
        return f"Pedido {self.id}"


class OrderLine(models.Model):
    """ Modelo para gestionar Productos de una Orden """
    order = models.ForeignKey(Order, related_name='order_lines', on_delete=models.CASCADE)
    orderProduct = models.ForeignKey(OrderProduct, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unitPrice = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.orderProduct.name} - {self.quantity}"
