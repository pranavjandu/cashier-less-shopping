"""shopping URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.mainpage, name="loginpage"),
    path('homepage', views.dashboard, name="customerhomepage"),
    path('logout', views.logoutuser, name='logout'),
    path('scanner', views.scanner, name='scanner'),
    path('cart', views.cart, name="cart"),
    path('addtocart', views.addtocart),
    path('checkout',views.checkout, name="checkout"),

    path('guard/login', views.loginGuard, name="guardlogin"),
    path('guard/scanner', views.scanGuard, name="guardHome"),
    path('guard/verify', views.verifyGuard, name="verifyGuard"),
    path('guard/details', views.getdetailsGuard, name="getdetailsGuard"),
    path('guard/logout', views.logoutGuard, name="logoutGuard"),
    path('guard/raiseissue', views.raiseIssue, name="raiseIssue"),
    path('guard/verified', views.verified, name="verified"),
]
urlpatterns += static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT)
