from django.urls import path, include
from . import views
urlpatterns = [
    path("base/", views.home, name="home"),
    path("crud/", views.crud, name="crud"),
    # path("cart/", views.cart, name="cart"),
    path("payments/", views.payments, name="payments"),
    path("products/", views.products, name="products"),
    path("add_p/", views.add_p, name="add_p"),
    path("view_details/<int:id>/", views.view_details, name="view_details"),
    path("edit_p/<int:product_id>/", views.edit_p, name="edit_p"),
    path("delete_p/<int:id>/", views.delete_p, name="delete_p"),
    path("signin/", views.signin, name="signin"),
    path("signup/", views.signup, name="signup"),
    path('cart_detail/', views.cart_detail, name='cart_detail'),
    path('cart/update/<int:product_id>/', views.update_cart, name='update_cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),


]