<template>
  <div class="min-h-screen bg-gray-50">
    <div class="bg-white border-b border-gray-200 p-4">
      <div class="flex items-center justify-between">
        <div class="flex items-center space-x-4">
          <router-link to="/" class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-semibold transition">
            ← 返回首页
          </router-link>
          <h1 class="text-gray-900 text-xl font-bold">🤖 Agent 管理中心</h1>
        </div>
        <div class="flex items-center space-x-2">
          <span class="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
          <span class="text-xs text-gray-500">OpenClaw Connected</span>
        </div>
      </div>
    </div>

    <div class="p-6">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div class="lg:col-span-1">
          <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-4 sticky top-6">
            <h2 class="text-gray-900 text-lg font-semibold mb-4">🎯 Agent 列表</h2>
            <div class="space-y-2">
              <div 
                v-for="agent in agents" 
                :key="agent.id"
                @click="selectAgent(agent)"
                class="p-3 rounded-lg border cursor-pointer transition"
                :class="selectedAgent?.id === agent.id ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:bg-gray-50'"
              >
                <div class="flex items-center justify-between">
                  <div class="flex items-center space-x-2">
                    <span class="text-xl">{{ agent.icon }}</span>
                    <div>
                      <h3 class="text-gray-900 font-medium">{{ agent.name }}</h3>
                      <p class="text-gray-500 text-xs">{{ agent.skills.length }} 个技能</p>
                    </div>
                  </div>
                  <span :class="agent.status === 'online' ? 'text-green-500' : 'text-gray-400'" class="text-sm">
                    {{ agent.status === 'online' ? '● 在线' : '○ 离线' }}
                  </span>
                </div>
              </div>
            </div>

            <div class="mt-6 pt-4 border-t border-gray-200">
              <h3 class="text-gray-900 font-semibold mb-3">📊 统计概览</h3>
              <div class="space-y-2">
                <div class="flex justify-between text-sm">
                  <span class="text-gray-500">总 Agent</span>
                  <span class="text-gray-900 font-medium">{{ agents.length }}</span>
                </div>
                <div class="flex justify-between text-sm">
                  <span class="text-gray-500">在线 Agent</span>
                  <span class="text-green-600 font-medium">{{ agents.filter(a => a.status === 'online').length }}</span>
                </div>
                <div class="flex justify-between text-sm">
                  <span class="text-gray-500">总 Skills</span>
                  <span class="text-blue-600 font-medium">{{ totalSkills }}</span>
                </div>
                <div class="flex justify-between text-sm">
                  <span class="text-gray-500">今日任务</span>
                  <span class="text-purple-600 font-medium">{{ todayTasks }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="lg:col-span-2">
          <div v-if="selectedAgent" class="space-y-6">
            <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <div class="flex items-center justify-between mb-4">
                <div class="flex items-center space-x-3">
                  <span class="text-3xl">{{ selectedAgent.icon }}</span>
                  <div>
                    <h2 class="text-gray-900 text-xl font-bold">{{ selectedAgent.name }}</h2>
                    <p class="text-gray-500 text-sm">{{ selectedAgent.description }}</p>
                  </div>
                </div>
                <div class="flex items-center space-x-3">
                  <span :class="selectedAgent.status === 'online' ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-700'" class="px-3 py-1 rounded-full text-sm font-medium">
                    {{ selectedAgent.status === 'online' ? '在线' : '离线' }}
                  </span>
                  <button @click="addSkillToAgent" class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm font-semibold transition">
                    + 添加技能
                  </button>
                </div>
              </div>

              <div class="mt-6">
                <h3 class="text-gray-900 font-semibold mb-4">⚡ 已绑定技能</h3>
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                  <div 
                    v-for="skill in selectedAgent.skills" 
                    :key="skill.id"
                    class="bg-gray-50 rounded-lg p-4 border border-gray-200 hover:border-blue-300 transition"
                  >
                    <div class="flex items-center justify-between">
                      <div class="flex items-center space-x-2">
                        <span class="text-lg">{{ skill.icon }}</span>
                        <div>
                          <h4 class="text-gray-900 font-medium text-sm">{{ skill.name }}</h4>
                          <p class="text-gray-500 text-xs">{{ skill.description }}</p>
                        </div>
                      </div>
                      <button @click="removeSkillFromAgent(skill.id)" class="text-red-500 hover:text-red-700">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                        </svg>
                      </button>
                    </div>
                    <div class="mt-3 flex flex-wrap gap-1">
                      <span v-for="tag in skill.tags" :key="tag" class="bg-blue-100 text-blue-700 px-2 py-0.5 rounded text-xs">
                        {{ tag }}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <h3 class="text-gray-900 font-semibold mb-4">📋 任务分配</h3>
              <div class="overflow-x-auto">
                <table class="w-full">
                  <thead>
                    <tr class="border-b border-gray-200">
                      <th class="text-left py-3 px-4 text-gray-500 text-sm font-medium">任务名称</th>
                      <th class="text-left py-3 px-4 text-gray-500 text-sm font-medium">调用技能</th>
                      <th class="text-left py-3 px-4 text-gray-500 text-sm font-medium">状态</th>
                      <th class="text-left py-3 px-4 text-gray-500 text-sm font-medium">执行时间</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="task in selectedAgent.tasks" :key="task.id" class="border-b border-gray-100 hover:bg-gray-50">
                      <td class="py-3 px-4">
                        <div class="font-medium text-gray-900">{{ task.name }}</div>
                        <div class="text-xs text-gray-500">{{ task.description }}</div>
                      </td>
                      <td class="py-3 px-4">
                        <div class="flex flex-wrap gap-1">
                          <span v-for="skill in task.skillsUsed" :key="skill" class="bg-green-100 text-green-700 px-2 py-0.5 rounded text-xs">
                            {{ skill }}
                          </span>
                        </div>
                      </td>
                      <td class="py-3 px-4">
                        <span :class="getStatusClass(task.status)" class="px-2 py-1 rounded text-xs font-medium">
                          {{ task.status }}
                        </span>
                      </td>
                      <td class="py-3 px-4 text-sm text-gray-500">{{ task.executeTime }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

            <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <h3 class="text-gray-900 font-semibold mb-4">📝 执行日志</h3>
              <div class="space-y-2 max-h-60 overflow-y-auto">
                <div v-for="log in selectedAgent.logs" :key="log.id" class="bg-gray-50 rounded-lg p-3">
                  <div class="flex items-center space-x-2 text-sm">
                    <span class="text-gray-400">{{ log.time }}</span>
                    <span :class="getLogLevelClass(log.level)" class="font-medium">{{ log.level }}</span>
                    <span class="text-gray-700">{{ log.message }}</span>
                  </div>
                  <div v-if="log.skill" class="mt-1 text-xs text-gray-500">
                    调用技能: {{ log.skill }}
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div v-else class="bg-white rounded-xl shadow-sm border border-gray-200 p-12 text-center">
            <div class="text-6xl mb-4">🤖</div>
            <h3 class="text-gray-900 text-xl font-bold mb-2">选择一个 Agent</h3>
            <p class="text-gray-500">从左侧列表中选择一个 Agent 查看详细信息</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AgentManager',
  data() {
    return {
      selectedAgent: null,
      agents: [
        {
          id: 'taobao',
          name: '淘宝 Agent',
          icon: '🛒',
          description: '淘宝/天猫商品数据采集与分析',
          status: 'online',
          skills: [
            { id: 'tb1', name: 'taobao-fetcher', icon: '📦', description: '商品数据抓取', tags: ['淘宝', '抓取', '数据'] },
            { id: 'tb2', name: 'taobao-product-hunter', icon: '🔍', description: '新品挖掘', tags: ['淘宝', '新品'] },
            { id: 'tb3', name: 'taobao-shop-new-products', icon: '🏪', description: '店铺新品监控', tags: ['淘宝', '店铺', '监控'] },
            { id: 'tb4', name: 'taobao-query', icon: '❓', description: '商品价格查询', tags: ['淘宝', '价格'] },
            { id: 'tb5', name: 'taobao-roi-analyzer', icon: '📊', description: 'ROI投流分析', tags: ['淘宝', 'ROI', '分析'] },
            { id: 'tb6', name: 'taobao-low-roi-grab', icon: '⚠️', description: '低ROI高花费链接', tags: ['淘宝', 'ROI', '警告'] },
            { id: 'tb7', name: 'taobao-competitor-analyzer', icon: '⚔️', description: '竞品分析', tags: ['淘宝', '竞品'] },
            { id: 'tb8', name: 'taobao-rpa-fetch', icon: '🤖', description: 'RPA自动化抓取', tags: ['淘宝', 'RPA', '自动化'] },
            { id: 'tb9', name: 'taobao-price-monitor', icon: '📈', description: '价格监控', tags: ['淘宝', '价格', '监控'] },
            { id: 'tb10', name: 'taobao-sales-analytics', icon: '💰', description: '销量分析', tags: ['淘宝', '销量'] },
            { id: 'tb11', name: 'taobao-keyword-analysis', icon: '🔑', description: '关键词分析', tags: ['淘宝', '关键词'] },
            { id: 'tb12', name: 'taobao-crawler', icon: '🐜', description: '爬虫采集', tags: ['淘宝', '爬虫'] },
            { id: 'tb13', name: 'taobao-data-export', icon: '📥', description: '数据导出', tags: ['淘宝', '导出'] },
            { id: 'tb14', name: 'taobao-product-compare', icon: '⚖️', description: '商品对比', tags: ['淘宝', '对比'] }
          ],
          tasks: [
            { id: 't1', name: '每日商品抓取', description: '自动抓取淘宝商品数据', skillsUsed: ['taobao-fetcher', 'taobao-rpa-fetch'], status: 'COMPLETED', executeTime: '2026-04-14 10:00' },
            { id: 't2', name: '新品监控', description: '监控店铺新品上架', skillsUsed: ['taobao-shop-new-products'], status: 'IN_PROGRESS', executeTime: '2026-04-14 11:00' },
            { id: 't3', name: 'ROI分析', description: '分析投流ROI数据', skillsUsed: ['taobao-roi-analyzer'], status: 'COMPLETED', executeTime: '2026-04-14 09:00' }
          ],
          logs: [
            { id: 'l1', time: '10:00:00', level: 'INFO', message: '开始执行商品抓取任务', skill: 'taobao-fetcher' },
            { id: 'l2', time: '10:30:00', level: 'SUCCESS', message: '成功抓取1000条商品数据', skill: 'taobao-rpa-fetch' },
            { id: 'l3', time: '11:00:00', level: 'INFO', message: '开始监控店铺新品', skill: 'taobao-shop-new-products' }
          ]
        },
        {
          id: 'xiaohongshu',
          name: '小红书 Agent',
          icon: '📕',
          description: '小红书内容运营与数据分析',
          status: 'online',
          skills: [
            { id: 'xhs1', name: 'xiaohongshu-cli', icon: '💻', description: '命令行发布/操作', tags: ['小红书', 'CLI'] },
            { id: 'xhs2', name: 'xhs-master', icon: '👑', description: '全栈运营', tags: ['小红书', '运营'] },
            { id: 'xhs3', name: 'lowfans-hunter', icon: '🎯', description: '低粉爆品挖掘', tags: ['小红书', '爆品'] },
            { id: 'xhs4', name: 'xhs-viral-content', icon: '🔥', description: '爆文公式', tags: ['小红书', '爆文'] },
            { id: 'xhs5', name: 'xhs-competitor-analysis', icon: '🔍', description: '竞品分析', tags: ['小红书', '竞品'] },
            { id: 'xhs6', name: 'xhs-data-analytics', icon: '📊', description: '数据分析', tags: ['小红书', '数据'] },
            { id: 'xhs7', name: 'xhs-downloader', icon: '⬇️', description: '图片/视频下载', tags: ['小红书', '下载'] },
            { id: 'xhs8', name: 'xhs-comment-engagement', icon: '💬', description: '评论区运营', tags: ['小红书', '评论'] },
            { id: 'xhs9', name: 'xhs-keyword-tracker', icon: '🔑', description: '关键词追踪', tags: ['小红书', '关键词'] },
            { id: 'xhs10', name: 'xhs-trend-analysis', icon: '📈', description: '趋势分析', tags: ['小红书', '趋势'] },
            { id: 'xhs11', name: 'xhs-content-planner', icon: '📅', description: '内容规划', tags: ['小红书', '规划'] },
            { id: 'xhs12', name: 'xhs-hashtag-generator', icon: '🏷️', description: '标签生成', tags: ['小红书', '标签'] },
            { id: 'xhs13', name: 'xhs-account-manager', icon: '👤', description: '账号管理', tags: ['小红书', '账号'] },
            { id: 'xhs14', name: 'xhs-content-publisher', icon: '📤', description: '内容发布', tags: ['小红书', '发布'] },
            { id: 'xhs15', name: 'xhs-follower-analytics', icon: '👥', description: '粉丝分析', tags: ['小红书', '粉丝'] },
            { id: 'xhs16', name: 'xhs-like-tracker', icon: '❤️', description: '点赞追踪', tags: ['小红书', '点赞'] },
            { id: 'xhs17', name: 'xhs-comment-analytics', icon: '💬', description: '评论分析', tags: ['小红书', '评论'] },
            { id: 'xhs18', name: 'xhs-share-analytics', icon: '🔗', description: '分享分析', tags: ['小红书', '分享'] },
            { id: 'xhs19', name: 'xhs-collection-analytics', icon: '📁', description: '收藏分析', tags: ['小红书', '收藏'] },
            { id: 'xhs20', name: 'xhs-content-scraper', icon: '🐜', description: '内容抓取', tags: ['小红书', '抓取'] }
          ],
          tasks: [
            { id: 't4', name: '低粉爆品挖掘', description: '挖掘低粉高互动内容', skillsUsed: ['lowfans-hunter', 'xhs-viral-content'], status: 'COMPLETED', executeTime: '2026-04-14 08:00' },
            { id: 't5', name: '竞品分析', description: '分析竞品账号数据', skillsUsed: ['xhs-competitor-analysis'], status: 'IN_PROGRESS', executeTime: '2026-04-14 14:00' },
            { id: 't6', name: '每日发帖', description: '自动发布笔记', skillsUsed: ['xiaohongshu-cli', 'xhs-content-publisher'], status: 'COMPLETED', executeTime: '2026-04-14 15:00' }
          ],
          logs: [
            { id: 'l4', time: '08:00:00', level: 'INFO', message: '开始挖掘低粉爆品', skill: 'lowfans-hunter' },
            { id: 'l5', time: '08:30:00', level: 'SUCCESS', message: '发现20个潜在爆品', skill: 'xhs-viral-content' },
            { id: 'l6', time: '15:00:00', level: 'INFO', message: '开始发布笔记', skill: 'xiaohongshu-cli' }
          ]
        },
        {
          id: 'ai-image',
          name: 'AI图像 Agent',
          icon: '🎨',
          description: 'AI图像生成与处理',
          status: 'online',
          skills: [
            { id: 'img1', name: 'image_generate', icon: '🖼️', description: '生成图片', tags: ['AI', '图像', '生成'] },
            { id: 'img2', name: 'gpt-image-1', icon: '🤖', description: 'GPT图片生成', tags: ['AI', 'GPT', '图像'] },
            { id: 'img3', name: 'gemini-image-generator', icon: '💎', description: 'Gemini图片', tags: ['AI', 'Gemini', '图像'] },
            { id: 'img4', name: 'background-removal', icon: '✂️', description: '背景去除', tags: ['AI', '图像处理'] },
            { id: 'img5', name: 'product-scene-generator', icon: '🏙️', description: '场景图生成', tags: ['AI', '场景', '生成'] },
            { id: 'img6', name: 'video_generate', icon: '🎬', description: '视频生成', tags: ['AI', '视频', '生成'] },
            { id: 'img7', name: 'libtv', icon: '📺', description: 'AI视频', tags: ['AI', '视频'] },
            { id: 'img8', name: 'image-upscale', icon: '🔍', description: '图片放大', tags: ['AI', '图像', '放大'] },
            { id: 'img9', name: 'image-colorize', icon: '🎨', description: '图片上色', tags: ['AI', '图像', '上色'] },
            { id: 'img10', name: 'image-restoration', icon: '🔧', description: '图片修复', tags: ['AI', '图像', '修复'] },
            { id: 'img11', name: 'art-style-transfer', icon: '🎭', description: '风格迁移', tags: ['AI', '图像', '风格'] },
            { id: 'img12', name: 'image-caption', icon: '📝', description: '图片描述', tags: ['AI', '图像', '描述'] }
          ],
          tasks: [
            { id: 't7', name: '商品场景图生成', description: '生成商品场景图', skillsUsed: ['product-scene-generator', 'image_generate'], status: 'COMPLETED', executeTime: '2026-04-14 10:00' },
            { id: 't8', name: '视频制作', description: 'AI生成视频内容', skillsUsed: ['video_generate', 'libtv'], status: 'IN_PROGRESS', executeTime: '2026-04-14 16:00' }
          ],
          logs: [
            { id: 'l7', time: '10:00:00', level: 'INFO', message: '开始生成商品场景图', skill: 'product-scene-generator' },
            { id: 'l8', time: '10:15:00', level: 'SUCCESS', message: '场景图生成完成', skill: 'image_generate' }
          ]
        },
        {
          id: 'cross-border',
          name: '跨境电商 Agent',
          icon: '🌍',
          description: '跨境电商运营工具',
          status: 'online',
          skills: [
            { id: 'cb1', name: 'aliexpress-scraper', icon: '📦', description: '1688采集', tags: ['跨境', '1688', '采集'] },
            { id: 'cb2', name: 'product-filter-selector', icon: '🔍', description: '智能选品', tags: ['跨境', '选品'] },
            { id: 'cb3', name: 'batch-product-processor', icon: '⚡', description: '批量处理', tags: ['跨境', '批量'] },
            { id: 'cb4', name: 'amazon-auto-publisher', icon: '🚀', description: '亚马逊上架', tags: ['跨境', '亚马逊'] },
            { id: 'cb5', name: 'competitor-analyzer', icon: '🔍', description: '竞品分析', tags: ['跨境', '竞品'] },
            { id: 'cb6', name: 'swimwear-product-processor', icon: '👙', description: '泳装处理', tags: ['跨境', '泳装'] },
            { id: 'cb7', name: 'product-listing-generator', icon: '📝', description: 'Listing生成', tags: ['跨境', 'Listing'] },
            { id: 'cb8', name: 'price-comparator', icon: '⚖️', description: '价格对比', tags: ['跨境', '价格'] }
          ],
          tasks: [
            { id: 't9', name: '1688商品采集', description: '采集1688商品数据', skillsUsed: ['aliexpress-scraper', 'batch-product-processor'], status: 'COMPLETED', executeTime: '2026-04-14 09:00' },
            { id: 't10', name: '亚马逊上架', description: '自动上架商品', skillsUsed: ['amazon-auto-publisher'], status: 'IN_PROGRESS', executeTime: '2026-04-14 11:00' }
          ],
          logs: [
            { id: 'l9', time: '09:00:00', level: 'INFO', message: '开始采集1688商品', skill: 'aliexpress-scraper' },
            { id: 'l10', time: '09:30:00', level: 'SUCCESS', message: '采集完成，处理500件商品', skill: 'batch-product-processor' }
          ]
        },
        {
          id: 'content',
          name: '内容运营 Agent',
          icon: '✍️',
          description: '内容创作与运营',
          status: 'online',
          skills: [
            { id: 'cnt1', name: 'wewrite', icon: '📝', description: '公众号文章', tags: ['内容', '公众号'] },
            { id: 'cnt2', name: 'english-title-dehumanizer', icon: '🔤', description: '英文标题去AI化', tags: ['内容', '英文', 'AI'] },
            { id: 'cnt3', name: 'ecommerce-fission', icon: '💥', description: '裂变增长策略', tags: ['内容', '裂变'] },
            { id: 'cnt4', name: 'fission-strategist', icon: '🧠', description: '裂变增长专家', tags: ['内容', '裂变', '策略'] },
            { id: 'cnt5', name: 'content-writer', icon: '✍️', description: '内容写作', tags: ['内容', '写作'] },
            { id: 'cnt6', name: 'title-generator', icon: '📌', description: '标题生成', tags: ['内容', '标题'] }
          ],
          tasks: [
            { id: 't11', name: '公众号文章生成', description: '自动生成公众号文章', skillsUsed: ['wewrite'], status: 'COMPLETED', executeTime: '2026-04-14 08:00' },
            { id: 't12', name: '裂变活动策划', description: '策划裂变活动', skillsUsed: ['ecommerce-fission', 'fission-strategist'], status: 'COMPLETED', executeTime: '2026-04-14 10:00' }
          ],
          logs: [
            { id: 'l11', time: '08:00:00', level: 'INFO', message: '开始生成公众号文章', skill: 'wewrite' },
            { id: 'l12', time: '08:15:00', level: 'SUCCESS', message: '文章生成完成', skill: 'wewrite' }
          ]
        },
        {
          id: 'tools',
          name: '工具 Agent',
          icon: '🔧',
          description: '实用工具集合',
          status: 'online',
          skills: [
            { id: 'tool1', name: 'browser-remote', icon: '🌐', description: '远程浏览器控制', tags: ['工具', '浏览器'] },
            { id: 'tool2', name: 'dingtalk', icon: '💬', description: '钉钉消息', tags: ['工具', '钉钉'] },
            { id: 'tool3', name: 'discord', icon: '💬', description: 'Discord消息', tags: ['工具', 'Discord'] },
            { id: 'tool4', name: 'daily-hot-news', icon: '🔥', description: '每日热榜', tags: ['工具', '新闻'] },
            { id: 'tool5', name: 'weather', icon: '🌤️', description: '天气查询', tags: ['工具', '天气'] },
            { id: 'tool6', name: 'github', icon: '🐙', description: 'GitHub操作', tags: ['工具', 'GitHub'] },
            { id: 'tool7', name: 'slack', icon: '💬', description: 'Slack消息', tags: ['工具', 'Slack'] },
            { id: 'tool8', name: 'web-markdown', icon: '📄', description: '网页转Markdown', tags: ['工具', 'Markdown'] },
            { id: 'tool9', name: 'summarize', icon: '📝', description: 'URL摘要', tags: ['工具', '摘要'] },
            { id: 'tool10', name: 'url-shortener', icon: '🔗', description: 'URL短链接', tags: ['工具', '链接'] },
            { id: 'tool11', name: 'qrcode-generator', icon: '📱', description: '二维码生成', tags: ['工具', '二维码'] },
            { id: 'tool12', name: 'text-translator', icon: '🌍', description: '文本翻译', tags: ['工具', '翻译'] },
            { id: 'tool13', name: 'json-formatter', icon: '📋', description: 'JSON格式化', tags: ['工具', 'JSON'] },
            { id: 'tool14', name: 'html-validator', icon: '✅', description: 'HTML验证', tags: ['工具', 'HTML'] },
            { id: 'tool15', name: 'password-generator', icon: '🔑', description: '密码生成', tags: ['工具', '密码'] }
          ],
          tasks: [
            { id: 't13', name: '每日简报', description: '生成每日简报', skillsUsed: ['daily-hot-news', 'summarize'], status: 'COMPLETED', executeTime: '2026-04-14 07:00' },
            { id: 't14', name: '钉钉通知', description: '发送钉钉消息', skillsUsed: ['dingtalk'], status: 'COMPLETED', executeTime: '2026-04-14 08:00' }
          ],
          logs: [
            { id: 'l13', time: '07:00:00', level: 'INFO', message: '开始生成每日简报', skill: 'daily-hot-news' },
            { id: 'l14', time: '07:10:00', level: 'SUCCESS', message: '简报生成完成', skill: 'summarize' },
            { id: 'l15', time: '08:00:00', level: 'INFO', message: '发送钉钉通知', skill: 'dingtalk' }
          ]
        },
        {
          id: 'memory',
          name: '记忆 Agent',
          icon: '🧠',
          description: '长期记忆与知识管理',
          status: 'online',
          skills: [
            { id: 'mem1', name: 'memory-save', icon: '💾', description: '记忆存储', tags: ['记忆', '存储'] },
            { id: 'mem2', name: 'memory-retrieve', icon: '🔍', description: '记忆检索', tags: ['记忆', '检索'] },
            { id: 'mem3', name: 'memory-update', icon: '🔄', description: '记忆更新', tags: ['记忆', '更新'] },
            { id: 'mem4', name: 'memory-delete', icon: '🗑️', description: '记忆删除', tags: ['记忆', '删除'] },
            { id: 'mem5', name: 'memory-cleanup', icon: '🧹', description: '记忆清理', tags: ['记忆', '清理'] },
            { id: 'mem6', name: 'knowledge-graph', icon: '🕸️', description: '知识图谱', tags: ['记忆', '图谱'] },
            { id: 'mem7', name: 'memory-search', icon: '🔎', description: '记忆搜索', tags: ['记忆', '搜索'] },
            { id: 'mem8', name: 'memory-export', icon: '📤', description: '记忆导出', tags: ['记忆', '导出'] },
            { id: 'mem9', name: 'memory-import', icon: '📥', description: '记忆导入', tags: ['记忆', '导入'] },
            { id: 'mem10', name: 'memory-backup', icon: '💽', description: '记忆备份', tags: ['记忆', '备份'] }
          ],
          tasks: [
            { id: 't15', name: '记忆整理', description: '整理每日记忆', skillsUsed: ['memory-save', 'knowledge-graph'], status: 'COMPLETED', executeTime: '2026-04-14 00:00' },
            { id: 't16', name: '记忆清理', description: '清理过期记忆', skillsUsed: ['memory-cleanup'], status: 'COMPLETED', executeTime: '2026-04-14 03:00' }
          ],
          logs: [
            { id: 'l16', time: '00:00:00', level: 'INFO', message: '开始整理记忆', skill: 'memory-save' },
            { id: 'l17', time: '00:30:00', level: 'SUCCESS', message: '记忆整理完成', skill: 'knowledge-graph' }
          ]
        },
        {
          id: 'security',
          name: '安全 Agent',
          icon: '🛡️',
          description: '安全检查与监控',
          status: 'online',
          skills: [
            { id: 'sec1', name: 'security-scan', icon: '🔍', description: '安全扫描', tags: ['安全', '扫描'] },
            { id: 'sec2', name: 'log-monitor', icon: '📋', description: '日志监控', tags: ['安全', '日志'] },
            { id: 'sec3', name: 'threat-detection', icon: '⚠️', description: '威胁检测', tags: ['安全', '威胁'] },
            { id: 'sec4', name: 'access-control', icon: '🔑', description: '权限管理', tags: ['安全', '权限'] },
            { id: 'sec5', name: 'audit-log', icon: '📝', description: '审计日志', tags: ['安全', '审计'] },
            { id: 'sec6', name: 'vulnerability-scan', icon: '🔒', description: '漏洞扫描', tags: ['安全', '漏洞'] },
            { id: 'sec7', name: 'firewall', icon: '🧱', description: '防火墙管理', tags: ['安全', '防火墙'] },
            { id: 'sec8', name: 'anti-virus', icon: '🦠', description: '病毒检测', tags: ['安全', '病毒'] },
            { id: 'sec9', name: 'data-encryption', icon: '🔐', description: '数据加密', tags: ['安全', '加密'] },
            { id: 'sec10', name: 'secure-backup', icon: '💾', description: '安全备份', tags: ['安全', '备份'] }
          ],
          tasks: [
            { id: 't17', name: '每日安全检查', description: '执行安全扫描', skillsUsed: ['security-scan', 'threat-detection'], status: 'COMPLETED', executeTime: '2026-04-14 07:00' },
            { id: 't18', name: '权限审计', description: '检查权限配置', skillsUsed: ['access-control', 'audit-log'], status: 'COMPLETED', executeTime: '2026-04-14 06:00' }
          ],
          logs: [
            { id: 'l18', time: '07:00:00', level: 'INFO', message: '开始安全检查', skill: 'security-scan' },
            { id: 'l19', time: '07:15:00', level: 'SUCCESS', message: '安全检查完成', skill: 'threat-detection' }
          ]
        },
        {
          id: 'instreet',
          name: 'InStreet Agent',
          icon: '🏬',
          description: 'InStreet学习库管理',
          status: 'online',
          skills: [
            { id: 'is1', name: 'content-sync', icon: '🔄', description: '内容同步', tags: ['学习', '同步'] },
            { id: 'is2', name: 'content-publish', icon: '📤', description: '内容发布', tags: ['学习', '发布'] },
            { id: 'is3', name: 'data-statistics', icon: '📊', description: '数据统计', tags: ['学习', '统计'] },
            { id: 'is4', name: 'user-analysis', icon: '👥', description: '用户分析', tags: ['学习', '用户'] },
            { id: 'is5', name: 'course-manager', icon: '📚', description: '课程管理', tags: ['学习', '课程'] },
            { id: 'is6', name: 'progress-tracker', icon: '📈', description: '进度追踪', tags: ['学习', '进度'] },
            { id: 'is7', name: 'quiz-generator', icon: '❓', description: '测验生成', tags: ['学习', '测验'] },
            { id: 'is8', name: 'certificate-manager', icon: '🏆', description: '证书管理', tags: ['学习', '证书'] }
          ],
          tasks: [
            { id: 't19', name: '学习库同步', description: '同步学习内容', skillsUsed: ['content-sync'], status: 'COMPLETED', executeTime: '2026-04-14 08:00' },
            { id: 't20', name: '每日统计', description: '统计学习数据', skillsUsed: ['data-statistics', 'user-analysis'], status: 'COMPLETED', executeTime: '2026-04-14 09:00' }
          ],
          logs: [
            { id: 'l20', time: '08:00:00', level: 'INFO', message: '开始学习库同步', skill: 'content-sync' },
            { id: 'l21', time: '08:20:00', level: 'SUCCESS', message: '同步完成', skill: 'content-sync' }
          ]
        },
        {
          id: 'main',
          name: '主 Agent',
          icon: '🤖',
          description: '核心智能助手',
          status: 'online',
          skills: [
            { id: 'main1', name: 'web-browser', icon: '🌐', description: '网页浏览', tags: ['浏览器'] },
            { id: 'main2', name: 'api-caller', icon: '🔌', description: 'API调用', tags: ['API'] },
            { id: 'main3', name: 'file-operations', icon: '📁', description: '文件操作', tags: ['文件'] },
            { id: 'main4', name: 'db-operations', icon: '🗄️', description: '数据库操作', tags: ['数据库'] },
            { id: 'main5', name: 'email-sender', icon: '📧', description: '邮件发送', tags: ['邮件'] },
            { id: 'main6', name: 'sms-sender', icon: '📱', description: '短信发送', tags: ['短信'] },
            { id: 'main7', name: 'wechat-message', icon: '💬', description: '微信消息', tags: ['微信'] },
            { id: 'main8', name: 'http-client', icon: '🌐', description: 'HTTP请求', tags: ['HTTP'] },
            { id: 'main9', name: 'json-handler', icon: '📋', description: 'JSON处理', tags: ['JSON'] },
            { id: 'main10', name: 'text-processor', icon: '📝', description: '文本处理', tags: ['文本'] },
            { id: 'main11', name: 'date-parser', icon: '📅', description: '日期解析', tags: ['日期'] },
            { id: 'main12', name: 'number-calculator', icon: '🧮', description: '数值计算', tags: ['计算'] },
            { id: 'main13', name: 'string-formatter', icon: '🔤', description: '字符串格式化', tags: ['字符串'] },
            { id: 'main14', name: 'list-processor', icon: '📋', description: '列表处理', tags: ['列表'] },
            { id: 'main15', name: 'dict-processor', icon: '📚', description: '字典处理', tags: ['字典'] },
            { id: 'main16', name: 'logic-operator', icon: '⚙️', description: '逻辑运算', tags: ['逻辑'] },
            { id: 'main17', name: 'condition-checker', icon: '❓', description: '条件判断', tags: ['条件'] },
            { id: 'main18', name: 'loop-controller', icon: '🔄', description: '循环控制', tags: ['循环'] },
            { id: 'main19', name: 'error-handler', icon: '⚠️', description: '错误处理', tags: ['错误'] },
            { id: 'main20', name: 'logging', icon: '📝', description: '日志记录', tags: ['日志'] }
          ],
          tasks: [
            { id: 't21', name: '数据同步', description: '同步数据', skillsUsed: ['api-caller', 'db-operations'], status: 'IN_PROGRESS', executeTime: '2026-04-14 11:00' },
            { id: 't22', name: '邮件通知', description: '发送邮件', skillsUsed: ['email-sender'], status: 'COMPLETED', executeTime: '2026-04-14 10:00' }
          ],
          logs: [
            { id: 'l22', time: '10:00:00', level: 'INFO', message: '发送邮件通知', skill: 'email-sender' },
            { id: 'l23', time: '11:00:00', level: 'INFO', message: '开始数据同步', skill: 'api-caller' }
          ]
        }
      ]
    }
  },
  computed: {
    totalSkills() {
      return this.agents.reduce((sum, agent) => sum + agent.skills.length, 0)
    },
    todayTasks() {
      return this.agents.reduce((sum, agent) => sum + agent.tasks.length, 0)
    }
  },
  methods: {
    selectAgent(agent) {
      this.selectedAgent = agent
    },
    addSkillToAgent() {
      const newSkill = {
        id: Date.now().toString(),
        name: '新技能',
        icon: '✨',
        description: '新添加的技能',
        tags: ['新技能']
      }
      if (this.selectedAgent) {
        this.selectedAgent.skills.push(newSkill)
      }
    },
    removeSkillFromAgent(skillId) {
      if (this.selectedAgent) {
        this.selectedAgent.skills = this.selectedAgent.skills.filter(s => s.id !== skillId)
      }
    },
    getStatusClass(status) {
      const classes = {
        'COMPLETED': 'bg-green-100 text-green-700',
        'IN_PROGRESS': 'bg-blue-100 text-blue-700',
        'FAILED': 'bg-red-100 text-red-700',
        'PENDING': 'bg-yellow-100 text-yellow-700'
      }
      return classes[status] || 'bg-gray-100 text-gray-700'
    },
    getLogLevelClass(level) {
      const classes = {
        'INFO': 'text-blue-600',
        'SUCCESS': 'text-green-600',
        'WARNING': 'text-yellow-600',
        'ERROR': 'text-red-600'
      }
      return classes[level] || 'text-gray-600'
    }
  }
}
</script>
