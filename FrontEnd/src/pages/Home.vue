<template>
  <el-container>
    <el-aside :style="{ width: isCollapse ? 'fit-content' : '250px' }">
      <div class="logo">城市空气质量智慧查询系统</div>
      <el-menu>
        <div>
          <el-menu-item v-if="role === '用户'" :class="{ 'is-active': activeMenu === 'air-quality-query' }"
            @click="showAirQualityQuery">
            <el-icon>
              <House />
            </el-icon>空气质量数据查询
          </el-menu-item>
          <el-menu-item v-if="role === '用户'" :class="{ 'is-active': activeMenu === 'analysis-query' }"
            @click="showAnalysisQuery">
            <el-icon>
              <User />
            </el-icon>空气质量分析结果查询
          </el-menu-item>
          <el-menu-item v-if="role === '用户'" :class="{ 'is-active': activeMenu === 'feedback' }" @click="showFeedback">
            <el-icon>
              <User />
            </el-icon>意见反馈
          </el-menu-item>
          <!-- 监测员专属菜单项 -->
          <el-menu-item v-if="role === '监测员'" :class="{ 'is-active': activeMenu2 === 'data-manage' }"
            @click="showDataManage">
            <el-icon>
              <Upload />
            </el-icon>监测数据与站点管理
          </el-menu-item>

          <el-menu-item v-if="role === '研究员'" :class="{ 'is-active': activeMenu3 === 'analysis-manage' }"
            @click="showAnalysisManage">
            <el-icon>
              <Upload />
            </el-icon>空气质量分析结果管理
          </el-menu-item>

          <el-menu-item v-if="role === '监测员' || role === '研究员'" :class="{ 'is-active': activeMenu2 === 'rcv-feedback' && role === '监测员' || activeMenu3 === 'rcv-feedback' && role === '研究员'}"
            @click="showReceiveFeedBack">
            <el-icon>
              <Monitor />
            </el-icon>查看反馈
          </el-menu-item>

        </div>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header>
        <el-dropdown style="cursor: pointer;height:80%;display: flex;line-height: 60px;margin-left: 1100px;">
          <div style="padding: 0 10px;display: flex;align-items: center;justify-content: center;">
            <el-avatar :size="30"
              src="https://gw.alipayobjects.com/zos/antfincdn/XAosXuNZyF/BiazfanxmamNRoxxVxka.png" />
            <span style="margin-left:10px;color:#909399;">{{ userInfo }}</span>
          </div>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item @click="toPerson">个人设置</el-dropdown-item>
              <el-dropdown-item divided @click="quitLogin">退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </el-header>
      <el-main>
        <!-- 动态显示空气质量查询组件 -->
        <AirQualityQuery v-if="isAirQualityQueryVisible && role === '用户'" />
        <FeedBack v-if="isFeedBackVisible && role === '用户'" :userId="userId" />
        <AnalysisQuery v-if="isAnalysisQueryVisible && role === '用户'" />
        <ReceiveFeedBack v-if="isReceiveFeedBackVisible && role !== '用户'" />
        <DataManage v-if="isDataManageVisible && role === '监测员'" />
        <AnalysisManage v-if="isAnalysisManageVisible && role === '研究员'" />
        <router-view v-else />
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
import AirQualityQuery from '@/components/AirQualityQuery.vue'; // 引入空气质量查询组件
import FeedBack from '@/components/FeedBack.vue'; // 引入意见反馈组件
import AnalysisQuery from '@/components/AnalysisQuery.vue'; // 引入空气质量分析结果查询组件
import ReceiveFeedBack from '@/components/ReceiveFeedBack.vue';
import DataManage from '@/components/DataManage.vue';
import AnalysisManage from '@/components/AnalysisManage.vue';

export default {
  components: {
    AirQualityQuery,
    FeedBack,
    AnalysisQuery,
    ReceiveFeedBack,
    DataManage,
    AnalysisManage
  },
  data() {
    return {
      userInfo: '',
      userId: '',
      role: '用户', // 默认角色为用户
      isAirQualityQueryVisible: true, // 控制空气质量查询组件的显示
      isFeedBackVisible: false, // 控制意见反馈组件的显示
      isAnalysisQueryVisible: false, // 控制空气质量分析结果查询组件的显示
      isReceiveFeedBackVisible: false, // 控制监测员仪表盘组件的显示
      isDataManageVisible: true, // 控制数据上传组件的显示
      isAnalysisManageVisible: true, // 控制空气质量分析结果管理组件的显示
      activeMenu: 'air-quality-query', // 默认高亮的菜单项
      activeMenu2: 'data-manage',
      activeMenu3: 'analysis-manage'
    };
  },
  created() {
    this.userInfo = localStorage.getItem('userInfo');
    this.userId = localStorage.getItem('id');
    this.role = localStorage.getItem('role') || '用户'; // 获取用户角色，默认为用户
  },
  methods: {
    toPerson() {
      this.$router.push('/person')
    },
    quitLogin() {
      localStorage.clear();
      this.$router.push('/welcome');
    },
    showAirQualityQuery() {
      this.activeMenu = 'air-quality-query';
      this.isAirQualityQueryVisible = true; // 显示空气质量查询组件
      this.isAnalysisQueryVisible = false;
      this.isFeedBackVisible = false;
      this.isReceiveFeedBackVisible = false;
      this.isDataManageVisible = false;
      this.isAnalysisManageVisible = false;
    },
    showAnalysisQuery() {
      this.activeMenu = 'analysis-query';
      this.isAirQualityQueryVisible = false; // 隐藏空气质量查询组件
      this.isAnalysisQueryVisible = true; // 显示空气质量分析结果查询组件
      this.isFeedBackVisible = false;
      this.isReceiveFeedBackVisible = false;
      this.isDataManageVisible = false;
      this.isAnalysisManageVisible = false;
    },
    showFeedback() {
      this.activeMenu = 'feedback';
      this.isAirQualityQueryVisible = false; // 隐藏空气质量查询组件
      this.isAnalysisQueryVisible = false;
      this.isFeedBackVisible = true; // 显示意见反馈组件
      this.isReceiveFeedBackVisible = false;
      this.isDataManageVisible = false;
      this.isAnalysisManageVisible = false;
    },
    showReceiveFeedBack() {
      this.activeMenu2 = 'rcv-feedback';
      this.activeMenu3 = 'rcv-feedback';
      this.isAirQualityQueryVisible = false;
      this.isAnalysisQueryVisible = false;
      this.isFeedBackVisible = false;
      this.isReceiveFeedBackVisible = true; // 显示监测员仪表盘组件
      this.isDataManageVisible = false;
      this.isAnalysisManageVisible = false;
    },
    showDataManage() {
      this.activeMenu2 = 'data-manage';
      this.isAirQualityQueryVisible = false;
      this.isAnalysisQueryVisible = false;
      this.isFeedBackVisible = false;
      this.isReceiveFeedBackVisible = false;
      this.isDataManageVisible = true; // 显示数据上传组件
      this.isAnalysisManageVisible = false;
    },
    showAnalysisManage() {
      this.activeMenu3 = 'analysis-manage';
      this.isAirQualityQueryVisible = false;
      this.isAnalysisQueryVisible = false;
      this.isFeedBackVisible = false;
      this.isReceiveFeedBackVisible = false;
      this.isDataManageVisible = false;
      this.isAnalysisManageVisible = true; // 显示空气质量分析结果管理组件
    },
  }
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
  background: linear-gradient(0deg, rgba(151, 227, 228, 1) 0%, rgba(33, 34, 124, 1) 100%);
  border-radius: 10px;
}

.el-header {
  line-height: 60px;
  padding: 0 10px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: #09004a;
  z-index: 9;
  box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);
  border-radius: 10px;
}

.el-main {
  background-color: #e2e9f3;
  position: relative;
  margin-bottom: 50px;
  border-radius: 2px;
}

.el-menu {
  border: none;
}

.el-menu-item.is-active {
  background-color: #0a0265 !important;
}

.el-menu-item {
  background-color: #21227c;
  color: #c1d3ed
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