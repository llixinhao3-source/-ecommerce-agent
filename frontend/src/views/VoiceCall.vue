<template>
  <div class="wechat-chat">
    <!-- 顶部导航栏 -->
    <div class="wechat-header">
      <button class="back-btn" @click="goHome">
        <span>←</span>
      </button>
      <div class="contact-info">
        <div class="contact-name">微信聊天</div>
        <div class="contact-status">{{ isCalling ? '通话中' : '在线' }}</div>
      </div>
      <div class="header-actions">
        <button class="action-btn" @click="toggleVoiceCall">
          📞 {{ isCalling ? '挂断' : '语音通话' }}
        </button>
      </div>
    </div>
    
    <!-- 聊天消息区域 -->
    <div class="wechat-messages" ref="chatMessages">
      <div v-for="(message, index) in messages" :key="index" :class="['message-item', message.type]">
        <div class="avatar" :style="{ backgroundColor: message.avatar }">
          {{ message.avatarText }}
        </div>
        <div class="message-body">
          <div class="bubble">
            <p v-if="message.voice && message.duration" class="voice-info">
              <span class="voice-wave">◉◉◉</span>
              <span class="voice-duration">{{ message.duration }}"</span>
            </p>
            <p v-else-if="message.emoji">{{ message.emoji }}</p>
            <p v-else-if="message.content">{{ message.content }}</p>
            <img v-if="message.image" :src="message.image" class="message-image" />
            <div v-if="message.file" class="message-file">
              <span class="file-icon">📄</span>
              <div class="file-info">
                <div class="file-name">{{ message.fileName }}</div>
                <div class="file-size">{{ message.fileSize }}</div>
              </div>
            </div>
            <div v-if="message.location" class="location-info">
              <span class="location-icon">📍</span>
              <span class="location-address">{{ message.address }}</span>
            </div>
            <div v-if="message.video" class="video-preview">
              <span class="video-icon">🎬</span>
              <span class="video-duration">{{ message.duration }}</span>
            </div>
          </div>
          <div class="message-time">{{ message.time }}</div>
        </div>
      </div>
      
      <!-- 通话状态消息 -->
      <div v-if="callStatus" class="call-status-message">
        <span>{{ callStatus }}</span>
      </div>
    </div>
    
    <!-- 表情包面板 -->
    <div v-if="showEmojiPanel" class="emoji-panel">
      <div class="emoji-category">
        <div 
          v-for="(emoji, index) in emojis" 
          :key="index" 
          class="emoji-item"
          @click="sendEmoji(emoji)"
        >
          {{ emoji }}
        </div>
      </div>
    </div>
    
    <!-- 底部输入区域 -->
    <div class="wechat-input-area">
      <div class="input-tools">
        <button class="tool-btn" @click="toggleToolPanel">+</button>
        <button class="tool-btn" @click="toggleEmojiPanel">😊</button>
        <button class="tool-btn" @click="startRecording" v-if="!isRecording">🎤</button>
        <button class="tool-btn recording" @click="stopRecording" v-else>⏹️</button>
      </div>
      
      <!-- 工具面板 -->
      <div v-if="showToolPanel" class="tool-panel">
        <div class="tool-grid">
          <div class="tool-item" @click="selectImage">
            <span class="tool-icon">🖼️</span>
            <span class="tool-label">图片</span>
          </div>
          <div class="tool-item" @click="selectFile">
            <span class="tool-icon">📁</span>
            <span class="tool-label">文件</span>
          </div>
          <div class="tool-item" @click="selectLocation">
            <span class="tool-icon">📍</span>
            <span class="tool-label">位置</span>
          </div>
          <div class="tool-item" @click="selectVideo">
            <span class="tool-icon">🎬</span>
            <span class="tool-label">视频</span>
          </div>
        </div>
      </div>
      
      <!-- 隐藏的文件输入 -->
      <input type="file" id="image-upload" accept="image/*" class="hidden-upload" @change="handleImageUpload">
      <input type="file" id="file-upload" class="hidden-upload" @change="handleFileUpload">
      <div class="input-wrapper">
        <input 
          type="text" 
          v-model="inputMessage" 
          placeholder="输入消息..." 
          class="message-input"
          @keyup.enter="sendMessage"
        />
        <button class="send-btn" @click="sendMessage" :disabled="!inputMessage.trim()">发送</button>
      </div>
      
      <!-- 语音录制状态 -->
      <div v-if="isRecording" class="recording-status">
        <span class="recording-dot"></span>
        <span>正在录音 {{ recordingDuration }}</span>
        <div v-if="currentVoiceText" class="voice-text">{{ currentVoiceText }}</div>
        <button class="cancel-recording" @click="cancelRecording">取消</button>
        <button class="stop-recording" @click="stopRecording">结束录音</button>
      </div>
    </div>
    
    <!-- 通话面板 -->
    <div v-if="isCalling" class="call-panel">
      <div class="call-avatar">好友</div>
      <div class="call-info">
        <div class="call-name">微信好友</div>
        <div class="call-duration">{{ callDuration }}</div>
      </div>
      <div class="call-controls">
        <button class="call-control-btn" @click="toggleMute">
          {{ isMuted ? '🔇' : '🔊' }}
        </button>
        <button class="call-control-btn" @click="toggleSpeaker">
          {{ isSpeakerOn ? '🔈' : '🎧' }}
        </button>
        <button class="call-control-btn danger" @click="hangUp">
          ❌
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'VoiceCall',
  data() {
    return {
      messages: [
        {
          type: 'received',
          content: '你好！我是 Minimax AI，有什么可以帮助你的吗？',
          avatar: '#1890ff',
          avatarText: 'M',
          time: new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
        }
      ],
      inputMessage: '',
      isCalling: false,
      isMuted: false,
      isSpeakerOn: false,
      isRecording: false,
      recordingDuration: '00:00',
      recordingTimer: null,
      currentVoiceText: '',
      recognition: null,
      callDuration: '00:00',
      callTimer: null,
      callStatus: null,
      callSettings: {
        fromNumber: '+8613800138000',
        toNumber: '+8613900139000',
        provider: 'mock'
      },
      showEmojiPanel: false,
      showToolPanel: false,
      emojis: [
        '😀', '😃', '😄', '😁', '😆', '😅', '🤣', '😂',
        '🙂', '😊', '😇', '🥰', '😍', '🤩', '😘', '😗',
        '😚', '😋', '🤤', '😛', '😜', '🤪', '😝', '🤑',
        '🤗', '🤭', '🤫', '🤔', '🤐', '🤨', '😐', '😑',
        '😶', '😏', '😒', '🙄', '😬', '🤥', '😌', '😔',
        '😪', '🤤', '😴', '😷', '🤒', '🤕', '🤢', '🤮',
        '🥵', '🥶', '🥴', '😵', '🤯', '🤠', '🥳', '🥸',
        '😎', '🤓', '🧐', '😕', '😟', '🙁', '☹️', '😮',
        '😯', '😲', '😳', '🥺', '😦', '😧', '😨', '😰',
        '😥', '😢', '😭', '😱', '😖', '😣', '😞', '😓',
        '😩', '😫', '🥱', '😤', '😡', '😠', '🤬', '😈',
        '👿', '💀', '☠️', '💩', '🤡', '👹', '👺', '👻',
        '👽', '👾', '🤖', '🎃', '😺', '😸', '😹', '😻',
        '😼', '😽', '🙀', '😿', '😾', '💋', '👄', '👅',
        '👂', '👃', '👁️', '👀', '👅', '👋', '🤚', '🖐️',
        '✋', '🖖', '👌', '🤏', '✌️', '🤞', '🤟', '🤘',
        '🤙', '👈', '👉', '👆', '👇', '☝️', '✋', '🤚'
      ],
      minimaxApiKey: 'sk-c3723d8b944a48c585675323daf4f7c1',
      conversationId: null
    }
  },
  methods: {
    goHome() {
      this.$router.push('/')
    },
    async sendMessage() {
      if (!this.inputMessage.trim()) return
      
      const messageContent = this.inputMessage.trim()
      
      const userMessage = {
        type: 'sent',
        content: messageContent,
        avatar: '#07c160',
        avatarText: '我',
        time: new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
      }
      
      this.messages.push(userMessage)
      this.inputMessage = ''
      this.scrollToBottom()
      
      try {
        const reply = await this.callMinimaxApi(messageContent)
        const replyMessage = {
          type: 'received',
          content: reply,
          avatar: '#1890ff',
          avatarText: 'M',
          time: new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
        }
        this.messages.push(replyMessage)
        this.scrollToBottom()
      } catch (error) {
        const errorMessage = {
          type: 'received',
          content: `抱歉，API调用失败：${error.message}`,
          avatar: '#1890ff',
          avatarText: 'M',
          time: new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
        }
        this.messages.push(errorMessage)
        this.scrollToBottom()
      }
    },
    async callMinimaxApi(message) {
      const url = 'https://api.deepseek.com/v1/chat/completions'
      
      const payload = {
        model: 'deepseek-chat',
        messages: [
          {
            role: 'user',
            content: message
          }
        ],
        max_tokens: 1024,
        temperature: 0.7
      }
      
      const response = await axios.post(url, payload, {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.minimaxApiKey}`
        },
        timeout: 30000
      })
      
      console.log('DeepSeek API Response:', response.data)
      
      if (!response.data) {
        throw new Error('API响应为空')
      }
      
      if (response.data.error) {
        throw new Error(`API错误: ${response.data.error.message}`)
      }
      
      if (response.data.choices && response.data.choices[0]) {
        const choice = response.data.choices[0]
        if (choice.message && choice.message.content) {
          return choice.message.content
        } else if (choice.text) {
          return choice.text
        }
      } else if (response.data.message) {
        return response.data.message
      }
      
      throw new Error('无法获取响应内容: ' + JSON.stringify(response.data))
    },
    sendEmoji(emoji) {
      const emojiMessage = {
        type: 'sent',
        emoji: emoji,
        avatar: '#07c160',
        avatarText: '我',
        time: new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
      }
      
      this.messages.push(emojiMessage)
      this.showEmojiPanel = false
      this.scrollToBottom()
      
      setTimeout(() => {
        const replyEmojis = ['😊', '😄', '👍', '🎉', '❤️', '🙌']
        const randomEmoji = replyEmojis[Math.floor(Math.random() * replyEmojis.length)]
        const replyMessage = {
          type: 'received',
          emoji: randomEmoji,
          avatar: '#1890ff',
          avatarText: 'M',
          time: new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
        }
        this.messages.push(replyMessage)
        this.scrollToBottom()
      }, 500)
    },
    toggleEmojiPanel() {
      this.showEmojiPanel = !this.showEmojiPanel
    },
    toggleToolPanel() {
      this.showToolPanel = !this.showToolPanel
      this.showEmojiPanel = false
      this.isRecording = false
      if (this.recordingTimer) {
        clearInterval(this.recordingTimer)
        this.recordingTimer = null
      }
    },
    selectImage() {
      document.getElementById('image-upload').click()
    },
    selectFile() {
      document.getElementById('file-upload').click()
    },
    selectLocation() {
      this.showToolPanel = false
      const locationMessage = {
        type: 'sent',
        location: true,
        address: '北京市朝阳区',
        avatar: '#07c160',
        avatarText: '我',
        time: new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
      }
      this.messages.push(locationMessage)
      this.scrollToBottom()
    },
    selectVideo() {
      this.showToolPanel = false
      const videoMessage = {
        type: 'sent',
        video: true,
        duration: '00:15',
        avatar: '#07c160',
        avatarText: '我',
        time: new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
      }
      this.messages.push(videoMessage)
      this.scrollToBottom()
    },
    handleImageUpload(event) {
      const file = event.target.files[0]
      if (file) {
        const reader = new FileReader()
        reader.onload = (e) => {
          const imageMessage = {
            type: 'sent',
            image: e.target.result,
            avatar: '#07c160',
            avatarText: '我',
            time: new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
          }
          this.messages.push(imageMessage)
          this.scrollToBottom()
        }
        reader.readAsDataURL(file)
      }
      event.target.value = ''
      this.showToolPanel = false
    },
    handleFileUpload(event) {
      const file = event.target.files[0]
      if (file) {
        const fileMessage = {
          type: 'sent',
          file: true,
          fileName: file.name,
          fileSize: this.formatFileSize(file.size),
          avatar: '#07c160',
          avatarText: '我',
          time: new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
        }
        this.messages.push(fileMessage)
        this.scrollToBottom()
      }
      event.target.value = ''
      this.showToolPanel = false
    },
    formatFileSize(bytes) {
      if (bytes < 1024) return bytes + ' B'
      if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
      return (bytes / (1024 * 1024)).toFixed(1) + ' MB'
    },
    startRecording() {
      this.isRecording = true
      this.recordingDuration = '00:00'
      this.showToolPanel = false
      this.currentVoiceText = ''
      
      let seconds = 0
      this.recordingTimer = setInterval(() => {
        seconds++
        const mins = Math.floor(seconds / 60).toString().padStart(2, '0')
        const secs = (seconds % 60).toString().padStart(2, '0')
        this.recordingDuration = `${mins}:${secs}`
      }, 1000)
      
      this.startVoiceRecognition()
    },
    startVoiceRecognition() {
      if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
        this.recognition = new SpeechRecognition()
        this.recognition.continuous = true
        this.recognition.interimResults = true
        this.recognition.lang = 'zh-CN'
        
        this.recognition.onresult = (event) => {
          let interimTranscript = ''
          let finalTranscript = ''
          
          for (let i = event.resultIndex; i < event.results.length; i++) {
            const transcript = event.results[i][0].transcript
            if (event.results[i].isFinal) {
              finalTranscript += transcript
            } else {
              interimTranscript += transcript
            }
          }
          
          this.currentVoiceText = finalTranscript + interimTranscript
        }
        
        this.recognition.onerror = (event) => {
          console.log('语音识别错误:', event.error)
        }
        
        this.recognition.start()
      }
    },
    stopRecording() {
      this.isRecording = false
      if (this.recordingTimer) {
        clearInterval(this.recordingTimer)
        this.recordingTimer = null
      }
      
      if (this.recognition) {
        this.recognition.stop()
        this.recognition = null
      }
      
      if (this.currentVoiceText.trim()) {
        const textMessage = {
          type: 'sent',
          content: this.currentVoiceText,
          avatar: '#07c160',
          avatarText: '我',
          time: new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
        }
        this.messages.push(textMessage)
        this.scrollToBottom()
        this.sendMessageWithAI(this.currentVoiceText)
      } else {
        const voiceMessage = {
          type: 'sent',
          voice: true,
          duration: Math.floor(parseInt(this.recordingDuration.split(':')[0]) * 60 + parseInt(this.recordingDuration.split(':')[1])),
          avatar: '#07c160',
          avatarText: '我',
          time: new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
        }
        this.messages.push(voiceMessage)
        this.scrollToBottom()
      }
      
      this.currentVoiceText = ''
    },
    cancelRecording() {
      this.isRecording = false
      if (this.recordingTimer) {
        clearInterval(this.recordingTimer)
        this.recordingTimer = null
      }
      
      if (this.recognition) {
        this.recognition.stop()
        this.recognition = null
      }
      
      this.currentVoiceText = ''
    },
    toggleVoiceCall() {
      if (this.isCalling) {
        this.hangUp()
      } else {
        this.makeCall()
      }
    },
    makeCall() {
      this.isCalling = true
      this.callDuration = '00:00'
      this.callStatus = `正在拨打电话给 ${this.callSettings.toNumber}...`
      
      let seconds = 0
      this.callTimer = setInterval(() => {
        seconds++
        const mins = Math.floor(seconds / 60).toString().padStart(2, '0')
        const secs = (seconds % 60).toString().padStart(2, '0')
        this.callDuration = `${mins}:${secs}`
      }, 1000)
      
      if (this.callSettings.provider === 'mock') {
        setTimeout(() => {
          this.callStatus = `已接通，正在通话中...`
        }, 2000)
      } else {
        this.makeRealCall()
      }
    },
    async makeRealCall() {
      try {
        const response = await axios.post('/api/voice-call', {
          fromNumber: this.callSettings.fromNumber,
          toNumber: this.callSettings.toNumber,
          provider: this.callSettings.provider,
          content: ''
        })
        
        if (response.data.success) {
          setTimeout(() => {
            this.callStatus = '电话已接通！'
          }, 2000)
        } else {
          this.handleCallError(response.data.error)
        }
      } catch (error) {
        this.handleCallError(error.message || '通话失败')
      }
    },
    handleCallError(errorMessage) {
      this.isCalling = false
      if (this.callTimer) {
        clearInterval(this.callTimer)
        this.callTimer = null
      }
      this.callStatus = `通话失败: ${errorMessage}`
    },
    hangUp() {
      this.isCalling = false
      this.callStatus = `通话结束，时长：${this.callDuration}`
      
      if (this.callTimer) {
        clearInterval(this.callTimer)
        this.callTimer = null
      }
      
      setTimeout(() => {
        this.callStatus = null
      }, 3000)
    },
    toggleMute() {
      this.isMuted = !this.isMuted
    },
    toggleSpeaker() {
      this.isSpeakerOn = !this.isSpeakerOn
    },
    toggleToolPanel() {
      
    },
    scrollToBottom() {
      this.$nextTick(() => {
        const chatMessages = this.$refs.chatMessages
        if (chatMessages) {
          chatMessages.scrollTop = chatMessages.scrollHeight
        }
      })
    }
  },
  beforeDestroy() {
    if (this.callTimer) {
      clearInterval(this.callTimer)
    }
    if (this.recordingTimer) {
      clearInterval(this.recordingTimer)
    }
  }
}
</script>

<style scoped>
.wechat-chat {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 80px);
  background-color: #e5e5e5;
}

.wechat-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 15px;
  background-color: #07c160;
  color: white;
}

.back-btn {
  width: 40px;
  height: 40px;
  border: none;
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.2);
  color: white;
  font-size: 20px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.contact-info {
  flex: 1;
  text-align: center;
}

.contact-name {
  font-size: 16px;
  font-weight: bold;
}

.contact-status {
  font-size: 12px;
  opacity: 0.8;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.action-btn {
  padding: 8px 16px;
  border: none;
  border-radius: 20px;
  background-color: rgba(255, 255, 255, 0.2);
  color: white;
  font-size: 14px;
  cursor: pointer;
}

.wechat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 15px;
}

.message-item {
  display: flex;
  margin-bottom: 20px;
  align-items: flex-start;
}

.message-item.sent {
  flex-direction: row-reverse;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  overflow: hidden;
  margin: 0 10px;
  flex-shrink: 0;
}

.avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.message-body {
  display: flex;
  flex-direction: column;
  max-width: 70%;
}

.bubble {
  padding: 10px 14px;
  border-radius: 0;
  background-color: white;
  line-height: 1.5;
  word-wrap: break-word;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.message-item.received .bubble {
  border-radius: 0 12px 12px 12px;
}

.message-item.sent .bubble {
  background-color: #95ec69;
  color: #333;
  border-radius: 12px 0 12px 12px;
}

.message-image {
  max-width: 100%;
  max-height: 200px;
  border-radius: 8px;
  margin-top: 5px;
}

.voice-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.voice-wave {
  color: #666;
  font-size: 16px;
}

.voice-duration {
  font-size: 12px;
  color: #666;
}

.message-time {
  font-size: 12px;
  color: #999;
  margin-top: 5px;
  padding: 0 4px;
}

.message-item.sent .message-time {
  text-align: right;
}

.call-status-message {
  text-align: center;
  padding: 8px 12px;
  background-color: rgba(0, 0, 0, 0.1);
  border-radius: 20px;
  font-size: 12px;
  color: #666;
  margin-bottom: 15px;
}

.emoji-panel {
  background-color: white;
  border-top: 1px solid #ddd;
  padding: 10px;
  max-height: 200px;
  overflow-y: auto;
}

.emoji-category {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
}

.emoji-item {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  cursor: pointer;
  border-radius: 8px;
  transition: background-color 0.2s;
}

.emoji-item:hover {
  background-color: #f0f0f0;
}

.wechat-input-area {
  padding: 10px 15px;
  background-color: white;
  border-top: 1px solid #ddd;
}

.input-tools {
  display: flex;
  gap: 15px;
  margin-bottom: 10px;
}

.tool-btn {
  width: 40px;
  height: 40px;
  border: none;
  border-radius: 50%;
  background-color: #f5f5f5;
  font-size: 20px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.tool-btn.recording {
  background-color: #ff4d4f;
  color: white;
}

.input-wrapper {
  display: flex;
  gap: 10px;
}

.message-input {
  flex: 1;
  padding: 10px 15px;
  border: none;
  border-radius: 25px;
  background-color: #f5f5f5;
  font-size: 14px;
}

.message-input:focus {
  outline: none;
}

.send-btn {
  padding: 10px 20px;
  border: none;
  border-radius: 25px;
  background-color: #07c160;
  color: white;
  font-size: 14px;
  cursor: pointer;
}

.send-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.recording-status {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 10px 15px;
  background-color: #ff4d4f;
  color: white;
  border-radius: 25px;
  margin-top: 10px;
  flex-wrap: wrap;
}

.voice-text {
  flex: 1;
  min-width: 100px;
  text-align: left;
  font-size: 14px;
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.recording-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background-color: white;
  animation: pulse 1s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.cancel-recording {
  padding: 5px 15px;
  border: 1px solid white;
  border-radius: 15px;
  background-color: transparent;
  color: white;
  font-size: 14px;
  cursor: pointer;
}

.tool-panel {
  background-color: white;
  border-top: 1px solid #ddd;
  padding: 15px;
}

.tool-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 15px;
}

.tool-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
  padding: 15px;
  border-radius: 10px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.tool-item:hover {
  background-color: #f5f5f5;
}

.tool-icon {
  font-size: 32px;
}

.tool-label {
  font-size: 12px;
  color: #666;
}

.hidden-upload {
  display: none;
}

.message-file {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
  background-color: #f5f5f5;
  border-radius: 8px;
  margin-top: 5px;
}

.file-icon {
  font-size: 24px;
}

.file-info {
  flex: 1;
}

.file-name {
  font-size: 14px;
  color: #333;
}

.file-size {
  font-size: 12px;
  color: #999;
}

.location-info {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
  background-color: #f5f5f5;
  border-radius: 8px;
  margin-top: 5px;
}

.location-icon {
  font-size: 20px;
}

.location-address {
  font-size: 14px;
  color: #333;
}

.video-preview {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px;
  background-color: #f5f5f5;
  border-radius: 8px;
  margin-top: 5px;
}

.video-icon {
  font-size: 24px;
}

.video-duration {
  font-size: 12px;
  color: #999;
}

.stop-recording {
  padding: 5px 15px;
  border: none;
  border-radius: 15px;
  background-color: white;
  color: #ff4d4f;
  font-size: 14px;
  cursor: pointer;
}

.call-panel {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #1a1a1a;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 100;
}

.call-avatar {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  background-color: #07c160;
  color: white;
  font-size: 48px;
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 20px;
}

.call-info {
  text-align: center;
  margin-bottom: 40px;
}

.call-name {
  font-size: 24px;
  color: white;
  margin-bottom: 10px;
}

.call-duration {
  font-size: 18px;
  color: rgba(255, 255, 255, 0.7);
}

.call-controls {
  display: flex;
  gap: 40px;
}

.call-control-btn {
  width: 70px;
  height: 70px;
  border: none;
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.2);
  color: white;
  font-size: 28px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.call-control-btn.danger {
  background-color: #ff4d4f;
}
</style>