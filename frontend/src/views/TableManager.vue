<template>
  <div class="table-manager">
    <div class="page-header">
      <button class="back-btn" @click="goBack">
        <span>←</span>
      </button>
      <h2>📊 多维表格管理</h2>
    </div>

    <div class="table-container">
      <div class="tabs">
        <button 
          v-for="tab in tabs" 
          :key="tab.id"
          :class="['tab-btn', { active: activeTab === tab.id }]"
          @click="activeTab = tab.id"
        >
          {{ tab.name }}
        </button>
      </div>

      <div class="tab-content">
        <!-- 飞书表格 -->
        <div v-if="activeTab === 'feishu'" class="tab-panel">
          <div class="panel-header">
            <h3>飞书多维表格</h3>
            <button class="add-btn" @click="showFeishuModal = true">+ 添加表格</button>
          </div>
          <div class="table-grid">
            <div v-for="table in feishuTables" :key="table.id" class="table-card">
              <div class="card-header">
                <span class="table-icon">📋</span>
                <span class="table-name">{{ table.name }}</span>
              </div>
              <p class="table-desc">{{ table.description }}</p>
              <div class="table-info">
                <span>📝 {{ table.rows }} 行</span>
                <span>📁 {{ table.columns }} 列</span>
              </div>
              <div class="table-actions">
                <a v-if="table.url" :href="table.url" target="_blank" rel="noopener noreferrer" class="action-btn">打开</a>
                <span v-else class="action-btn disabled">暂无链接</span>
                <button class="action-btn ai-btn" @click="analyzeTable(table)">🤖 分析</button>
              </div>
            </div>
          </div>
        </div>

        <!-- 钉钉表格 -->
        <div v-if="activeTab === 'dingtalk'" class="tab-panel">
          <div class="panel-header">
            <h3>钉钉多维表格</h3>
            <button class="add-btn" @click="showDingtalkModal = true">+ 添加表格</button>
          </div>
          <div class="table-grid">
            <div v-for="table in dingtalkTables" :key="table.id" class="table-card">
              <div class="card-header">
                <span class="table-icon">📊</span>
                <span class="table-name">{{ table.name }}</span>
              </div>
              <p class="table-desc">{{ table.description }}</p>
              <div class="table-info">
                <span>📝 {{ table.rows }} 行</span>
                <span>📁 {{ table.columns }} 列</span>
              </div>
              <div class="table-actions">
                <button v-if="table.url" class="action-btn" @click="openDingtalkTable(table.url)">打开</button>
                <span v-else class="action-btn disabled">暂无链接</span>
                <button class="action-btn ai-btn" @click="analyzeTable(table)">🤖 分析</button>
              </div>
            </div>
          </div>
        </div>

        <!-- AI分析 -->
        <div v-if="activeTab === 'ai'" class="tab-panel">
          <div class="ai-panel">
            <div class="ai-header">
              <h3>🤖 AI数据分析</h3>
              <p class="ai-desc">上传表格数据，让AI帮您分析</p>
            </div>
            
            <div class="ai-input-section">
              <div class="form-group">
                <label>选择数据源</label>
                <select v-model="aiSettings.dataSource" class="form-input">
                  <option value="">请选择表格</option>
                  <optgroup label="飞书表格">
                    <option v-for="table in feishuTables" :key="table.id" :value="'feishu:' + table.id">
                      {{ table.name }}
                    </option>
                  </optgroup>
                  <optgroup label="钉钉表格">
                    <option v-for="table in dingtalkTables" :key="table.id" :value="'dingtalk:' + table.id">
                      {{ table.name }}
                    </option>
                  </optgroup>
                </select>
              </div>

              <div class="form-group">
                <label>分析需求</label>
                <textarea v-model="aiSettings.prompt" class="form-input" rows="4" placeholder="请描述您想要分析的内容，例如：分析销售数据趋势、找出异常值、生成报告等..."></textarea>
              </div>

              <div class="form-group">
                <label>分析类型</label>
                <div class="analysis-types">
                  <button 
                    v-for="type in analysisTypes" 
                    :key="type.id"
                    :class="['type-btn', { active: aiSettings.analysisType === type.id }]"
                    @click="aiSettings.analysisType = type.id"
                  >
                    {{ type.icon }} {{ type.name }}
                  </button>
                </div>
              </div>

              <button class="ai-analyze-btn" @click="runAnalysis" :disabled="!aiSettings.dataSource || !aiSettings.prompt">
                🚀 开始分析
              </button>
            </div>

            <div v-if="aiResult" class="ai-result">
              <div class="result-header">
                <h4>分析结果</h4>
                <button class="close-result" @click="aiResult = null">×</button>
              </div>
              <div class="result-content">
                <pre>{{ aiResult }}</pre>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 飞书表格弹窗 -->
    <div v-if="showFeishuModal" class="modal-overlay" @click.self="showFeishuModal = false">
      <div class="modal-content">
        <h3>添加飞书表格</h3>
        <form @submit.prevent="addFeishuTable">
          <div class="form-group">
            <label>表格名称</label>
            <input type="text" v-model="feishuForm.name" required placeholder="输入表格名称" class="form-input">
          </div>
          <div class="form-group">
            <label>表格描述</label>
            <textarea v-model="feishuForm.description" placeholder="输入表格描述" class="form-input"></textarea>
          </div>
          <div class="form-group">
            <label>表格链接</label>
            <input type="text" v-model="feishuForm.url" placeholder="输入飞书表格链接" class="form-input">
          </div>
          <div class="form-actions">
            <button type="button" class="cancel-btn" @click="showFeishuModal = false">取消</button>
            <button type="submit" class="submit-btn">添加</button>
          </div>
        </form>
      </div>
    </div>

    <!-- 钉钉表格弹窗 -->
    <div v-if="showDingtalkModal" class="modal-overlay" @click.self="showDingtalkModal = false">
      <div class="modal-content">
        <h3>添加钉钉表格</h3>
        <form @submit.prevent="addDingtalkTable">
          <div class="form-group">
            <label>表格名称</label>
            <input type="text" v-model="dingtalkForm.name" required placeholder="输入表格名称" class="form-input">
          </div>
          <div class="form-group">
            <label>表格描述</label>
            <textarea v-model="dingtalkForm.description" placeholder="输入表格描述" class="form-input"></textarea>
          </div>
          <div class="form-group">
            <label>表格链接</label>
            <input type="text" v-model="dingtalkForm.url" placeholder="输入钉钉表格链接" class="form-input">
          </div>
          <div class="form-actions">
            <button type="button" class="cancel-btn" @click="showDingtalkModal = false">取消</button>
            <button type="submit" class="submit-btn">添加</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'TableManager',
  data() {
    return {
      activeTab: 'feishu',
      tabs: [
        { id: 'feishu', name: '飞书表格' },
        { id: 'dingtalk', name: '钉钉表格' },
        { id: 'ai', name: 'AI分析' }
      ],
      feishuTables: [],
      dingtalkTables: [],
      showFeishuModal: false,
      showDingtalkModal: false,
      feishuForm: {
        name: '',
        description: '',
        url: ''
      },
      dingtalkForm: {
        name: '',
        description: '',
        url: ''
      },
      aiSettings: {
        dataSource: '',
        prompt: '',
        analysisType: 'summary'
      },
      analysisTypes: [
        { id: 'summary', name: '数据汇总', icon: '📊' },
        { id: 'trend', name: '趋势分析', icon: '📈' },
        { id: 'anomaly', name: '异常检测', icon: '⚠️' },
        { id: 'predict', name: '预测分析', icon: '🔮' },
        { id: 'report', name: '生成报告', icon: '📝' }
      ],
      aiResult: null
    }
  },
  mounted() {
    this.loadTables()
  },
  methods: {
    goBack() {
      this.$router.push('/')
    },
    getDingtalkUrl(url) {
      if (!url) return ''
      if (url.startsWith('dingtalk://')) {
        return url
      }
      if (url.startsWith('https://space.dingtalk.com/')) {
        const match = url.match(/space\.dingtalk\.com\/s\/([^/?]+)/)
        if (match && match[1]) {
          const spaceId = match[1]
          return `dingtalk://dingtalkclient/space/home?spaceId=${spaceId}`
        }
      }
      const encodedUrl = encodeURIComponent(url)
      return `dingtalk://dingtalkclient/page/link?url=${encodedUrl}&pc_slide=true`
    },
    openDingtalkTable(url) {
      if (!url || url.includes('some-space-id') || url.includes('another-space-id') || url.includes('third-space-id')) {
        alert('当前表格链接为演示数据，请添加真实的钉钉多维表格链接后再试')
        return
      }
      
      const dingtalkUrl = this.getDingtalkUrl(url)
      const link = document.createElement('a')
      link.href = dingtalkUrl
      link.target = '_blank'
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      
      setTimeout(() => {
        const fallbackUrl = `https://im.dingtalk.com/#/login?redirectUrl=${encodeURIComponent(url)}`
        window.open(fallbackUrl, '_blank')
      }, 2000)
      
      alert('正在尝试打开钉钉客户端...\n\n如果钉钉没有自动打开，请在浏览器中手动打开网页版')
    },
    async loadTables() {
      try {
        const response = await axios.get('/api/tables')
        if (response.data.success) {
          this.feishuTables = response.data.data.feishu || this.getMockFeishuTables()
          this.dingtalkTables = response.data.data.dingtalk || this.getMockDingtalkTables()
        } else {
          this.feishuTables = this.getMockFeishuTables()
          this.dingtalkTables = this.getMockDingtalkTables()
        }
      } catch (error) {
        this.feishuTables = this.getMockFeishuTables()
        this.dingtalkTables = this.getMockDingtalkTables()
      }
    },
    getMockFeishuTables() {
      return [
        { id: 'feishu-001', name: '销售数据报表', description: '2024年度销售数据汇总', rows: 156, columns: 8, url: 'https://www.feishu.cn/drive/folder/fldabc123' },
        { id: 'feishu-002', name: '客户信息表', description: '客户联系信息和跟进记录', rows: 320, columns: 12, url: 'https://www.feishu.cn/drive/folder/fldabc124' },
        { id: 'feishu-003', name: '库存管理', description: '产品库存和出入库记录', rows: 89, columns: 6, url: 'https://www.feishu.cn/drive/folder/fldabc125' },
        { id: 'feishu-004', name: '项目进度跟踪', description: '各项目进度和里程碑', rows: 24, columns: 10, url: 'https://www.feishu.cn/drive/folder/fldabc126' }
      ]
    },
    getMockDingtalkTables() {
      return [
        { id: 'dingtalk-001', name: '周报汇总', description: '团队周报汇总表', rows: 45, columns: 5, url: 'https://space.dingtalk.com/s/some-space-id' },
        { id: 'dingtalk-002', name: '考勤记录', description: '员工考勤打卡记录', rows: 500, columns: 4, url: 'https://space.dingtalk.com/s/another-space-id' },
        { id: 'dingtalk-003', name: '采购订单', description: '采购申请和订单记录', rows: 78, columns: 15, url: 'https://space.dingtalk.com/s/third-space-id' }
      ]
    },
    async addFeishuTable() {
      try {
        const response = await axios.post('/api/tables/feishu', {
          name: this.feishuForm.name,
          description: this.feishuForm.description,
          url: this.feishuForm.url
        })
        if (response.data.success) {
          this.feishuTables.push(response.data.data)
          this.showFeishuModal = false
          this.feishuForm = { name: '', description: '', url: '' }
        }
      } catch (error) {
        console.error('添加飞书表格失败:', error)
      }
    },
    async addDingtalkTable() {
      try {
        const response = await axios.post('/api/tables/dingtalk', {
          name: this.dingtalkForm.name,
          description: this.dingtalkForm.description,
          url: this.dingtalkForm.url
        })
        if (response.data.success) {
          this.dingtalkTables.push(response.data.data)
          this.showDingtalkModal = false
          this.dingtalkForm = { name: '', description: '', url: '' }
        }
      } catch (error) {
        console.error('添加钉钉表格失败:', error)
      }
    },
    
    async analyzeTable(table) {
      this.activeTab = 'ai'
      this.aiSettings.dataSource = table.url ? table.url : (table.id.startsWith('feishu') ? 'feishu:' : 'dingtalk:') + table.id
      this.aiSettings.prompt = `请帮我分析这个表格的数据：${table.name}`
    },
    async runAnalysis() {
      try {
        this.aiResult = '🤖 AI正在分析数据，请稍候...'
        
        console.log('[DEBUG] 发送分析请求:', {
          dataSource: this.aiSettings.dataSource,
          prompt: this.aiSettings.prompt,
          analysisType: this.aiSettings.analysisType
        })
        
        const response = await axios.post('/api/tables/analyze', {
          dataSource: this.aiSettings.dataSource,
          prompt: this.aiSettings.prompt,
          analysisType: this.aiSettings.analysisType
        }, {
          headers: {
            'Content-Type': 'application/json'
          }
        })
        
        console.log('[DEBUG] 分析响应:', response.data)
        
        if (response.data.success) {
          this.aiResult = response.data.data.result
        } else {
          this.aiResult = '分析失败：' + response.data.error
        }
      } catch (error) {
        console.error('[ERROR] 分析请求失败:', error)
        this.aiResult = '分析失败：' + (error.message || '未知错误')
      }
    }
  }
}
</script>

<style scoped>
.table-manager {
  min-height: 100vh;
  background: #f5f7fa;
  padding: 20px;
}

.page-header {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 20px;
  color: #333;
}

.back-btn {
  background: #f0f0f0;
  border: 1px solid #e0e0e0;
  color: #333;
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

.table-container {
  max-width: 1200px;
  margin: 0 auto;
}

.tabs {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  background: white;
  padding: 10px;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
}

.tab-btn {
  padding: 12px 24px;
  border: none;
  background: transparent;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  color: #666;
  transition: all 0.3s;
}

.tab-btn.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.tab-content {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.05);
}

.tab-panel {
  min-height: 400px;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.panel-header h3 {
  margin: 0;
  color: #333;
}

.add-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 14px;
}

.table-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.table-card {
  background: #fafafa;
  border-radius: 12px;
  padding: 20px;
  border: 1px solid #e0e0e0;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 10px;
}

.table-icon {
  font-size: 24px;
}

.table-name {
  font-weight: bold;
  color: #333;
}

.table-desc {
  color: #666;
  font-size: 14px;
  margin-bottom: 15px;
}

.table-info {
  display: flex;
  gap: 15px;
  margin-bottom: 15px;
  font-size: 12px;
  color: #999;
}

.table-actions {
  display: flex;
  gap: 10px;
}

.action-btn {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid #ddd;
  background: white;
  border-radius: 6px;
  cursor: pointer;
  font-size: 12px;
  transition: all 0.3s;
}

.action-btn:hover {
  border-color: #667eea;
  color: #667eea;
}

.action-btn.ai-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  color: white;
}

.action-btn.ai-btn:hover {
  opacity: 0.8;
}

.action-btn.disabled {
  background: #f5f5f5;
  color: #999;
  cursor: not-allowed;
  border-color: #e0e0e0;
}

/* AI面板 */
.ai-panel {
  max-width: 800px;
  margin: 0 auto;
}

.ai-header {
  text-align: center;
  margin-bottom: 30px;
}

.ai-header h3 {
  font-size: 20px;
  color: #333;
}

.ai-desc {
  color: #666;
  font-size: 14px;
}

.ai-input-section {
  background: #fafafa;
  padding: 20px;
  border-radius: 12px;
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

.form-input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  box-sizing: border-box;
}

.form-input:focus {
  outline: none;
  border-color: #667eea;
}

.analysis-types {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.type-btn {
  padding: 8px 16px;
  border: 1px solid #ddd;
  background: white;
  border-radius: 20px;
  cursor: pointer;
  font-size: 13px;
  transition: all 0.3s;
}

.type-btn.active {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-color: transparent;
  color: white;
}

.ai-analyze-btn {
  width: 100%;
  padding: 15px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  cursor: pointer;
  margin-top: 10px;
}

.ai-analyze-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.ai-result {
  margin-top: 20px;
  background: #f0f8ff;
  border: 1px solid #b3d9ff;
  border-radius: 12px;
}

.result-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 20px;
  border-bottom: 1px solid #b3d9ff;
}

.result-header h4 {
  margin: 0;
  color: #333;
}

.close-result {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #999;
}

.result-content {
  padding: 20px;
}

.result-content pre {
  white-space: pre-wrap;
  word-break: break-all;
  color: #333;
  font-family: inherit;
  font-size: 14px;
  line-height: 1.6;
}

/* 弹窗样式 */
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