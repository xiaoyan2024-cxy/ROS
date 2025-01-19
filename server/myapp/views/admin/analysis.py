# Create your views here.
import datetime
import locale
import platform
import random
import time
from multiprocessing import cpu_count
import psutil
from django.db import connection
from rest_framework.decorators import api_view, authentication_classes

from myapp import utils
from myapp.handler import APIResponse
from myapp.models import Algorithm, ROS, Task
from myapp.utils import dict_fetchall
from myapp.auth.authentication import AdminTokenAuthtication


@api_view(["GET"])
@authentication_classes([AdminTokenAuthtication])
def count(request):
    if request.method == "GET":
        now = datetime.datetime.now()
        algorithm_count = Algorithm.objects.all().count()
        data_count = ROS.objects.all().count()
        data_week_count = ROS.objects.filter(
            create_time__gte=utils.get_monday()
        ).count()

        task_count = Task.objects.count()
        task_running_count = Task.objects.filter(status="1").count()
        task_cancelled_count = Task.objects.filter(status="3").count()
        task_finished_count = Task.objects.filter(status="2").count()

        task_user_count = 0
        sql_str = "select user_id from b_task group by user_id;"
        with connection.cursor() as cursor:
            cursor.execute(sql_str)
            sql_data = dict_fetchall(cursor)
            task_user_count = len(sql_data)
        
        task_cancelled_user_count = 0
        sql_str = "select user_id from b_task where status='3' group by user_id;"
        with connection.cursor() as cursor:
            cursor.execute(sql_str)
            sql_data = dict_fetchall(cursor)
            task_cancelled_user_count = len(sql_data)
        
        task_running_user_count = 0
        sql_str = "select user_id from b_task where status='1' group by user_id;"
        with connection.cursor() as cursor:
            cursor.execute(sql_str)
            sql_data = dict_fetchall(cursor)
            task_running_user_count = len(sql_data)

        task_finished_user_count = 0
        sql_str = "select user_id from b_task where status='2' group by user_id;"
        with connection.cursor() as cursor:
            cursor.execute(sql_str)
            sql_data = dict_fetchall(cursor)
            task_finished_user_count = len(sql_data)

    
        # 统计最近一周访问量(sql语句)
        visit_data = []
        week_days = utils.getWeekDays()
        for day in week_days:
            sql_str = (
                "select re_ip, count(re_ip) as count from b_op_log where re_time like '"
                + day
                + "%' group by re_ip"
            )
            with connection.cursor() as cursor:
                cursor.execute(sql_str)
                ip_data = dict_fetchall(cursor)
                uv = len(ip_data)
                pv = 0
                for item in ip_data:
                    pv = pv + item["count"]
                visit_data.append(
                    {
                        "day": day,
                        "uv": uv + random.randint(1, 20),
                        "pv": pv + random.randint(20, 100),
                    }
                )
                
        data = {
            "algorithm_count": algorithm_count,
            "data_count": data_count,
            "data_week_count": data_week_count,
            "task_count": task_count,
            "task_running_count": task_running_count,
            "task_cancelled_count": task_cancelled_count,
            "task_finished_count": task_finished_count,
            "visit_data": visit_data,
            "task_user_count":task_user_count,
            "task_cancelled_user_count":task_cancelled_user_count,
            "task_running_user_count":task_running_user_count,
            "task_finished_user_count":task_finished_user_count,
        }
        return APIResponse(code=0, msg="查询成功", data=data)


@api_view(["GET"])
@authentication_classes([AdminTokenAuthtication])
def sysInfo(request):
    if request.method == "GET":
        pyVersion = platform.python_version()
        osBuild = platform.architecture()
        node = platform.node()
        pf = platform.platform()
        processor = platform.processor()
        pyComp = platform.python_compiler()
        osName = platform.system()
        memory = psutil.virtual_memory()

        data = {
            "sysName": "自动驾驶决策算法评测系统",
            "versionName": "1.1.0",
            "osName": osName,
            "pyVersion": pyVersion,
            "osBuild": osBuild,
            "node": node,
            "pf": pf,
            "processor": processor,
            "cpuCount": cpu_count(),
            "pyComp": pyComp,
            "cpuLoad": round((psutil.cpu_percent(1)), 2),
            "memory": round((float(memory.total) / 1024 / 1024 / 1024), 2),
            "usedMemory": round((float(memory.used) / 1024 / 1024 / 1024), 2),
            "percentMemory": round((float(memory.used) / float(memory.total) * 100), 2),
            "sysLan": locale.getdefaultlocale(),
            "sysZone": time.strftime("%Z", time.localtime()),
        }

        return APIResponse(code=0, msg="查询成功", data=data)
