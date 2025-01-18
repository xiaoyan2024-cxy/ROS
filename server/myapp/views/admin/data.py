# Create your views here.
from django.db import connection
from django.db.models import Q
from rest_framework.decorators import api_view, authentication_classes
from django.urls import reverse
from myapp.auth.authentication import AdminTokenAuthtication
from myapp.handler import APIResponse
from myapp.models import ROS
from myapp.permission.permission import isDemoAdminUser
from myapp.serializers import ROSSerializer
from myapp.utils import dict_fetchall

@api_view(['GET'])
def list_api(request):
    if request.method == 'GET':
        keyword = request.GET.get("keyword", None)
        if keyword:
            ros_data = ROS.objects.filter(name__contains=keyword).order_by('-create_time')
        else:
            ros_data = ROS.objects.all().order_by('-create_time')
        serializer = ROSSerializer(ros_data, many=True)
        return APIResponse(code=0, msg='查询成功', data=serializer.data)


@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def create(request):
    # if isDemoAdminUser(request):
    #     return APIResponse(code=1, msg='演示帐号无法操作')
    
    print("----inside ROS create----")
    print(request.data)
    ros_data = ROS.objects.filter(name=request.data['name'])

    if len(ros_data) > 0:
        return APIResponse(code=1, msg='该名称已存在')
    serializer = ROSSerializer(data=request.data)

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
        pk = request.GET.get('id', -1)
        ros_data = ROS.objects.get(pk=pk)
    except ROS.DoesNotExist:
        return APIResponse(code=1, msg='对象不存在')

    serializer = ROSSerializer(ros_data, data=request.data)
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
   
        ROS.objects.filter(Q(id__in=ids_arr)).delete()
    except ROS.DoesNotExist:
        return APIResponse(code=1, msg='对象不存在')
    return APIResponse(code=0, msg='删除成功')
