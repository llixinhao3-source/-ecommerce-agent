<template>
<div class="dashboard">
  <nav>
    <div class="nav-left">
      <span class="logo">OpenClaw</span>
    </div>
    <div class="nav-right">
      <router-link to="/">首页</router-link>
    </div>
  </nav>
  
  <div class="content">
    <h1>关键词趋势分析</h1>
    
    <div class="range-buttons">
      <button @click="selectRange('7days')" :class="{active: selectedRange === '7days'}">7天</button>
      <button @click="selectRange('15days')" :class="{active: selectedRange === '15days'}">15天</button>
      <button @click="selectRange('30days')" :class="{active: selectedRange === '30days'}">30天</button>
    </div>
    
    <div class="word-cloud">
      <span v-for="(kw, i) in currentKeywords" :key="i" :class="['word', kw.size]" :style="{opacity: kw.opacity}">{{ kw.text }}</span>
    </div>
    
    <h2>Active Agents</h2>
    <div class="agents-grid">
      <div v-for="(agent, i) in currentAgents" :key="i" class="agent-card">
        <h3>{{ agent.name }}</h3>
        <p class="agent-id">ID: {{ agent.id }}</p>
        <span :class="['status', agent.statusColor]">{{ agent.status }}</span>
        <div class="progress-bar">
          <div class="progress-fill" :style="{width: agent.progress + '%'}"></div>
        </div>
        <p class="progress-text">{{ agent.progressText }} - {{ agent.progress }}%</p>
      </div>
    </div>
    
    <div class="stats">
      <div class="stat-item">
        <span class="stat-value">128</span>
        <span class="stat-label">今日请求</span>
      </div>
      <div class="stat-item">
        <span class="stat-value">98.5%</span>
        <span class="stat-label">成功率</span>
      </div>
      <div class="stat-item">
        <span class="stat-value">156ms</span>
        <span class="stat-label">平均延迟</span>
      </div>
    </div>
  </div>
</div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Dashboard',
  data() {
    return {
      selectedRange: '7days',
      realKeywords: [],
      realAgents: [],
      keywordsLoaded: false,
      agentsLoaded: false,
      keywordsData: {
        '7days': [
          { text: '淘宝搜索', size: 'large', opacity: 0.9 },
          { text: '自动化', size: 'small', opacity: 0.4 },
          { text: '百畅旗舰店', size: 'medium', opacity: 0.6 },
          { text: '数据抓取', size: 'large', opacity: 0.8 },
          { text: 'AI Agent', size: 'medium', opacity: 0.6 },
          { text: '物流查询', size: 'small', opacity: 0.5 },
          { text: '每日简报', size: 'small', opacity: 0.3 }
        ],
        '15days': [
          { text: '数据分析', size: 'large', opacity: 0.9 },
          { text: '爬虫开发', size: 'small', opacity: 0.5 },
          { text: '商品监控', size: 'medium', opacity: 0.7 },
          { text: 'API集成', size: 'small', opacity: 0.4 },
          { text: '智能推荐', size: 'medium', opacity: 0.6 },
          { text: '竞品分析', size: 'small', opacity: 0.55 },
          { text: '批量操作', size: 'medium', opacity: 0.65 }
        ],
        '30days': [
          { text: '系统优化', size: 'large', opacity: 0.9 },
          { text: '定时任务', size: 'small', opacity: 0.45 },
          { text: '报表生成', size: 'medium', opacity: 0.75 },
          { text: '异常告警', size: 'small', opacity: 0.35 },
          { text: '性能监控', size: 'medium', opacity: 0.65 },
          { text: '日志分析', size: 'small', opacity: 0.5 },
          { text: '安全审计', size: 'medium', opacity: 0.6 }
        ]
      },
      agentsData: {
        '7days': [
          { name: 'Procurement-Bot', id: 'OC-4492', status: 'WORKING', statusColor: 'status-working', progress: 65, progressText: '淘宝元素定位中' },
          { name: 'DataScraper-AI', id: 'OC-7721', status: 'IDLE', statusColor: 'status-idle', progress: 0, progressText: '系统空闲中' }
        ],
        '15days': [
          { name: 'Analysis-Bot', id: 'OC-5521', status: 'WORKING', statusColor: 'status-working', progress: 85, progressText: '月度报告生成中' },
          { name: 'Monitor-AI', id: 'OC-8834', status: 'RUNNING', statusColor: 'status-running', progress: 100, progressText: '监控任务完成' }
        ],
        '30days': [
          { name: 'Scheduler-Bot', id: 'OC-2299', status: 'SCHEDULED', statusColor: 'status-scheduled', progress: 45, progressText: '季度任务调度中' },
          { name: 'Audit-AI', id: 'OC-1156', status: 'WORKING', statusColor: 'status-working', progress: 70, progressText: '安全扫描进行中' }
        ]
      },
      chatKeywords: []
    }
  },
  mounted() {
    this.loadRealData()
  },
  methods: {
    async loadRealData() {
      try {
        const response = await axios.get('/cron/jobs.json')
        if (response.data && response.data.jobs && response.data.jobs.length > 0) {
          const jobs = response.data.jobs
          const keywords = {}
          jobs.forEach(job => {
            const name = job.name
            if (name) {
              keywords[name] = (keywords[name] || 0) + 1
            }
          })
          this.realKeywords = Object.entries(keywords).map(([text, weight]) => ({
            text,
            weight: Math.min(10, Math.max(1, Math.floor(weight * 3)))
          }))
          this.keywordsLoaded = true
        }
        
        this.loadChatKeywords()
      } catch (error) {
        console.error('Failed to load real data:', error)
      }
    },
    loadChatKeywords() {
      const chatHistory = localStorage.getItem('chatHistory')
      if (chatHistory) {
        try {
          const history = JSON.parse(chatHistory)
          const keywords = {}
          
          history.forEach(item => {
            if (item.messages && item.messages.length > 1) {
              const userMessages = item.messages.filter(msg => msg.type === 'user')
              userMessages.forEach(msg => {
                if (msg.content) {
                  const words = msg.content.split(/[\s，,。！!?、]+/)
                  words.forEach(word => {
                    const cleanWord = word.trim().replace(/[^\u4e00-\u9fa5a-zA-Z0-9]/g, '')
                    if (cleanWord.length >= 2) {
                      keywords[cleanWord] = (keywords[cleanWord] || 0) + 1
                    }
                  })
                }
              })
            }
          })
          
          const sizes = ['small', 'small', 'medium', 'medium', 'large', 'large', 'large']
          const sorted = Object.entries(keywords).sort((a, b) => b[1] - a[1])
          this.chatKeywords = sorted.slice(0, 7).map(([text, count], index) => ({
            text: text,
            size: sizes[index] || 'medium',
            opacity: 0.3 + (1 - index / 7) * 0.6,
            count: count
          }))
        } catch (e) {
          console.error('Failed to parse chat history:', e)
        }
      }
    },
    formatKeywords(keywords) {
      const sizes = ['small', 'small', 'medium', 'medium', 'large', 'large', 'large']
      const sorted = keywords.sort((a, b) => (b.count || 0) - (a.count || 0))
      return sorted.slice(0, 7).map((kw, index) => ({
        text: kw.keyword || kw.text,
        size: sizes[index] || 'medium',
        opacity: 0.3 + (1 - index / 7) * 0.6
      }))
    },
    formatAgents(agents) {
      return agents.map(agent => ({
        name: agent.name,
        id: agent.id,
        status: agent.status || 'IDLE',
        statusColor: agent.status === 'WORKING' ? 'status-working' : 
                     agent.status === 'RUNNING' ? 'status-running' : 
                     agent.status === 'SCHEDULED' ? 'status-scheduled' : 'status-idle',
        progress: Math.round(agent.progress || 0),
        progressText: agent.activity || '系统空闲中'
      })).slice(0, 2)
    },
    selectRange(range) {
      this.selectedRange = range
      this.loadRealData()
    }
  },
  computed: {
    currentKeywords() {
      if (this.chatKeywords.length > 0) return this.chatKeywords
      if (this.keywordsLoaded && this.realKeywords.length > 0) return this.realKeywords
      return this.keywordsData[this.selectedRange]
    },
    currentAgents() {
      if (this.agentsLoaded && this.realAgents.length > 0) return this.realAgents
      return this.agentsData[this.selectedRange]
    }
  }
}
</script>

<style scoped>
.dashboard {
  padding: 20px;
  font-family: 'Inter', sans-serif;
}

nav {
  display: flex;
  justify-content: space-between;
  margin-bottom: 30px;
}

.logo {
  font-weight: 600;
  letter-spacing: 0.2em;
  text-transform: uppercase;
}

.nav-right a {
  color: #666;
  text-decoration: none;
}

.content {
  max-width: 1000px;
  margin: 0 auto;
}

h1 {
  font-size: 28px;
  font-weight: 300;
  margin-bottom: 15px;
}

.range-buttons {
  margin-bottom: 20px;
}

.range-buttons button {
  margin-right: 10px;
  padding: 8px 20px;
  border: 1px solid #ddd;
  border-radius: 20px;
  background: white;
  cursor: pointer;
  font-size: 12px;
}

.range-buttons button.active {
  background: black;
  color: white;
  border-color: black;
}

.word-cloud {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  padding: 30px;
  border: 1px solid #eee;
  border-radius: 15px;
  background: #fafafa;
  margin-bottom: 30px;
  min-height: 150px;
  align-items: center;
  justify-content: center;
}

.word {
  cursor: default;
  transition: transform 0.3s;
}

.word:hover {
  transform: scale(1.1);
}

.word.small { font-size: 16px; }
.word.medium { font-size: 24px; }
.word.large { font-size: 36px; }

h2 {
  font-size: 14px;
  font-weight: 600;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: #999;
  margin-bottom: 15px;
}

.agents-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 30px;
}

.agent-card {
  padding: 20px;
  border: 1px solid #eee;
  border-radius: 10px;
}

.agent-card h3 {
  margin-bottom: 5px;
}

.agent-id {
  font-size: 10px;
  font-family: monospace;
  color: #999;
  margin-bottom: 10px;
}

.status {
  font-size: 10px;
  padding: 3px 8px;
  border-radius: 3px;
  font-weight: 600;
}

.status-working { background: #ECFDF5; color: #059669; }
.status-idle { background: #EFF6FF; color: #2563EB; }
.status-running { background: #FFFBEB; color: #D97706; }
.status-scheduled { background: #F5F3FF; color: #7C3AED; }

.progress-bar {
  height: 2px;
  background: #eee;
  margin: 15px 0;
  border-radius: 1px;
}

.progress-fill {
  height: 100%;
  background: black;
  transition: width 1s;
}

.progress-text {
  font-size: 11px;
  color: #666;
}

.stats {
  display: flex;
  gap: 30px;
}

.stat-item {
  text-align: center;
}

.stat-value {
  display: block;
  font-size: 28px;
  font-weight: 600;
}

.stat-label {
  font-size: 11px;
  color: #999;
}
</style>