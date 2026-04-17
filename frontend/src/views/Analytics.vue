<template>
  <div class="analytics">
    <div class="analytics-card">
      <div class="card-header">
        <button class="home-btn" @click="goHome">
          <span class="home-icon">🏠</span>
        </button>
        <span>数据分析</span>
        <span class="refresh-btn" @click="loadData">🔄</span>
      </div>
      <div class="analytics-content">
        <div class="stats-grid">
          <div class="stat-card">
            <div class="stat-value">{{ stats.totalRequests.toLocaleString() }}</div>
            <div class="stat-label">总请求数</div>
          </div>
          <div class="stat-card">
            <div class="stat-value">{{ stats.successRate }}%</div>
            <div class="stat-label">成功率</div>
          </div>
          <div class="stat-card">
            <div class="stat-value">{{ stats.avgResponseTime }}ms</div>
            <div class="stat-label">平均响应时间</div>
          </div>
          <div class="stat-card">
            <div class="stat-value">{{ stats.status }}</div>
            <div class="stat-label">运行状态</div>
          </div>
        </div>
        
        <div class="charts-section">
          <div class="chart-card">
            <div class="chart-header">请求趋势</div>
            <div class="chart-placeholder">
              <div class="bar-chart">
                <div v-for="(height, index) in chartData.requestTrend" :key="index" 
                     class="bar" :style="{ height: height + '%' }"></div>
              </div>
              <div class="chart-labels">{{ chartData.labels.join(' ') }}</div>
            </div>
          </div>
          
          <div class="chart-card">
            <div class="chart-header">分布统计</div>
            <div class="chart-placeholder">
              <div class="pie-chart" :style="{ background: pieChartGradient }"></div>
              <div class="pie-legend">
                <div v-for="(item, index) in chartData.distribution" :key="index" class="legend-item">
                  <span class="legend-color" :class="'color-' + (index + 1)"></span>
                  {{ item.name }} {{ item.value }}%
                </div>
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
  name: 'Analytics',
  data() {
    return {
      stats: {
        totalRequests: 0,
        successRate: 0,
        avgResponseTime: 0,
        status: '加载中...'
      },
      chartData: {
        requestTrend: [],
        labels: ['周一', '周二', '周三', '周四', '周五', '周六', '周日'],
        distribution: []
      },
      colors: ['#1890ff', '#67c23a', '#e6a23c', '#f56c6c', '#909399']
    }
  },
  computed: {
    pieChartGradient() {
      let gradient = 'conic-gradient('
      let currentDeg = 0
      this.chartData.distribution.forEach((item, index) => {
        const deg = (item.value / 100) * 360
        gradient += `${this.colors[index]} ${currentDeg}deg ${currentDeg + deg}deg`
        if (index < this.chartData.distribution.length - 1) gradient += ', '
        currentDeg += deg
      })
      gradient += ')'
      return gradient
    }
  },
  mounted() {
    this.loadData()
    this.refreshInterval = setInterval(() => {
      this.loadData()
    }, 30000)
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
    async loadData() {
      try {
        const response = await axios.get('/cron/jobs.json')
        if (response.data && response.data.jobs && response.data.jobs.length > 0) {
          const jobs = response.data.jobs
          
          this.stats.totalRequests = jobs.length
          
          const successCount = jobs.filter(j => j.state?.lastRunStatus === 'ok').length
          this.stats.successRate = ((successCount / jobs.length) * 100).toFixed(1)
          
          const avgDuration = jobs.reduce((sum, j) => sum + (j.state?.lastDurationMs || 0), 0) / jobs.length
          this.stats.avgResponseTime = Math.round(avgDuration)
          
          const hasRunning = jobs.some(j => j.enabled)
          this.stats.status = hasRunning ? '运行中' : '已停止'
          
          this.chartData.requestTrend = jobs.slice(0, 7).map(j => {
            const duration = j.state?.lastDurationMs || 0
            return Math.min(100, Math.max(10, (duration / 60000) * 100))
          })
          
          const taskTypes = {}
          jobs.forEach(j => {
            const msg = j.payload?.message || ''
            if (msg.includes('淘宝')) taskTypes['淘宝'] = (taskTypes['淘宝'] || 0) + 1
            else if (msg.includes('小红书')) taskTypes['小红书'] = (taskTypes['小红书'] || 0) + 1
            else if (msg.includes('安全')) taskTypes['安全检查'] = (taskTypes['安全检查'] || 0) + 1
            else if (msg.includes('记忆')) taskTypes['记忆'] = (taskTypes['记忆'] || 0) + 1
            else taskTypes['其他'] = (taskTypes['其他'] || 0) + 1
          })
          
          this.chartData.distribution = Object.entries(taskTypes).map(([name, count]) => ({
            name,
            value: ((count / jobs.length) * 100).toFixed(0)
          }))
        }
      } catch (error) {
        console.error('加载数据分析失败:', error)
        this.loadMockData()
      }
    },
    loadMockData() {
      this.stats = {
        totalRequests: 1234,
        successRate: 98.5,
        avgResponseTime: 156,
        status: '24/7'
      }
      this.chartData.requestTrend = [40, 65, 45, 80, 55, 70, 90]
      this.chartData.distribution = [
        { name: 'AI聊天', value: 40 },
        { name: '浏览器', value: 25 },
        { name: '语音通话', value: 20 },
        { name: '其他', value: 15 }
      ]
    }
  }
}
</script>

<style scoped>
.analytics {
  padding: 20px 0;
}

.analytics-card {
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
  justify-content: space-between;
  padding: 16px 20px;
  border-bottom: 1px solid #f0f0f0;
  font-size: 18px;
  font-weight: bold;
}

.refresh-btn {
  font-size: 18px;
  cursor: pointer;
  padding: 8px;
  border-radius: 50%;
  transition: background 0.3s;
}

.refresh-btn:hover {
  background: #f0f0f0;
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

.analytics-content {
  padding: 20px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 15px;
  margin-bottom: 20px;
}

.stat-card {
  background: #f5f7fa;
  border-radius: 12px;
  padding: 20px;
  text-align: center;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #1890ff;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 14px;
  color: #909399;
}

.charts-section {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 15px;
}

.chart-card {
  background: #f5f7fa;
  border-radius: 12px;
  padding: 15px;
}

.chart-header {
  font-size: 14px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 15px;
}

.chart-placeholder {
  height: 200px;
}

.bar-chart {
  display: flex;
  justify-content: space-around;
  align-items: flex-end;
  height: 160px;
  padding: 0 20px;
}

.bar {
  width: 40px;
  background: linear-gradient(180deg, #1890ff 0%, #69c0ff 100%);
  border-radius: 4px 4px 0 0;
  transition: height 0.3s ease;
}

.chart-labels {
  display: flex;
  justify-content: space-around;
  font-size: 12px;
  color: #909399;
  margin-top: 10px;
}

.pie-chart {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  background: conic-gradient(
    #1890ff 0deg 144deg,
    #67c23a 144deg 234deg,
    #e6a23c 234deg 306deg,
    #f56c6c 306deg 360deg
  );
  margin: 0 auto;
  position: relative;
}

.pie-chart::before {
  content: '';
  position: absolute;
  top: 20%;
  left: 20%;
  width: 60%;
  height: 60%;
  background: #f5f7fa;
  border-radius: 50%;
}

.pie-legend {
  margin-top: 15px;
  padding-left: 20px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
  font-size: 12px;
  color: #666;
}

.legend-color {
  width: 12px;
  height: 12px;
  border-radius: 3px;
}

.color-1 { background-color: #1890ff; }
.color-2 { background-color: #67c23a; }
.color-3 { background-color: #e6a23c; }
.color-4 { background-color: #f56c6c; }
</style>