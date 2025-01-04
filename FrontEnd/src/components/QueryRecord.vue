<template>
    <div class="details-container">

        <el-table :data="queryRecords" style="width: 100%" border height="260px">
            <el-table-column prop="RecordTime" label="查询时间" width="500" fixed />
            <el-table-column label="" width="auto">
                <template #default="{ row }">
                    <el-button type="success" size="small" @click="showDetails(row)">
                        查看详情
                    </el-button>
                    <el-button style="background-color:gainsboro;" size="small" @click="openDeleteDialog(row)">
                        删除
                    </el-button>
                </template>
            </el-table-column>
        </el-table>

    </div>

    <!-- 详情展示区域 -->
    <div class="details-container">
        <h3>查询详情</h3>
        <!-- 固定高度的表格容器 -->
        <div class="table-container">
            <el-table :data="tableData" style="width: 100%" height="100%">
                <el-table-column prop="station" label="监测站点" width="210" fixed></el-table-column>
                <el-table-column prop="pollutant" label="污染物" width="180" fixed></el-table-column>
                <el-table-column prop="value" label="浓度值" width="180" fixed></el-table-column>
                <el-table-column prop="time" label="时间" width="180" fixed></el-table-column>
            </el-table>
        </div>
    </div>

    <!-- 删除确认弹窗 -->
    <el-dialog :model-value="deleteDialogVisible" title="提示" @close="deleteDialogVisible = false">
        <span>确定要删除这条查询记录吗？</span>
        <template #footer>
            <el-button @click="deleteDialogVisible = false">取消</el-button>
            <el-button type="success" @click="confirmDelete">确定</el-button>
        </template>
    </el-dialog>

    <!-- 删除成功提示弹窗 -->
    <el-dialog v-model="deleteSuccessDialogVisible" title="提示">
        <span>查询记录删除成功！</span>
    </el-dialog>
</template>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            queryRecords: [], // 查询记录数据
            userID: localStorage.getItem('id'), // 从 localStorage 获取 UserID
            selectedRecord: null, // 当前选中的记录
            tableData: [], // 表格数据
            deleteDialogVisible: false, // 控制删除弹窗显示
            deleteSuccessDialogVisible: false, // 控制删除成功提示弹窗显示
            recordToDelete: null, // 待删除的记录
        };
    },
    created() {
        this.fetchQueryRecords();
    },
    methods: {
        async fetchQueryRecords() {
            try {
                const response = await axios.get('http://127.0.0.1:8000/api/query-records/', {
                    params: {
                        user_id: this.userID, // 将 UserID 作为查询参数发送
                    },
                });
                this.queryRecords = response.data;
            } catch (error) {
                console.error('获取查询记录失败', error);
            }
        },
        async showDetails(row) {
            // 提取所有 DataID
            const dataIds = row.Records.map(record => record.DataID);

            try {
                // 发送批量查询请求
                const response = await axios.post('http://127.0.0.1:8000/api/data-details/', {
                    data_ids: dataIds,
                });
                this.tableData = response.data; // 更新表格数据
            } catch (error) {
                console.error('获取详情失败', error);
            }

            // 显示详情区域
            this.selectedRecord = row;
        },
        openDeleteDialog(row) {
            // 打开删除确认弹窗，并存储待删除的记录
            console.log('待删除的记录:', row); // 打印 row 对象
            this.recordToDelete = row;
            this.deleteDialogVisible = true;
        },
        async confirmDelete() {
            try {
                this.deleteDialogVisible = false;
                // 发送删除请求
                await axios.post('http://127.0.0.1:8000/api/delete-record/', {
                    record_time: this.recordToDelete.RecordTime, // 发送 RecordTime
                });
                this.deleteSuccessDialogVisible = true; // 显示删除成功提示弹窗
                // 重新获取查询记录
                this.fetchQueryRecords();
            } catch (error) {
                console.error("删除记录失败");
            }
        },
    },
};
</script>

<style scoped>
.query-record-container {
    padding: 20px;
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.details-container {
    margin-top: 20px;
    padding: 20px;
    background-color: #f9f9f9;
    border-radius: 8px;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

h3 {
    margin-bottom: 16px;
    color: #333;
}

.table-container {
    height: 270px;
    /* 固定高度 */
    overflow: auto;
    /* 允许滚动 */
}
</style>