<template>
  <div class="schedule-manager">
    <div class="page-header">
      <button class="back-btn" @click="goBack">
        <span>←</span>
      </button>
      <h2>⏰ 定时任务管理</h2>
    </div>

    <div class="schedule-container">
      <div class="schedule-list">
        <div class="list-header">
          <h3>定时任务列表</h3>
          <button class="add-btn" @click="showAddModal = true">+ 添加定时任务</button>
        </div>
        <div v-if="schedules.length === 0" class="empty-state">
          <p>暂无定时任务</p>
          <button class="add-btn" @click="showAddModal = true">+ 添加定时任务</button>
        </div>
        <div v-else class="task-cards">
          <div v-for="schedule in schedules" :key="schedule.id" class="task-card">
            <div class="task-header">
              <span class="task-name">{{ schedule.name }}</span>
              <span :class="['status-badge', schedule.status.toLowerCase()]">{{ schedule.status }}</span>
            </div>
            <div class="task-info">
              <p><strong>任务描述:</strong> {{ schedule.description }}</p>
              <p><strong>执行时间:</strong> {{ schedule.cron_expression }}</p>
              <p><strong>上次执行:</strong> {{ schedule.last_run || '从未执行' }}</p>
              <p><strong>下次执行:</strong> {{ schedule.next_run }}</p>
              <p v-if="schedule.consecutiveErrors > 0" class="error-info">
                <strong>连续失败:</strong> {{ schedule.consecutiveErrors }} 次
              </p>
            </div>
            <div class="task-actions">
              <button class="action-btn edit-btn" @click="editSchedule(schedule)">编辑</button>
              <button v-if="schedule.enabled" class="action-btn stop-btn" @click="toggleSchedule(schedule.id, false)">禁用</button>
              <button v-else class="action-btn start-btn" @click="toggleSchedule(schedule.id, true)">启用</button>
              <button class="action-btn delete-btn" @click="deleteSchedule(schedule.id)">删除</button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 添加/编辑定时任务弹窗 -->
    <div v-if="showAddModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content">
        <h3>{{ editingSchedule ? '编辑定时任务' : '添加定时任务' }}</h3>
        <form @submit.prevent="saveSchedule">
          <div class="form-group">
            <label>任务名称</label>
            <input type="text" v-model="scheduleForm.name" required placeholder="请输入任务名称">
          </div>
          <div class="form-group">
            <label>任务描述</label>
            <textarea v-model="scheduleForm.description" placeholder="请输入任务描述"></textarea>
          </div>
          <div class="form-group">
            <label>执行时间 (Cron表达式)</label>
            <input type="text" v-model="scheduleForm.cron_expression" required placeholder="例如: 0 0 * * * (每天凌晨)">
          </div>
          <div class="form-group">
            <label>时区</label>
            <input type="text" v-model="scheduleForm.timezone" placeholder="Asia/Shanghai" value="Asia/Shanghai">
          </div>
          <div class="form-group">
            <label>任务消息</label>
            <textarea v-model="scheduleForm.message" placeholder="请输入要执行的任务消息"></textarea>
          </div>
          <div class="form-actions">
            <button type="button" class="cancel-btn" @click="closeModal">取消</button>
            <button type="submit" class="submit-btn">保存</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'ScheduleManager',
  data() {
    return {
      schedules: [
        { id: '1', name: '每日安全检查', description: '执行安全检查任务', cron_expression: '0 10 * * *', timezone: 'Asia/Shanghai', enabled: true, status: 'COMPLETED', last_run: '2026-04-14 10:00:00', next_run: '2026-04-15 10:00:00', consecutiveErrors: 0 },
        { id: '2', name: 'InStreet学习库', description: '浏览网站内容，学习当天更新', cron_expression: '0 8 * * *', timezone: 'Asia/Shanghai', enabled: true, status: 'COMPLETED', last_run: '2026-04-14 08:00:00', next_run: '2026-04-15 08:00:00', consecutiveErrors: 0 },
        { id: '3', name: '小红书高粉爆品同步', description: '抓取数据并同步到数据库', cron_expression: '0 9 * * *', timezone: 'Asia/Shanghai', enabled: true, status: 'FAILED', last_run: '2026-04-14 09:00:00', next_run: '2026-04-15 09:00:00', consecutiveErrors: 3 },
        { id: '4', name: '淘宝新品-4Agent流程', description: '执行淘宝新品自动抓取流程', cron_expression: '0 8 * * *', timezone: 'Asia/Shanghai', enabled: true, status: 'COMPLETED', last_run: '2026-04-14 08:00:00', next_run: '2026-04-15 08:00:00', consecutiveErrors: 0 },
        { id: '5', name: '百畅系统全页面截图', description: '截图任务', cron_expression: '0 10 * * *', timezone: 'Asia/Shanghai', enabled: true, status: 'FAILED', last_run: '2026-04-14 10:00:00', next_run: '2026-04-15 10:00:00', consecutiveErrors: 12 }
      ],
      showAddModal: false,
      editingSchedule: null,
      scheduleForm: {
        name: '',
        description: '',
        cron_expression: '',
        timezone: 'Asia/Shanghai',
        message: ''
      }
    }
  },
  mounted() {
    this.loadSchedules()
    this.refreshInterval = setInterval(() => {
      this.loadSchedules()
    }, 15000)
  },
  beforeDestroy() {
    if (this.refreshInterval) {
      clearInterval(this.refreshInterval)
    }
  },
  methods: {
    goBack() {
      this.$router.push('/')
    },
    formatTimestamp(ms) {
      if (!ms) return '从未执行'
      const date = new Date(ms)
      return date.toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
      })
    },
    async loadSchedules() {
      try {
        const response = await axios.get('/cron/jobs.json')
        console.log('定时任务数据:', response.data)
        if (response.data && response.data.jobs && response.data.jobs.length > 0) {
          this.schedules = response.data.jobs.map(job => ({
            id: job.id,
            name: job.name,
            description: job.payload?.message?.substring(0, 50) + (job.payload?.message?.length > 50 ? '...' : '') || '无描述',
            cron_expression: job.schedule?.expr || '',
            timezone: job.schedule?.tz || 'Asia/Shanghai',
            enabled: job.enabled,
            status: job.state?.lastRunStatus === 'ok' ? 'COMPLETED' : (job.state?.lastRunStatus === 'error' ? 'FAILED' : 'IDLE'),
            last_run: this.formatTimestamp(job.state?.lastRunAtMs),
            next_run: this.formatTimestamp(job.state?.nextRunAtMs),
            consecutiveErrors: job.state?.consecutiveErrors || 0,
            raw: job
          }))
        }
      } catch (error) {
        console.error('加载定时任务失败:', error)
      }
    },
    addSchedule() {
      this.editingSchedule = null
      this.scheduleForm = {
        name: '',
        description: '',
        cron_expression: '',
        timezone: 'Asia/Shanghai',
        message: ''
      }
      this.showAddModal = true
    },
    editSchedule(schedule) {
      this.editingSchedule = schedule
      this.scheduleForm = {
        name: schedule.name,
        description: schedule.description,
        cron_expression: schedule.cron_expression,
        timezone: schedule.timezone,
        message: schedule.raw?.payload?.message || ''
      }
      this.showAddModal = true
    },
    closeModal() {
      this.showAddModal = false
      this.editingSchedule = null
    },
    async saveSchedule() {
      try {
        let response
        const payload = {
          name: this.scheduleForm.name,
          schedule: {
            expr: this.scheduleForm.cron_expression,
            kind: 'cron',
            tz: this.scheduleForm.timezone
          },
          payload: {
            kind: 'agentTurn',
            message: this.scheduleForm.message
          },
          enabled: true,
          agentId: 'main',
          sessionKey: 'agent:main:main',
          sessionTarget: 'isolated',
          wakeMode: 'now',
          delivery: {
            mode: 'none'
          }
        }

        if (this.editingSchedule) {
          response = await axios.put(`/schedules/${this.editingSchedule.id}`, payload)
        } else {
          response = await axios.post('/schedules', payload)
        }
        if (response.data) {
          this.closeModal()
          this.loadSchedules()
        }
      } catch (error) {
        console.error('保存定时任务失败:', error)
        alert('保存失败，请检查输入')
      }
    },
    async toggleSchedule(id, enabled) {
      try {
        const response = await axios.post(`/api/schedules/${id}/toggle`, { enabled })
        if (response.data) {
          this.loadSchedules()
        }
      } catch (error) {
        console.error('切换定时任务状态失败:', error)
      }
    },
    async deleteSchedule(id) {
      if (!confirm('确定要删除这个定时任务吗？')) return
      try {
        const response = await axios.delete(`/api/schedules/${id}`)
        if (response.data) {
          this.loadSchedules()
        }
      } catch (error) {
        console.error('删除定时任务失败:', error)
      }
    }
  }
}
</script>

<style scoped>
.schedule-manager {
  min-height: 100vh;
  background: #ffffff;
  padding: 20px;
}

.page-header {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 20px;
  color: #333333;
}

.back-btn {
  background: #f0f0f0;
  border: 1px solid #e0e0e0;
  color: #333333;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  font-size: 18px;
  cursor: pointer;
  transition: background 0.3s;
}

.back-btn:hover {
  background: #e0e0e0;
}

.page-header h2 {
  margin: 0;
  font-size: 24px;
}

.schedule-container {
  max-width: 1200px;
  margin: 0 auto;
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.schedule-list h3 {
  color: white;
  margin: 0;
  font-size: 18px;
}

.empty-state {
  background: white;
  border-radius: 12px;
  padding: 40px;
  text-align: center;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.empty-state p {
  color: #666;
  margin-bottom: 20px;
}

.add-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  transition: transform 0.3s;
}

.add-btn:hover {
  transform: translateY(-2px);
}

.task-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
}

.task-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.task-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.task-name {
  font-weight: bold;
  font-size: 16px;
}

.status-badge {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: bold;
}

.status-badge.running {
  background: #52c41a;
  color: white;
}

.status-badge.stopped {
  background: #f5a623;
  color: white;
}

.status-badge.completed {
  background: #1890ff;
  color: white;
}

.status-badge.failed {
  background: #f5222d;
  color: white;
}

.status-badge.idle {
  background: #666666;
  color: white;
}

.error-info {
  color: #f5222d;
  font-weight: bold;
}

.task-info p {
  margin: 5px 0;
  color: #666;
  font-size: 14px;
}

.task-progress {
  margin-top: 15px;
}

.progress-bar {
  height: 8px;
  background: #f0f0f0;
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 4px;
  transition: width 0.3s;
}

.progress-text {
  display: block;
  text-align: right;
  color: #666;
  font-size: 12px;
  margin-top: 5px;
}

.task-actions {
  display: flex;
  gap: 10px;
  margin-top: 15px;
}

.action-btn {
  flex: 1;
  padding: 8px 12px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 12px;
  transition: opacity 0.3s;
}

.action-btn:hover {
  opacity: 0.8;
}

.edit-btn {
  background: #f0f0f0;
  color: #333;
}

.start-btn {
  background: #52c41a;
  color: white;
}

.stop-btn {
  background: #f5a623;
  color: white;
}

.delete-btn {
  background: #f5222d;
  color: white;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 12px;
  padding: 30px;
  width: 90%;
  max-width: 500px;
}

.modal-content h3 {
  margin-top: 0;
  margin-bottom: 20px;
  color: #333;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  color: #666;
  font-size: 14px;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  box-sizing: border-box;
}

.form-group textarea {
  height: 80px;
  resize: vertical;
}

.form-actions {
  display: flex;
  gap: 10px;
  margin-top: 20px;
}

.cancel-btn {
  flex: 1;
  padding: 10px;
  background: #f0f0f0;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

.submit-btn {
  flex: 2;
  padding: 10px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}
</style>