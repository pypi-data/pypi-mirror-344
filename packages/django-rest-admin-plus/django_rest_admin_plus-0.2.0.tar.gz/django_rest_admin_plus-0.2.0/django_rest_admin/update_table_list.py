__author__ = "songjiangshan"
__copyright__ = "Copyright (C) 2021 songjiangshan \n All Rights Reserved."
__license__ = ""
__version__ = "1.0"

from .models import DbTableToRest,RouteExec
from django  import  VERSION
from django.apps import apps

from django.db import models
from django.db import connection

def update_table_list(request):
    table_name_exception = ['sqlite_sequence', 'django_migrations']
    index = 0

    # 清空所有记录
    DbTableToRest.objects.all().delete()

    # 添加由 models 映射的表
    models_to_loop = apps.get_models(include_auto_created=True)
    for i in models_to_loop:
        table_name = i._meta.db_table
        app_name = i._meta.app_label
        model_name = i.__name__
        if DbTableToRest.objects.filter(table_name=table_name).exists():
            continue

        index += 1
        tab_rcd = DbTableToRest()
        tab_rcd.id = index
        tab_rcd.table_name = table_name
        tab_rcd.in_app_name = app_name
        tab_rcd.has_api = RouteExec.objects.filter(table_name=table_name).count()
        tab_rcd.model_name = model_name
        tab_rcd.save()

    # 获取数据库类型
    vendor = connection.vendor  # 'sqlite', 'postgresql', 'mysql'

    cursor = connection.cursor()

    if vendor == 'sqlite':
        sql_tables = "SELECT name FROM sqlite_master WHERE type='table';"
        sql_views = "SELECT name FROM sqlite_master WHERE type='view';"
    elif vendor == 'postgresql':
        sql_tables = """
            SELECT table_name FROM information_schema.tables
            WHERE table_schema = 'public' AND table_type = 'BASE TABLE';
        """
        sql_views = """
            SELECT table_name FROM information_schema.views
            WHERE table_schema = 'public';
        """
    elif vendor == 'mysql':
        db_name = connection.settings_dict['NAME']
        sql_tables = f"""
            SELECT table_name FROM information_schema.tables
            WHERE table_schema = '{db_name}' AND table_type = 'BASE TABLE';
        """
        sql_views = f"""
            SELECT table_name FROM information_schema.views
            WHERE table_schema = '{db_name}';
        """
    else:
        raise NotImplementedError(f"Unsupported database vendor: {vendor}")

    # 添加表
    cursor.execute(sql_tables)
    for (table_name,) in cursor.fetchall():
        if table_name in table_name_exception:
            continue

        obj, created = DbTableToRest.objects.get_or_create(table_name=table_name)
        obj.t_type = 'table'
        obj.in_app_name = obj.in_app_name or None
        obj.model_name = obj.model_name or None
        obj.has_api = RouteExec.objects.filter(table_name=table_name).count()
        obj.save()
        if created:
            index += 1
            obj.id = index
            obj.save()

    # 添加视图
    cursor.execute(sql_views)
    for (view_name,) in cursor.fetchall():
        if view_name in table_name_exception:
            continue

        obj, created = DbTableToRest.objects.get_or_create(table_name=view_name)
        obj.t_type = 'view'
        obj.in_app_name = obj.in_app_name or None
        obj.model_name = obj.model_name or None
        obj.has_api = RouteExec.objects.filter(table_name=view_name).count()
        obj.save()
        if created:
            index += 1
            obj.id = index
            obj.save()




