<template>
  <div class="settings">
    <div class="settings-card">
      <div class="card-header">
        <button class="home-btn" @click="goHome">
          <span class="home-icon">🏠</span>
        </button>
        <span>系统设置</span>
      </div>
      <div class="settings-content">
        <div class="tabs">
          <div class="tab-nav">
            <div 
              v-for="tab in tabs" 
              :key="tab.name"
              :class="['tab-item', { active: activeTab === tab.name }]"
              @click="activeTab = tab.name"
            >
              {{ tab.label }}
            </div>
          </div>
          
          <div class="tab-content" v-show="activeTab === 'basic'">
            <div class="form-group">
              <label>工作目录</label>
              <input type="text" v-model="settings.workingDirectory" disabled class="form-input" />
            </div>
            <div class="form-group">
              <label>最大并发</label>
              <input type="number" v-model.number="settings.maxConcurrency" min="1" max="10" class="form-input" />
            </div>
            <div class="form-group">
              <label>子代理最大并发</label>
              <input type="number" v-model.number="settings.maxSubAgentConcurrency" min="1" max="20" class="form-input" />
            </div>
            <div class="form-group">
              <label>超时时间 (秒)</label>
              <input type="number" v-model.number="settings.timeoutSeconds" min="30" max="600" class="form-input" />
            </div>
          </div>
          
          <div class="tab-content" v-show="activeTab === 'ai'">
            <div class="form-group">
              <label>主模型</label>
              <select v-model="aiSettings.mainModel" class="form-input">
                <option value="minimax/MiniMax-M2.7">MiniMax M2.7</option>
                <option value="minimax-portal/MiniMax-M2.5">MiniMax M2.5</option>
                <option value="minimax-portal/MiniMax-M2.5-highspeed">MiniMax M2.5 Highspeed</option>
                <option value="minimax-portal/MiniMax-M2.5-Lightning">MiniMax M2.5 Lightning</option>
              </select>
            </div>
            <div class="form-group">
              <label class="checkbox-label">
                <input type="checkbox" v-model="aiSettings.memorySearch.enabled" />
                启用内存搜索
              </label>
            </div>
            <div class="form-group">
              <label>压缩模式</label>
              <select v-model="aiSettings.compressionMode" class="form-input">
                <option value="safeguard">安全保护模式</option>
                <option value="balanced">平衡模式</option>
                <option value="aggressive">激进模式</option>
              </select>
            </div>
          </div>
          
          <div class="tab-content" v-show="activeTab === 'channels'">
            <div class="form-group">
              <label class="checkbox-label">
                <input type="checkbox" v-model="channelSettings.dingtalk.enabled" />
                启用钉钉连接器
              </label>
            </div>
            <div class="form-group">
              <label class="checkbox-label">
                <input type="checkbox" v-model="channelSettings.weixin.enabled" />
                启用微信集成
              </label>
            </div>
            <div class="form-group">
              <label class="checkbox-label">
                <input type="checkbox" v-model="channelSettings.voiceCall.enabled" />
                启用语音通话
              </label>
            </div>
          </div>
          
          <div class="tab-content" v-show="activeTab === 'browser'">
            <div class="form-group">
              <label class="checkbox-label">
                <input type="checkbox" v-model="browserSettings.enabled" />
                启用浏览器自动化
              </label>
            </div>
            <div class="form-group">
              <label>默认配置</label>
              <input type="text" v-model="browserSettings.defaultProfile" class="form-input" />
            </div>
            <div class="form-group">
              <label>CDP端口</label>
              <input type="number" v-model.number="browserSettings.cdpPort" min="9000" max="9999" class="form-input" :disabled="!browserSettings.enabled" />
            </div>
            <div class="form-group">
              <label>颜色标识</label>
              <input type="color" v-model="browserSettings.color" class="form-input color-input" />
            </div>
          </div>
        </div>
        
        <div class="settings-actions">
          <button class="btn btn-primary" @click="saveSettings">保存设置</button>
          <button class="btn btn-default" @click="resetSettings">重置</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Settings',
  data() {
    return {
      activeTab: 'basic',
      tabs: [
        { name: 'basic', label: '基本设置' },
        { name: 'ai', label: 'AI模型' },
        { name: 'channels', label: '通讯渠道' },
        { name: 'browser', label: '浏览器' }
      ],
      settings: {
        workingDirectory: 'C:\\Users\\IT\\.openclaw\\workspace',
        maxConcurrency: 4,
        maxSubAgentConcurrency: 8,
        timeoutSeconds: 300
      },
      aiSettings: {
        mainModel: 'minimax/MiniMax-M2.7',
        memorySearch: {
          enabled: true
        },
        compressionMode: 'safeguard'
      },
      channelSettings: {
        dingtalk: {
          enabled: true
        },
        weixin: {
          enabled: true
        },
        voiceCall: {
          enabled: true
        }
      },
      browserSettings: {
        enabled: true,
        defaultProfile: 'openclaw',
        cdpPort: 9222,
        color: '#FF4500'
      }
    }
  },
  methods: {
    goHome() {
      this.$router.push('/')
    },
    saveSettings() {
      alert('设置保存成功')
    },
    resetSettings() {
      if (confirm('确定要重置所有设置吗？')) {
        this.settings = {
          workingDirectory: 'C:\\Users\\IT\\.openclaw\\workspace',
          maxConcurrency: 4,
          maxSubAgentConcurrency: 8,
          timeoutSeconds: 300
        }
        this.aiSettings = {
          mainModel: 'minimax/MiniMax-M2.7',
          memorySearch: {
            enabled: true
          },
          compressionMode: 'safeguard'
        }
        this.channelSettings = {
          dingtalk: {
            enabled: true
          },
          weixin: {
            enabled: true
          },
          voiceCall: {
            enabled: true
          }
        }
        this.browserSettings = {
          enabled: true,
          defaultProfile: 'openclaw',
          cdpPort: 9222,
          color: '#FF4500'
        }
        alert('设置已重置')
      }
    }
  }
}
</script>

<style scoped>
.settings {
  padding: 20px 0;
}

.settings-card {
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

.settings-content {
  padding: 20px;
}

.tabs {
  margin-bottom: 20px;
}

.tab-nav {
  display: flex;
  border-bottom: 1px solid #ebeef5;
  margin-bottom: 20px;
}

.tab-item {
  padding: 12px 20px;
  cursor: pointer;
  color: #606266;
  border-bottom: 2px solid transparent;
  transition: all 0.3s;
}

.tab-item:hover {
  color: #1890ff;
}

.tab-item.active {
  color: #1890ff;
  border-bottom-color: #1890ff;
}

.tab-content {
  padding: 10px 0;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  color: #606266;
  font-size: 14px;
}

.form-input {
  width: 100%;
  max-width: 400px;
  padding: 10px 15px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  font-size: 14px;
}

.form-input:focus {
  outline: none;
  border-color: #1890ff;
}

.form-input:disabled {
  background-color: #f5f7fa;
  color: #c0c4cc;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.checkbox-label input[type="checkbox"] {
  width: 18px;
  height: 18px;
  cursor: pointer;
}

.color-input {
  width: 100px;
  height: 40px;
  padding: 2px;
  cursor: pointer;
}

.settings-actions {
  margin-top: 30px;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.btn {
  padding: 10px 24px;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-primary {
  background-color: #1890ff;
  color: white;
}

.btn-primary:hover {
  background-color: #40a9ff;
}

.btn-default {
  background-color: #f4f4f5;
  color: #606266;
  border: 1px solid #dcdfe6;
}

.btn-default:hover {
  background-color: #e9e9eb;
}
</style>