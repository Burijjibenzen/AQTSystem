import pandas as pd
from django.core.management.base import BaseCommand
from aqt.models import Location, Station

class Command(BaseCommand):
    help = 'Insert Station data from CSV file based on existing Location data'

    def handle(self, *args, **kwargs):
        # CSV 文件路径
        csv_file_path = 'stationData.csv'

        try:
            # 读取 CSV 文件
            df = pd.read_csv(csv_file_path)
            print("CSV 文件读取成功！")

            # 逐行插入 Station 数据
            for index, row in df.iterrows():
                try:
                    # 根据 LocationName 获取对应的 Location 实例
                    id = Location.objects.get(LocationID=row['LocationID'])

                    # 插入 Station 数据
                    Station.objects.create(
                        StationName=row['StationName'],
                        LocationID=id,
                        isValid=row['isValid']
                    )
                    print(f"插入成功: {row['StationName']} (Location: {row['LocationName']})")
                except Location.DoesNotExist:
                    print(f"插入失败: Location {row['LocationName']} 不存在，跳过该行: {row}")
                except Exception as e:
                    print("next")

            self.stdout.write(self.style.SUCCESS('数据插入完成！'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"发生错误: {e}"))