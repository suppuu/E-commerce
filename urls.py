from django.urls import path, include
from . import views
from .views import (
    HomeView, ItemDetailView, Search, register, OrderSummary, add_to_cart, remove_single_item, remove_all_item, contacts
)


app_name = "home"
urlpatterns = [
    path("", HomeView.as_view(), name="homepage"),
    path("products/<slug>", ItemDetailView.as_view(), name="products"),
    path("search/", Search.as_view(), name="search"),
    path("signup/", register, name="signup"),
    path("orders/", OrderSummary.as_view(), name="orders"),
    path("add-to-cart/<slug>/", add_to_cart, name="add-to-cart"),
    path("remove-single-item/<slug>/", remove_single_item, name="remove-single-item"),
    path("remove-all-item/<slug>/", remove_all_item, name="remove-all-item"),
    path("contact-us/", contacts, name="contact-us"),
    path("api/", include('home.api_urls')),
    path('category/<str:title>/', views.category_list, name='category'),
    path('base/', views.base)
]