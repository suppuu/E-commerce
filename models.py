from django.db import models
from django.conf import settings
from django.shortcuts import reverse

# Create your models here.
STATUS = (("In Stock", "In Stock"), ("Out of Stock", "Out of Stock"))
LABELS = (("sale", "sale"), ("new", "new"), ("hot", "hot"), ("", "default"))
ACTIVE = (("active", "active"), (" ", "default"))


class Category(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("home:products", kwargs={"slug": self.title})


class Item(models.Model):
    title = models.CharField(max_length=200)
    price = models.IntegerField()
    discounted_price = models.IntegerField()
    description = models.TextField(max_length=200)
    image = models.ImageField(upload_to="images")
    slug = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, default=0)
    status = models.CharField(choices=STATUS, max_length=20)
    labels = models.CharField(choices=LABELS, max_length=20)

    def __str__(self):
        return self.title     # shows the title name instead of Item Object(1)

    def get_absolute_url(self):
        return reverse("home:products", kwargs={"slug": self.slug})

    def get_add_to_cart(self):
        return reverse("home:add-to-cart", kwargs={"slug": self.slug})

    def get_remove_single_item(self):
        return reverse("home:remove-single-item", kwargs={"slug": self.slug})

    def get_remove_all_item(self):
        return reverse("home:remove-all-item", kwargs={"slug": self.slug})


class Brand(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=200)
    image = models.ImageField(upload_to='brands')

    def __str__(self):
        return self.title


class Ad(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="ads")
    rank = models.IntegerField()
    status = models.CharField(choices=ACTIVE, max_length=20)
    description = models.TextField()

    def __str__(self):
        return self.title


class Slider(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='sliders')
    rank = models.IntegerField()
    status = models.CharField(choices=ACTIVE, max_length=20)
    description = models.TextField()

    def __str__(self):
        return self.title


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return self.item.title

    def get_total_price(self):
        return self.quantity * self.item.price

    def get_total_discounted_price(self):
        return self.quantity * self.item.discounted_price

    def get_total_sum_price(self):
        if self.item.discounted_price:
            return self.get_total_discounted_price()
        else:
            return self.get_total_price()


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    ordered = models.BooleanField(default=False)
    order_date = models.DateTimeField()

    def __str__(self):
        return self.user.username

    def get_total_amount(self):
        total_price = 0
        for orders in self.items.all():
            total_price += orders.get_total_sum_price()
        return total_price

    def total_amount_after_adding_shipping_cost(self):
        all_total = self.get_total_amount()+100
        return all_total


class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=100)
    message = models.TextField()
    phone = models.CharField(max_length=50)

    def __str__(self):
        return self.name





























