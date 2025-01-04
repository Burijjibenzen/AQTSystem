<template>
  <div class='page-container'>
    <div class="form-wrapper">
      <el-form ref="ruleFormRef" style="max-width: 600px" :model="ruleForm" status-icon :rules="rules"
        label-width="auto" class="demo-ruleForm">
        
        <el-tag size="large">用户注册</el-tag>
        <el-button type="info" style="margin-left: 10px; width: 50px; height: 30px;" @click="back">返回</el-button>

        <el-form-item label="用户ID" prop="id" :error="idError">
          <p>请输入您想创建的用户id（8位纯数字）</p>
          <el-input v-model="ruleForm.id" type="id" autocomplete="off" />
        </el-form-item>

        <el-form-item label="密码" prop="pass">
          <p>请输入您的密码</p>
          <el-input v-model="ruleForm.pass" type="password" autocomplete="off" />
        </el-form-item>

        <el-form-item label="确认密码" prop="checkPass">
          <p>请再次确认您的密码</p>
          <el-input v-model="ruleForm.checkPass" type="password" autocomplete="off" />
        </el-form-item>

        <el-button type="primary" @click="submitForm(ruleFormRef)">确定</el-button>
        <el-button @click="resetForm(ruleFormRef)">重置</el-button>
      </el-form>
    </div>

    <el-dialog :model-value="dialogVisible" title="提示" @close="dialogVisible = false">
      <span>注册成功！</span>
    </el-dialog>
  </div>
</template>

<script setup lang='ts'>
import { reactive, ref } from 'vue';
import type { FormInstance, FormRules } from 'element-plus';
import { useRouter } from 'vue-router'
const router = useRouter()

const ruleFormRef = ref<FormInstance>();
const idError = ref('');
const dialogVisible = ref(false)

const back = () => {
  router.push('/welcome')
}
const checkid = (rule: any, value: any, callback: any) => {
  if (!value) {
    return callback(new Error('请输入用户id'));
  }

  // 确保所有字符都是数字并且长度为8
  if (typeof value !== 'string' || value.length !== 8 || !/^\d+$/.test(value)) {
    return callback(new Error('请输入8位纯数字'));
  }

  // 检查是否有前导0
  if (value[0] === '0') {
    return callback(new Error('用户id不能有前导0'));
  }

  callback(); // 通过验证
};

const validatePass = (rule: any, value: any, callback: any) => {
  if (value === '') {
    callback(new Error('请输入密码'));
  } else {
    // 检查密码是否为8到20位数字或字母组合
    if (!/^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,20}$/.test(value)) {
      callback(new Error('密码必须为8到20位数字与字母组合'));
    } else {
      if (ruleForm.checkPass !== '') {
        if (!ruleFormRef.value) return;
        ruleFormRef.value.validateField('checkPass');
      }
      callback();
    }
  }
}

const validatePass2 = (rule: any, value: any, callback: any) => {
  if (value === '') {
    callback(new Error('请再次输入密码'));
  } else if (value !== ruleForm.pass) {
    callback(new Error("两次输入的密码不一致！"));
  } else {
    callback();
  }
}

const ruleForm = reactive({
  id: '',
  pass: '',
  checkPass: '',
});

const rules = reactive<FormRules<typeof ruleForm>>({
  id: [{ validator: checkid, trigger: 'blur' }],
  pass: [{ validator: validatePass, trigger: 'blur' }],
  checkPass: [{ validator: validatePass2, trigger: 'blur' }],
});

const submitForm = (formEl: FormInstance | undefined) => {
  if (!formEl) return;
  formEl.validate((valid) => {
    if (valid) {
      // 清除之前的错误信息
      idError.value = '';

      // const url = 'http://localhost:3000/register';
      const url = 'http://127.0.0.1:8000/api/register/';
      console.log('Sending request to:', url); // 打印请求URL

      // 发送请求到后端进行注册
      fetch(url, {
        method: 'POST', // 确保使用POST请求
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          id: ruleForm.id,
          password: ruleForm.pass,
        }),
      })
        .then(response => {
          if (!response.ok) {
            return response.json().then(data => {
              throw new Error(data.message);
            });
          }
          return response.json();
        })
        .then(data => {
          if (data.success) {
            console.log('Registration successful:', data.message);
            // 处理注册成功后的逻辑
            dialogVisible.value = true;
            localStorage.setItem('role', '用户');
            setTimeout(() => {
              router.push('/login');
            }, 2000);
          } else {
            console.error('Registration failed:', data.message);
            // 处理注册失败后的逻辑
          }
        })
        .catch(error => {
          console.error('Error registering:', error);
          // 处理注册错误后的逻辑
          if (error.message.includes('ID已存在')) {
            idError.value = error.message;
          } else {
            alert(error.message);
          }
        });
    } else {
      console.log('error submit!');
    }
  });
};

const resetForm = (formEl: FormInstance | undefined) => {
  if (!formEl) return;
  formEl.resetFields();
  idError.value = '';
};
</script>

<style scoped>
.form-wrapper {
  padding: 20px;
  /* 内边距 */
  border-radius: 4px;
  /* 圆角 */
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  /* 阴影 */
  background-color: rgba(255, 255, 255, 0.661);
  /* 背景颜色为白色 */
}

.page-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background: url('/Logos/bg2.gif') no-repeat center center fixed;
  background-size: cover;
  height: 100vh;
  width: 100vw;
}

.custom-stepper {
  width: 1100px;
  height: 700px;
  margin: 70px auto 0;
  padding: 20px;
}

.custom-card {
  width: 100%;
  height: 100%;
  max-width: 600px;
  margin: 100px auto;
}

.input-spacing {
  margin-bottom: 20px;
  /* 增加输入框之间的间距 */
}

.confirm-button {
  display: block;
  /* 确保按钮是块级元素，以便对齐 */
  margin: 20px auto;
  /* 设置外边距以确保按钮在卡片底部居中对齐 */
  height: 40px;
  /* 设置按钮高度以对齐 */
}

.image-container {
  position: relative;
}

.full-width-image {
  width: 100%;
  position: fixed;
  top: 0;
  left: 0;
  z-index: 1;
}
</style>