<template>
    <div class="feedback-container">
        <!-- 上下浮动的 Slogan -->
        <div class="slogan">
            <span class="slogan-text">用户的反馈是我们进步的动力</span>
        </div>
        <div class="details-container">


            <el-table :data="advices" style="width: 100%" stripe height="260px">
                <el-table-column prop="AdviceID" label="反馈ID" width="100" fixed />
                <el-table-column prop="UserID" label="用户ID" width="100" fixed />
                <el-table-column prop="Content" label="反馈内容" width="650" fixed />
                <el-table-column prop="AdviceTime" label="反馈时间" width="200" fixed />
            </el-table>
        </div>
    </div>
</template>

<script>
import axios from "axios";

export default {
    data() {
        return {
            advices: [], // 存储反馈数据
        };
    },
    created() {
        this.fetchAdvices();
    },
    methods: {
        async fetchAdvices() {
            try {
                const response = await axios.get("http://127.0.0.1:8000/api/advices/"); // 调用后端 API
                this.advices = response.data;
            } catch (error) {
                console.error("获取反馈数据失败:", error);
                // this.$message.error("获取反馈数据失败，请稍后重试");
            }
        },
    },
};
</script>

<style scoped>
.details-container {
    margin-top: 20px;
    padding: 20px;
    background-color: #f9f9f9;
    border-radius: 8px;
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
    width: 1100px;
}

.feedback-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 50vh;
    margin-top: 120px;
    border-radius: 15px;
    background: linear-gradient(135deg, #f5f7fa, #c3cfe2);
    /* 渐变背景 */
    padding: 20px;
}

.slogan {
    font-size: 28px;
    font-weight: bold;
    color: #303133;
    margin-top: 30px;
    margin-bottom: 30px;
    text-align: center;
    background: linear-gradient(135deg, #6a11cb, #2575fc);
    /* 渐变背景 */
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: float 3s ease-in-out infinite;
}

@keyframes float {

    0%,
    100% {
        transform: translateY(0);
    }

    50% {
        transform: translateY(-10px);
    }
}

.slogan-text {
    display: inline-block;
}
</style>