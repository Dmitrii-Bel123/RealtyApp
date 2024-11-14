from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator

from rest_framework import serializers
from rest_framework.exceptions import NotFound
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from .models import Advert

class ApiAdvertSerializer(serializers.Serializer):
    fio = serializers.CharField()
    phone = serializers.CharField()
    type = serializers.CharField()
    district = serializers.CharField()
    address = serializers.CharField()
    rooms = serializers.IntegerField()
    apart_area = serializers.IntegerField()
    floor = serializers.IntegerField()
    floors = serializers.IntegerField()
    description = serializers.CharField()
    price = serializers.FloatField()
    create_time = serializers.DateTimeField()


class ApiAdvertsListSerializer(serializers.Serializer):
    adverts = serializers.ListField(child=ApiAdvertSerializer())
    total_pages = serializers.IntegerField()
    page = serializers.IntegerField()


class ApiValidationSerializer(serializers.Serializer):
    detail = serializers.DictField()


@extend_schema(
    summary="Возращает список объявлений по заданным параметрам",
    description="Возращает список объявлений по заданным параметрам",
    parameters=[
        OpenApiParameter(name="type", type=OpenApiTypes.INT, location=OpenApiParameter.QUERY, required=False, description="Тип объекта"),
        OpenApiParameter(name="district", type=OpenApiTypes.INT, location=OpenApiParameter.QUERY, required=False, description="Район"),
        OpenApiParameter(name="rooms", type={'type': 'array', 'items': {'type': 'number'}}, required=False, location=OpenApiParameter.QUERY, description="кол-во комнат: [1,2,3,4,5]"),
        OpenApiParameter(name="apart_area_from", type=OpenApiTypes.INT, location=OpenApiParameter.QUERY, required=False, description="Площадь от"),
        OpenApiParameter(name="apart_area_to", type=OpenApiTypes.INT, location=OpenApiParameter.QUERY, required=False, description="Площадь до"),
        OpenApiParameter(name="floors_from", type=OpenApiTypes.INT, location=OpenApiParameter.QUERY, required=False, description="Этаж от"),
        OpenApiParameter(name="floors_to", type=OpenApiTypes.INT, location=OpenApiParameter.QUERY, required=False, description="Этаж до"),
        OpenApiParameter(name="price_from", type=OpenApiTypes.FLOAT, location=OpenApiParameter.QUERY, required=False, description="Цена от"),
        OpenApiParameter(name="price_to", type=OpenApiTypes.FLOAT, location=OpenApiParameter.QUERY, required=False, description="Цена до"),
        OpenApiParameter(name="page", type=OpenApiTypes.INT, location=OpenApiParameter.QUERY, required=False, default=1, description="Номер страницы"),
    ],
    responses={
        status.HTTP_200_OK: ApiAdvertsListSerializer,
        status.HTTP_404_NOT_FOUND: ApiValidationSerializer,
    },
)
@api_view(['GET'])
def adverts(request):
    query = Advert.objects.select_related('owner', 'object').order_by('-create_time')
    if request.query_params.get('type'):
        query = query.filter(object__type=request.query_params.get('type'))
    if request.query_params.get('district'):
        query = query.filter(object__district=request.query_params.get('district'))
    if request.query_params.get('rooms'):
        query = query.filter(object__rooms__in=request.query_params.get('rooms'))
    if request.query_params.get('apart_area_from'):
        query = query.filter(object__apart_area__gte=request.query_params.get('apart_area_from'))
    if request.query_params.get('apart_area_to'):
        query = query.filter(object__apart_area__lte=request.query_params.get('apart_area_to'))

    if request.query_params.get('floors_from'):
        query = query.filter(object__floor__gte=request.query_params.get('floors_from'))
    if request.query_params.get('floors_to'):
        query = query.filter(object__floor__lte=request.query_params.get('floors_to'))

    if request.query_params.get('price_from'):
        query = query.filter(price__gte=request.query_params.get('price_from'))
    if request.query_params.get('price_to'):
        query = query.filter(price__lte=request.query_params.get('price_to'))

    try:
        page = int(request.query_params.get('page'))
    except:
        page = 1

    paginator = Paginator(query, 50)
    try:
        adverts = paginator.page(page)
    except PageNotAnInteger:
        adverts = []
    except EmptyPage:
        adverts = []

    if len(adverts) == 0:
        raise NotFound({'detail': {'message': 'По заданным параметрам объявления не найдены.'}})

    list_adverts = []
    for adv in adverts:
        list_adverts.append({
            'fio': adv.owner.fio,
            'phone': adv.owner.phone,
            'type': adv.object.type.title,
            'district': adv.object.district.title,
            'address': adv.object.address(),
            'rooms':  adv.object.rooms,
            'apart_area':  adv.object.apart_area,
            'floor':  adv.object.floor,
            'floors': adv.object.floors,
            'description': adv.object.description,
            'price': adv.price,
            'create_time': adv.create_time,
        })

    data = {
        'adverts': list_adverts,
        'total_pages': paginator.num_pages,
        'page': page,
    }
    serializer = ApiAdvertsListSerializer(data)
    return Response(serializer.data)