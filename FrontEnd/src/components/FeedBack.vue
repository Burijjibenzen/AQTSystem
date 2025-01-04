<template>
    <div class="feedback-container">
        <!-- 动态 Slogan -->
        <div class="slogan">
            <span class="slogan-text">{{ sloganText }}</span>
            <span class="cursor">|</span>
        </div>

        <el-form :model="feedbackForm" label-width="100px" class="feedback-form">
            <el-form-item label="反馈内容">
                <el-input v-model="feedbackForm.content" type="textarea" :rows="5" placeholder="请输入您的反馈内容"></el-input>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="submitFeedback" class="submit-button">提交反馈</el-button>
            </el-form-item>
        </el-form>

        <!-- 成功提示对话框 -->
        <el-dialog v-model="successDialogVisible" title="提示">
            <span>反馈提交成功！</span>
        </el-dialog>

        <!-- 失败提示对话框 -->
        <el-dialog v-model="errorDialogVisible" title="提示">
            <span>反馈提交失败！</span>
        </el-dialog>

        <!-- 错误提示对话框 -->
        <el-dialog v-model="errorOccurredDialogVisible" title="提示">
            <span>提交反馈时发生错误！</span>
        </el-dialog>

        <!-- 空内容提示对话框 -->
        <el-dialog v-model="emptyContentDialogVisible" title="提示">
            <span>反馈内容不能为空！</span>
        </el-dialog>
    </div>
</template>

<script>
import axios from 'axios';
import { SuccessFilled, WarningFilled } from '@element-plus/icons-vue'; // 引入图标

export default {
    props: {
        userId: {
            type: String, // 假设 userId 是字符串类型
            required: true // 确保 userId 是必传的
        }
    },
    data() {
        return {
            feedbackForm: {
                content: '' // 反馈内容
            },
            successDialogVisible: false, // 控制成功提示对话框的显示
            errorDialogVisible: false, // 控制失败提示对话框的显示
            errorOccurredDialogVisible: false, // 控制错误提示对话框的显示
            emptyContentDialogVisible: false, // 控制空内容提示对话框的显示
            sloganText: '', // Slogan 文字
            sloganFullText: '您的反馈是对我们最好的支持', // 完整的 Slogan
            typingInterval: null // 用于存储定时器
        };
    },
    mounted() {
        this.startTyping(); // 启动 Slogan 打字机效果
    },
    beforeUnmount() {
        // 组件销毁时清除定时器
        if (this.typingInterval) {
            clearInterval(this.typingInterval);
        }
    },
    methods: {
        // 启动打字机效果
        startTyping() {
            let index = 0;
            const typingSpeed = 150; // 打字速度（每 100ms 打一个字）

            this.typingInterval = setInterval(() => {
                if (index < this.sloganFullText.length) {
                    this.sloganText += this.sloganFullText[index];
                    index++;
                } else {
                    this.sloganText = ''; // 清空内容
                    index = 0; // 重置索引
                }
            }, typingSpeed);
        },
        // 提交反馈
        async submitFeedback() {
            if (!this.feedbackForm.content) {
                this.emptyContentDialogVisible = true; // 显示空内容提示对话框
                return;
            }

            try {
                const response = await axios.post('http://127.0.0.1:8000/api/advice/', {
                    UserID: this.userId, // 使用 this.userId
                    Content: this.feedbackForm.content // 反馈内容
                });

                // 确保后端返回的响应中包含 status 字段
                if (response.data && response.data.status === 'success') {
                    this.successDialogVisible = true; // 显示成功提示对话框
                    this.feedbackForm.content = ''; // 清空表单
                } else {
                    this.errorDialogVisible = true; // 显示失败提示对话框
                }
            } catch (error) {
                // 打印完整的错误信息
                console.error('提交反馈时发生错误:', error);
                this.errorOccurredDialogVisible = true; // 显示错误提示对话框
            }
        }
    }
};
</script>

<style scoped>
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

.cursor {
    display: inline-block;
    animation: blink 1s infinite;
}

@keyframes blink {

    0%,
    100% {
        opacity: 1;
    }

    50% {
        opacity: 0;
    }
}

.feedback-form {
    max-width: 800px;
    width: 100%;
    background-color: #ffffff;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.submit-button {
    width: 100%;
    background: linear-gradient(135deg, #043c8a, #2575fc);
    /* 渐变背景 */
    border: none;
    color: white;
    font-weight: bold;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.submit-button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.dialog-icon {
    margin-right: 10px;
    font-size: 24px;
}

.el-table {
    margin-top: 20px;
}
</style>