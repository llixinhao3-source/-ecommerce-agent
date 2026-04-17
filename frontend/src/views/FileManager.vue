<template>
  <div class="file-manager">
    <div class="file-card">
      <div class="card-header">
        <button class="home-btn" @click="goHome">
          <span class="home-icon">🏠</span>
        </button>
        <span>文件管理</span>
        <button class="upload-btn" @click="uploadFile">📤 上传文件</button>
      </div>
      <div class="file-content">
        <div class="file-nav">
          <div 
            v-for="tab in tabs" 
            :key="tab.id"
            :class="['nav-item', { active: activeTab === tab.id }]"
            @click="activeTab = tab.id"
          >
            {{ tab.name }}
            <span class="nav-count">{{ tab.count }}</span>
          </div>
        </div>
        
        <div class="file-list">
          <div v-if="filteredFiles.length === 0" class="empty-state">
            <span class="empty-icon">📂</span>
            <p>暂无{{ activeTab === 'all' ? '' : getTabName(activeTab) }}文件</p>
          </div>
          <div v-else class="files-grid">
            <div 
              v-for="file in filteredFiles" 
              :key="file.id" 
              class="file-item"
              @click="openFile(file)"
            >
              <div :class="['file-icon', file.type]">{{ getFileIcon(file.type) }}</div>
              <div class="file-name">{{ file.name }}</div>
              <div class="file-info">{{ file.size }} · {{ file.date }}</div>
            </div>
          </div>
        </div>
        
        <input type="file" id="file-input" class="hidden-input" @change="handleFileUpload">
      </div>
      
      <!-- 图片预览弹窗 -->
      <div v-if="showPreview" class="preview-modal" @click="closePreview">
        <div class="preview-content" @click.stop>
          <button class="close-btn" @click="closePreview">×</button>
          <img :src="previewImage" alt="图片预览" class="preview-image">
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'FileManager',
  data() {
    return {
      activeTab: 'all',
      showPreview: false,
      previewImage: '',
      tabs: [
        { id: 'all', name: '全部', count: 12 },
        { id: 'image', name: '图片', count: 5 },
        { id: 'document', name: '文档', count: 4 },
        { id: 'other', name: '其他', count: 3 }
      ],
      files: [
        { id: 1, name: '项目报告.pdf', type: 'document', size: '2.3 MB', date: '2024-01-15' },
        { id: 2, name: '设计稿.png', type: 'image', size: '1.5 MB', date: '2024-01-14' },
        { id: 3, name: '数据表格.xlsx', type: 'document', size: '856 KB', date: '2024-01-13' },
        { id: 4, name: '截图.png', type: 'image', size: '456 KB', date: '2024-01-12' },
        { id: 5, name: '会议记录.docx', type: 'document', size: '128 KB', date: '2024-01-11' },
        { id: 6, name: 'logo.svg', type: 'image', size: '24 KB', date: '2024-01-10' },
        { id: 7, name: '演示文稿.pptx', type: 'document', size: '5.6 MB', date: '2024-01-09' },
        { id: 8, name: '照片.jpg', type: 'image', size: '2.1 MB', date: '2024-01-08' },
        { id: 9, name: '压缩包.zip', type: 'other', size: '15 MB', date: '2024-01-07' },
        { id: 10, name: '配置文件.json', type: 'other', size: '2 KB', date: '2024-01-06' },
        { id: 11, name: '代码.js', type: 'other', size: '45 KB', date: '2024-01-05' },
        { id: 12, name: '头像.png', type: 'image', size: '128 KB', date: '2024-01-04' }
      ]
    }
  },
  methods: {
    goHome() {
      this.$router.push('/')
    },
    getFileIcon(type) {
      const icons = {
        image: '🖼️',
        document: '📄',
        other: '📁'
      }
      return icons[type] || '📁'
    },
    uploadFile() {
      document.getElementById('file-input').click()
    },
    async handleFileUpload(event) {
      const file = event.target.files[0]
      if (file) {
        const formData = new FormData()
        formData.append('file', file)
        
        try {
          const response = await fetch('/api/files/upload', {
            method: 'POST',
            body: formData
          })
          
          if (response.ok) {
            const result = await response.json()
            const type = file.type.startsWith('image/') ? 'image' : 
                         file.name.match(/\.(pdf|docx|xlsx|pptx)$/i) ? 'document' : 'other'
            const newFile = {
              id: result.id,
              name: file.name,
              type: type,
              size: this.formatSize(file.size),
              date: new Date().toISOString().split('T')[0],
              url: result.url
            }
            this.files.unshift(newFile)
            this.tabs.forEach(tab => {
              if (tab.id === 'all' || tab.id === type) {
                tab.count++
              }
            })
          }
        } catch (error) {
          console.error('文件上传失败:', error)
          const type = file.type.startsWith('image/') ? 'image' : 
                       file.name.match(/\.(pdf|docx|xlsx|pptx)$/i) ? 'document' : 'other'
          const newFile = {
            id: Date.now(),
            name: file.name,
            type: type,
            size: this.formatSize(file.size),
            date: new Date().toISOString().split('T')[0],
            url: `https://picsum.photos/800/600?random=${Date.now()}`
          }
          this.files.unshift(newFile)
          this.tabs.forEach(tab => {
            if (tab.id === 'all' || tab.id === type) {
              tab.count++
            }
          })
        }
      }
      event.target.value = ''
    },
    formatSize(bytes) {
      if (bytes < 1024) return bytes + ' B'
      if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
      return (bytes / (1024 * 1024)).toFixed(1) + ' MB'
    },
    openFile(file) {
      if (file.type === 'image') {
        this.previewImage = file.url || `https://picsum.photos/800/600?random=${file.id}`
        this.showPreview = true
      } else {
        alert(`打开文件: ${file.name}`)
      }
    },
    closePreview() {
      this.showPreview = false
      this.previewImage = ''
    },
    getTabName(tabId) {
      const tab = this.tabs.find(t => t.id === tabId)
      return tab ? tab.name : ''
    }
  },
  computed: {
    filteredFiles() {
      if (this.activeTab === 'all') {
        return this.files
      }
      return this.files.filter(file => file.type === this.activeTab)
    }
  }
}
</script>

<style scoped>
.file-manager {
  padding: 20px 0;
}

.file-card {
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

.upload-btn {
  margin-left: auto;
  padding: 8px 16px;
  border: none;
  border-radius: 8px;
  background-color: #1890ff;
  color: white;
  font-size: 14px;
  cursor: pointer;
}

.file-content {
  padding: 20px;
}

.file-nav {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.nav-item {
  padding: 8px 16px;
  border-radius: 20px;
  background-color: #f5f7fa;
  font-size: 14px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 5px;
  transition: all 0.3s ease;
}

.nav-item.active {
  background-color: #1890ff;
  color: white;
}

.nav-count {
  background-color: rgba(0, 0, 0, 0.1);
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 12px;
}

.nav-item.active .nav-count {
  background-color: rgba(255, 255, 255, 0.2);
}

.file-list {
  min-height: 400px;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px;
  color: #909399;
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 15px;
}

.files-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 15px;
}

.file-item {
  background: #f5f7fa;
  border-radius: 12px;
  padding: 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.file-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.file-icon {
  font-size: 40px;
  margin-bottom: 10px;
}

.file-name {
  font-size: 14px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 5px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.file-info {
  font-size: 12px;
  color: #909399;
}

.hidden-input {
  display: none;
}

.preview-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.preview-content {
  position: relative;
  max-width: 90%;
  max-height: 90%;
  background: white;
  border-radius: 12px;
  overflow: hidden;
}

.close-btn {
  position: absolute;
  top: 15px;
  right: 15px;
  width: 40px;
  height: 40px;
  border: none;
  border-radius: 50%;
  background-color: rgba(0, 0, 0, 0.5);
  color: white;
  font-size: 24px;
  cursor: pointer;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-btn:hover {
  background-color: rgba(0, 0, 0, 0.7);
}

.preview-image {
  max-width: 100%;
  max-height: 80vh;
  display: block;
}
</style>