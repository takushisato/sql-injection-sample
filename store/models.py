from django.conf import settings
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="products"
    )
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


class Address(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="addresses",
    )
    full_name = models.CharField(max_length=120)
    postal_code = models.CharField(max_length=16)
    prefecture = models.CharField(max_length=64)
    city = models.CharField(max_length=120)
    address_line = models.CharField(max_length=200)
    phone = models.CharField(max_length=32, blank=True)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} / {self.postal_code}"


class Cart(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cart",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart({self.user})"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("cart", "product")

    def __str__(self):
        return f"{self.product} x {self.quantity}"


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        PAID = "paid", "Paid"
        SHIPPED = "shipped", "Shipped"
        DELIVERED = "delivered", "Delivered"
        CANCELLED = "cancelled", "Cancelled"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="orders",
    )
    shipping_address = models.ForeignKey(
        Address, on_delete=models.PROTECT, related_name="orders"
    )
    status = models.CharField(
        max_length=16, choices=Status.choices, default=Status.PENDING
    )
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order#{self.pk} ({self.user})"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    product_name = models.CharField(max_length=200)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product_name} x {self.quantity}"

    @property
    def subtotal(self):
        return self.unit_price * self.quantity


class Review(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("product", "user")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.product} ({self.rating})"
