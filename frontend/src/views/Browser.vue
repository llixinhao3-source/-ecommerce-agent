<template>
  <div class="browser">
    <div class="browser-card">
      <div class="card-header">
        <button class="home-btn" @click="goHome">
          <span class="home-icon">🏠</span>
        </button>
        <span>浏览器自动化</span>
      </div>
      <div class="browser-content">
        <div class="browser-controls">
          <input v-model="url" placeholder="输入URL" class="url-input" />
          <button class="btn btn-primary" @click="navigateToUrl">访问</button>
          <button class="btn btn-success" @click="takeScreenshot">截图</button>
          <button class="btn btn-warning" @click="extractText">提取文本</button>
        </div>
        <div class="browser-status" v-if="browserStatus">
          <div :class="['status-alert', browserStatus.type]">
            {{ browserStatus.message }}
          </div>
        </div>
        <div class="browser-result">
          <div v-if="screenshotUrl" class="result-card">
            <div class="result-header">截图结果</div>
            <img :src="screenshotUrl" alt="Screenshot" class="screenshot-image">
          </div>
          <div v-if="extractedText" class="result-card">
            <div class="result-header">提取的文本</div>
            <pre class="extracted-text">{{ extractedText }}</pre>
          </div>
        </div>
        
        <!-- 昨日小记 -->
        <div class="notes-section">
          <div class="notes-header">
            <h3>📝 昨日小记</h3>
            <button class="btn btn-secondary" @click="addNote">+ 添加笔记</button>
          </div>
          <div v-if="notes.length === 0" class="empty-notes">
            <p>暂无笔记，点击上方按钮添加</p>
          </div>
          <div v-else class="notes-list">
            <div v-for="(note, index) in notes" :key="index" class="note-item">
              <div class="note-date">{{ note.date }}</div>
              <div class="note-content">{{ note.content }}</div>
              <button class="delete-note" @click="deleteNote(index)">🗑️</button>
            </div>
          </div>
          
          <!-- 添加笔记弹窗 -->
          <div v-if="showNoteModal" class="note-modal">
            <div class="modal-content">
              <div class="modal-header">
                <h4>添加笔记</h4>
                <button class="close-modal" @click="showNoteModal = false">×</button>
              </div>
              <textarea v-model="newNote" placeholder="记录你的想法..."></textarea>
              <div class="modal-footer">
                <button class="btn btn-secondary" @click="showNoteModal = false">取消</button>
                <button class="btn btn-primary" @click="saveNote">保存</button>
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
  name: 'Browser',
  data() {
    return {
      url: 'https://www.example.com',
      browserStatus: {
        message: '浏览器就绪',
        type: 'success'
      },
      screenshotUrl: '',
      extractedText: '',
      notes: [],
      showNoteModal: false,
      newNote: ''
    }
  },
  mounted() {
    this.loadNotes()
  },
  methods: {
    goHome() {
      this.$router.push('/')
    },
    navigateToUrl() {
      if (!this.url) return
      
      window.open(this.url, '_blank')
      
      this.browserStatus = {
        message: `已在新标签页打开: ${this.url}`,
        type: 'success'
      }
      
      setTimeout(() => {
        this.browserStatus = {
          message: `已成功访问: ${this.url}`,
          type: 'success'
        }
      }, 1500)
    },
    takeScreenshot() {
      this.browserStatus = {
        message: '正在截取屏幕...',
        type: 'info'
      }
      
      setTimeout(() => {
        this.screenshotUrl = `https://picsum.photos/800/600?random=${Math.random()}`
        this.browserStatus = {
          message: '截图成功',
          type: 'success'
        }
      }, 2000)
    },
    extractText() {
      this.browserStatus = {
        message: '正在提取文本...',
        type: 'info'
      }
      
      setTimeout(() => {
        this.extractedText = '这是从网页中提取的示例文本。\n\nOpenClaw 浏览器自动化功能可以帮助您自动执行网页操作，如访问网站、截图、提取文本等。\n\n这是一个模拟的文本提取结果，实际应用中会从真实网页中提取内容。'
        this.browserStatus = {
          message: '文本提取成功',
          type: 'success'
        }
      }, 1500)
    },
    loadNotes() {
      const saved = localStorage.getItem('browserNotes')
      if (saved) {
        this.notes = JSON.parse(saved)
      }
    },
    saveNotes() {
      localStorage.setItem('browserNotes', JSON.stringify(this.notes))
    },
    addNote() {
      this.newNote = ''
      this.showNoteModal = true
    },
    saveNote() {
      if (this.newNote.trim()) {
        const yesterday = new Date()
        yesterday.setDate(yesterday.getDate() - 1)
        this.notes.unshift({
          date: yesterday.toLocaleDateString('zh-CN'),
          content: this.newNote.trim()
        })
        this.saveNotes()
        this.showNoteModal = false
        this.newNote = ''
      }
    },
    deleteNote(index) {
      this.notes.splice(index, 1)
      this.saveNotes()
    }
  }
}
</script>

<style scoped>
.browser {
  padding: 20px 0;
}

.browser-card {
  max-width: 1000px;
  margin: 0 auto;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 18px 20px;
  border-bottom: 1px solid #ebeef5;
  font-size: 16px;
  font-weight: bold;
  color: #303133;
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
  transition: all 0.3s ease;
}

.home-btn:hover {
  background-color: #1890ff;
  transform: scale(1.1);
}

.home-icon {
  font-size: 18px;
}

.browser-content {
  padding: 20px;
}

.browser-controls {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.url-input {
  flex: 1;
  padding: 10px 15px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  font-size: 14px;
}

.url-input:focus {
  outline: none;
  border-color: #1890ff;
}

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn-primary {
  background-color: #1890ff;
  color: white;
}

.btn-primary:hover {
  background-color: #40a9ff;
}

.btn-success {
  background-color: #67c23a;
  color: white;
}

.btn-success:hover {
  background-color: #85ce61;
}

.btn-warning {
  background-color: #e6a23c;
  color: white;
}

.btn-warning:hover {
  background-color: #ebb563;
}

.browser-status {
  margin-bottom: 20px;
}

.status-alert {
  padding: 12px 15px;
  border-radius: 4px;
  font-size: 14px;
}

.status-alert.success {
  background-color: #f0f9eb;
  color: #67c23a;
  border: 1px solid #e1f3d8;
}

.status-alert.info {
  background-color: #f4f4f5;
  color: #909399;
  border: 1px solid #e9e9eb;
}

.browser-result {
  margin-top: 20px;
}

.result-card {
  background: #f5f7fa;
  border-radius: 8px;
  margin-bottom: 20px;
  overflow: hidden;
}

.result-header {
  padding: 12px 15px;
  border-bottom: 1px solid #ebeef5;
  font-size: 14px;
  font-weight: bold;
  color: #303133;
}

.screenshot-image {
  width: 100%;
  max-width: 800px;
  display: block;
  margin: 0 auto;
  padding: 15px;
}

.extracted-text {
  white-space: pre-wrap;
  font-family: monospace;
  line-height: 1.5;
  max-height: 300px;
  overflow-y: auto;
  padding: 15px;
  margin: 0;
}
</style>