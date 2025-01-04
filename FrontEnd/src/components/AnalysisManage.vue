<template>
    <!-- AQI 和污染程度关系图表 -->
    <div id="chart" class="aqi-chart"></div>
    <div class="analysis-manage">

        <el-form :model="analysisForm" :rules="rules" ref="analysisForm" label-width="120px">
            <!-- 监测站点选择 -->
            <el-form-item label="监测站点">
                <el-select v-model="analysisForm.StationID" placeholder="请选择监测站点" filterable>
                    <el-option v-for="station in stations" :key="station.StationID" :label="station.StationName"
                        :value="station.StationID" />
                </el-select>
            </el-form-item>

            <!-- 污染等级输入 -->
            <el-form-item label="污染等级">
                <el-input v-model="analysisForm.ContaminationLevel" placeholder="污染等级将根据AQI自动计算" disabled />
            </el-form-item>

            <!-- 分析时间选择 -->
            <el-form-item label="分析时间">
                <el-date-picker v-model="analysisForm.AnalysisTime" type="datetime" placeholder="选择分析时间"
                    value-format="YYYY-MM-DD HH:mm:ss" />
            </el-form-item>

            <!-- AQI 输入（滑条） -->
            <el-form-item label="AQI">
                <el-slider v-model="analysisForm.AQI" :min="0" :max="300" :step="1" show-input
                    @change="updateContaminationLevel" />
            </el-form-item>

            <!-- 建议输入 -->
            <el-form-item label="建议">
                <el-input v-model="analysisForm.Advice" type="textarea" placeholder="请输入建议" :rows="4" />
            </el-form-item>

            <!-- 提交按钮 -->
            <el-form-item>
                <el-button type="primary" @click="showConfirmDialog">提交</el-button>
                <el-button @click="resetForm">重置</el-button>
            </el-form-item>
        </el-form>

        <!-- 数据不完整提示对话框 -->
        <el-dialog v-model="incompleteDialogVisible" title="提示">
            <span>请填写完整信息！</span>
        </el-dialog>

        <!-- 提交成功提示对话框 -->
        <el-dialog v-model="successDialogVisible" title="提示">
            <span>数据提交成功！</span>
        </el-dialog>

        <!-- 提交确认对话框 -->
        <el-dialog v-model="confirmDialogVisible" title="确认提交" @close="confirmDialogVisible = false">
            <span>是否确认提交数据？</span>
            <template #footer>
                <el-button @click="confirmDialogVisible = false">取消</el-button>
                <el-button type="primary" @click="submitForm">确认</el-button>
            </template>
        </el-dialog>
    </div>
</template>

<script>
import axios from 'axios';
import * as echarts from 'echarts';

export default {
    data() {
        return {
            // 表单数据
            analysisForm: {
                StationID: '', // 监测站点 ID
                ContaminationLevel: '', // 污染等级
                AnalysisTime: '', // 分析时间
                AQI: null, // AQI 值（整数）
                Advice: '', // 建议
            },
            // 表单验证规则
            rules: {
                StationID: [{ required: true, message: '请选择监测站点', trigger: 'change' }],
                ContaminationLevel: [{ required: true, message: '污染等级不能为空', trigger: 'blur' }],
                AnalysisTime: [{ required: true, message: '请选择分析时间', trigger: 'change' }],
                AQI: [
                    { required: true, message: '请输入AQI值', trigger: 'blur' },
                    { type: 'number', message: 'AQI值必须为整数', trigger: 'blur' },
                ],
                Advice: [{ required: true, message: '请输入建议', trigger: 'blur' }],
            },
            // 监测站点列表
            stations: [],
            chart: null,
            incompleteDialogVisible: false, // 数据不完整提示对话框
            successDialogVisible: false, // 提交成功提示对话框
            confirmDialogVisible: false, // 确认对话框显示状态
        };
    },
    created() {
        this.fetchStations(); // 获取监测站点列表
    },
    mounted() {
        this.initChart(); // 初始化图表
    },
    methods: {
        // 获取监测站点列表
        async fetchStations() {
            try {
                const response = await axios.get('http://127.0.0.1:8000/api/stations/');
                this.stations = response.data;
            } catch (error) {
                console.error('获取监测站点失败:', error);
                // this.$message.error('获取监测站点失败，请稍后重试');
            }
        },

        // 显示提交确认对话框
        showConfirmDialog() {
            if (
                !this.analysisForm.StationID ||
                !this.analysisForm.AnalysisTime ||
                !this.analysisForm.AQI ||
                !this.analysisForm.Advice
            ) {
                console.log('请填写完整信息！');
                this.incompleteDialogVisible = true; // 显示填写完整信息提示对话框
                return;
            }
            this.confirmDialogVisible = true; // 显示确认对话框
        },
        // 根据 AQI 更新污染等级
        updateContaminationLevel() {
            const aqi = this.analysisForm.AQI;
            if (aqi === null || aqi === '') {
                this.analysisForm.ContaminationLevel = '';
                return;
            }
            if (aqi >= 0 && aqi <= 50) {
                this.analysisForm.ContaminationLevel = '优';
            } else if (aqi <= 100) {
                this.analysisForm.ContaminationLevel = '良';
            } else if (aqi <= 150) {
                this.analysisForm.ContaminationLevel = '轻度污染';
            } else if (aqi <= 200) {
                this.analysisForm.ContaminationLevel = '中度污染';
            } else {
                this.analysisForm.ContaminationLevel = '重度污染';
            }
            this.updateChart(aqi); // 更新图表
        },
        // 初始化图表
        initChart() {
            const chartDom = document.getElementById('chart');
            const chart = echarts.init(chartDom);

            // 图表配置
            const option = {
                xAxis: {
                    type: 'value',
                    name: 'AQI 值',
                    min: 0,
                    max: 300,
                    splitLine: {
                        show: false,
                    },
                    axisLabel: {
                        fontSize: 12,
                        color: '#666',
                    },
                    nameTextStyle: {
                        fontSize: 14,
                        color: '#333',
                    },
                },
                yAxis: {
                    type: 'category',
                    data: ['AQI 范围'],
                    axisLabel: {
                        show: false,
                    },
                    axisTick: {
                        show: false,
                    },
                },
                series: [
                    {
                        name: 'AQI',
                        type: 'bar',
                        data: [300], // 最大值
                        barWidth: 50,
                        itemStyle: {
                            color: {
                                type: 'linear',
                                x: 0,
                                y: 0,
                                x2: 1,
                                y2: 0,
                                colorStops: [
                                    { offset: 0, color: 'rgba(82, 196, 26, 0.9)' }, // 0-50: 绿色，50% 透明度
                                    { offset: 0.16, color: 'rgba(82, 196, 26, 0.5)' }, // 50
                                    { offset: 0.16, color: 'rgba(250, 219, 20, 0.9)' }, // 51-100: 黄色，50% 透明度
                                    { offset: 0.32, color: 'rgba(250, 219, 20, 0.5)' }, // 100
                                    { offset: 0.32, color: 'rgba(250, 140, 22, 0.9)' }, // 101-150: 橙色，50% 透明度
                                    { offset: 0.48, color: 'rgba(250, 140, 22, 0.5)' }, // 150
                                    { offset: 0.48, color: 'rgba(245, 34, 45, 0.9)' }, // 151-200: 红色，50% 透明度
                                    { offset: 0.64, color: 'rgba(245, 34, 45, 0.5)' }, // 200
                                    { offset: 0.64, color: 'rgba(130, 0, 20, 0.9)' }, // 201-300: 深红色，50% 透明度
                                    { offset: 1, color: 'rgba(130, 0, 20, 0.5)' }, // 300
                                ],
                            },
                            borderRadius: [10, 10, 10, 10], // 圆角设计
                            shadowColor: 'rgba(0, 0, 0, 0.3)', // 阴影颜色
                            shadowBlur: 10, // 阴影模糊大小
                            shadowOffsetY: 5, // 阴影垂直偏移
                        },
                    },
                ],
            };

            // 设置图表配置
            chart.setOption(option);
        },
        // 提交表单
        async submitForm() {
            this.confirmDialogVisible = false; // 关闭确认对话框
            try {
                // 构造提交数据
                const payload = {
                    StationID: this.analysisForm.StationID,
                    ContaminationLevel: this.analysisForm.ContaminationLevel,
                    AnalysisTime: this.analysisForm.AnalysisTime,
                    AQI: this.analysisForm.AQI,
                    Advice: this.analysisForm.Advice,
                };

                // 提交数据到后端
                const response = await axios.post('http://127.0.0.1:8000/api/analysis/', payload);
                if (response.data && response.data.status === 'success') {
                    this.successDialogVisible = true; // 显示提交成功对话框
                    this.resetForm(); // 重置表单
                } else {
                    console.error('提交数据失败');
                }
            } catch (error) {
                console.error('提交数据失败:', error);
                // this.$message.error('提交数据失败，请稍后重试');
            }
        },
        // 重置表单
        resetForm() {
            this.analysisForm.StationID = '';
            this.analysisForm.AnalysisTime = '';
            this.analysisForm.Advice = '';
            this.analysisForm.AQI = 0; // 清空 AQI 的值
            this.analysisForm.ContaminationLevel = ''; // 手动重置污染等级
        },
    },
};
</script>

<style scoped>
.analysis-manage {
    padding: 20px;
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
    margin-top: 50px;
    margin-left: 60px;
    width: 90%;
}

.el-form {
    max-width: 600px;
    margin: 0 auto;
}

.aqi-chart {
    width: 100%;
    height: 200px;
    margin-top: -20px;
}

/* 滑条样式 */
.el-slider {
    width: 80%;
    margin-left: 20px;
}
</style>