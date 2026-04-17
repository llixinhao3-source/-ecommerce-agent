import axios from 'axios'

const GATEWAY_TOKEN = '3060a9f22417e0359e7738a94590d9dca38591c3ee2b7e1e'

const getBaseURL = () => {
  if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    return 'http://localhost:18789'
  }
  return '/api'
}

const api = axios.create({
  baseURL: getBaseURL(),
  timeout: 300000,
  headers: {
    'Authorization': `Bearer ${GATEWAY_TOKEN}`,
    'Content-Type': 'application/json',
    'ngrok-skip-browser-warning': 'true'
  }
})

const formApi = axios.create({
  baseURL: getBaseURL(),
  timeout: 300000,
  headers: {
    'Authorization': `Bearer ${GATEWAY_TOKEN}`,
    'ngrok-skip-browser-warning': 'true'
  }
})

api.interceptors.response.use(
  response => response,
  error => {
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)

formApi.interceptors.response.use(
  response => response,
  error => {
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)

export default {
  healthCheck() {
    return api.get('/health')
  },
  
  aiChat(message, model = 'openclaw') {
    return api.post('/v1/chat/completions', {
      messages: [
        {
          role: 'user',
          content: message
        }
      ],
      agent: 'main',
      stream: false
    }).then(response => {
      const content = response.data.choices?.[0]?.message?.content || 
                      response.data.result || 
                      response.data.message || 
                      response.data.reply || '响应成功'
      return {
        data: {
          reply: content
        }
      }
    })
  },
  
  understandImage(imageFile, prompt = '描述这张图片') {
    const formData = new FormData()
    formData.append('image', imageFile)
    formData.append('prompt', prompt)
    
    return formApi.post('/v1/image/understand', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    }).then(response => {
      return {
        data: {
          description: response.data.description || response.data.result || '图片识别完成'
        }
      }
    })
  },
  
  getDashboardData() {
    return api.get('/dashboard')
  }
}