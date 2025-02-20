from django.urls import path

from . import views
from .views import StationListView, RegionFilterListView, StationFilterApiVew, RegionListAiView, RouteCreateView, \
    ActiveRoutesByRegionView, RouteByAPIView, CarListView, RouteDeleteAPIView, CarModelIdFilterListView, \
    CarSeatFilterListView, CarModelListView, CreateOrderViewSet, OrderListView, OrderFilterApiView

urlpatterns = [
    path('api/v1/station/<int:pk>/', StationFilterApiVew.as_view(), name='station-list'),
    path('api/v1/station/region/<int:pk>/', RegionFilterListView.as_view(), name='region-list'),
    path('api/v1/station', StationListView.as_view(), name='station-list'),
    path('api/v1/region', RegionListAiView.as_view(), name='region-list'),
]


urlpatterns +=[
    path('api/v1/routes', RouteCreateView.as_view(), name='Route-filter'),
    path('api/v1/routes/region/<int:pk>', ActiveRoutesByRegionView.as_view(), name='Route-filter'),
    path('api/v1/routes/<int:pk>', RouteByAPIView.as_view(), name='Route-filter'),
    path('api/v1/routes/delite/<int:pk>', RouteDeleteAPIView.as_view(), name='Route-filter'),
    path('api/v1/routes/filter', views.get_routes_filter, name='Route-filter'),
]

urlpatterns += [
    path('api/v1/car', CarListView.as_view(), name='station-list'),
    path('api/v1/car/seat/<int:pk>', CarSeatFilterListView.as_view(), name='station-list'),
    path('api/v1/car/model/<int:pk>', CarModelIdFilterListView.as_view(), name='station-list'),

]

urlpatterns +=[
    path('api/v1/car/model', CarModelListView.as_view(), name='station-list'),
    path('api/v1/order/create', CreateOrderViewSet.as_view(), name='station-list'),
    path('api/v1/order', OrderListView.as_view(), name='station-list'),
    path('api/v1/order/<int:pk>', OrderFilterApiView.as_view(), name='station-list'),
    path('api/v1/order/filter', views.get_order_filter, name='Route-filter'),

]

# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from .views import OrderViewSet
#
# router = DefaultRouter()
# router.register(r'orders', OrderViewSet, basename='order')
#
# urlpatterns = [
#     path('api/v1/', include(router.urls)),
# ]