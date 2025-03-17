<template>
  <div class="container">
    <!-- 1. 项目标题 -->
    <header class="header">
      <h1>BiliNews</h1>
      <p>B站视频智能分析平台</p>
    </header>

    <!-- 2. 检索按钮 -->
    <div class="search-button-section">
      <el-button 
        type="primary" 
        size="large" 
        :loading="loading" 
        @click="startAnalysis"
        class="main-search-button"
      >
        {{ loading ? '分析中...' : '开始分析' }}
      </el-button>
    </div>

    <!-- 3. 可折叠的配置面板 -->
    <el-collapse v-model="activeCollapse">
      <el-collapse-item title="配置信息" name="config">
        <el-form :model="form" label-width="120px">
          <el-form-item label="B站用户UID">
            <el-input v-model="form.uid" placeholder="请输入UP主的UID" />
          </el-form-item>
          
          <el-form-item label="B站Cookie">
            <el-input 
              v-model="form.cookie" 
              type="textarea" 
              placeholder="请输入B站Cookie"
              :rows="3"
            />
          </el-form-item>
          
          <el-form-item label="OpenRouter Key">
            <el-input v-model="form.apiKey" placeholder="请输入OpenRouter API Key" />
          </el-form-item>
          
          <el-form-item label="页面范围">
            <el-row :gutter="20">
              <el-col :span="11">
                <el-input-number v-model="form.startPage" :min="1" label="起始页" />
              </el-col>
              <el-col :span="2" class="text-center">至</el-col>
              <el-col :span="11">
                <el-input-number v-model="form.endPage" :min="1" label="结束页" />
              </el-col>
            </el-row>
          </el-form-item>
        </el-form>
      </el-collapse-item>
    </el-collapse>

    <!-- 4. 结果展示区域 -->
    <!-- 修改结果展示区域为单列滚动布局 -->
    <div 
      v-if="results.length" 
      class="results-section"
      v-loading="loading"
    >
      <div class="results-scroll">
        <el-timeline>
          <el-timeline-item
            v-for="(result, index) in results"
            :key="index"
            :timestamp="result.video_info.title"
            placement="top"
          >
            <el-card>
              <div class="video-info">
                <div class="video-details">
                  <h3>{{ result.video_info.title }}</h3>
                  <p>时长: {{ result.video_info.duration }}</p>
                  <el-link :href="result.video_info.url" target="_blank" type="primary">
                    观看视频
                  </el-link>
                </div>
              </div>
              
              <div class="analysis-content">
                <h4>AI 分析</h4>
                <p><strong>内容概述：</strong>{{ result.analysis.video_analysis.summary }}</p>
              </div>
            </el-card>
          </el-timeline-item>
        </el-timeline>
      </div>
    </div>
  </div>
</template>

<style scoped>
.container {
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: stretch;
  min-height: 100vh;
  box-sizing: border-box;
  position: relative;  /* 添加相对定位 */
}

.header {
  text-align: center;
  padding: 40px 0;
  width: 100%;
}

.header h1 {
  font-size: 2.8em;
  color: #00a1d6;
  margin-bottom: 10px;
}

.header p {
  font-size: 1.2em;
  color: #666;
}

.search-button-section {
  text-align: center;
  margin: 30px 0;
  width: 100%;
  display: flex;  /* 添加 flex 布局 */
  justify-content: center;  /* 添加水平居中 */
}
.main-search-button {
  padding: 20px 60px;
  font-size: 1.2em;
}

.el-collapse {
  width: 60%; /* 改为 100%，撑满容器 */
  max-width: 1000px; /* 与 container 一致 */
  margin: 0 auto 30px;
}

:deep(.el-form) {
  width: 100%;  /* 修改表单宽度 */
  max-width: 600px;  /* 添加最大宽度限制 */
  margin: 0 auto;
}

:deep(.el-form-item) {
  margin-bottom: 22px;  /* 增加表单项间距 */
}

:deep(.el-collapse-item__content) {
  padding: 20px;  /* 增加内边距 */
}

:deep(.el-input), 
:deep(.el-input-number) {
  width: 100%;  /* 确保输入框占满宽度 */
}

/* 确保时间线内容居中 */
:deep(.el-timeline) {
  width: 100%;  /* 修改为100% */
  padding: 0;   /* 移除内边距 */
}

:deep(.el-timeline-item__content) {
  width: 100%;
}

:deep(.el-card) {
  width: 100%;
  margin-bottom: 20px;  /* 增加卡片间距 */
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);  /* 轻微阴影 */
}

/* 删除重复的 .video-info 定义，保留这一个 */
.video-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 20px;
  width: 100%;
}

/* 删除重复的 .analysis-content 定义，保留这一个 */
.analysis-content {
  width: 100%;
  margin-top: 20px;
  padding: 20px;
  border-top: 1px solid #eee;
  background-color: #f8f9fa;
  border-radius: 8px;
}

/* 结果区域样式优化 */
.results-section {
  width: 100%;
  max-width: 800px;
  margin: 30px auto 0;
  align-self: center;
  position: relative;  /* 添加相对定位 */
  z-index: 1;  /* 设置较低的层级 */
}

.header {
  text-align: center;
  padding: 40px 0;
  width: 100%;
  position: relative;  /* 添加相对定位 */
  z-index: 2;  /* 设置较高的层级，确保在结果区域之上 */
  background-color: #fff;  /* 添加背景色 */
}

.results-scroll {
  max-height: calc(100vh - 400px);  /* 动态计算高度，留出顶部空间 */
  overflow-y: auto;
  padding: 20px;
  border-radius: 8px;
  background: #fff;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);
  margin-bottom: 40px;  /* 添加底部间距 */
}
</style>

<script setup lang="ts">
import { ref, reactive, computed } from 'vue'  // 修正：合并导入
import axios from 'axios'
import { 
  ElMessage, 
  ElButton, 
  ElCollapse, 
  ElCollapseItem, 
  ElForm, 
  ElFormItem, 
  ElInput, 
  ElInputNumber, 
  ElRow, 
  ElCol,
  ElTimeline,
  ElTimelineItem,
  ElCard,
  ElImage,
  ElLink
} from 'element-plus'
import type { VideoResult } from './types'

const activeCollapse = ref(['config'])
const loading = ref(false)
const results = ref([])

// 添加计算属性，将结果数组分成两列
const splitResults = computed(() => {
  const mid = Math.ceil(results.value.length / 2)
  return [
    results.value.slice(0, mid),
    results.value.slice(mid)
  ]
})

const form = reactive({
  uid: '',
  cookie: '',
  apiKey: '',
  startPage: 1,
  endPage: 5
})

async function startAnalysis() {
  if (!form.uid || !form.cookie || !form.apiKey) {
    ElMessage.warning('请填写所有必要信息')
    return
  }

  loading.value = true
  activeCollapse.value = [] // 收起配置面板

  try {
    const response = await axios.post(
      `/api/analysis/user/dynamics/analysis/${form.uid}`,
      {},
      {
        params: {
          cookie: form.cookie,
          api_key: form.apiKey,  // 确保这里正确传递
          max_pages: form.endPage
        }
      }
    )

    if (!response.data || !response.data.analysis_results) {
      throw new Error('API返回数据格式错误')
    }

    results.value = response.data.analysis_results
    ElMessage.success(`分析完成，共分析 ${response.data.total_videos} 个视频`)
  } catch (error: any) {
    console.error('完整错误:', error)
    ElMessage.error(`分析失败: ${error.message || '未知错误'}`)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.container {
  max-width: 1200px;
  width: 100%; /* 改回100% */
  margin: 0 auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: stretch;
  min-height: 100vh;
  box-sizing: border-box;
}

.header {
  text-align: center;
  padding: 40px 0;
  width: 100%;
}

.header h1 {
  font-size: 2.8em;
  color: #00a1d6;
  margin-bottom: 10px;
}

.header p {
  font-size: 1.2em;
  color: #666;
}

.search-button-section {
  text-align: center;
  margin: 30px 0;
  width: 100%;
  display: flex;  /* 添加 flex 布局 */
  justify-content: center;  /* 添加水平居中 */
}
.main-search-button {
  padding: 20px 60px;
  font-size: 1.2em;
}

.el-collapse {
  width: 60%; /* 改为 100%，撑满容器 */
  max-width: 1000px; /* 与 container 一致 */
  margin: 0 auto 30px;
}

:deep(.el-form) {
  width: 100%;  /* 修改表单宽度 */
  max-width: 600px;  /* 添加最大宽度限制 */
  margin: 0 auto;
}

:deep(.el-form-item) {
  margin-bottom: 22px;  /* 增加表单项间距 */
}

:deep(.el-collapse-item__content) {
  padding: 20px;  /* 增加内边距 */
}

:deep(.el-input), 
:deep(.el-input-number) {
  width: 100%;  /* 确保输入框占满宽度 */
}

/* 确保时间线内容居中 */
:deep(.el-timeline) {
  width: 100%;  /* 修改为100% */
  padding: 0;   /* 移除内边距 */
}

:deep(.el-timeline-item__content) {
  width: 100%;
}

:deep(.el-card) {
  width: 100%;
  margin-bottom: 20px;  /* 增加卡片间距 */
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.05);  /* 轻微阴影 */
}

/* 删除重复的 .video-info 定义，保留这一个 */
.video-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 20px;
  width: 100%;
}

/* 删除重复的 .analysis-content 定义，保留这一个 */
.analysis-content {
  width: 100%;
  margin-top: 20px;
  padding: 20px;
  border-top: 1px solid #eee;
  background-color: #f8f9fa;
  border-radius: 8px;
}

/* 结果区域样式优化 */
.results-section {
  width: 100%;
  max-width: 1000px;
  margin: 30px auto 0;
  align-self: center; /* 确保结果区域居中 */
}

.video-cover {
  width: 200px;
  height: 120px;
  border-radius: 4px;
}

.video-details {
  flex: 1;
}

.analysis-content {
  margin-top: 20px;
  padding: 20px;  /* 增加内边距 */
  border-top: 1px solid #eee;
  background-color: #f8f9fa;  /* 添加背景色 */
  border-radius: 8px;  /* 添加圆角 */
}

.text-center {
  text-align: center;
  line-height: 32px;
}

:deep(.el-collapse-item__header) {
  font-size: 16px;
  color: #409EFF;
}

@media (max-width: 768px) {
  .container {
    padding: 20px;
  }
  
  .video-info {
    flex-direction: column;
  }
  
  .video-cover {
    width: 100%;
    height: auto;
  }
}
</style>
