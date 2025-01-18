# Create your views here.
from rest_framework.decorators import api_view, authentication_classes
from myapp import utils
from myapp.auth.authentication import AdminTokenAuthtication
from myapp.handler import APIResponse
from myapp.models import Type
from myapp.permission.permission import isDemoAdminUser
from myapp.serializers import TypeSerializer



@api_view(['GET'])
def list_api(request):
    if request.method == 'GET':
        types = Type.objects.all().order_by('-create_time')
        serializer = TypeSerializer(types, many=True)
        print("---all Types---")
        print(serializer.data)
        return APIResponse(code=0, msg='查询成功', data=serializer.data)



@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def create(request):
    # if isDemoAdminUser(request):
    #     return APIResponse(code=1, msg='演示帐号无法操作')

    types = Type.objects.filter(title=request.data['title'])
    if len(types) > 0:
        return APIResponse(code=1, msg='该名称已存在')

    serializer = TypeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return APIResponse(code=0, msg='创建成功', data=serializer.data)
    else:
        utils.log_error(request, '参数错误')

    return APIResponse(code=1, msg='创建失败')


@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def update(request):
    if isDemoAdminUser(request):
        return APIResponse(code=1, msg='演示帐号无法操作')

    try:
        pk = request.GET.get('id', -1)
        types = Type.objects.get(pk=pk)

    except Type.DoesNotExist:
        return APIResponse(code=1, msg='对象不存在')

    serializer = TypeSerializer(types, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return APIResponse(code=0, msg='更新成功', data=serializer.data)
    else:
        utils.log_error(request, '参数错误')

    return APIResponse(code=1, msg='更新失败')

# 批量删除
@api_view(['POST'])
@authentication_classes([AdminTokenAuthtication])
def delete(request):
    if isDemoAdminUser(request):
        return APIResponse(code=1, msg='演示帐号无法操作')
    try:
        ids = request.GET.get('ids')
        ids_arr = ids.split(',')
        
        # id__in 查询表达式: 用于检查字段的值是否在给定的列表或查询集中。
        Type.objects.filter(id__in=ids_arr).delete()
    except Type.DoesNotExist:
        return APIResponse(code=1, msg='对象不存在')
    return APIResponse(code=0, msg='删除成功')
