import pandas as pd
from django.core.management.base import BaseCommand
from aqt.models import Analysis, Station

class Command(BaseCommand):
    help = 'Insert Station data from CSV file based on existing Location data'

    def handle(self, *args, **kwargs):
        # CSV 文件路径
        csv_file_path = 'analysisData.csv'

        try:
            # 读取 CSV 文件
            df = pd.read_csv(csv_file_path)
            print("CSV 文件读取成功！")

            # 逐行插入 Station 数据
            for index, row in df.iterrows():
                try:
                    # 根据 LocationName 获取对应的 Location 实例
                    station_id = Station.objects.get(StationID=row['StationID'])

                    # 插入 Station 数据
                    Analysis.objects.create(
                        StationID=station_id,
                        ContaminationLevel=row['ContaminationLevel'],
                        AnalysisTime=row['AnalysisTime'],
                        AQI=row['AQI'],
                        Advice=row['Advice'],
                    )
                    print("插入成功")
                except Exception as e:
                    print(e)

            self.stdout.write(self.style.SUCCESS('数据插入完成！'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"发生错误: {e}"))