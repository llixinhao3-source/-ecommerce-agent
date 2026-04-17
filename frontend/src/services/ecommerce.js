/**
 * 电商运营API服务
 * Ecommerce Operation API Service
 */

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
    'Content-Type': 'application/json'
  }
})

api.interceptors.response.use(
  response => response,
  error => {
    console.error('电商API Error:', error)
    return Promise.reject(error)
  }
)

export default {
  /**
   * 低粉爆品挖掘
   * @param {string} platform - 平台 (xiaohongshu/douyin)
   * @param {string} keyword - 搜索关键词
   * @param {string} output - 输出文件路径
   */
  lowFansHunter(platform, keyword, output) {
    return api.post('/v1/chat/completions', {
      messages: [
        {
          role: 'user',
          content: `执行低粉爆品挖掘技能：
          平台：${platform}
          关键词：${keyword}
          输出：${output}
          
          请运行 low_fans_hunter 技能并返回结果。`
        }
      ],
      agent: 'main',
      stream: false
    }).then(response => {
      return {
        data: {
          reply: response.data.choices?.[0]?.message?.content || '执行完成'
        }
      }
    })
  },

  /**
   * 高粉爆品追踪
   * @param {string} platform - 平台
   * @param {string} keyword - 搜索关键词
   * @param {string} output - 输出文件路径
   */
  highFansTracker(platform, keyword, output) {
    return api.post('/v1/chat/completions', {
      messages: [
        {
          role: 'user',
          content: `执行高粉爆品追踪技能：
          平台：${platform}
          关键词：${keyword}
          输出：${output}
          
          请运行 high_fans_tracker 技能并返回结果。`
        }
      ],
      agent: 'main',
      stream: false
    }).then(response => {
      return {
        data: {
          reply: response.data.choices?.[0]?.message?.content || '执行完成'
        }
      }
    })
  },

  /**
   * 违禁词检测
   * @param {string} filePath - Excel文件路径
   * @param {string} output - 输出报告路径
   */
  prohibitedWordChecker(filePath, output) {
    return api.post('/v1/chat/completions', {
      messages: [
        {
          role: 'user',
          content: `执行客服违禁词检测技能：
          文件路径：${filePath}
          输出：${output}
          
          请运行 prohibited_word_checker 技能并返回结果。`
        }
      ],
      agent: 'main',
      stream: false
    }).then(response => {
      return {
        data: {
          reply: response.data.choices?.[0]?.message?.content || '检测完成'
        }
      }
    })
  },

  /**
   * ROI分析
   * @param {string} filePath - 广告数据文件路径
   * @param {string} output - 输出报告路径
   */
  roiAnalyzer(filePath, output) {
    return api.post('/v1/chat/completions', {
      messages: [
        {
          role: 'user',
          content: `执行ROI分析技能：
          文件路径：${filePath}
          输出：${output}
          
          请运行 roi_analyzer 技能并返回结果。`
        }
      ],
      agent: 'main',
      stream: false
    }).then(response => {
      return {
        data: {
          reply: response.data.choices?.[0]?.message?.content || '分析完成'
        }
      }
    })
  },

  /**
   * 标题去AI化
   * @param {string} product - 产品名称
   * @param {string} style - 风格 (casual/curious/enthusiastic)
   */
  aiTitleDehumanizer(product, style) {
    return api.post('/v1/chat/completions', {
      messages: [
        {
          role: 'user',
          content: `执行标题去AI化技能：
          产品：${product}
          风格：${style}
          
          请生成3个去AI化的标题。`
        }
      ],
      agent: 'main',
      stream: false
    }).then(response => {
      return {
        data: {
          reply: response.data.choices?.[0]?.message?.content || '生成完成'
        }
      }
    })
  },

  /**
   * 白底图生成
   * @param {string} inputPath - 输入图片路径
   * @param {string} outputPath - 输出目录
   * @param {string} platform - 平台
   */
  whiteBackgroundGenerator(inputPath, outputPath, platform) {
    return api.post('/v1/chat/completions', {
      messages: [
        {
          role: 'user',
          content: `执行白底图生成技能：
          输入：${inputPath}
          输出：${outputPath}
          平台：${platform}
          
          请运行 white_background_generator 技能。`
        }
      ],
      agent: 'main',
      stream: false
    }).then(response => {
      return {
        data: {
          reply: response.data.choices?.[0]?.message?.content || '生成完成'
        }
      }
    })
  },

  /**
   * 竞品监控
   * @param {string} urls - 商品URL列表 (JSON数组)
   * @param {string} output - 输出文件路径
   */
  competitorMonitor(urls, output) {
    return api.post('/v1/chat/completions', {
      messages: [
        {
          role: 'user',
          content: `执行竞品监控技能：
          商品URL：${urls}
          输出：${output}
          
          请运行 competitor_monitor 技能。`
        }
      ],
      agent: 'main',
      stream: false
    }).then(response => {
      return {
        data: {
          reply: response.data.choices?.[0]?.message?.content || '监控完成'
        }
      }
    })
  },

  /**
   * 亚马逊选品
   * @param {string} filePath - 产品数据文件路径
   * @param {string} output - 输出文件路径
   */
  amazonProductSelector(filePath, output) {
    return api.post('/v1/chat/completions', {
      messages: [
        {
          role: 'user',
          content: `执行亚马逊选品技能：
          文件路径：${filePath}
          输出：${output}
          
          请运行 amazon_product_selector 技能并返回选品分析结果。`
        }
      ],
      agent: 'main',
      stream: false
    }).then(response => {
      return {
        data: {
          reply: response.data.choices?.[0]?.message?.content || '选品完成'
        }
      }
    })
  },

  /**
   * 亚马逊自动上架
   * @param {string} filePath - 产品数据文件路径
   * @param {string} output - 输出文件路径
   */
  amazonListingPublisher(filePath, output) {
    return api.post('/v1/chat/completions', {
      messages: [
        {
          role: 'user',
          content: `执行亚马逊自动上架技能：
          文件路径：${filePath}
          输出：${output}
          
          请运行 amazon_listing_publisher 技能。`
        }
      ],
      agent: 'main',
      stream: false
    }).then(response => {
      return {
        data: {
          reply: response.data.choices?.[0]?.message?.content || '上架完成'
        }
      }
    })
  },

  /**
   * 发送钉钉消息
   * @param {string} message - 消息内容
   */
  sendDingtalk(message) {
    return api.post('/v1/chat/completions', {
      messages: [
        {
          role: 'user',
          content: `发送钉钉消息：${message}`
        }
      ],
      agent: 'main',
      stream: false
    })
  }
}
