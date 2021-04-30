from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("",views.index, name="index"),
    path("reg",views.reg, name="reg"),
    path("login",views.login, name="login"),
    path("contact",views.contact, name="contact"),
    path("logout",views.logout, name="logout"),
    path("customize",views.customize, name="customize"),
    path("category",views.category, name="category"),
    path("aboutus",views.aboutus, name="aboutus"),
    path("checkout",views.checkout, name="checkout"),
    path("p",views.p, name="p"),
    path("cart",views.cart, name="cart"),
    path("update_item/",views.updateItem, name="update_item"),
    path("reset_password/", auth_views.PasswordResetView.as_view(template_name="password_reset.html"), name="reset_password"),

    path("reset_password_sent/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),

    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),

    path("reset_password_complete/", auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_done.html"), name="password_reset_complete"), 
    path("payment/success/",views.success, name="success"),
    path("payment/",views.payment, name="payment"),

   
    


    
   
   
    ]
