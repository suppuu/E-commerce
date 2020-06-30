from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, DetailView, ListView
from .models import Item, Slider, Ad, Brand, Order, OrderItem, Contact, Category
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.utils import timezone


from rest_framework import viewsets
from home.serializers import UserSerializers, ItemSerializers
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.views import APIView
from rest_framework import generics
# Create your views here.


class BaseView(View):
    template_context = {
        "items": Item.objects.all()
    }


class HomeView(BaseView):
    def get(self, request):
        self.template_context["items"] = Item.objects.all()
        self.template_context["sliders"] = Slider.objects.all()
        self.template_context["ads"] = Ad.objects.all()
        self.template_context["brands"] = Brand.objects.all()
        self.template_context["categorys"] = Category.objects.all()
        self.template_context["item_sale"] = Item.objects.filter(labels="sale")
        self.template_context["item_hot"] = Item.objects.filter(labels="hot")
        return render(request, "shop-index.html", self.template_context)


class ItemDetailView(DetailView):
    model = Item
    template_name = "shop-item.html"


class Search(BaseView):
    def get(self, request):
        query = request.GET.get('query', None)
        if not query:
            return redirect("/")
        self.template_context['search_result'] = Item.objects.filter(
            title__icontains=query
        )
        self.template_context['search_query'] = query
        return render(request, 'shop-search-result.html', self.template_context)


def register(request):
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        password1 = request.POST["password1"]

        if password == password1:
            if User.objects.filter(username = username).exists():
                messages.error(request, "This UserName is already taken.")
                return render(request, "signup.html")
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, "This Email is already taken.")
                    return render(request, "signup.html")
                else:
                    user = User.objects.create_user(
                        first_name=first_name,
                        last_name=last_name,
                        username=username,
                        email=email,
                        password=password
                    )
                    user.save()
                    messages.success(request, "You are registered.")
                    return redirect("/accounts/login")
        else:
            messages.error(request, "Passwords doesnot match.")
            return redirect("home:signup")

    else:
        return render(request, "signup.html")


class OrderSummary(BaseView):
    def get(self, *arg, **kwargs):
        try:
            order = Order.objects.get(
                user=self.request.user,
                ordered=False

            )
            self.template_context["object"] = order
            return render(self.request, "shop-shopping-cart.html", self.template_context)

        except ObjectDoesNotExist:
            messages.error(self.request, "Some Error Occured.")
            return redirect("/")


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )[0]
    orders = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if orders.exists():
        order=orders[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity +=1
            order_item.save()
            messages.info(request, "The quantity is updated.")
            return redirect("home:orders")
        else:
            order.items.add(order_item)
            messages.info(request, "The item is updated in your cart.")
            return redirect("home:orders")
    else:
        order_date = timezone.now()
        order = Order.objects.create(
            user=request.user,
            order_date = order_date
        )
        order.items.add(order_item)
        messages.info(request, "Item is added")
        return redirect("home:orders")


def remove_single_item(request,slug):
    item = get_object_or_404(Item, slug=slug)
    orders = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if orders.exists():
        order = orders[0]
        if order.items.filter(item__slug=item.slug, ordered=False):
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()

    else:
        messages.info(request, "You don't have this item in your cart.")
        return redirect("home:orders")

    return redirect("home:orders")


def remove_all_item(request, slug):
    item = get_object_or_404(Item, slug=slug)
    orders = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if orders.exists():
        order = orders[0]
        if order.items.filter(item__slug=item.slug, ordered=False):
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            ).delete()
    else:
        messages.info(request, "You don't have removed this item from your cart.")
        return redirect("home:orders")

    return redirect("home:orders")


def contacts(request):
    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        message = request.POST["message"]

        contact = Contact(
            name=name,
            email=email,
            message=message,
            phone=phone
        )
        contact.save()
        messages.success(request, "Submitted")
        return redirect('home:contact-us')

    else:
        return render(request, "shop-contacts.html")


# for API development
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializers


class ItemFilterListView(generics.ListAPIView):
    serializer_class = ItemSerializers
    queryset = Item.objects.all()
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filter_fields = ('title', 'price', 'id', 'status', 'labels')
    ordering_fields = ('title', 'price', 'id')
    ordering = ('title', )
    search_fields = ('title', 'description', 'slug')


def category_list(request, *args, **kwargs):
    title = kwargs.get('title')
    name = get_object_or_404(Category.objects.all(), title=title)
    return render(request, 'categorylist.html', {'category': name})


'''def categorys(request):
    categorys = Category.objects.filter'''

def base(request):
    return render(request, 'base.html')

