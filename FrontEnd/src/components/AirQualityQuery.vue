<template>
  <div>
    <el-form :inline="true" :model="queryForm" class="demo-form-inline">
      <el-form-item label="监测站点">
        <el-input v-model="queryForm.station" placeholder="请输入监测站点"></el-input>
      </el-form-item>
      <el-form-item label="污染物" style="width: 15%">
        <el-select v-model="queryForm.pollutant" placeholder="请选择污染物" filterable clearable>
          <el-option label="PM2.5" value="PM2.5"></el-option>
          <el-option label="PM10" value="PM10"></el-option>
          <el-option label="臭氧" value="O3"></el-option>
          <el-option label="二氧化硫" value="SO2"></el-option>
          <el-option label="一氧化碳" value="CO"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="时间范围">
        <el-date-picker v-model="queryForm.timeRange" type="daterange" range-separator="至" start-placeholder="开始日期"
          end-placeholder="结束日期">
        </el-date-picker>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="onQuery" style="width: 50px;">查询</el-button>
        <el-button type="success" @click="downloadExcel" style="width: 90px;">下载 Excel</el-button>
        <el-button type="warning" @click="downloadCSV" style="width: 80px;">下载 CSV</el-button>
        <p style="font-size: small; color: midnightblue; margin-left: 20px;">注意*
          各指标单位：PM2.5（μg/m³）PM10（μg/m³）O3（μg/m³）SO2（μg/m³）CO（mg/m³）</p>
      </el-form-item>
    </el-form>

    <!-- 固定高度的表格容器 -->
    <div class="table-container">
      <el-table :data="tableData" style="width: 100%" height="100%">
        <el-table-column prop="station" label="监测站点" width="310" fixed></el-table-column>
        <el-table-column prop="pollutant" label="污染物" width="280" fixed></el-table-column>
        <el-table-column prop="value" label="浓度值" width="280" fixed></el-table-column>
        <el-table-column prop="time" label="时间" width="280" fixed></el-table-column>
      </el-table>
    </div>

    <!-- 监测站选择 -->
    <el-form :inline="true" class="demo-form-inline" style="margin-top: 15px;">
      <el-form-item label="选择需绘制污染物变化趋势的监测站" style="width: 40%">
        <el-select v-model="selectedStation" placeholder="请选择监测站" @change="renderChartByStation">
          <el-option v-for="station in stations" :key="station" :label="station" :value="station"></el-option>
        </el-select>
      </el-form-item>
    </el-form>

    <!-- 图表容器 -->
    <div ref="chart" class="chart-container"></div>

    <!-- 提示对话框 -->
    <el-dialog :model-value="dialogVisible" title="提示" @close="dialogVisible = false">
      <span>{{ dialogMessage }}</span>
    </el-dialog>
  </div>
</template>

<script>
import axios from 'axios';
import * as echarts from 'echarts';
import * as XLSX from 'xlsx'; // 引入 xlsx 库

export default {
  data() {
    return {
      queryForm: {
        station: '',
        pollutant: '',
        timeRange: [] // 时间范围，初始化为空数组
      },
      tableData: [],
      chart: null, // 用于存储 ECharts 实例
      stations: [], // 所有监测站列表
      selectedStation: '', // 用户选择的监测站
      dialogVisible: false, // 控制对话框的显示和隐藏
      dialogMessage: '' // 对话框显示的消息内容
    };
  },
  methods: {
    async onQuery() {
      try {
        const params = {
          station: this.queryForm.station,
          pollutant: this.queryForm.pollutant,
        };

        const timeRange = this.queryForm.timeRange;

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
          console.log('开始时间:', params.start_time);
        } else {
          // 如果时间范围为空，设置默认值
          params.start_time = '1900-01-01T00:00:00Z'; // 最小值
          params.end_time = '2100-12-31T23:59:59Z'; // 最大值
          console.log('默认时间范围:', params.start_time, '至', params.end_time);
        }

        console.log('查询参数:', params);

        // 查询数据
        const response = await axios.get('http://127.0.0.1:8000/api/query-data/', { params });
        console.log('查询结果:', response.data);
        this.tableData = response.data.map(item => ({
          station: item.StationName,
          pollutant: item.IndicatorName,
          value: item.Value,
          time: item.DataTime
        }));

        // 提取所有监测站
        this.stations = [...new Set(response.data.map(item => item.StationName))];
        this.selectedStation = this.stations[0] || ''; // 默认选择第一个监测站

        // 生成图表
        this.renderChartByStation();

        // 保存查询记录
        if (response.data.length > 0) {
          const user_id = localStorage.getItem('id');

          // 获取当前时间（北京时间）
          const now = new Date();
          const beijingTime = new Date(now.getTime() + 8 * 60 * 60 * 1000); // 增加 8 小时
          const recordTime = beijingTime.toISOString(); // 转换为 ISO 8601 格式

          // 构造查询记录列表
          const records = response.data.map(item => ({
            data_id: item.DataID, // 假设每条查询结果对应一个 DataID
            record_time: recordTime // 传递当前时间
          }));

          // 发送 POST 请求保存记录
          await axios.post('http://127.0.0.1:8000/api/save-query-records/', {
            user_id: user_id,
            records: records
          }, {
            headers: {
              'Content-Type': 'application/json'
            }
          });
          console.log('查询记录保存成功');
        }
      } catch (error) {
        console.error('查询失败:', error);
      }
    },
    renderChartByStation() {
      if (!this.selectedStation) return;

      // 过滤出当前选择的监测站的数据
      const filteredData = this.tableData.filter(item => item.station === this.selectedStation);

      // 按时间排序
      filteredData.sort((a, b) => new Date(a.time) - new Date(b.time));

      // 销毁之前的图表实例
      if (this.chart) {
        this.chart.dispose();
      }

      // 初始化图表
      this.chart = echarts.init(this.$refs.chart);

      // 按污染物类型分组数据
      const pollutantData = {};
      filteredData.forEach(item => {
        if (!pollutantData[item.pollutant]) {
          pollutantData[item.pollutant] = [];
        }
        pollutantData[item.pollutant].push({
          time: item.time,
          value: item.value
        });
      });

      // 生成 X 轴数据（时间）
      const xAxisData = [...new Set(filteredData.map(item => item.time))];

      // 生成系列数据
      const series = Object.keys(pollutantData).map((pollutant, index) => {
        const color = this.getColor(index); // 获取颜色
        return {
          name: pollutant,
          type: 'line',
          data: pollutantData[pollutant].map(item => item.value),
          smooth: true, // 平滑曲线
          lineStyle: {
            color: color
          },
          itemStyle: {
            color: color
          }
        };
      });

      // 配置图表选项
      const option = {
        title: {
          text: `${this.selectedStation} 污染物浓度变化趋势`,
          left: 'center'
        },
        tooltip: {
          trigger: 'item', // 鼠标悬停在坐标轴上触发
          axisPointer: {
            type: 'cross', // 使用十字线指示器
          },
        },
        legend: {
          data: Object.keys(pollutantData), // 图例
          orient: 'vertical', // 图例竖着排列
          right: 10, // 图例距离右侧的距离
          top: 'middle', // 图例垂直居中
          selectedMode: false // 禁用图例点击交互
        },
        xAxis: {
          type: 'category',
          data: xAxisData,
          name: '时间'
        },
        yAxis: {
          type: 'value',
          name: '浓度值'
        },
        height: 220,
        series: series
      };

      // 渲染图表
      this.chart.setOption(option);
    },
    getColor(index) {
      // 预定义颜色列表
      const colors = [
        '#5470C6', // 蓝色
        '#91CC75', // 绿色
        '#EE6666', // 红色
        '#FAC858', // 黄色
        '#73C0DE', // 浅蓝色
        '#3BA272', // 深绿色
        '#FC8452', // 橙色
        '#9A60B4', // 紫色
        '#EA7CCC'  // 粉色
      ];
      return colors[index % colors.length]; // 循环使用颜色
    },
    // 下载 Excel
    downloadExcel() {
      if (this.tableData.length === 0) {
        this.dialogMessage = '没有数据可下载';
        this.dialogVisible = true; // 显示对话框
        return;
      }

      // 将表格数据转换为 Excel 工作表
      const worksheet = XLSX.utils.json_to_sheet(this.tableData);
      const workbook = XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(workbook, worksheet, '空气质量数据');

      // 生成 Excel 文件并下载
      XLSX.writeFile(workbook, '空气质量数据.xlsx');
      // this.$message.success('Excel 文件下载成功');
    },
    // 下载 CSV（UTF-8 带 BOM）
    downloadCSV() {
      if (this.tableData.length === 0) {
        this.dialogMessage = '没有数据可下载';
        this.dialogVisible = true; // 显示对话框
        return;
      }

      // 将表格数据转换为 CSV 格式
      const headers = Object.keys(this.tableData[0]).join(','); // 表头
      const rows = this.tableData.map(item =>
        Object.values(item).map(value => `"${value}"`).join(',') // 每行数据
      ).join('\n');

      const csvContent = `${headers}\n${rows}`;

      // 添加 BOM（\uFEFF）到文件开头
      const bom = '\uFEFF';
      const blob = new Blob([bom + csvContent], { type: 'text/csv;charset=utf-8;' });

      // 下载文件
      const link = document.createElement('a');
      link.href = URL.createObjectURL(blob);
      link.download = '空气质量数据.csv';
      link.click();
      // this.$message.success('CSV 文件下载成功');
    }
  },
  mounted() {
    // 初始化图表容器
    this.chart = echarts.init(this.$refs.chart);
  },
  beforeDestroy() {
    // 组件销毁时销毁图表实例
    if (this.chart) {
      this.chart.dispose();
    }
  }
};
</script>

<style scoped>
.demo-form-inline {
  margin-bottom: 2px;
}

.table-container {
  height: 240px;
  overflow-y: auto;
  border: 1px solid #ebeef5;
  overflow-x: hidden;
  border-radius: 10px;
}

/* 图表容器 */
.chart-container {
  width: 95%;
  height: 305px;
  border-radius: 10px;
}
</style>