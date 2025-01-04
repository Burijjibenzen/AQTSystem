<template>
    <div class="container">
        <el-card class="add-data-container">
            <el-form :model="dataForm" label-width="120px" class="data-form">
                <el-form-item label="监测站点">
                    <el-select v-model="dataForm.StationID" placeholder="请选择监测站点">
                        <el-option v-for="station in stations" :key="station.StationID" :label="station.StationName"
                            :value="station.StationID" />
                    </el-select>
                </el-form-item>
                <el-form-item label="监测指标">
                    <el-select v-model="dataForm.IndicatorID" placeholder="请选择监测指标">
                        <el-option v-for="indicator in indicators" :key="indicator.IndicatorID"
                            :label="indicator.IndicatorName" :value="indicator.IndicatorID" />
                    </el-select>
                </el-form-item>
                <el-form-item label="监测时间">
                    <el-date-picker v-model="dataForm.DataTime" type="datetime" placeholder="选择监测时间" />
                </el-form-item>
                <el-form-item label="监测值">
                    <el-input v-model="dataForm.Value" placeholder="请输入监测值" />
                </el-form-item>
                <el-form-item>
                    <div style="display: flex;">
                        <el-button type="primary" @click="showConfirmDialog">提交</el-button>
                        <p style="font-size:0.8em; color: midnightblue; margin-left: 15px;">注意*
                            各指标单位：PM2.5（μg/m³）PM10（μg/m³）O3（μg/m³）SO2（μg/m³）CO（mg/m³）</p>
                    </div>
                </el-form-item>
            </el-form>

            <!-- 提交确认对话框 -->
            <el-dialog :model-value="confirmDialogVisible" title="提示" @close="confirmDialogVisible = false">
                <span>确定要提交这条监测数据吗？</span>
                <template #footer>
                    <el-button @click="confirmDialogVisible = false">取消</el-button>
                    <el-button type="primary" @click="confirmSubmit">确定</el-button>
                </template>
            </el-dialog>

            <!-- 成功提示对话框 -->
            <el-dialog v-model="successDialogVisible" title="提示">
                <span>数据提交成功！</span>
            </el-dialog>

            <!-- 失败提示对话框 -->
            <el-dialog v-model="errorDialogVisible" title="提示">
                <span>数据提交失败！</span>
            </el-dialog>

            <!-- 填写完整信息提示对话框 -->
            <el-dialog v-model="incompleteDialogVisible" title="提示">
                <span>请填写完整信息！</span>

            </el-dialog>
        </el-card>

        <!-- 右侧 GIF 图片 -->
        <div class="gif-container">
            <img src="/Logos/global.gif" alt="GIF 图片" class="gif-image" />
        </div>
    </div>

    <!-- 站点管理模块 -->
    <el-card class="station-management-container">
      <h3 style="margin-bottom: 10px;">站点管理</h3>
      <div class="station-list">
        <el-row :gutter="20">
          <el-col :span="12" v-for="station in allstations" :key="station.StationID">
            <div class="station-item">
              <span>{{ station.StationName }}</span>
              <el-switch v-model="station.isValid" @change="updateStationStatus(station)" />
            </div>
          </el-col>
        </el-row>
      </div>
    </el-card>
</template>

<script>
import axios from "axios";

export default {
    data() {
        return {
            dataForm: {
                StationID: "", // 监测站点 ID
                IndicatorID: "", // 监测指标 ID
                DataTime: "", // 监测时间
                Value: "", // 监测值
            },
            stations: [], // 监测站点列表
            allstations: [], // 所有（包括未启用）
            indicators: [], // 监测指标列表
            confirmDialogVisible: false, // 控制提交确认对话框的显示
            successDialogVisible: false, // 控制成功提示对话框的显示
            errorDialogVisible: false, // 控制失败提示对话框的显示
            incompleteDialogVisible: false, // 控制填写完整信息提示对话框的显示
        };
    },
    created() {
        this.fetchStations();
        this.fetchAllStations();
        this.fetchIndicators();
    },
    methods: {
        // 获取监测站点列表
        async fetchStations() {
            try {
                const response = await axios.get("http://127.0.0.1:8000/api/stations/");
                this.stations = response.data;
            } catch (error) {
                console.error("获取监测站点失败:", error);
                // this.$message.error("获取监测站点失败，请稍后重试");
            }
        },
        async fetchAllStations() {
            try {
                const response = await axios.get("http://127.0.0.1:8000/api/all-stations/");
                this.allstations = response.data;
            } catch (error) {
                console.error("获取监测站点失败:", error);
                // this.$message.error("获取监测站点失败，请稍后重试");
            }
        },
        // 获取监测指标列表
        async fetchIndicators() {
            try {
                const response = await axios.get("http://127.0.0.1:8000/api/indicators/");
                this.indicators = response.data;
            } catch (error) {
                console.error("获取监测指标失败:", error);
                // this.$message.error("获取监测指标失败，请稍后重试");
            }
        },
        // 显示提交确认对话框
        showConfirmDialog() {
            if (
                !this.dataForm.StationID ||
                !this.dataForm.IndicatorID ||
                !this.dataForm.DataTime ||
                !this.dataForm.Value
            ) {
                this.incompleteDialogVisible = true; // 显示填写完整信息提示对话框
                return;
            }
            this.confirmDialogVisible = true; // 显示确认对话框
        },
        // 提交监测数据
        async confirmSubmit() {
            this.confirmDialogVisible = false; // 关闭确认对话框

            try {
                this.dataForm.DataTime.setHours(this.dataForm.DataTime.getHours() + 8);
                const response = await axios.post("http://127.0.0.1:8000/api/data/", this.dataForm);
                if (response.data && response.data.status === "success") {
                    this.successDialogVisible = true; // 显示成功提示对话框
                    this.dataForm = {
                        StationID: "",
                        IndicatorID: "",
                        DataTime: "",
                        Value: "",
                    }; // 清空表单
                } else {
                    this.errorDialogVisible = true; // 显示失败提示对话框
                }
            } catch (error) {
                console.error("提交数据失败:", error);
                this.errorDialogVisible = true; // 显示失败提示对话框
            }
        },
        async updateStationStatus(station) {
            try {
                // 使用 POST 请求更新站点状态
                const response = await axios.post(
                    "http://127.0.0.1:8000/api/station-management/",
                    { StationID: station.StationID, isValid: station.isValid }
                );

                if (response.data && response.data.status === "success") {
                    // this.$message.success("站点状态更新成功！");

                    // 更新本地数据
                    const index = this.allstations.findIndex(s => s.StationID === station.StationID);
                    if (index !== -1) {
                        this.allstations[index].isValid = station.isValid;
                    }

                    this.fetchStations();

                } else {
                    console.error("更新站点状态失败");
                }
            } catch (error) {
                console.error("更新站点状态失败:", error);
                // this.$message.error("更新站点状态失败，请稍后重试");
            }
        }
    },
};
</script>

<style scoped>
/* 外层容器 */
.container {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin: 20px;
}

/* 表单容器 */
.add-data-container {
  flex: 1;
  padding: 20px;
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  margin-right: 20px;
  height: 300px;
}

.data-form {
  max-width: 800px;
}

/* GIF 图片容器 */
.gif-container {
  width: 400px;
  height: auto;
  border-radius: 8px;
  overflow: hidden;
}

/* GIF 图片 */
.gif-image {
  width: 100%;
  height: auto;
  border-radius: 8px;
}

/* 站点管理容器 */
.station-management-container {
  margin-top: 10px;
  margin-left: 20px;
  width: 96.5%;
}

/* 站点条目样式 */
.station-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  border: 1px solid #ebeef5;
  border-radius: 4px;
  margin-bottom: 10px;
  background-color: #fafafa;
}

.station-item span {
  font-size: 14px;
  color: #606266;
}

.station-list {
  height: 270px; /* 固定高度 */
  overflow-y: auto; /* 添加垂直滚动条 */
  padding-right: 10px; /* 避免滚动条遮挡内容 */
}
</style>