
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework import routers

from . import views
from .yasg import urlpatterns as doc_urls


router = routers.SimpleRouter()
router.register(r'product', views.ProductsViewSet)
router.register(r'wishlist', views.WishlistsViewSet)


# app_name = 'commerce'
urlpatterns = [
    path('', views.home, name="home"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("products", views.products, name="products"),
    path("wishlists", views.WishlistView.as_view(), name="wishlists"),

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

]

urlpatterns += router.urls
urlpatterns += doc_urls

