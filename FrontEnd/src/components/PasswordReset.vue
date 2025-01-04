<template>
  <div class="password-reset-container">
    <!-- 表单和动图容器 -->
    <div class="form-gif-container">
      <!-- 密码重置表单 -->
      <el-form :model="passwordForm" :rules="rules" ref="passwordForm" label-width="120px" class="password-reset-form">
        <el-form-item label="旧密码" prop="oldPassword">
          <el-input type="password" v-model="passwordForm.oldPassword" placeholder="请输入旧密码"></el-input>
        </el-form-item>
        <el-form-item label="新密码" prop="newPassword">
          <el-input type="password" v-model="passwordForm.newPassword" placeholder="请输入新密码"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitForm" class="submit-button">提交</el-button>
          <el-button @click="resetForm" class="reset-button">清空</el-button>
        </el-form-item>
      </el-form>

      <!-- 动图 -->
      <div class="slogan-gif">
        <img src="/pass.gif" alt="安全提示" class="gif-image" />
      </div>
    </div>

    <!-- 成功提示对话框 -->
    <el-dialog v-model="successDialogVisible" title="提示">
      <span>密码重置成功！</span>
    </el-dialog>

    <!-- 失败提示对话框 -->
    <el-dialog v-model="errorDialogVisible" title="提示">
      <span>密码重置失败！</span>
    </el-dialog>

    <!-- 错误提示对话框 -->
    <el-dialog v-model="errorOccurredDialogVisible" title="提示">
      <span>密码重置时发生错误！</span>
    </el-dialog>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    // 密码验证规则
    const validatePassword = (rule, value, callback) => {
      if (!value) {
        callback(new Error('请输入新密码'));
      } else if (!/^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,20}$/.test(value)) {
        callback(new Error('密码必须为8到20位数字与字母组合'));
      } else {
        callback();
      }
    };

    return {
      passwordForm: {
        oldPassword: '',
        newPassword: '',
      },
      rules: {
        oldPassword: [
          { required: true, message: '请输入旧密码', trigger: 'blur' },
        ],
        newPassword: [
          { required: true, message: '请输入新密码', trigger: 'blur' },
          { validator: validatePassword, trigger: 'blur' }, // 自定义密码验证规则
        ],
      },
      successDialogVisible: false, // 控制成功提示对话框的显示
      errorDialogVisible: false, // 控制失败提示对话框的显示
      errorOccurredDialogVisible: false, // 控制错误提示对话框的显示
      userID: localStorage.getItem('id'),
    };
  },
  methods: {
    // 提交表单
    submitForm() {
      this.$refs.passwordForm.validate((valid) => {
        if (valid) {
          this.resetPassword();
        } else {
          return false;
        }
      });
    },
    // 重置表单
    resetForm() {
      this.$refs.passwordForm.resetFields();
    },
    // 提交密码重置请求
    async resetPassword() {
      try {
        // 从 localStorage 获取角色
        const role = localStorage.getItem('role');

        // 根据角色设置 RoleID
        let roleID;
        if (role === '用户') {
          roleID = 1; // 如果角色是 "用户"，设置 RoleID 为 1
        }

        const response = await axios.post('http://127.0.0.1:8000/api/password-reset/', {
          role_id: roleID, // 假设 RoleID 是从用户信息中获取的
          user_id: this.userID,
          old_password: this.passwordForm.oldPassword,
          new_password: this.passwordForm.newPassword,
        });
        this.successDialogVisible = true; // 显示成功提示对话框
        this.resetForm(); // 清空表单
      } catch (error) {
        if (error.response) {
          this.errorDialogVisible = true; // 显示失败提示对话框
        } else {
          this.errorOccurredDialogVisible = true; // 显示错误提示对话框
        }
      }
    }
  },
};
</script>

<style scoped>
.password-reset-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 50vh;
  margin-top: 120px;
  border-radius: 15px;
  background: linear-gradient(135deg, #f5faf8, #c3e2de);
  /* 渐变背景 */
  padding: 20px;
}

.form-gif-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
  max-width: 1000px;
  /* 调整容器最大宽度 */
}

.password-reset-form {
  width: 70%;
  /* 表单宽度 */
  background-color: #ffffff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.slogan-gif {
  width: 48%;
  /* 动图宽度 */
  text-align: center;
}

.gif-image {
  max-width: 50%;
  height: auto;
  border-radius: 10px;
  /* box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); */
}

.submit-button {
  width: 48%;
  background: linear-gradient(135deg, #048a68, #0eb475);
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

.reset-button {
  width: 48%;
  background: linear-gradient(135deg, #70807c, #9dbdb1);
  /* 渐变背景 */
  border: none;
  color: white;
  font-weight: bold;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.reset-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}
</style>