<template>
  <div class="chat-container">
    <!-- 左侧历史记录面板 -->
    <div class="history-panel" :class="{ 'collapsed': !showHistory }">
      <div class="history-header">
        <span>📋 聊天历史</span>
        <button class="collapse-btn" @click="toggleHistory">
          {{ showHistory ? '◀' : '▶' }}
        </button>
      </div>
      <div class="history-list">
        <div 
          v-for="(history, index) in chatHistory" 
          :key="index"
          class="history-item"
          :class="{ 'active': currentHistoryIndex === index }"
          @click="loadHistory(index)"
        >
          <div class="history-preview">{{ history.preview }}</div>
          <div class="history-time">{{ history.time }}</div>
          <button class="delete-history-btn" @click.stop="deleteHistory(index)">✕</button>
        </div>
        <div v-if="chatHistory.length === 0" class="empty-history">
          暂无聊天记录
        </div>
      </div>
      <button class="new-chat-btn" @click="newChat">
        ➕ 新对话
      </button>
    </div>
    
    <!-- 右侧聊天区域 -->
    <div class="chat-main">
      <div class="chat-card">
        <div class="card-header">
          <button class="home-btn" @click="goHome">
            <span class="home-icon">🏠</span>
          </button>
          <span>AI 聊天</span>
          <select v-model="selectedModel" class="model-select">
            <option value="openclaw">OpenClaw</option>
          </select>
        </div>
        <div class="chat-content">
          <div class="chat-messages" ref="chatMessages">
            <div v-for="(message, index) in messages" :key="index" :class="['message-item', message.type]">
              <div class="message-avatar">{{ message.type === 'user' ? '我' : 'AI' }}</div>
              <div class="message-content">
                <p v-if="message.content">{{ message.content }}</p>
                <img v-if="message.image" :src="message.image" class="message-image" alt="图片" />
              </div>
            </div>
            <div v-if="loading" class="message-item ai">
              <div class="message-avatar">AI</div>
              <div class="message-content">
                <span class="loading-icon">⏳</span>
                <span>AI正在思考...</span>
              </div>
            </div>
          </div>
          <div class="chat-input">
            <div v-if="uploadedImage" class="image-preview">
              <img :src="uploadedImage" class="preview-image" />
              <button class="remove-image-btn" @click="removeImage">✕</button>
            </div>
            <textarea
              v-model="inputMessage"
              rows="3"
              placeholder="输入消息..."
              @keyup.enter.ctrl="sendMessage"
              class="message-textarea"
            ></textarea>
            <div class="chat-actions">
              <label class="upload-btn">
                <input type="file" accept="image/*" @change="handleImageUpload" class="file-input" />
                <span>📷 上传图片</span>
              </label>
              <button class="send-btn" @click="sendMessage">发送</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '../services/api'
import axios from 'axios'

const API_TOKEN = '3060a9f22417e0359e7738a94590d9dca38591c3ee2b7e1e'

export default {
  name: 'Chat',
  data() {
    return {
      messages: [
        {
          type: 'ai',
          content: '你好！我是 OpenClaw AI 助手，有什么可以帮助你的吗？\n\n📷 你可以上传图片，我来帮你识别！'
        }
      ],
      inputMessage: '',
      selectedModel: 'openclaw',
      loading: false,
      uploadedImage: null,
      imageFile: null,
      // 历史记录相关
      chatHistory: [],
      currentHistoryIndex: -1,
      showHistory: true,
      historyChanged: false,
      // WebSocket 相关
      ws: null,
      wsConnected: false,
      pendingRequests: {},
      wsRetryCount: 0,
      maxWsRetries: 3
    }
  },
  mounted() {
    this.loadChatHistory()
    this.connectWebSocket()
  },
  beforeDestroy() {
    if (this.ws) {
      this.ws.close()
    }
  },
  watch: {
    messages: {
      deep: true,
      handler() {
        if (this.messages.length > 1) {
          this.historyChanged = true
        }
      }
    }
  },
  methods: {

    // 历史记录方法
    loadChatHistory() {
      const saved = localStorage.getItem('chatHistory')
      if (saved) {
        this.chatHistory = JSON.parse(saved)
      }
    },
    saveChatHistory() {
      if (this.historyChanged && this.messages.length > 1) {
        const preview = this.messages[1]?.content || '新对话'
        const time = new Date().toLocaleString('zh-CN', {
          month: '2-digit',
          day: '2-digit',
          hour: '2-digit',
          minute: '2-digit'
        })
        
        if (this.currentHistoryIndex >= 0) {
          // 更新现有记录
          this.chatHistory[this.currentHistoryIndex] = {
            messages: JSON.parse(JSON.stringify(this.messages)),
            preview: preview.slice(0, 30) + (preview.length > 30 ? '...' : ''),
            time: time
          }
        } else {
          // 创建新记录
          this.chatHistory.unshift({
            messages: JSON.parse(JSON.stringify(this.messages)),
            preview: preview.slice(0, 30) + (preview.length > 30 ? '...' : ''),
            time: time
          })
        }
        
        // 最多保存10条记录
        if (this.chatHistory.length > 10) {
          this.chatHistory = this.chatHistory.slice(0, 10)
        }
        
        localStorage.setItem('chatHistory', JSON.stringify(this.chatHistory))
        this.historyChanged = false
      }
    },
    loadHistory(index) {
      const history = this.chatHistory[index]
      if (history) {
        this.messages = JSON.parse(JSON.stringify(history.messages))
        this.currentHistoryIndex = index
        this.historyChanged = false
        this.scrollToBottom()
      }
    },
    deleteHistory(index) {
      this.chatHistory.splice(index, 1)
      localStorage.setItem('chatHistory', JSON.stringify(this.chatHistory))
      if (this.currentHistoryIndex === index) {
        this.newChat()
      } else if (this.currentHistoryIndex > index) {
        this.currentHistoryIndex--
      }
    },
    newChat() {
      this.messages = [
        {
          type: 'ai',
          content: '你好！我是 OpenClaw AI 助手，有什么可以帮助你的吗？\n\n📷 你可以上传图片，我来帮你识别！'
        }
      ]
      this.currentHistoryIndex = -1
      this.historyChanged = false
      this.scrollToBottom()
    },
    toggleHistory() {
      this.showHistory = !this.showHistory
    },
    goHome() {
      this.$router.push('/')
    },
    handleImageUpload(event) {
      const file = event.target.files[0]
      if (file) {
        const reader = new FileReader()
        reader.onload = (e) => {
          this.uploadedImage = e.target.result
          this.imageFile = file
        }
        reader.readAsDataURL(file)
      }
    },
    removeImage() {
      this.uploadedImage = null
      this.imageFile = null
    },
    connectWebSocket() {
      if (this.wsRetryCount >= this.maxWsRetries) {
        console.log('WebSocket max retries reached, falling back to HTTP')
        return
      }
      
      try {
        let wsUrl
        if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
          wsUrl = `ws://localhost:18789/ws?token=${API_TOKEN}`
        } else {
          const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
          wsUrl = `${protocol}//${window.location.host}/ws?token=${API_TOKEN}`
        }
        this.ws = new WebSocket(wsUrl)
        
        this.ws.onopen = () => {
          this.wsConnected = true
          this.wsRetryCount = 0
          console.log('WebSocket connected to OpenClaw')
        }
        
        this.ws.onmessage = (event) => {
          try {
            const data = JSON.parse(event.data)
            
            if (data.type === 'event' && data.event === 'connect.challenge') {
              const challengeResponse = {
                id: 'challenge_' + Date.now(),
                type: 'event',
                event: 'connect.challenge.response',
                payload: {
                  nonce: data.payload.nonce,
                  ts: data.payload.ts,
                  token: API_TOKEN
                }
              }
              this.ws.send(JSON.stringify(challengeResponse))
            } else if (data.id && this.pendingRequests[data.id]) {
              const callback = this.pendingRequests[data.id]
              delete this.pendingRequests[data.id]
              callback(null, data)
            } else if (data.type === 'response' || data.result || data.data) {
              for (const reqId in this.pendingRequests) {
                const callback = this.pendingRequests[reqId]
                delete this.pendingRequests[reqId]
                callback(null, data)
                break
              }
            }
          } catch (e) {
            console.error('WebSocket message error:', e)
          }
        }
        
        this.ws.onerror = (error) => {
          console.error('WebSocket error:', error)
          this.wsConnected = false
        }
        
        this.ws.onclose = () => {
          this.wsConnected = false
          this.wsRetryCount++
          if (this.wsRetryCount < this.maxWsRetries) {
            const delay = Math.pow(2, this.wsRetryCount) * 1000
            console.log(`WebSocket closed, retrying (${this.wsRetryCount}/${this.maxWsRetries}) in ${delay}ms`)
            setTimeout(() => this.connectWebSocket(), delay)
          } else {
            console.log('WebSocket max retries reached, falling back to HTTP API')
          }
        }
      } catch (e) {
        console.error('Failed to connect WebSocket:', e)
        this.wsRetryCount++
        if (this.wsRetryCount < this.maxWsRetries) {
          setTimeout(() => this.connectWebSocket(), 1000)
        }
      }
    },
    
    sendWsMessage(message) {
      return new Promise((resolve, reject) => {
        const requestId = 'req_' + Date.now()
        
        this.pendingRequests[requestId] = (error, data) => {
          if (error) {
            reject(error)
          } else {
            resolve(data)
          }
        }
        
        const wsMessage = {
          id: requestId,
          type: 'request',
          action: 'chat',
          data: {
            message: message,
            agent: 'main',
            model: 'minimax-portal/MiniMax-M2.5'
          }
        }
        
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
          this.ws.send(JSON.stringify(wsMessage))
        } else {
          setTimeout(() => {
            if (this.ws && this.ws.readyState === WebSocket.OPEN) {
              this.ws.send(JSON.stringify(wsMessage))
            } else {
              delete this.pendingRequests[requestId]
              reject(new Error('WebSocket not connected'))
            }
          }, 1000)
        }
      })
    },

    async sendMessage() {
      if (!this.inputMessage.trim() && !this.uploadedImage) return

      const userMessage = {
        type: 'user',
        content: this.inputMessage.trim() || '识别这张图片',
        image: this.uploadedImage || null
      }
      this.messages.push(userMessage)

      const messageContent = this.inputMessage.trim() || '描述这张图片'
      this.inputMessage = ''

      this.scrollToBottom()

      this.loading = true

      if (this.imageFile) {
        api.understandImage(this.imageFile, messageContent)
          .then(response => {
            this.messages.push({
              type: 'ai',
              content: response.data.description
            })
          })
          .catch(error => {
            let errorMessage = '图片识别失败'
            if (error.response && error.response.data && error.response.data.error) {
              errorMessage = error.response.data.error
            } else if (error.message) {
              errorMessage = error.message
            }
            this.messages.push({
              type: 'ai',
              content: `抱歉，图片识别失败：${errorMessage}`
            })
          })
          .finally(() => {
            this.loading = false
            this.removeImage()
            this.scrollToBottom()
            this.saveChatHistory()
          })
      } else {
        if (this.wsConnected) {
          this.sendWsMessage(messageContent)
            .then(response => {
              const content = response.result || response.data || response.message || '响应成功'
              this.messages.push({
                type: 'ai',
                content: String(content)
              })
            })
            .catch(error => {
              console.error('WebSocket error:', error)
              api.aiChat(messageContent, this.selectedModel)
                .then(response => {
                  this.messages.push({
                    type: 'ai',
                    content: response.data.reply
                  })
                })
                .catch(httpError => {
                  let errorMessage = '未知错误'
                  if (httpError.response && httpError.response.data) {
                    if (httpError.response.data.error) {
                      errorMessage = typeof httpError.response.data.error === 'object' ? JSON.stringify(httpError.response.data.error) : httpError.response.data.error
                    } else if (httpError.response.data.message) {
                      errorMessage = httpError.response.data.message
                    }
                  } else if (httpError.message) {
                    errorMessage = httpError.message
                  }
                  this.messages.push({
                    type: 'ai',
                    content: `哎呀，AI暂时无法响应 😔\n\n错误原因：${errorMessage}\n\n请稍后再试，或检查网络连接~`
                  })
                })
            })
            .finally(() => {
              this.loading = false
              this.scrollToBottom()
              this.saveChatHistory()
            })
        } else {
          api.aiChat(messageContent, this.selectedModel)
            .then(response => {
              this.messages.push({
                type: 'ai',
                content: response.data.reply
              })
            })
            .catch(error => {
              let errorMessage = '未知错误'
              if (error.response && error.response.data) {
                if (error.response.data.error) {
                  errorMessage = typeof error.response.data.error === 'object' ? JSON.stringify(error.response.data.error) : error.response.data.error
                } else if (error.response.data.message) {
                  errorMessage = error.response.data.message
                }
              } else if (error.message) {
                errorMessage = error.message
              }
              this.messages.push({
                type: 'ai',
                content: `哎呀，AI暂时无法响应 😔\n\n错误原因：${errorMessage}\n\n请稍后再试，或检查网络连接~`
              })
            })
            .finally(() => {
              this.loading = false
              this.scrollToBottom()
              this.saveChatHistory()
            })
        }
      }
    },
    async sendNormalChat(messageContent) {
      // 如果有图片，调用图片识别API
      if (this.imageFile) {
        api.understandImage(this.imageFile, messageContent)
          .then(response => {
            this.messages.push({
              type: 'ai',
              content: response.data.description
            })
          })
          .catch(error => {
            let errorMessage = '图片识别失败'
            if (error.response && error.response.data && error.response.data.error) {
              errorMessage = error.response.data.error
            } else if (error.message) {
              errorMessage = error.message
            }
            this.messages.push({
              type: 'ai',
              content: `抱歉，图片识别失败：${errorMessage}`
            })
          })
          .finally(() => {
            this.loading = false
            this.removeImage()
            this.scrollToBottom()
            this.saveChatHistory()
          })
      } else {
        // 调用普通文本API
        api.aiChat(messageContent, this.selectedModel)
          .then(response => {
            this.messages.push({
              type: 'ai',
              content: response.data.reply
            })
          })
          .catch(error => {
            let errorMessage = '未知错误'
            if (error.response && error.response.data) {
              if (error.response.data.error) {
                errorMessage = typeof error.response.data.error === 'object' ? JSON.stringify(error.response.data.error) : error.response.data.error
              } else if (error.response.data.message) {
                errorMessage = error.response.data.message
              }
            } else if (error.message) {
              errorMessage = error.message
            }
            this.messages.push({
              type: 'ai',
              content: `抱歉，AI回复失败：${errorMessage}`
            })
          })
          .finally(() => {
            this.loading = false
            this.scrollToBottom()
            this.saveChatHistory()
          })
      }
    },
    scrollToBottom() {
      this.$nextTick(() => {
        const chatMessages = this.$refs.chatMessages
        if (chatMessages) {
          chatMessages.scrollTop = chatMessages.scrollHeight
        }
      })
    }
  }
}
</script>

<style scoped>
.chat-container {
  display: flex;
  height: calc(100vh - 120px);
  gap: 20px;
  padding: 20px;
}

.history-panel {
  width: 280px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  transition: width 0.3s ease;
}

.history-panel.collapsed {
  width: 40px;
}

.history-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  border-bottom: 1px solid #ebeef5;
  font-weight: bold;
}

.collapse-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 14px;
  color: #999;
}

.history-list {
  flex: 1;
  overflow-y: auto;
  padding: 10px;
}

.history-item {
  padding: 12px;
  margin-bottom: 8px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s ease;
  background: #f8f9fa;
  position: relative;
}

.history-item:hover {
  background: #e8eaed;
}

.history-item.active {
  background: #1890ff;
  color: white;
}

.history-preview {
  font-size: 14px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.history-time {
  font-size: 12px;
  color: #999;
  margin-top: 4px;
}

.history-item.active .history-time {
  color: rgba(255, 255, 255, 0.7);
}

.delete-history-btn {
  position: absolute;
  right: 8px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  cursor: pointer;
  color: #999;
  font-size: 14px;
  opacity: 0;
  transition: opacity 0.2s;
}

.history-item:hover .delete-history-btn {
  opacity: 1;
}

.history-item.active .delete-history-btn {
  color: rgba(255, 255, 255, 0.7);
}

.empty-history {
  text-align: center;
  color: #999;
  padding: 40px 20px;
}

.new-chat-btn {
  padding: 12px;
  margin: 10px;
  background: #1890ff;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.2s;
}

.new-chat-btn:hover {
  background: #40a9ff;
}

.chat-main {
  flex: 1;
  display: flex;
  justify-content: center;
}

.chat {
  padding: 0;
}

.chat-card {
  width: 100%;
  max-width: 900px;
  height: 100%;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 18px 20px;
  border-bottom: 1px solid #ebeef5;
  font-size: 16px;
  font-weight: bold;
  color: #303133;
  gap: 15px;
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

.model-select {
  width: 200px;
  padding: 8px 12px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  font-size: 14px;
}

.chat-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  border-bottom: 1px solid #ebeef5;
}

.message-item {
  display: flex;
  margin-bottom: 20px;
  align-items: flex-start;
}

.message-item.user {
  flex-direction: row-reverse;
}

.message-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background-color: #1890ff;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 10px;
  flex-shrink: 0;
  font-size: 14px;
}

.message-item.user .message-avatar {
  background-color: #67c23a;
}

.message-content {
  max-width: 70%;
  padding: 10px 15px;
  border-radius: 10px;
  background-color: #f5f7fa;
  line-height: 1.5;
  word-wrap: break-word;
}

.message-item.user .message-content {
  background-color: #1890ff;
  color: white;
}

.loading-icon {
  margin-right: 8px;
}

.chat-input {
  padding: 20px;
  border-top: 1px solid #ebeef5;
}

.message-textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  font-size: 14px;
  resize: vertical;
  font-family: inherit;
}

.message-textarea:focus {
  outline: none;
  border-color: #1890ff;
}

.image-preview {
  position: relative;
  max-width: 200px;
  margin-bottom: 10px;
  border-radius: 8px;
  overflow: hidden;
  border: 1px solid #dcdfe6;
}

.preview-image {
  width: 100%;
  display: block;
}

.remove-image-btn {
  position: absolute;
  top: 5px;
  right: 5px;
  width: 24px;
  height: 24px;
  border: none;
  border-radius: 50%;
  background-color: rgba(0, 0, 0, 0.6);
  color: white;
  font-size: 14px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.remove-image-btn:hover {
  background-color: rgba(0, 0, 0, 0.8);
}

.chat-actions {
  margin-top: 10px;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.upload-btn {
  padding: 10px 16px;
  background-color: #67c23a;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.upload-btn:hover {
  background-color: #85ce61;
}

.file-input {
  display: none;
}

.send-btn {
  padding: 10px 24px;
  background-color: #1890ff;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.send-btn:hover {
  background-color: #40a9ff;
}

.message-image {
  max-width: 100%;
  max-height: 200px;
  border-radius: 8px;
  margin-top: 5px;
}
</style>