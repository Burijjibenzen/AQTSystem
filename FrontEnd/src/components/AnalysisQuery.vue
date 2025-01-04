<template>
    <div>
        <el-form :inline="true" :model="queryForm" class="demo-form-inline">
            <el-form-item label="监测站点">
                <el-input v-model="queryForm.station" placeholder="请输入监测站点"></el-input>
            </el-form-item>
            <el-form-item label="时间范围">
                <el-date-picker v-model="queryForm.timeRange" type="daterange" range-separator="至"
                    start-placeholder="开始日期" end-placeholder="结束日期"></el-date-picker>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="onQuery">查询</el-button>
            </el-form-item>
        </el-form>

        <!-- 表格容器 -->
        <div class="table-container">
            <el-table :data="analysisData" style="width: 100%;" height="100%">
                <el-table-column prop="StationName" label="监测站点" width="200" fixed></el-table-column>
                <el-table-column prop="ContaminationLevel" label="污染程度" width="100" fixed></el-table-column>
                <el-table-column prop="AQI" label="空气质量指数AQI" width="150" fixed></el-table-column>
                <el-table-column prop="Advice" label="健康建议" width="380" fixed></el-table-column>
                <el-table-column prop="AnalysisTime" label="时间" width="180" fixed></el-table-column>
            </el-table>
        </div>

        <!-- 地图和图表容器 -->
        <div class="map-chart-container">
            <!-- 地图容器 -->
            <div id="map" class="map-container"></div>

            <!-- 图表容器 -->
            <div id="chart" class="chart-container"></div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import L from 'leaflet'; // 引入 Leaflet
import 'leaflet/dist/leaflet.css'; // 引入 Leaflet 的样式
import * as echarts from 'echarts'; // 引入 ECharts

export default {
    data() {
        return {
            queryForm: {
                station: '', // 选择的监测站点
                timeRange: [], // 时间范围，初始化为空数组
            },
            analysisData: [], // 查询到的分析结果数据
            stationsWithLocation: [], // 包含经纬度的监测站数据
            map: null, // Leaflet 地图实例
            mapCenter: [30.25, 120.15], // 地图中心点（默认杭州）
            chart: null, // ECharts 实例
        };
    },
    methods: {
        async onQuery() {
            try {
                // 获取查询参数
                const station = this.queryForm.station;
                const timeRange = this.queryForm.timeRange;

                // 构造请求参数
                const params = {};
                if (station) {
                    params.station = station;
                }
                // 处理时间范围
                if (timeRange && timeRange.length === 2) {
                    // 将时间字符串转换为 Date 对象
                    const startTime = new Date(timeRange[0]);
                    const endTime = new Date(timeRange[1]);

                    // 增加 8 小时
                    startTime.setHours(startTime.getHours() + 8);
                    endTime.setHours(endTime.getHours() + 8 + 23);
                    endTime.setMinutes(endTime.getMinutes() + 59);
                    endTime.setSeconds(endTime.getSeconds() + 59);

                    // 格式化时间为 ISO 字符串
                    params.start_time = startTime.toISOString();
                    params.end_time = endTime.toISOString();
                } else {
                    // 如果时间范围为空，设置默认值
                    params.start_time = '1900-01-01T00:00:00Z'; // 最小值
                    params.end_time = '2100-12-31T23:59:59Z'; // 最大值
                }

                // 调用后端接口
                const response = await axios.get('http://127.0.0.1:8000/api/query-analysis/', { params });

                // 更新表格数据
                this.analysisData = response.data;

                // 获取监测站的经纬度信息
                this.stationsWithLocation = await this.getStationsWithLocation(response.data);

                // 渲染地图标记
                this.renderMapMarkers();

                // 自动定位到第一个站点
                if (this.stationsWithLocation.length > 0) {
                    const firstStation = this.stationsWithLocation[0];
                    this.mapCenter = [firstStation.Latitude, firstStation.Longitude];
                    this.map.setView(this.mapCenter, 5); // 设置地图中心点和缩放级别
                }
            } catch (error) {
                console.error('查询失败:', error);
            }
        },
        async getStationsWithLocation(analysisData) {
            try {
                // 提取所有监测站名称
                const stationNames = [...new Set(analysisData.map(item => item.StationName))];

                // 调用后端接口获取监测站的经纬度
                const response = await axios.post('http://127.0.0.1:8000/api/get-stations-location/', {
                    station_names: stationNames,
                });

                return response.data;
            } catch (error) {
                console.error('获取监测站经纬度失败:', error);
                return [];
            }
        },
        initMap() {
            // 初始化地图
            this.map = L.map('map').setView(this.mapCenter, 10);

            // 添加地图图层
            L.tileLayer('https://tile-a.openstreetmap.fr/hot/{z}/{x}/{y}.png', {
                attribution: '© OpenStreetMap contributors',
            }).addTo(this.map);
        },
        renderMapMarkers() {
            if (!this.map) return;

            // 清除之前的标记
            this.map.eachLayer(layer => {
                if (layer instanceof L.Marker) {
                    this.map.removeLayer(layer);
                }
            });

            // 添加新的标记
            this.stationsWithLocation.forEach(station => {
                const marker = L.marker([station.Latitude, station.Longitude]).addTo(this.map);
                marker.bindPopup(station.StationName);

                // 点击标记时显示 AQI 变化图表
                marker.on('click', () => {
                    this.renderAQIChart(station.StationName);
                });
            });
        },
        renderAQIChart(stationName) {
            // 过滤当前站点的 AQI 数据
            const stationData = this.analysisData.filter(item => item.StationName === stationName);

            stationData.sort((a, b) => new Date(a.AnalysisTime) - new Date(b.AnalysisTime));
            // 提取时间和 AQI 数据
            const xAxisData = [...new Set(stationData.map(item => item.AnalysisTime))];
            // const xAxisData = stationData.map(item => item.AnalysisTime);
            const seriesData = stationData.map(item => item.AQI);
            const contaminationLevels = stationData.map(item => item.ContaminationLevel);

            // 打印数据以检查格式
            console.log('xAxisData:', xAxisData);
            console.log('seriesData:', seriesData);
            console.log('contaminationLevels:', contaminationLevels);

            // 初始化 ECharts 实例
            if (!this.chart) {
                const chartDom = document.getElementById('chart');
                if (chartDom) {
                    this.chart = echarts.init(chartDom);
                } else {
                    console.error('未找到 ECharts 容器');
                    return;
                }
            }

            // 根据污染程度设置颜色
            const colors = contaminationLevels.map(level => {
                if (level === '轻度污染') return '#ff8000';
                if (level === '中度污染') return '#db2c00';
                if (level === '重度污染') return '#9c001d';
                if (level === '优') return '#91CC75';
                if (level === '良') return '#FAC858';
                return '#5470C6'; // 默认颜色
            });

            // 配置图表选项
            const option = {
                title: {
                    text: `${stationName} AQI 变化趋势`,
                    left: 'center',
                },
                tooltip: {
                    trigger: 'item', // 鼠标悬停在坐标轴上触发
                    axisPointer: {
                        type: 'cross', // 使用十字线指示器
                    },
                },
                xAxis: {
                    type: 'category',
                    data: xAxisData,
                    name: '时间',
                },
                yAxis: {
                    type: 'value',
                    name: 'AQI',
                },
                series: [
                    {
                        name: 'AQI',
                        type: 'line',
                        data: seriesData,
                        smooth: true, // 平滑曲线
                        lineStyle: {
                            color: {
                                type: 'linear',
                                x: 0,
                                y: 0,
                                x2: 1,
                                y2: 0,
                                colorStops: seriesData.map((value, index) => ({
                                    offset: index / (seriesData.length - 1), // 渐变位置
                                    color: colors[index], // 渐变颜色
                                })),
                            },
                        },
                        itemStyle: {
                            color: (params) => colors[params.dataIndex], // 数据点颜色
                        },
                    },
                ],
                visualMap: {
                    type: 'piecewise', // 分段式视觉映射
                    show: true, // 显示视觉映射组件
                    right: 10, // 距离右侧 10px
                    top: 10,
                    orient: 'vertical', // 垂直方向
                    pieces: [
                        { gt: 0, lte: 50, color: '#91CC75', label: '优 (0-50)' }, // 优
                        { gt: 50, lte: 100, color: '#FAC858', label: '良 (51-100)' }, // 良
                        { gt: 100, lte: 150, color: '#ff8000', label: '轻度污染 (101-150)' }, // 轻度污染
                        { gt: 150, lte: 200, color: '#db2c00', label: '中度污染 (151-200)' }, // 中度污染
                        { gt: 200, color: '#9c001d', label: '重度污染 (>200)' }, // 重度污染
                    ],
                    outOfRange: {
                        color: '#5470C6', // 默认颜色
                    },
                },
            };

            // 渲染图表
            this.chart.setOption(option);
        }

    },
    mounted() {
        // 初始化地图
        this.initMap();

        // 初始化 ECharts 实例
        const chartDom = document.getElementById('chart');
        if (chartDom) {
            this.chart = echarts.init(chartDom);
            console.log('ECharts 容器尺寸:', chartDom.offsetWidth, chartDom.offsetHeight);
        } else {
            console.error('未找到 ECharts 容器');
        }
    },
};
</script>

<style scoped>
.air-quality-analysis {
    padding: 20px;
    background-color: #fff;
    border-radius: 10px;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.table-container {
    height: 240px;
    overflow-y: auto;
    border: 1px solid #ebeef5;
    overflow-x: hidden;
    border-radius: 10px;
    margin-bottom: 20px;
}

.map-chart-container {
    display: flex;
    gap: 20px;
    margin-top: 20px;
}

.map-container {
    height: 388px;
    width: 50%;
    border: 1px solid #ebeef5;
    border-radius: 10px;
    margin-top: 8px;
}

.chart-container {
    height: 388px;
    width: 50%;
    /* border: 1px solid #ebeef5; */
    border-radius: 10px;
    margin-top: 20px;
}
</style>