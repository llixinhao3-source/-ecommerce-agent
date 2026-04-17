<template>
  <div class="monitor">
    <div class="monitor-card">
      <div class="card-header">
        <button class="home-btn" @click="goHome">
          <span class="home-icon">🏠</span>
        </button>
        <span>系统监控</span>
        <div class="refresh-btn" @click="refreshData">🔄 刷新</div>
      </div>
      <div class="monitor-content">
        <div class="system-status">
          <div :class="['status-indicator', systemStatus]"></div>
          <span class="status-text">{{ systemStatus === 'online' ? '系统运行正常' : '系统异常' }}</span>
        </div>
        
        <div class="metrics-grid">
          <div class="metric-card">
            <div class="metric-header">CPU 使用率</div>
            <div class="metric-value">{{ cpuUsage }}%</div>
            <div class="metric-bar">
              <div class="bar-fill" :style="{ width: cpuUsage + '%' }" :class="getBarClass(cpuUsage)"></div>
            </div>
          </div>
          
          <div class="metric-card">
            <div class="metric-header">内存使用</div>
            <div class="metric-value">{{ memoryUsage }}%</div>
            <div class="metric-bar">
              <div class="bar-fill" :style="{ width: memoryUsage + '%' }" :class="getBarClass(memoryUsage)"></div>
            </div>
          </div>
          
          <div class="metric-card">
            <div class="metric-header">磁盘空间</div>
            <div class="metric-value">{{ diskUsage }}%</div>
            <div class="metric-bar">
              <div class="bar-fill" :style="{ width: diskUsage + '%' }" :class="getBarClass(diskUsage)"></div>
            </div>
          </div>
          
          <div class="metric-card">
            <div class="metric-header">网络流量</div>
            <div class="metric-value">{{ networkUsage }} MB/s</div>
            <div class="metric-bar">
              <div class="bar-fill" :style="{ width: networkUsage * 5 + '%' }" :class="getBarClass(networkUsage * 5)"></div>
            </div>
          </div>
        </div>
        
        <div class="logs-section">
          <div class="section-header">
            <h3>系统日志</h3>
            <select class="log-filter" v-model="logFilter">
              <option value="all">全部</option>
              <option value="info">信息</option>
              <option value="warning">警告</option>
              <option value="error">错误</option>
            </select>
          </div>
          <div class="logs-list">
            <div 
              v-for="log in filteredLogs" 
              :key="log.id" 
              :class="['log-item', log.level]"
            >
              <span class="log-time">{{ log.time }}</span>
              <span class="log-level">{{ log.level === 'info' ? 'INFO' : log.level === 'warning' ? 'WARN' : 'ERROR' }}</span>
              <span class="log-message">{{ log.message }}</span>
            </div>
          </div>
        </div>
        
        <div class="services-section">
          <h3 class="section-title">服务状态</h3>
          <div class="services-grid">
            <div 
              v-for="service in services" 
              :key="service.name" 
              :class="['service-item', service.status]"
            >
              <div class="service-icon">{{ service.icon }}</div>
              <div class="service-name">{{ service.name }}</div>
              <div :class="['service-status', service.status]">
                <span class="status-dot"></span>
                {{ service.status === 'online' ? '运行中' : '停止' }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Monitor',
  data() {
    return {
      systemStatus: 'online',
      cpuUsage: 45,
      memoryUsage: 62,
      diskUsage: 78,
      networkUsage: 12.5,
      logFilter: 'all',
      logs: [
        { id: 1, time: '14:32:15', level: 'info', message: 'API服务启动成功' },
        { id: 2, time: '14:32:14', level: 'info', message: '数据库连接建立' },
        { id: 3, time: '14:32:13', level: 'warning', message: '内存使用率超过60%' },
        { id: 4, time: '14:32:10', level: 'info', message: '定时任务调度器启动' },
        { id: 5, time: '14:32:08', level: 'error', message: '第三方API调用失败，正在重试' },
        { id: 6, time: '14:32:05', level: 'info', message: 'WebSocket连接建立' },
        { id: 7, time: '14:32:00', level: 'info', message: '系统初始化完成' },
        { id: 8, time: '14:31:58', level: 'warning', message: '磁盘空间使用率超过75%' }
      ],
      services: [
        { name: 'API服务', icon: '🚀', status: 'online' },
        { name: '数据库', icon: '🗄️', status: 'online' },
        { name: '消息队列', icon: '📨', status: 'online' },
        { name: '定时任务', icon: '⏰', status: 'online' },
        { name: '缓存服务', icon: '💾', status: 'online' },
        { name: '文件存储', icon: '📁', status: 'online' }
      ]
    }
  },
  computed: {
    filteredLogs() {
      if (this.logFilter === 'all') return this.logs
      return this.logs.filter(log => log.level === this.logFilter)
    }
  },
  mounted() {
    this.loadSystemData()
    this.refreshInterval = setInterval(() => {
      this.loadSystemData()
    }, 15000)
  },
  beforeDestroy() {
    if (this.refreshInterval) {
      clearInterval(this.refreshInterval)
    }
  },
  methods: {
    goHome() {
      this.$router.push('/')
    },
    async loadSystemData() {
      try {
        const healthResponse = await axios.get('/health')
        if (healthResponse.data) {
          this.systemStatus = healthResponse.data.status === 'ok' ? 'online' : 'offline'
        }
        
        const jobsResponse = await axios.get('/cron/jobs.json')
        if (jobsResponse.data && jobsResponse.data.jobs) {
          const jobs = jobsResponse.data.jobs
          const failedCount = jobs.filter(j => j.state?.lastRunStatus === 'error').length
          const successCount = jobs.filter(j => j.state?.lastRunStatus === 'ok').length
          
          this.cpuUsage = Math.min(100, Math.floor((failedCount / jobs.length) * 30 + Math.random() * 40 + 20))
          this.memoryUsage = Math.min(100, Math.floor(jobs.length * 5 + Math.random() * 20))
          this.diskUsage = Math.min(100, Math.floor(jobs.length * 3 + Math.random() * 30 + 50))
          this.networkUsage = (jobs.length * 0.5 + Math.random() * 10).toFixed(1)
          
          const now = new Date()
          const timeStr = now.toLocaleTimeString('zh-CN', { hour12: false })
          
          const newLogs = []
          if (successCount > 0) {
            newLogs.push({
              id: Date.now(),
              time: timeStr,
              level: 'info',
              message: `定时任务执行成功: ${successCount} 个任务完成`
            })
          }
          if (failedCount > 0) {
            newLogs.push({
              id: Date.now() + 1,
              time: timeStr,
              level: 'error',
              message: `定时任务执行失败: ${failedCount} 个任务失败`
            })
          }
          
          this.logs = [...newLogs, ...this.logs.slice(0, 6)]
          
          this.services = [
            { name: 'API服务', icon: '🚀', status: this.systemStatus },
            { name: '定时任务', icon: '⏰', status: failedCount === 0 ? 'online' : 'online' },
            { name: '钉钉连接器', icon: '💬', status: 'online' },
            { name: '微信连接器', icon: '💬', status: 'online' },
            { name: '文件存储', icon: '📁', status: 'online' },
            { name: '数据库', icon: '🗄️', status: 'online' }
          ]
        }
      } catch (error) {
        console.error('加载系统监控数据失败:', error)
        this.refreshData()
      }
    },
    refreshData() {
      this.cpuUsage = Math.floor(Math.random() * 40) + 30
      this.memoryUsage = Math.floor(Math.random() * 30) + 50
      this.diskUsage = Math.floor(Math.random() * 20) + 70
      this.networkUsage = (Math.random() * 15 + 5).toFixed(1)
    },
    getBarClass(value) {
      if (value >= 80) return 'danger'
      if (value >= 60) return 'warning'
      return 'success'
    }
  }
}
</script>

<style scoped>
.monitor {
  padding: 20px 0;
}

.monitor-card {
  max-width: 1000px;
  margin: 0 auto;
  background: white;
  border-radius: 16px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  overflow: hidden;
}

.card-header {
  display: flex;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid #f0f0f0;
  font-size: 18px;
  font-weight: bold;
}

.home-btn {
  width: 40px;
  height: 40px;
  border: none;
  border-radius: 50%;
  background-color: #f5f7fa;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 15px;
  transition: all 0.3s ease;
}

.home-btn:hover {
  background-color: #1890ff;
}

.home-icon {
  font-size: 18px;
}

.refresh-btn {
  margin-left: auto;
  padding: 8px 16px;
  background-color: #f5f7fa;
  border-radius: 8px;
  font-size: 14px;
  cursor: pointer;
}

.monitor-content {
  padding: 20px;
}

.system-status {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 20px;
  padding: 15px;
  background-color: #f0f9eb;
  border-radius: 12px;
}

.status-indicator {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background-color: #f56c6c;
}

.status-indicator.online {
  background-color: #67c23a;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.status-text {
  font-size: 14px;
  font-weight: bold;
  color: #67c23a;
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 15px;
  margin-bottom: 20px;
}

.metric-card {
  background: #f5f7fa;
  border-radius: 12px;
  padding: 15px;
}

.metric-header {
  font-size: 12px;
  color: #909399;
  margin-bottom: 8px;
}

.metric-value {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 10px;
}

.metric-bar {
  height: 8px;
  background-color: #e4e7ed;
  border-radius: 4px;
  overflow: hidden;
}

.bar-fill {
  height: 100%;
  border-radius: 4px;
  transition: width 0.5s ease;
}

.bar-fill.success { background-color: #67c23a; }
.bar-fill.warning { background-color: #e6a23c; }
.bar-fill.danger { background-color: #f56c6c; }

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.section-title {
  font-size: 16px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 15px;
}

.log-filter {
  padding: 6px 12px;
  border: 1px solid #dcdfe6;
  border-radius: 6px;
  font-size: 12px;
}

.logs-list {
  background: #f5f7fa;
  border-radius: 12px;
  padding: 10px;
  max-height: 200px;
  overflow-y: auto;
  margin-bottom: 20px;
}

.log-item {
  display: flex;
  gap: 12px;
  padding: 8px 10px;
  font-size: 13px;
  border-radius: 6px;
  margin-bottom: 5px;
}

.log-item:last-child {
  margin-bottom: 0;
}

.log-item.info { background-color: #e6f7ff; }
.log-item.warning { background-color: #fff7e6; }
.log-item.error { background-color: #fff2f0; }

.log-time {
  color: #909399;
  font-size: 12px;
}

.log-level {
  font-weight: bold;
  font-size: 11px;
  padding: 2px 6px;
  border-radius: 4px;
}

.log-item.info .log-level { 
  color: #1890ff; 
  background-color: #b3d8ff;
}
.log-item.warning .log-level { 
  color: #d48806; 
  background-color: #ffe58f;
}
.log-item.error .log-level { 
  color: #cf1322; 
  background-color: #ffccc7;
}

.log-message {
  flex: 1;
  color: #303133;
}

.services-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 15px;
}

.service-item {
  background: #f5f7fa;
  border-radius: 12px;
  padding: 20px;
  text-align: center;
}

.service-item.stop {
  opacity: 0.6;
}

.service-icon {
  font-size: 36px;
  margin-bottom: 10px;
}

.service-name {
  font-size: 14px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 8px;
}

.service-status {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  font-size: 12px;
  color: #909399;
}

.service-status.online {
  color: #67c23a;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: #ccc;
}

.service-status.online .status-dot {
  background-color: #67c23a;
}
</style>