<template>
  <div class="team">
    <div class="team-card">
      <div class="card-header">
        <button class="home-btn" @click="goHome">
          <span class="home-icon">🏠</span>
        </button>
        <span>团队协作</span>
        <button class="add-btn" @click="addMember">+ 添加成员</button>
      </div>
      <div class="team-content">
        <div class="team-stats">
          <div class="stat-item">
            <span class="stat-num">{{ members.length }}</span>
            <span class="stat-text">团队成员</span>
          </div>
          <div class="stat-item">
            <span class="stat-num">{{ isWorkingHours() ? members.length : 0 }}</span>
            <span class="stat-text">在线</span>
          </div>
          <div class="stat-item">
            <span class="stat-num">{{ tasks.length }}</span>
            <span class="stat-text">进行中任务</span>
          </div>
        </div>
        
        <div class="members-section">
          <h3 class="section-title">团队成员</h3>
          <div class="members-list">
            <a 
              v-for="member in members" 
              :key="member.id" 
              :href="'tel:' + member.phone"
              class="member-item"
            >
              <div :class="['member-avatar', { online: isWorkingHours() }]">
                {{ member.avatar }}
              </div>
              <div class="member-info">
                <div class="member-name">{{ member.name }}</div>
                <div class="member-role">{{ member.role }}</div>
                <div class="member-phone">{{ member.phone }}</div>
              </div>
              <div class="member-status">
                <span :class="['status-dot', { online: isWorkingHours() }]"></span>
                {{ isWorkingHours() ? '在线' : '离线' }}
              </div>
            </a>
          </div>
        </div>
        
        <div class="tasks-section">
          <h3 class="section-title">进行中任务</h3>
          <div class="tasks-list">
            <div 
              v-for="task in tasks" 
              :key="task.id" 
              class="task-item"
            >
              <div class="task-priority" :class="task.priority"></div>
              <div class="task-content">
                <div class="task-title">{{ task.title }}</div>
                <div class="task-meta">{{ task.assignee }} · {{ task.dueDate }}</div>
              </div>
              <div class="task-progress">
                <div class="progress-bar">
                  <div class="progress-fill" :style="{ width: task.progress + '%' }"></div>
                </div>
                <span class="progress-text">{{ task.progress }}%</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Team',
  data() {
    return {
      members: [
        { id: 1, name: '李勇', role: 'AI信息部主管', avatar: '李', phone: '19898889598', online: true },
        { id: 2, name: '陈鑫', role: 'AI信息部技术人员', avatar: '陈', phone: '17872087298', online: true },
        { id: 3, name: '陈粤', role: 'AI信息部技术人员', avatar: '陈', phone: '18998461134', online: true },
        { id: 4, name: '黎超成', role: 'AI信息部技术人员', avatar: '黎', phone: '19212035920', online: false },
        { id: 5, name: '杨业文', role: 'AI信息部技术人员', avatar: '杨', phone: '17728889115', online: true },
        { id: 6, name: '李心皓', role: 'AI信息部技术人员', avatar: '李', phone: '18022858406', online: true }
      ],
      tasks: [
        { id: 1, title: '完成UI界面设计', assignee: '李心皓', dueDate: '2026-04-12', priority: 'high', progress: 100 },
        { id: 2, title: 'OpenClaw后端接入', assignee: '李心皓', dueDate: '2026-04-13', priority: 'high', progress: 100 },
        { id: 3, title: 'OpenClaw Skills配置', assignee: '李心皓、陈鑫', dueDate: '2026-03-11 ~ 2026-04-13', priority: 'high', progress: 100 },
        { id: 4, title: 'Docker封装', assignee: '李心皓', dueDate: '2026-04-14', priority: 'medium', progress: 80 },
        { id: 5, title: '场外指导', assignee: '李勇、杨业文、陈粤、黎超成', dueDate: '', priority: 'low', progress: 60 }
      ]
    }
  },
  methods: {
    goHome() {
      this.$router.push('/')
    },
    addMember() {
      alert('添加团队成员')
    },
    isWorkingHours() {
      const now = new Date()
      const hours = now.getHours()
      const minutes = now.getMinutes()
      
      const startHour = 9
      const endHour = 18
      const endMinute = 30
      
      if (hours > startHour && hours < endHour) {
        return true
      }
      
      if (hours === startHour && minutes >= 0) {
        return true
      }
      
      if (hours === endHour && minutes <= endMinute) {
        return true
      }
      
      return false
    }
  }
}
</script>

<style scoped>
.team {
  padding: 20px 0;
}

.team-card {
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

.add-btn {
  margin-left: auto;
  padding: 8px 16px;
  border: none;
  border-radius: 8px;
  background-color: #67c23a;
  color: white;
  font-size: 14px;
  cursor: pointer;
}

.team-content {
  padding: 20px;
}

.team-stats {
  display: flex;
  justify-content: space-around;
  background: #f5f7fa;
  border-radius: 12px;
  padding: 30px;
  margin-bottom: 20px;
}

.stat-item {
  text-align: center;
}

.stat-num {
  display: block;
  font-size: 36px;
  font-weight: bold;
  color: #1890ff;
}

.stat-text {
  font-size: 14px;
  color: #909399;
}

.section-title {
  font-size: 16px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 15px;
}

.members-list {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  margin-bottom: 20px;
}

.member-item {
  display: flex;
  align-items: center;
  background: #f5f7fa;
  border-radius: 12px;
  padding: 12px 15px;
}

.member-avatar {
  width: 45px;
  height: 45px;
  border-radius: 50%;
  background-color: #1890ff;
  color: white;
  font-size: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 15px;
  position: relative;
}

.member-avatar.online::after {
  content: '';
  position: absolute;
  bottom: 0;
  right: 0;
  width: 12px;
  height: 12px;
  background-color: #67c23a;
  border-radius: 50%;
  border: 2px solid #f5f7fa;
}

.member-info {
  flex: 1;
}

.member-name {
  font-size: 14px;
  font-weight: bold;
  color: #303133;
}

.member-role {
  font-size: 12px;
  color: #909399;
}

.member-phone {
  font-size: 12px;
  color: #1890ff;
  margin-top: 2px;
}

.member-status {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 12px;
  color: #909399;
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: #ccc;
}

.status-dot.online {
  background-color: #67c23a;
}

.tasks-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.task-item {
  display: flex;
  align-items: center;
  background: #f5f7fa;
  border-radius: 12px;
  padding: 15px;
}

.task-priority {
  width: 8px;
  height: 40px;
  border-radius: 4px;
  margin-right: 15px;
}

.task-priority.high { background-color: #f56c6c; }
.task-priority.medium { background-color: #e6a23c; }
.task-priority.low { background-color: #67c23a; }

.task-content {
  flex: 1;
}

.task-title {
  font-size: 14px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 5px;
}

.task-meta {
  font-size: 12px;
  color: #909399;
}

.task-progress {
  display: flex;
  align-items: center;
  gap: 10px;
  width: 150px;
}

.progress-bar {
  flex: 1;
  height: 8px;
  background-color: #e4e7ed;
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background-color: #67c23a;
  border-radius: 4px;
  transition: width 0.3s ease;
}

.progress-text {
  font-size: 12px;
  color: #67c23a;
  font-weight: bold;
  min-width: 35px;
  text-align: right;
}
</style>