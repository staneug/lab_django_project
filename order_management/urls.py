from django.urls import path, include
from . import views
from .views import logout_view
from rest_framework.routers import DefaultRouter
from .views import intermediate_save_order

router = DefaultRouter()
router.register(r'orders', views.OrderViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('ajax/load-clinics/', views.load_clinics, name='ajax_load_clinics'),
    path('ajax/load-options/', views.load_options, name='ajax_load_options'),
    path('order/int:pk/intermediate-save/', intermediate_save_order, name='intermediate_save_order'),
    path('logout/', logout_view, name='logout'),
]
