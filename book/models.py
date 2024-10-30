from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.


class Users(models.Model):
    full_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    password = models.CharField(max_length=20)

    def __str__(self):
        return self.email


class Book_categories(models.Model):
    category_name = models.CharField(max_length=30)

    def __str__(self):
        return self.category_name


class Books(models.Model):
    title = models.CharField(max_length=50)
    author = models.CharField(max_length=50)
    publisher = models.CharField(max_length=50)
    price = models.CharField(max_length=10)
    image = models.ImageField('image', upload_to="books/")
    category = models.ForeignKey(Book_categories, on_delete=models.CASCADE,
                                 related_name='book_category',)
    quantity = models.CharField(max_length=10)

    def __str__(self):
        return f"book {self.title} of price {self.price}"


class cartitems(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE,
                             related_name='user_cart')
    book = models.ForeignKey(Books, on_delete=models.CASCADE,
                             related_name='cart_book')
    quantity = models.PositiveBigIntegerField()


class order(models.Model):
    PLACED = "Placed"
    CONFIRMED = "Confirmed"
    TRANSMITTED = "Transmitted"
    DELIVERED = "Delivered"
    CANCELLED = "Cancelled"
    STATUS_CHOICES = [
        (PLACED, _("Placed")),
        (CONFIRMED, _("Confirmed")),
        (TRANSMITTED, _("Transmitted")),
        (DELIVERED, _("DELIVERED")),
        (CANCELLED, _("Cancelled"))
    ]
    user = models.ForeignKey(
        Users, on_delete=models.SET_NULL, related_name='order_user', null=True)
    address = models.TextField(null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)
    total_quantity = models.PositiveBigIntegerField(null=True, blank=True)
    total_price = models.PositiveBigIntegerField(null=True, blank=True)
    grand_total = models.PositiveBigIntegerField(null=True, blank=True)
    status = models.CharField(choices=STATUS_CHOICES,
                              default=PLACED, max_length=20)
    reason = models.TextField(blank=True, null=True)


class orderitems(models.Model):
    order = models.ForeignKey(order, on_delete=models.CASCADE,
                              related_name='order_order')
    book = models.ForeignKey(Books, models.CASCADE, related_name='order_book')
    quantity = models.PositiveBigIntegerField()
