<template>
  <div class="home">
    <!-- Navigation -->
    <nav class="flex justify-between items-center px-8 py-6 sticky top-0 bg-white/80 backdrop-blur-md z-50">
      <div class="flex items-center space-x-2">
        <div class="w-2 h-2 bg-black rounded-full"></div>
        <span class="text-sm font-semibold tracking-widest uppercase">OpenClaw</span>
      </div>
      <div class="flex items-center space-x-6 text-gray-400">
        <router-link to="/dashboard" class="text-gray-400 hover:text-black transition">仪表盘</router-link>
        <router-link to="/chat" class="text-gray-400 hover:text-black transition">AI聊天</router-link>
        <router-link to="/browser" class="text-gray-400 hover:text-black transition">浏览器</router-link>
        <router-link to="/voice-call" class="text-gray-400 hover:text-black transition">语音通话</router-link>
        <router-link to="/analytics" class="text-gray-400 hover:text-black transition">数据分析</router-link>
        <router-link to="/file-manager" class="text-gray-400 hover:text-black transition">文件管理</router-link>
        <router-link to="/team" class="text-gray-400 hover:text-black transition">团队协作</router-link>
        <router-link to="/monitor" class="text-gray-400 hover:text-black transition">系统监控</router-link>
        <router-link to="/agent-manager" class="text-gray-400 hover:text-black transition">Agent管理</router-link>
        <router-link to="/ecommerce" class="text-gray-400 hover:text-black transition">电商运营</router-link>
        <router-link to="/schedule-manager" class="text-gray-400 hover:text-black transition">定时任务</router-link>
        <router-link to="/table-manager" class="text-gray-400 hover:text-black transition">多维表格</router-link>
        <router-link to="/lobster-test" class="text-gray-400 hover:text-black transition">🦞虾格测试</router-link>
        <router-link to="/settings" class="text-gray-400 hover:text-black transition">设置</router-link>
        <div class="w-8 h-8 rounded-full bg-gray-100 border border-gray-200"></div>
      </div>
    </nav>

    <!-- Hero Section -->
    <section class="max-w-7xl mx-auto px-8 mt-16 text-center">
      <div class="inline-flex items-center px-4 py-2 bg-blue-50 rounded-full mb-8">
        <i data-lucide="sparkles" class="w-4 h-4 text-blue-500 mr-2"></i>
        <span class="text-xs font-medium text-blue-600">全新智能AI代理平台</span>
      </div>
      
      <h1 class="text-5xl font-light mb-6">lebaic虾虾</h1>
      <p class="text-lg text-gray-400 max-w-2xl mx-auto mb-12">
        大家好～这里是 lebaic 虾虾🦐<br>
        我的创作者是 AI 信息部的小伙伴！<br>
        依托 OpenClaw 智能能力打造，聪明又能干，主打高效助力、趣味互动，随时待命，为大家带来超实用的 AI 小帮手服务～
      </p>

      <div class="flex justify-center space-x-4 mb-16">
        <button class="px-8 py-3 bg-black text-white rounded-full text-sm font-medium hover:bg-gray-800 transition" @click="goToChat">
          开始使用
        </button>
        <button class="px-8 py-3 border border-gray-200 rounded-full text-sm font-medium hover:border-gray-400 transition" @click="learnMore">
          了解更多
        </button>
      </div>
    </section>

    <!-- Features Section -->
    <section class="max-w-7xl mx-auto px-8">
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-6 gap-6">
        <router-link to="/chat" class="block p-8 border border-gray-100 rounded-3xl hover:border-gray-300 transition-all duration-500 group cursor-pointer">
          <div class="w-12 h-12 rounded-2xl bg-blue-50 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
            <i data-lucide="message-circle" class="w-6 h-6 text-blue-500"></i>
          </div>
          <h3 class="text-lg font-medium mb-2">AI 聊天</h3>
          <p class="text-sm text-gray-400">集成多种AI模型，支持智能对话</p>
        </router-link>

        <router-link to="/browser" class="block p-8 border border-gray-100 rounded-3xl hover:border-gray-300 transition-all duration-500 group cursor-pointer">
          <div class="w-12 h-12 rounded-2xl bg-green-50 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
            <i data-lucide="globe" class="w-6 h-6 text-green-500"></i>
          </div>
          <h3 class="text-lg font-medium mb-2">浏览器自动化</h3>
          <p class="text-sm text-gray-400">支持网页操作和数据采集</p>
        </router-link>

        <router-link to="/dashboard" class="block p-8 border border-gray-100 rounded-3xl hover:border-gray-300 transition-all duration-500 group cursor-pointer">
          <div class="w-12 h-12 rounded-2xl bg-purple-50 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
            <i data-lucide="trending-up" class="w-6 h-6 text-purple-500"></i>
          </div>
          <h3 class="text-lg font-medium mb-2">关键词趋势分析</h3>
          <p class="text-sm text-gray-400">分析搜索关键词热度趋势</p>
        </router-link>

        <router-link to="/chat" class="block p-8 border border-gray-100 rounded-3xl hover:border-gray-300 transition-all duration-500 group cursor-pointer">
          <div class="w-12 h-12 rounded-2xl bg-blue-50 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
            <i data-lucide="message-circle" class="w-6 h-6 text-blue-500"></i>
          </div>
          <h3 class="text-lg font-medium mb-2">chat聊天</h3>
          <p class="text-sm text-gray-400">支持文本聊天交互</p>
        </router-link>

        <router-link to="/agent-manager" class="block p-8 border border-gray-100 rounded-3xl hover:border-gray-300 transition-all duration-500 group cursor-pointer">
          <div class="w-12 h-12 rounded-2xl bg-indigo-50 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
            <i data-lucide="users" class="w-6 h-6 text-indigo-500"></i>
          </div>
          <h3 class="text-lg font-medium mb-2">Agent管理</h3>
          <p class="text-sm text-gray-400">任务分配与进度监控</p>
        </router-link>

        <router-link to="/schedule-manager" class="block p-8 border border-gray-100 rounded-3xl hover:border-gray-300 transition-all duration-500 group cursor-pointer">
          <div class="w-12 h-12 rounded-2xl bg-yellow-50 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
            <i data-lucide="clock" class="w-6 h-6 text-yellow-500"></i>
          </div>
          <h3 class="text-lg font-medium mb-2">定时任务</h3>
          <p class="text-sm text-gray-400">自动化任务调度管理</p>
        </router-link>

        <router-link to="/table-manager" class="block p-8 border border-gray-100 rounded-3xl hover:border-gray-300 transition-all duration-500 group cursor-pointer">
          <div class="w-12 h-12 rounded-2xl bg-cyan-50 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
            <i data-lucide="table" class="w-6 h-6 text-cyan-500"></i>
          </div>
          <h3 class="text-lg font-medium mb-2">多维表格</h3>
          <p class="text-sm text-gray-400">飞书钉钉表格集成与AI分析</p>
        </router-link>

        <router-link to="/lobster-test" class="block p-8 border border-gray-100 rounded-3xl hover:border-orange-300 transition-all duration-500 group cursor-pointer">
          <div class="w-12 h-12 rounded-2xl bg-gradient-to-br from-orange-50 to-pink-50 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
            <span class="text-xl">🦞</span>
          </div>
          <h3 class="text-lg font-medium mb-2">虾格测试</h3>
          <p class="text-sm text-gray-400">测测你的小龙虾人格</p>
        </router-link>

        <router-link to="/analytics" class="block p-8 border border-gray-100 rounded-3xl hover:border-gray-300 transition-all duration-500 group cursor-pointer">
          <div class="w-12 h-12 rounded-2xl bg-red-50 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
            <i data-lucide="bar-chart-2" class="w-6 h-6 text-red-500"></i>
          </div>
          <h3 class="text-lg font-medium mb-2">数据分析</h3>
          <p class="text-sm text-gray-400">可视化报表与数据洞察</p>
        </router-link>

        <router-link to="/file-manager" class="block p-8 border border-gray-100 rounded-3xl hover:border-gray-300 transition-all duration-500 group cursor-pointer">
          <div class="w-12 h-12 rounded-2xl bg-teal-50 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
            <i data-lucide="folder-open" class="w-6 h-6 text-teal-500"></i>
          </div>
          <h3 class="text-lg font-medium mb-2">文件管理</h3>
          <p class="text-sm text-gray-400">云端文件存储与共享</p>
        </router-link>

        <router-link to="/team" class="block p-8 border border-gray-100 rounded-3xl hover:border-gray-300 transition-all duration-500 group cursor-pointer">
          <div class="w-12 h-12 rounded-2xl bg-pink-50 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
            <i data-lucide="users" class="w-6 h-6 text-pink-500"></i>
          </div>
          <h3 class="text-lg font-medium mb-2">团队协作</h3>
          <p class="text-sm text-gray-400">团队任务分配与沟通</p>
        </router-link>

        <router-link to="/monitor" class="block p-8 border border-gray-100 rounded-3xl hover:border-gray-300 transition-all duration-500 group cursor-pointer">
          <div class="w-12 h-12 rounded-2xl bg-indigo-50 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
            <i data-lucide="activity" class="w-6 h-6 text-indigo-500"></i>
          </div>
          <h3 class="text-lg font-medium mb-2">系统监控</h3>
          <p class="text-sm text-gray-400">实时监控与告警通知</p>
        </router-link>
      </div>
    </section>

    <!-- Stats Section -->
    <section class="max-w-7xl mx-auto px-8 mt-20">
      <div class="p-10 bg-[#FAFAFA] rounded-3xl">
        <div class="grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
          <div>
            <p class="text-4xl font-semibold mb-2">100+</p>
            <p class="text-xs text-gray-400 uppercase tracking-wider">每日请求</p>
          </div>
          <div>
            <p class="text-4xl font-semibold mb-2">98.5%</p>
            <p class="text-xs text-gray-400 uppercase tracking-wider">成功率</p>
          </div>
          <div>
            <p class="text-4xl font-semibold mb-2">156ms</p>
            <p class="text-xs text-gray-400 uppercase tracking-wider">平均延迟</p>
          </div>
          <div>
            <p class="text-4xl font-semibold mb-2">24/7</p>
            <p class="text-xs text-gray-400 uppercase tracking-wider">持续运行</p>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="max-w-7xl mx-auto px-8 mt-20 pb-10">
      <div class="flex flex-col md:flex-row justify-between items-center pt-8 border-t border-gray-100">
        <div class="flex items-center space-x-2 mb-4 md:mb-0">
          <div class="w-2 h-2 bg-black rounded-full"></div>
          <span class="text-xs font-semibold tracking-widest uppercase text-gray-400">OpenClaw</span>
        </div>
        <p class="text-xs text-gray-400">© 2024 OpenClaw. All rights reserved.</p>
      </div>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'Home',
  mounted() {
    if (window.lucide) {
      window.lucide.createIcons()
    }
  },
  methods: {
    goToChat() {
      this.$router.push('/chat')
    },
    learnMore() {
      alert('OpenClaw 是一个智能AI代理平台，提供以下功能：\n\n1. AI聊天 - 集成多种AI模型，支持智能对话\n2. 浏览器自动化 - 支持网页操作和数据采集\n3. 通讯渠道 - 支持钉钉、微信等多渠道接入\n4. 语音通话 - 支持语音交互功能\n\n更多详情请访问官方文档。')
    }
  }
}
</script>

<style scoped>
.home {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  background-color: #FFFFFF;
  color: #1D1D1F;
  -webkit-font-smoothing: antialiased;
  min-height: 100vh;
}
</style>