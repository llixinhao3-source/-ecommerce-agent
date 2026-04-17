<template>
  <div class="ecommerce-container">
    <!-- 头部 -->
    <div class="header">
      <h1>🛒 电商全链路运营平台</h1>
      <div class="header-actions">
        <el-button type="primary" @click="refreshStatus" :loading="loading">
          刷新状态
        </el-button>
      </div>
    </div>

    <!-- 功能模块选择 -->
    <div class="module-grid">
      <!-- 选品挖掘 -->
      <div class="module-card" @click="activeModule = 'selection'">
        <div class="module-icon">🔍</div>
        <div class="module-title">选品挖掘</div>
        <div class="module-desc">低粉爆品 + 高粉爆品</div>
      </div>

      <!-- 内容创作 -->
      <div class="module-card" @click="activeModule = 'content'">
        <div class="module-icon">✍️</div>
        <div class="module-title">内容创作</div>
        <div class="module-desc">标题去AI化</div>
      </div>

      <!-- 图片处理 -->
      <div class="module-card" @click="activeModule = 'image'">
        <div class="module-icon">🎨</div>
        <div class="module-title">图片处理</div>
        <div class="module-desc">白底图生成</div>
      </div>

      <!-- 数据分析 -->
      <div class="module-card" @click="activeModule = 'analytics'">
        <div class="module-icon">📊</div>
        <div class="module-title">数据分析</div>
        <div class="module-desc">ROI + 竞品监控</div>
      </div>

      <!-- 违规检测 -->
      <div class="module-card" @click="activeModule = 'violation'">
        <div class="module-icon">⚠️</div>
        <div class="module-title">违规检测</div>
        <div class="module-desc">客服违禁词</div>
      </div>

      <!-- 亚马逊 -->
      <div class="module-card" @click="activeModule = 'amazon'">
        <div class="module-icon">🌐</div>
        <div class="module-title">亚马逊</div>
        <div class="module-desc">选品 + 上架</div>
      </div>
    </div>

    <!-- 功能面板 -->
    <div v-if="activeModule" class="panel">
      <!-- 选品挖掘面板 -->
      <div v-if="activeModule === 'selection'" class="panel-content">
        <h2>🔍 选品挖掘</h2>
        
        <el-tabs v-model="selectionTab">
          <el-tab-pane label="低粉爆品" name="low">
            <el-form label-width="120px">
              <el-form-item label="平台">
                <el-select v-model="lowFansForm.platform" placeholder="选择平台">
                  <el-option label="小红书" value="xiaohongshu"></el-option>
                  <el-option label="抖音" value="douyin"></el-option>
                </el-select>
              </el-form-item>
              <el-form-item label="关键词">
                <el-input v-model="lowFansForm.keyword" placeholder="输入搜索关键词"></el-input>
              </el-form-item>
              <el-form-item label="输出路径">
                <el-input v-model="lowFansForm.output" placeholder="./output/low_fans.xlsx"></el-input>
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="runLowFansHunter" :loading="running">
                  开始挖掘
                </el-button>
              </el-form-item>
            </el-form>
          </el-tab-pane>
          
          <el-tab-pane label="高粉爆品" name="high">
            <el-form label-width="120px">
              <el-form-item label="平台">
                <el-select v-model="highFansForm.platform" placeholder="选择平台">
                  <el-option label="小红书" value="xiaohongshu"></el-option>
                  <el-option label="抖音" value="douyin"></el-option>
                </el-select>
              </el-form-item>
              <el-form-item label="关键词">
                <el-input v-model="highFansForm.keyword" placeholder="留空则使用今日类目"></el-input>
              </el-form-item>
              <el-form-item label="输出路径">
                <el-input v-model="highFansForm.output" placeholder="./output/high_fans.xlsx"></el-input>
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="runHighFansTracker" :loading="running">
                  开始追踪
                </el-button>
              </el-form-item>
            </el-form>
          </el-tab-pane>
        </el-tabs>
      </div>

      <!-- 内容创作面板 -->
      <div v-if="activeModule === 'content'" class="panel-content">
        <h2>✍️ 内容创作</h2>
        <el-form label-width="120px">
          <el-form-item label="产品名称">
            <el-input v-model="titleForm.product" placeholder="输入产品名称"></el-input>
          </el-form-item>
          <el-form-item label="标题风格">
            <el-select v-model="titleForm.style" placeholder="选择风格">
              <el-option label="休闲casual" value="casual"></el-option>
              <el-option label="好奇curious" value="curious"></el-option>
              <el-option label="热情enthusiastic" value="enthusiastic"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="runTitleDehumanizer" :loading="running">
              生成标题
            </el-button>
          </el-form-item>
        </el-form>
        
        <div v-if="titleResults.length" class="results">
          <h3>生成的标题：</h3>
          <div v-for="(title, index) in titleResults" :key="index" class="result-item">
            {{ title }}
          </div>
        </div>
      </div>

      <!-- 图片处理面板 -->
      <div v-if="activeModule === 'image'" class="panel-content">
        <h2>🎨 图片处理</h2>
        <el-form label-width="120px">
          <el-form-item label="输入图片">
            <el-input v-model="imageForm.input" placeholder="输入图片路径或目录"></el-input>
          </el-form-item>
          <el-form-item label="输出目录">
            <el-input v-model="imageForm.output" placeholder="./output/white_bg"></el-input>
          </el-form-item>
          <el-form-item label="目标平台">
            <el-select v-model="imageForm.platform" placeholder="选择平台">
              <el-option label="通用" value="general"></el-option>
              <el-option label="亚马逊" value="amazon"></el-option>
              <el-option label="小红书" value="xiaohongshu"></el-option>
              <el-option label="淘宝" value="taobao"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="runWhiteBackground" :loading="running">
              生成白底图
            </el-button>
          </el-form-item>
        </el-form>
      </div>

      <!-- 数据分析面板 -->
      <div v-if="activeModule === 'analytics'" class="panel-content">
        <h2>📊 数据分析</h2>
        <el-tabs>
          <el-tab-pane label="ROI分析">
            <el-form label-width="120px">
              <el-form-item label="数据文件">
                <el-input v-model="roiForm.filePath" placeholder="广告数据Excel路径"></el-input>
              </el-form-item>
              <el-form-item label="输出报告">
                <el-input v-model="roiForm.output" placeholder="./output/roi_report.xlsx"></el-input>
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="runROIAnalyzer" :loading="running">
                  开始分析
                </el-button>
              </el-form-item>
            </el-form>
          </el-tab-pane>
          
          <el-tab-pane label="竞品监控">
            <el-form label-width="120px">
              <el-form-item label="商品URL">
                <el-input type="textarea" v-model="competitorForm.urls" placeholder='["url1", "url2"]'></el-input>
              </el-form-item>
              <el-form-item label="输出文件">
                <el-input v-model="competitorForm.output" placeholder="./output/competitor.xlsx"></el-input>
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="runCompetitorMonitor" :loading="running">
                  开始监控
                </el-button>
              </el-form-item>
            </el-form>
          </el-tab-pane>
        </el-tabs>
      </div>

      <!-- 违规检测面板 -->
      <div v-if="activeModule === 'violation'" class="panel-content">
        <h2>⚠️ 违规检测</h2>
        <el-form label-width="120px">
          <el-form-item label="聊天记录文件">
            <el-input v-model="violationForm.filePath" placeholder="Excel文件路径"></el-input>
          </el-form-item>
          <el-form-item label="输出报告">
            <el-input v-model="violationForm.output" placeholder="./output/violation_report.xlsx"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="runViolationChecker" :loading="running">
              开始检测
            </el-button>
          </el-form-item>
        </el-form>
      </div>

      <!-- 亚马逊面板 -->
      <div v-if="activeModule === 'amazon'" class="panel-content">
        <h2>🌐 亚马逊运营</h2>
        <el-tabs>
          <el-tab-pane label="选品">
            <el-form label-width="120px">
              <el-form-item label="产品数据文件">
                <el-input v-model="amazonForm.selectorFile" placeholder="Excel/JSON文件路径"></el-input>
              </el-form-item>
              <el-form-item label="输出报告">
                <el-input v-model="amazonForm.selectorOutput" placeholder="./output/selection.xlsx"></el-input>
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="runAmazonSelector" :loading="running">
                  开始选品
                </el-button>
              </el-form-item>
            </el-form>
          </el-tab-pane>
          
          <el-tab-pane label="上架">
            <el-form label-width="120px">
              <el-form-item label="产品数据文件">
                <el-input v-model="amazonForm.publisherFile" placeholder="Excel/JSON文件路径"></el-input>
              </el-form-item>
              <el-form-item label="输出文件">
                <el-input v-model="amazonForm.publisherOutput" placeholder="./output/listings.xlsx"></el-input>
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="runAmazonPublisher" :loading="running">
                  生成Listing
                </el-button>
              </el-form-item>
            </el-form>
          </el-tab-pane>
        </el-tabs>
      </div>
    </div>

    <!-- 执行日志 -->
    <div v-if="logs.length" class="logs">
      <h3>📋 执行日志</h3>
      <div v-for="(log, index) in logs" :key="index" class="log-item">
        <span class="log-time">{{ log.time }}</span>
        <span class="log-message">{{ log.message }}</span>
      </div>
    </div>
  </div>
</template>

<script>
import ecommerceApi from '@/services/ecommerce'

export default {
  name: 'Ecommerce',
  data() {
    return {
      loading: false,
      running: false,
      activeModule: null,
      logs: [],
      
      // 选品挖掘
      selectionTab: 'low',
      lowFansForm: {
        platform: 'xiaohongshu',
        keyword: '',
        output: './output/low_fans.xlsx'
      },
      highFansForm: {
        platform: 'xiaohongshu',
        keyword: '',
        output: './output/high_fans.xlsx'
      },
      
      // 内容创作
      titleForm: {
        product: '',
        style: 'casual'
      },
      titleResults: [],
      
      // 图片处理
      imageForm: {
        input: '',
        output: './output/white_bg',
        platform: 'general'
      },
      
      // 数据分析
      roiForm: {
        filePath: '',
        output: './output/roi_report.xlsx'
      },
      competitorForm: {
        urls: '[]',
        output: './output/competitor.xlsx'
      },
      
      // 违规检测
      violationForm: {
        filePath: '',
        output: './output/violation_report.xlsx'
      },
      
      // 亚马逊
      amazonForm: {
        selectorFile: '',
        selectorOutput: './output/selection.xlsx',
        publisherFile: '',
        publisherOutput: './output/listings.xlsx'
      }
    }
  },
  methods: {
    addLog(message, type = 'info') {
      const now = new Date()
      const time = `${now.getHours()}:${String(now.getMinutes()).padStart(2, '0')}:${String(now.getSeconds()).padStart(2, '0')}`
      this.logs.unshift({ time, message, type })
      if (this.logs.length > 50) {
        this.logs.pop()
      }
    },
    
    refreshStatus() {
      this.loading = true
      setTimeout(() => {
        this.loading = false
        this.addLog('状态刷新完成')
      }, 1000)
    },
    
    async runLowFansHunter() {
      this.running = true
      this.addLog('开始执行低粉爆品挖掘...')
      try {
        const response = await ecommerceApi.lowFansHunter(
          this.lowFansForm.platform,
          this.lowFansForm.keyword,
          this.lowFansForm.output
        )
        this.addLog('低粉爆品挖掘完成: ' + response.data.reply)
      } catch (error) {
        this.addLog('执行失败: ' + error.message, 'error')
      }
      this.running = false
    },
    
    async runHighFansTracker() {
      this.running = true
      this.addLog('开始执行高粉爆品追踪...')
      try {
        const response = await ecommerceApi.highFansTracker(
          this.highFansForm.platform,
          this.highFansForm.keyword,
          this.highFansForm.output
        )
        this.addLog('高粉爆品追踪完成: ' + response.data.reply)
      } catch (error) {
        this.addLog('执行失败: ' + error.message, 'error')
      }
      this.running = false
    },
    
    async runTitleDehumanizer() {
      this.running = true
      this.titleResults = []
      this.addLog('开始生成标题...')
      try {
        const response = await ecommerceApi.aiTitleDehumanizer(
          this.titleForm.product,
          this.titleForm.style
        )
        // 解析生成的标题
        const content = response.data.reply
        this.titleResults = content.split('\n').filter(line => line.trim())
        this.addLog('标题生成完成')
      } catch (error) {
        this.addLog('执行失败: ' + error.message, 'error')
      }
      this.running = false
    },
    
    async runWhiteBackground() {
      this.running = true
      this.addLog('开始生成白底图...')
      try {
        const response = await ecommerceApi.whiteBackgroundGenerator(
          this.imageForm.input,
          this.imageForm.output,
          this.imageForm.platform
        )
        this.addLog('白底图生成完成: ' + response.data.reply)
      } catch (error) {
        this.addLog('执行失败: ' + error.message, 'error')
      }
      this.running = false
    },
    
    async runROIAnalyzer() {
      this.running = true
      this.addLog('开始ROI分析...')
      try {
        const response = await ecommerceApi.roiAnalyzer(
          this.roiForm.filePath,
          this.roiForm.output
        )
        this.addLog('ROI分析完成: ' + response.data.reply)
      } catch (error) {
        this.addLog('执行失败: ' + error.message, 'error')
      }
      this.running = false
    },
    
    async runCompetitorMonitor() {
      this.running = true
      this.addLog('开始竞品监控...')
      try {
        const response = await ecommerceApi.competitorMonitor(
          this.competitorForm.urls,
          this.competitorForm.output
        )
        this.addLog('竞品监控完成: ' + response.data.reply)
      } catch (error) {
        this.addLog('执行失败: ' + error.message, 'error')
      }
      this.running = false
    },
    
    async runViolationChecker() {
      this.running = true
      this.addLog('开始违禁词检测...')
      try {
        const response = await ecommerceApi.prohibitedWordChecker(
          this.violationForm.filePath,
          this.violationForm.output
        )
        this.addLog('违禁词检测完成: ' + response.data.reply)
      } catch (error) {
        this.addLog('执行失败: ' + error.message, 'error')
      }
      this.running = false
    },
    
    async runAmazonSelector() {
      this.running = true
      this.addLog('开始亚马逊选品...')
      try {
        const response = await ecommerceApi.amazonProductSelector(
          this.amazonForm.selectorFile,
          this.amazonForm.selectorOutput
        )
        this.addLog('亚马逊选品完成: ' + response.data.reply)
      } catch (error) {
        this.addLog('执行失败: ' + error.message, 'error')
      }
      this.running = false
    },
    
    async runAmazonPublisher() {
      this.running = true
      this.addLog('开始生成Listing...')
      try {
        const response = await ecommerceApi.amazonListingPublisher(
          this.amazonForm.publisherFile,
          this.amazonForm.publisherOutput
        )
        this.addLog('Listing生成完成: ' + response.data.reply)
      } catch (error) {
        this.addLog('执行失败: ' + error.message, 'error')
      }
      this.running = false
    }
  }
}
</script>

<style scoped>
.ecommerce-container {
  padding: 20px;
  height: 100%;
  overflow-y: auto;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.header h1 {
  font-size: 24px;
  font-weight: 600;
}

.module-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-bottom: 30px;
}

.module-card {
  background: var(--bg-secondary, #1a1a1a);
  border: 1px solid var(--border-color, #333);
  border-radius: 12px;
  padding: 24px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.module-card:hover {
  border-color: var(--primary-color, #0070f3);
  transform: translateY(-2px);
}

.module-icon {
  font-size: 36px;
  margin-bottom: 12px;
}

.module-title {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 8px;
}

.module-desc {
  font-size: 14px;
  color: #888;
}

.panel {
  background: var(--bg-secondary, #1a1a1a);
  border: 1px solid var(--border-color, #333);
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 20px;
}

.panel-content h2 {
  font-size: 20px;
  margin-bottom: 20px;
}

.results {
  margin-top: 20px;
  padding: 16px;
  background: var(--bg-tertiary, #222);
  border-radius: 8px;
}

.results h3 {
  font-size: 16px;
  margin-bottom: 12px;
}

.result-item {
  padding: 12px;
  border-bottom: 1px solid #333;
  font-size: 14px;
}

.result-item:last-child {
  border-bottom: none;
}

.logs {
  background: var(--bg-secondary, #1a1a1a);
  border: 1px solid var(--border-color, #333);
  border-radius: 12px;
  padding: 20px;
}

.logs h3 {
  font-size: 16px;
  margin-bottom: 16px;
}

.log-item {
  display: flex;
  gap: 12px;
  padding: 8px 0;
  border-bottom: 1px solid #333;
  font-size: 14px;
}

.log-item:last-child {
  border-bottom: none;
}

.log-time {
  color: #888;
  min-width: 70px;
}

.log-message {
  flex: 1;
}

.log-item[error] .log-message {
  color: #f56c6c;
}
</style>
