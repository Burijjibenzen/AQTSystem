<template>
  <div class='page-container'>

    <div style='margin-bottom:60px'>
      <img src='/Logos/title2.png' style='width: 700px; margin-top: 100px' alt='Logo'>
    </div>
    <div class="login-container">
      <el-tag size="large">{{ rolename }}登录</el-tag>
      <el-button type="info" style="margin-left: 10px; width: 50px; height: 30px;" @click="back">返回</el-button>
      <div class='input-container'>
        <el-icon :size="40">
          <User />
        </el-icon>
        <el-input v-model="input_id" style="width: 300px; height: 40px; margin-left: 20px;" placeholder="请输入ID" />
      </div>


      <div class='input-container'>
        <el-icon :size="40">
          <Lock />
        </el-icon>
        <el-input v-model="input_password" type="password" style="width: 300px; height: 40px; margin-left: 20px;" placeholder="请输入密码" />
      </div>


      <div class='button-container'>
        <ShadowButton width='200px' height='50px' style='margin-left: 50px' @click="handleLogin">
          <p style='font-size: 20px;'>Log in</p>
        </ShadowButton>
      </div>
    </div>

    <el-dialog :model-value="dialogVisible1" title="提示" @close="dialogVisible1 = false">
      <span>请输入ID！</span>
    </el-dialog>

    <el-dialog :model-value="dialogVisible2" title="提示" @close="dialogVisible2 = false">
      <span>请输入密码！</span>
    </el-dialog>

    <el-dialog :model-value="dialogVisible3" title="提示" @close="dialogVisible3 = false">
      <span>登录成功！</span>
    </el-dialog>

    <el-dialog :model-value="dialogVisible4" title="提示" @close="dialogVisible4 = false">
      <span>ID不存在！</span>
    </el-dialog>

    <el-dialog :model-value="dialogVisible5" title="提示" @close="dialogVisible5 = false">
      <span>密码错误！</span>
    </el-dialog>

  </div>
</template>

<script setup lang='ts'>
import { Lock, User } from '@element-plus/icons-vue'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const input_id = ref('')
const input_password = ref('')
const router = useRouter()
const rolename = localStorage.getItem('role')
const dialogVisible1 = ref(false)
const dialogVisible2 = ref(false)
const dialogVisible3 = ref(false)
const dialogVisible4 = ref(false)
const dialogVisible5 = ref(false)

const back = () => {
  router.push('/welcome')
}
const handleLogin = async () => {
  if (!input_id.value) {
    //ElMessageBox.alert('Please enter ID')
    dialogVisible1.value = true;
    return
  }
  if (!input_password.value) {
    //ElMessageBox.alert('Please enter password')
    dialogVisible2.value = true;
    return
  }

  const url = 'http://127.0.0.1:8000/api/login/'
  console.log('Sending request to:', url) // 打印请求URL

  // 发送请求到后端进行登录
  fetch(url, {
    method: 'POST', // 确保使用POST请求
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      id: input_id.value,
      password: input_password.value,
      role: rolename,
    }),
  })
    .then(response => {
      if (!response.ok) {
        return response.json().then(data => {
          throw new Error(data.message)
        })
      }
      return response.json()
    })
    .then(data => {
      if (data.success) {
        // ElMessageBox.alert('login succeed')
        dialogVisible3.value = true;
        setTimeout(() => {
          localStorage.setItem('id', input_id.value);
          router.push('/home');
        }, 2000);
      } else {
        // ElMessageBox.alert(data.message)
        alert(data.message)
      }
    })
    .catch(error => {
      console.error('Error logging in:', error)
      //  ElMessageBox.alert(error.message)
      if (error.message === 'No such ID') {
        dialogVisible4.value = true;
      }
      else {
        dialogVisible5.value = true;
      }
    })
}

</script>

<style scoped>
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

.login-container {
  padding: 20px;
  /* 内边距 */
  border-radius: 4px;
  /* 圆角 */
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  /* 阴影 */
  background-color: rgba(255, 255, 255, 0.661);
  /* 背景颜色为白色 */
}

.input-container {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  margin-top: 30px;
}

.button-container {
  display: flex;
  flex-direction: column;
  margin-top: 30px;
  justify-content: center;
  align-items: center;

}
</style>
