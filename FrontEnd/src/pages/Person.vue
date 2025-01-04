<template>
  <el-container>
    <el-aside :style="{ width: isCollapse ? 'fit-content' : '250px' }">
      <div class="logo">个人中心</div>
      <el-menu>
        <div>
          <el-menu-item :class="{ 'is-active': activeMenu === 'password-reset' }" @click="showPasswordReset">
            <el-icon>
              <House />
            </el-icon>修改密码
          </el-menu-item>
          <el-menu-item v-if="role === '用户'" :class="{ 'is-active': activeMenu === 'record' }" @click="showAnalysisQuery">
            <el-icon>
              <User />
            </el-icon>查询记录
          </el-menu-item>
        </div>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header>
        <p style="display: inline; font-weight: bold; color: white; width: 200px; margin-left: 50px;"> {{role}} ID {{ id }}</p>
        <el-button type="info" @click="backHome" style="margin-right: 100px;">
          返回主页
        </el-button>
      </el-header>
      <el-main>
        <PasswordReset v-if="activeMenu === 'password-reset'" />
        <QueryRecord v-if="activeMenu === 'record'" />
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
import PasswordReset from '@/components/PasswordReset.vue';
import QueryRecord from '@/components/QueryRecord.vue';

export default {
  components: {
    PasswordReset,
    QueryRecord,
  },
  data() {
    return {
      activeMenu: 'password-reset', // 当前激活的菜单项
      id: localStorage.getItem('id'),
      role: localStorage.getItem('role'),
    };
  },
  methods: {
    backHome() {
      this.$router.push('/home');
    },
    showPasswordReset() {
      this.activeMenu = 'password-reset';
    },
    showAnalysisQuery() {
      this.activeMenu = 'record';
    },
  },
};
</script>

<style scoped>
.el-container {
  height: 95vh;
}

.el-aside {
  color: #fff;
  z-index: 10;
  box-shadow: 2px 0 6px rgba(0, 21, 41, 0.35);
  background: rgb(151, 227, 228);
  background: linear-gradient(0deg, rgba(162, 215, 174, 1) 0%, rgba(54, 102, 88, 1) 100%);
  border-radius: 10px;
}

.el-header {
  line-height: 60px;
  padding: 0 10px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: #003233;
  z-index: 9;
  box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);
  border-radius: 10px;
}

.el-main {
  background-color: #e2f3ed;
  position: relative;
  margin-bottom: 50px;
  border-radius: 2px;
}

.el-menu {
  border: none;
}

.el-menu-item.is-active {
  background-color: #004539 !important;
}

.el-menu-item {
  background-color: rgb(49, 94, 80);
  color: #c1ede0;
}

.el-menu-item:hover {
  color: #fff !important;
}

.logo {
  height: 60px;
  line-height: 60px;
  text-align: center;
}
</style>