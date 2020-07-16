from django.urls import path
from . import views

app_name = "selltour"
urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('details/<slug>.html', views.ItemDetailView.as_view(), name = 'detail'),
    path('order/<slug>', views.order.as_view(), name = 'information_order'),
    path('checkout/<slug>', views.order_tour, name = 'information_guess'),
    path('seach', views.seach, name='seach')
]