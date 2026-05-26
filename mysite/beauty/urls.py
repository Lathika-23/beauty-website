from django.urls import path
from beauty import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('cart/', views.cart, name='cart'),
    path('product/',views.product,name='product'),
  
    #path('productdetails1/',views.productdetails1,name='productdetails1'),
    #path('productdetails2/',views.productdetails2,name='productdetails2'),
    #path('productdetails3/',views.productdetails3,name='productdetails3'),
    #path('productdetails4/',views.productdetails4,name='productdetails4'),
    #path('products/',views.home,name='products'),
    path('home/',views.home_view,name='home'),
    path('register/',views.register_view,name='register'),
    path('login/',views.login_user,name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('product-details/<int:pk>/', views.productdetails, name='productdetails'),
    path('category/<str:foo>', views.category, name='category'),
    path('search/', views.search, name='search'),
    path('cart1/',views.cart_summary, name="cart_summary"),
    path('add/',views.cart_add, name="cart_add"),
    path('delete/',views.cart_delete, name="cart_delete"),
    path('update/',views.cart_update, name="cart_update"), 
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('delight/', views.delight, name='delight'),
    path('order/',views.order,name='order'),
    path('checkout', views.checkout, name='checkout'),
] 

