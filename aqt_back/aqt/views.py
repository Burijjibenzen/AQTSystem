from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from .models import User, Advice, Data, Station, Indicator, Record, Analysis
from .serializers import UserSerializer
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
from collections import defaultdict
from django.db.models import CharField
from django.db.models.functions import Cast

import random
import string

class RegisterView(APIView):
    def post(self, request):
        data = request.data
        user_id = int(data.get('id'))
        password = data.get('password')
        rold_id = 1

        # 检查用户ID是否已存在
        if User.objects.filter(UserID=user_id).exists():
            return Response({"success": False, "message": "ID已存在"}, status=status.HTTP_409_CONFLICT)

        hashed_password = make_password(password)
        # 创建新用户
        user_data = {
            'UserID': user_id,
            'RoleID': rold_id,
            'UserName': ''.join(random.choices(string.ascii_letters + string.digits, k=10)),
            'Password': hashed_password
        }
        serializer = UserSerializer(data=user_data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "message": "register successful"}, status=status.HTTP_201_CREATED)
        else:
            return Response({"success": False, "message": "Server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class LoginView(APIView):
    def post(self, request):
        data = request.data
        user_id = data.get('id')
        password = data.get('password')
        role = data.get('role')

        if role == '用户':
            role_id = 1
        if role == '监测员':
            role_id = 2
        if role == '研究员':
            role_id = 3

        # 检查用户ID是否存在
        try:
            user = User.objects.get(UserID=user_id, RoleID=role_id)
        except User.DoesNotExist:
            return Response({"success": False, "message": "No such ID"}, status=status.HTTP_409_CONFLICT)

        # 检查密码是否匹配
        if not check_password(password, user.Password):
            return Response({"success": False, "message": "Password and ID do not match"},
                            status=status.HTTP_400_BAD_REQUEST)

        # 登录成功
        return Response({"success": True, "message": "Login succeed"}, status=status.HTTP_201_CREATED)
    
class AdviceView(APIView):
    def post(self, request):
        user_id = request.data.get('UserID')
        content = request.data.get('Content')

        print(user_id, content)

        if not user_id or not content:
            return Response({'status': 'error', 'message': '用户ID和反馈内容不能为空'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(UserID=user_id)
        except User.DoesNotExist:
            return Response({'status': 'error', 'message': '用户不存在'}, status=status.HTTP_404_NOT_FOUND)

        advice = Advice(
            UserID=user,
            Content=content,
            AdviceTime=datetime.now()
        )
        advice.save()

        return Response({'status': 'success', 'message': '反馈提交成功'}, status=status.HTTP_201_CREATED)
    
class QueryDataView(APIView):
    def get(self, request):
        try:
            # 获取查询参数
            station_name = request.query_params.get('station', '').strip()
            pollutant = request.query_params.get('pollutant', '').strip()
            start_time = request.query_params.get('start_time', '').strip()
            end_time = request.query_params.get('end_time', '').strip()

            print(station_name, pollutant, start_time, end_time)

            # 构建查询条件
            query = Q()
            if station_name:
                query &= Q(StationID__StationName__icontains=station_name)  # 模糊搜索
            if pollutant:
                query &= Q(IndicatorID__IndicatorName__icontains=pollutant)  # 模糊搜索
            if start_time and end_time:
                # 检查时间格式是否有效
                try:
                    query &= Q(DataTime__range=[start_time, end_time])
                except ValueError:
                    return Response(
                        {"error": "时间格式无效，请使用 'YYYY-MM-DD HH:MM:SS' 格式"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            # 筛选 isValid 为 True 的监测站点
            query &= Q(StationID__isValid=True)

            # 查询数据
            data = Data.objects.filter(query)

            # 处理数据，添加 StationName 和 IndicatorName
            result = []
            for item in data:
                try:
                    station_name = Station.objects.get(StationID=item.StationID_id).StationName
                    indicator_name = Indicator.objects.get(IndicatorID=item.IndicatorID_id).IndicatorName
                    formatted_time = item.DataTime.strftime('%Y-%m-%d %H:%M:%S')  # 格式化时间

                    result.append({
                        "DataID": item.DataID,
                        "StationName": station_name,
                        "IndicatorName": indicator_name,
                        "DataTime": formatted_time,
                        "Value": item.Value
                    })
                except Station.DoesNotExist:
                    return Response(
                        {"error": f"未找到 StationID 为 {item.StationID_id} 的监测站点"},
                        status=status.HTTP_404_NOT_FOUND
                    )
                except Indicator.DoesNotExist:
                    return Response(
                        {"error": f"未找到 IndicatorID 为 {item.IndicatorID_id} 的污染物"},
                        status=status.HTTP_404_NOT_FOUND
                    )

            # 返回查询结果
            return Response(result, status=status.HTTP_200_OK)

        except Exception as e:
            # 捕获其他异常
            return Response(
                {"error": f"服务器内部错误: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
class SaveQueryRecordsView(APIView):
    def post(self, request):
        try:
            user_id = request.data.get('user_id')  # 用户 ID
            records_data = request.data.get('records')  # 查询记录列表

            # 构造 Record 对象列表
            record_objects = []
            for record_data in records_data:
                data_id = record_data['data_id']  # 每条记录对应的 DataID
                record_time_str = record_data.get('record_time')  # 前端传递的时间

                # 将前端传递的时间转换为 datetime 对象
                if record_time_str:
                    try:
                        record_time = datetime.fromisoformat(record_time_str.replace('Z', '+00:00'))
                    except ValueError:
                        record_time = timezone.now()  # 如果时间格式无效，使用当前时间
                else:
                    record_time = timezone.now()  # 如果未传递时间，使用当前时间

                # 创建 Record 对象
                record_objects.append(
                    Record(
                        UserID_id=user_id,
                        DataID_id=data_id,
                        RecordTime=record_time  # 使用前端传递的时间或当前时间
                    )
                )

            # 批量插入
            Record.objects.bulk_create(record_objects)

            return Response({'status': 'success', 'message': '查询记录保存成功'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class QueryAnalysisView(APIView):
    def get(self, request):
        try:
            # 获取查询参数
            station_name = request.query_params.get('station', '').strip()
            start_time = request.query_params.get('start_time', '').strip()
            end_time = request.query_params.get('end_time', '').strip()

            print(station_name, start_time, end_time)

            # 构建查询条件
            query = Q()
            if station_name:
                query &= Q(StationID__StationName__icontains=station_name)  # 模糊搜索监测站点
            if start_time and end_time:
                # 检查时间格式是否有效
                try:
                    query &= Q(AnalysisTime__range=[start_time, end_time])  # 时间范围筛选
                except ValueError:
                    return Response(
                        {"error": "时间格式无效，请使用 'YYYY-MM-DD HH:MM:SS' 格式"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            # 筛选 isValid 为 True 的监测站点
            query &= Q(StationID__isValid=True)

            # 查询数据
            analysis_data = Analysis.objects.filter(query)

            # 处理数据，添加 StationName
            result = []
            for item in analysis_data:
                try:
                    station_name = Station.objects.get(StationID=item.StationID_id).StationName
                    formatted_time = item.AnalysisTime.strftime('%Y-%m-%d %H:%M:%S')  # 格式化时间

                    result.append({
                        "AnalysisID": item.AnalysisID,
                        "StationName": station_name,
                        "ContaminationLevel": item.ContaminationLevel,
                        "AnalysisTime": formatted_time,
                        "AQI": int(item.AQI),  # AQI 只输出整数部分
                        "Advice": item.Advice
                    })
                except Station.DoesNotExist:
                    return Response(
                        {"error": f"未找到 StationID 为 {item.StationID_id} 的监测站点"},
                        status=status.HTTP_404_NOT_FOUND
                    )

            # 返回查询结果
            return Response(result, status=status.HTTP_200_OK)

        except Exception as e:
            # 捕获其他异常
            return Response(
                {"error": f"服务器内部错误: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
class GetStationsLocationView(APIView):
    def post(self, request):
        station_names = request.data.get('station_names', [])
        stations = Station.objects.filter(StationName__in=station_names)
        locations = []
        for station in stations:
            locations.append({
                'StationName': station.StationName,
                'Latitude': station.LocationID.Latitude,
                'Longitude': station.LocationID.Longitude,
            })
        return Response(locations)
    
class PasswordResetView(APIView):
    def post(self, request, *args, **kwargs):
        # 获取请求数据
        role_id = request.data.get('role_id')
        user_id = request.data.get('user_id')
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        # 检查必填字段
        if not all([role_id, user_id, old_password, new_password]):
            return Response({"error": "缺少必要字段"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # 获取用户
            user = User.objects.get(UserID=user_id, RoleID=role_id)
        except User.DoesNotExist:
            return Response({"error": "用户不存在"}, status=status.HTTP_404_NOT_FOUND)

        # 验证旧密码
        if not check_password(old_password, user.Password):
            return Response({"error": "旧密码不正确"}, status=status.HTTP_400_BAD_REQUEST)

        # 更新密码
        user.Password = make_password(new_password)
        user.save()

        # 返回成功响应
        return Response({"message": "密码重置成功"}, status=status.HTTP_200_OK)
    
class QueryRecordView(APIView):
    def get(self, request):
        # 从请求中获取 UserID
        user_id = request.query_params.get('user_id')

        if not user_id:
            return Response(
                {"error": "UserID 不能为空"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 获取当前用户的查询记录
        records = Record.objects.filter(UserID=user_id).order_by('-RecordTime')

        # 按 RecordTime 合并记录
        merged_records = defaultdict(list)
        for record in records:
            merged_records[record.RecordTime].append({
                'RecordID': record.RecordID,
                'DataID': record.DataID.DataID,  # 假设 DataID 是外键，获取其主键值
                'UserID': record.UserID.UserID,  # 假设 UserID 是外键，获取其主键值
            })

        # 构造响应数据
        response_data = []
        for record_time, records in merged_records.items():
            response_data.append({
                'RecordTime': record_time.strftime('%Y-%m-%d %H:%M:%S'),  # 格式化时间
                'Records': records,
            })

        return Response(response_data, status=status.HTTP_200_OK)
    
class DataDetailsView(APIView):
    def post(self, request):
        # 获取请求体中的 DataID 列表
        data_ids = request.data.get('data_ids', [])

        if not data_ids:
            return Response({"error": "DataID 列表不能为空"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 一次性获取所有 DataID 对应的 Data 记录
            data_records = Data.objects.filter(DataID__in=data_ids).select_related('StationID', 'IndicatorID')

            # 构造响应数据
            response_data = []
            for data in data_records:
                response_data.append({
                    'station': data.StationID.StationName,  # 假设 Station 模型中有 StationName 字段
                    'pollutant': data.IndicatorID.IndicatorName,  # 假设 Indicator 模型中有 IndicatorName 字段
                    'value': float(data.Value),  # 将 Decimal 转换为 float
                    'time': data.DataTime.strftime('%Y-%m-%d %H:%M:%S'),  # 格式化时间
                })

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class DeleteRecordView(APIView):
    def post(self, request):
        # 获取请求体中的 RecordTime
        record_time = request.data.get('record_time')

        if not record_time:
            return Response({"success": False, "message": "RecordTime 不能为空"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # 将 RecordTime 转换为字符串后进行前缀匹配
            Record.objects.annotate(
                record_time_str=Cast('RecordTime', output_field=CharField())
            ).filter(record_time_str__startswith=record_time).delete()
            return Response({"success": True, "message": "记录删除成功"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"success": False, "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class AdviceListView(APIView):
    def get(self, request):
        # 获取所有反馈数据，按 AdviceTime 倒序排序
        advices = Advice.objects.all().order_by('-AdviceTime')

        # 构造响应数据
        response_data = []
        for advice in advices:
            response_data.append({
                'AdviceID': advice.AdviceID,
                'UserID': advice.UserID_id,  # 获取外键的 ID
                'Content': advice.Content,
                'AdviceTime': advice.AdviceTime.strftime('%Y-%m-%d %H:%M:%S'),  # 格式化时间
            })

        return Response(response_data, status=status.HTTP_200_OK)
    
class StationListView(APIView):
    def get(self, request):
        try:
            # 获取所有监测站点
            stations = Station.objects.filter(isValid=True)
            # 构造响应数据
            response_data = []
            for station in stations:
                response_data.append({
                    "StationID": station.StationID,
                    "StationName": station.StationName,
                    "LocationID": station.LocationID_id,  # 获取外键的 ID
                })
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 获取监测指标列表
class IndicatorListView(APIView):
    def get(self, request):
        try:
            # 获取所有监测指标
            indicators = Indicator.objects.all()
            # 构造响应数据
            response_data = []
            for indicator in indicators:
                response_data.append({
                    "IndicatorID": indicator.IndicatorID,
                    "IndicatorName": indicator.IndicatorName,
                    "Unit": indicator.Unit,
                })
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 提交监测数据
class DataCreateView(APIView):
    def post(self, request):
        try:
            # 获取请求数据
            station_id = request.data.get("StationID")
            indicator_id = request.data.get("IndicatorID")
            data_time = request.data.get("DataTime")
            value = request.data.get("Value")

            # 验证数据
            if not all([station_id, indicator_id, data_time, value]):
                return Response(
                    {"error": "所有字段均为必填项"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # 创建数据
            data = Data.objects.create(
                StationID_id=station_id,
                IndicatorID_id=indicator_id,
                DataTime=data_time,
                Value=value,
            )

            return Response({"status": "success", "data_id": data.DataID}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class StationManagementView(APIView):
    def get(self, request):
        try:
            # 获取所有监测站点
            stations = Station.objects.all()
            # 构造响应数据
            response_data = []
            for station in stations:
                response_data.append({
                    "StationID": station.StationID,
                    "StationName": station.StationName,
                    "LocationID": station.LocationID_id,  # 外键 ID
                    "LocationName": station.LocationID.LocationName,  # 位置名称
                    "isValid": station.isValid,  # 启用状态
                })
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
            try:
                # 获取请求体中的 StationID 和 isValid 值
                station_id = request.data.get("StationID")
                isValid = request.data.get("isValid")

                # 更新站点启用状态
                station = Station.objects.get(pk=station_id)
                station.isValid = isValid
                station.save()

                return Response({"status": "success", "message": "站点状态更新成功"}, status=status.HTTP_200_OK)
            except Station.DoesNotExist:
                return Response({"error": "站点不存在"}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
class AnalysisCreateView(APIView):
    def post(self, request):
        try:
            # 解析请求体中的数据
            data = request.data
            station_id = data.get('StationID')
            contamination_level = data.get('ContaminationLevel')
            analysis_time = data.get('AnalysisTime')
            aqi = data.get('AQI')
            advice = data.get('Advice')

            # 验证数据
            if not all([station_id, contamination_level, analysis_time, aqi, advice]):
                return Response({"status": "error", "message": "所有字段均为必填项"}, status=status.HTTP_400_BAD_REQUEST)

            # 检查监测站点是否存在
            try:
                station = Station.objects.get(StationID=station_id)
            except Station.DoesNotExist:
                return Response({"status": "error", "message": "监测站点不存在"}, status=status.HTTP_400_BAD_REQUEST)

            # 创建分析记录
            analysis = Analysis(
                StationID=station,
                ContaminationLevel=contamination_level,
                AnalysisTime=analysis_time,
                AQI=aqi,
                Advice=advice
            )
            analysis.save()

            # 返回成功响应
            return Response({"status": "success", "message": "数据提交成功"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)