<template>
  <div class='page-container'>
    <div style='margin-bottom:60px'>
      <img src='/Logos/title2.png' style='width: 700px; margin-bottom: 40px; margin-top: 150px' alt='Logo'>
    </div>
    <div class="login-container">
      <div style="border: 1px solid #a3a3a3; padding: 10px; border-radius: 5px; background-color: rgba(255, 255, 255, 0.5); ">
        <div class='drop-down'>
          <p style='font-size: 15px; margin-right: 40px'>请选择登录角色</p>
          <el-select v-model="role" placeholder="身份" size="large" style="width: 100px">
            <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value" />
          </el-select>
        </div>
      </div>

      <div class='button-container'>
        <ShadowButton width='200px' height='50px' style="margin-bottom: 5px" @click="login">
          <p style='font-size: 20px'>Log in</p>
        </ShadowButton>
        <ShadowButton width='200px' height='50px' style="margin-top: 10px" @click="handleRegister">
          <p style='font-size: 20px'>Sign up</p>
        </ShadowButton>
      </div>
    </div>

    <el-dialog :model-value="dialogVisible1" title="提示" @close="dialogVisible1 = false">
      <span>监测员账号不能注册</span>
    </el-dialog>

    <el-dialog :model-value="dialogVisible2" title="提示" @close="dialogVisible2 = false">
      <span>研究员账号不能注册</span>
    </el-dialog>

    <el-dialog :model-value="dialogVisible3" title="提示" @close="dialogVisible3 = false">
      <span>请选择登录角色</span>
    </el-dialog>

  </div>
</template>

<script setup lang='ts'>

import ShadowButton from '@/components/ShadowButton.vue'
import { useRouter } from 'vue-router'
const router = useRouter()

import { ref } from 'vue'

// 控制弹窗显示的状态
const dialogVisible1 = ref(false)
const dialogVisible2 = ref(false)
const dialogVisible3 = ref(false)

const role = ref('')

const options = [
  {
    value: 'user',
    label: '用户',
  },
  {
    value: 'monitor',
    label: '监测员',
  },
  {
    value: 'researcher',
    label: '研究员',
  }
]

const login = () => {
  if (role.value === 'user') {
    router.push('/login')
    localStorage.setItem('role', '用户')
  } else if (role.value === 'monitor') {
    router.push('/login')
    localStorage.setItem('role', '监测员')
  } else if (role.value === 'researcher') {
    router.push('/login')
    localStorage.setItem('role', '研究员')
  } else {
    // 处理未选择角色的情况，例如提示用户
    dialogVisible3.value = true  // 显示弹窗
  }
}

const handleRegister = () => {
  if (role.value === 'user') {
    router.push('/register')
  } else if (role.value === 'monitor') {
    dialogVisible1.value = true  // 显示弹窗
  } else if (role.value === 'researcher') {
    dialogVisible2.value = true  // 显示弹窗
  }
  else {
    router.push('/register') // 不选注册默认到用户注册
  }
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
  padding: 20px; /* 内边距 */
  border-radius: 4px; /* 圆角 */
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1); /* 阴影 */
  background-color: rgba(255, 255, 255, 0.661); /* 背景颜色为白色 */
}

.drop-down {
  display: flex;
  flex-direction: row;

  justify-content: center;
  align-items: center;

}

.button-container {
  display: flex;
  margin-top: 20px;
  justify-content: center;
  align-items: center;
  flex-direction: column;
}

.example-showcase .el-dropdown-link {
  cursor: pointer;
  color: var(--el-color-primary);
  display: flex;
  align-items: center;
}
</style>
