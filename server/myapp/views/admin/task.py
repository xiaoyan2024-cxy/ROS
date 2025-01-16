# Create your views here.
from django.db import connection
from django.db.models import Q
from rest_framework.decorators import api_view, authentication_classes
from django.urls import reverse
from myapp.auth.authentication import AdminTokenAuthtication
from myapp.handler import APIResponse
from myapp.models import Task
from django.utils import timezone
from myapp.permission.permission import isDemoAdminUser
from myapp.serializers import TaskSerializer
from myapp.utils import dict_fetchall

@api_view(['GET'])
def list_api(request):
    if request.method == 'GET':
        keyword = request.GET.get("keyword", None)
        if keyword:
            tasks = Task.objects.filter(title__contains=keyword).order_by('-create_time')
        else:
            tasks = Task.objects.all().order_by('-create_time')
        serializer = TaskSerializer(tasks, many=True)
        return APIResponse(code=0, msg='查询成功', data=serializer.data)
    

@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def create(request):
    # if isDemoAdminUser(request):
    #     return APIResponse(code=1, msg='演示帐号无法操作')
    
    print(request.data)
    tasks = Task.objects.filter(title=request.data['title'])

    if len(tasks) > 0:
        return APIResponse(code=1, msg='该名称已存在')
    serializer = TaskSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return APIResponse(code=0, msg='创建成功', data=serializer.data)

    return APIResponse(code=1, msg='创建失败')


@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def update(request):
    try:
        print(request.GET)
        print(request.data)

        pk = request.GET.get('id', -1)
        tasks = Task.objects.get(pk=pk)

    except Task.DoesNotExist:
        return APIResponse(code=1, msg='对象不存在')
    
    data = request.data.copy()
    data['update_time'] = timezone.now()  # 设置更新时间
    print(data)

    serializer = TaskSerializer(tasks, data=data)
    if serializer.is_valid():
        serializer.save()
        return APIResponse(code=0, msg='更新成功', data=serializer.data)
    return APIResponse(code=1, msg='更新失败')


@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def delete(request):
    try:
        ids = request.GET.get('ids')
        ids_arr = ids.split(',')
   
        Task.objects.filter(Q(id__in=ids_arr)).delete()
    except Task.DoesNotExist:
        return APIResponse(code=1, msg='对象不存在')
    return APIResponse(code=0, msg='删除成功')
