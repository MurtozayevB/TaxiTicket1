
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Station, Region, Route, Car, CarModel, Order
from .serializers import StationModelSerializer, RegionModelSerializer, RouteModelSerializer, \
    CarModelSerializer, RouteDeleteModelSerializer, CarModelModelSerializer, OrderSerializer


@extend_schema(tags=['station'], request=StationModelSerializer)
class RegionFilterListView(ListAPIView):
    serializer_class = StationModelSerializer
    def get_queryset(self):
        region_id = self.kwargs['pk']
        return Station.objects.filter(region_id=region_id)


@extend_schema(tags=['station'])
class StationListView(ListAPIView):
    queryset = Station.objects.all()
    serializer_class = StationModelSerializer

@extend_schema(tags=['station'], request=StationModelSerializer)
class StationFilterApiVew(RetrieveAPIView):
    queryset = Station.objects.all()
    serializer_class = StationModelSerializer
    lookup_field = 'pk'


@extend_schema(tags=['region'], request=RegionModelSerializer)
class RegionListAiView(ListAPIView):
    serializer_class = RegionModelSerializer
    queryset = Region.objects.all()

# ===============================================Route===========
@extend_schema(tags=['route'], request=RouteModelSerializer,responses=RouteModelSerializer)
class RouteCreateView(CreateAPIView):
    queryset = Route.objects.all()
    serializer_class = RouteModelSerializer


@extend_schema(tags=['route'], request=RouteModelSerializer,responses=RouteModelSerializer)
class ActiveRoutesByRegionView(ListAPIView):
    serializer_class = RouteModelSerializer

    def get_queryset(self):
        region_id = self.kwargs.get('pk')
        return Route.objects.filter(finish_location__region_id=region_id, status='in_progress')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


@extend_schema(tags=['route'], request=RouteModelSerializer,responses=RouteModelSerializer)
class RouteByAPIView(ListAPIView):
    serializer_class = RouteModelSerializer
    def get_queryset(self):
        rout_id = self.kwargs.get('pk')
        return Route.objects.filter(id=rout_id)

@extend_schema(
    tags=['route'],
    parameters=[
        OpenApiParameter(name='departure_at', description='Departure date and time (YYYY-MM-DD HH:MM:SS)', required=False, type=str),
        OpenApiParameter(name='start_station', description='Starting station name', required=False, type=str),
        OpenApiParameter(name='finish_station', description='Finishing station name', required=False, type=str),
        OpenApiParameter(name='initial_price', description='Minimum ticket price', required=False, type=float),
        OpenApiParameter(name='last_price', description='Maximum ticket price', required=False, type=float),
        OpenApiParameter(name='car_model', description='Car model used for the route', required=False, type=str),
    ]
)
@api_view(['GET'])
def get_routes_filter(request):
    departure_at=request.query_params.get('departure_at')
    start_station=request.query_params.get('start_station')
    finish_station=request.query_params.get('finish_station')
    initial_price=request.query_params.get('initial_price')
    last_price=request.query_params.get('last_price')
    car_model=request.query_params.get('car_model')


    routes=Route.objects.all()

    if departure_at:
        routes=routes.filter(departure_at=departure_at)

    elif start_station:
        routes=routes.filter(start_location_id=start_station)
    elif finish_station:
        routes=routes.filter(finish_location_id=finish_station)

    elif initial_price:
        routes=routes.filter(price__gte=int(initial_price))
    elif last_price:
        routes=routes.filter(price__lte=int(last_price))
    elif car_model:
        routes=routes.filter(car__car_model_id=car_model)

    serializer=RouteModelSerializer(instance=routes,many=True)
    return Response(serializer.data,status=HTTP_200_OK)


@extend_schema(tags=['route'], request=RouteDeleteModelSerializer,responses=RouteDeleteModelSerializer)
class RouteDeleteAPIView(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RouteDeleteModelSerializer
    queryset = Route.objects.all()
    lookup_field = 'pk'

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        self.perform_destroy(instance)
        return Response(serializer.data, status=HTTP_200_OK)

# ========================Car========================================

@extend_schema(tags=['car'])
class CarListView(ListAPIView):
    queryset = Car.objects.all()
    serializer_class = CarModelSerializer


@extend_schema(tags=['car'], request=CarModelSerializer)
class CarSeatFilterListView(ListAPIView):
    serializer_class = CarModelSerializer
    def get_queryset(self):
        id = self.kwargs['pk']
        return Car.objects.filter(seats_count=id)

@extend_schema(tags=['car'], request=CarModelSerializer)
class CarModelIdFilterListView(RetrieveAPIView):
    serializer_class = CarModelSerializer
    queryset = Car.objects.all()
    lookup_field = 'pk'


@extend_schema(tags=['model'])
class CarModelListView(ListAPIView):
    queryset = CarModel.objects.all()
    serializer_class = CarModelModelSerializer


@extend_schema(tags=['order'],request=OrderSerializer,responses=OrderSerializer)
class CreateOrderViewSet(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

@extend_schema(tags=['order'])
class OrderListView(ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer



@extend_schema(tags=['order'], request=OrderSerializer)
class OrderFilterApiView(ListAPIView):
    serializer_class = OrderSerializer
    def get_queryset(self):
        id = self.kwargs['pk']
        return Order.objects.filter(id=id)


@extend_schema(
    tags=['order'],
    parameters=[
        OpenApiParameter(name='departure_at', description='Departure date and time (YYYY-MM-DD HH:MM:SS)', required=False, type=str),
        OpenApiParameter(name='status', description='Starting station name', required=False, type=str),
    ],
    request = OrderSerializer,
    responses=OrderSerializer
)
@api_view(['GET'])
def get_order_filter(request):
    departure_at=request.query_params.get('departure_at')
    status=request.query_params.get('status')


    orders=Order.objects.all()

    if departure_at:
        orders=orders.filter(orders__ordered_at=departure_at)

    elif status:
        orders=orders.filter(orders__status=status)
    serializer = OrderSerializer(instance=orders, many=True)
    return Response(serializer.data, status=HTTP_200_OK)


