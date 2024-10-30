from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.loginpage, name='loginpage'),
    path('loginpage', views.loginpage, name='loginpage'),
    path('index', views.index, name='index'),
    path('forgotpasswordpage/', views.forgot_password_page,
         name='forgotpasswordpage'),
    path('homepage/', views.homepage, name='homepage'),
    path('orderpage/', views.orderpage, name='orderpage'),
    path('trackorderpage/', views.trackorderpage, name='trackorderpage'),
    path('profile/', views.profile, name='profile'),
    path('signuppage/', views.signuppage, name='signuppage'),
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('setpasswordpage', views.setpasswordpage, name='setpasswordpage'),
    path('confirm_email', views.confirm_email, name='confirm_email'),
    path('setpassword', views.setpassword, name='setpassword'),
    path('cartpage', views.cartpage, name='cartpage'),
    path('update_profile', views.update_profile, name='update_profile'),
    path('orderhistorypage', views.orderhistorypage, name='orderhistorypage'),
    path('add_to_cart', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart', views.remove_from_cart, name='remove_from_cart'),
    path('plus_cart', views.plus_cart, name='plus_cart'),
    path('minus_cart', views.minus_cart, name='minus_cart'),
    path('category_filter', views.category_filter, name='category_filter'),
    path('placeorder', views.placeorder, name='placeorder')
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
