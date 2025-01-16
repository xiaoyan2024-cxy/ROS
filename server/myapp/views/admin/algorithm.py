# Create your views here.
from django.db import connection
from django.db.models import Q
from rest_framework.decorators import api_view, authentication_classes
from django.urls import reverse
from myapp.auth.authentication import AdminTokenAuthtication
from myapp.handler import APIResponse
from myapp.models import Algorithm
from myapp.permission.permission import isDemoAdminUser
from myapp.serializers import AlgorithmSerializer
from myapp.utils import dict_fetchall



@api_view(['GET'])
def list_api(request):
    if request.method == 'GET':
        algorithms = Algorithm.objects.all().order_by('-create_time')
        serializer = AlgorithmSerializer(algorithms, many=True)
        return APIResponse(code=0, msg='查询成功', data=serializer.data)


@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def create(request):
    # if isDemoAdminUser(request):
    #     return APIResponse(code=1, msg='演示帐号无法操作')
    
    print("----inside /authentication/create")
    print(request.data)
    algorithms = Algorithm.objects.filter(title=request.data['title'])

    if len(algorithms) > 0:
        return APIResponse(code=1, msg='该名称已存在')
    serializer = AlgorithmSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return APIResponse(code=0, msg='创建成功', data=serializer.data)

    return APIResponse(code=1, msg='创建失败')


@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def update(request):
    # if isDemoAdminUser(request):
    #     return APIResponse(code=1, msg='演示帐号无法操作')

    try:
        print("request.GET in /myapp/admin/classification/update")
        print(request.GET)
        print(request.data)

        pk = request.GET.get('id', -1)
        algorithms = Algorithm.objects.get(pk=pk)
    except Algorithm.DoesNotExist:
        return APIResponse(code=1, msg='对象不存在')

    serializer = AlgorithmSerializer(algorithms, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return APIResponse(code=0, msg='更新成功', data=serializer.data)

    return APIResponse(code=1, msg='更新失败')


@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def delete(request):
    # if isDemoAdminUser(request):
    #     return APIResponse(code=1, msg='演示帐号无法操作')
    try:
        ids = request.GET.get('ids')
        ids_arr = ids.split(',')
   
        Algorithm.objects.filter(Q(id__in=ids_arr)).delete()
    except Algorithm.DoesNotExist:
        return APIResponse(code=1, msg='对象不存在')
    return APIResponse(code=0, msg='删除成功')
