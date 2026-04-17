<template>
  <div class="lobster-test min-h-screen bg-gradient-to-br from-orange-50 via-pink-50 to-purple-50">
    <!-- Header -->
    <nav class="flex justify-between items-center px-8 py-6 border-b border-gray-100 sticky top-0 bg-white/80 backdrop-blur-md z-50">
      <div class="flex items-center space-x-3">
        <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-orange-400 to-pink-500 flex items-center justify-center text-xl">🦞</div>
        <span class="text-sm font-bold tracking-widest uppercase text-gray-900">OpenClaw</span>
      </div>
      <div class="flex items-center space-x-6">
        <router-link to="/" class="text-gray-500 hover:text-gray-900 transition text-sm">首页</router-link>
        <router-link to="/dashboard" class="text-gray-500 hover:text-gray-900 transition text-sm">仪表盘</router-link>
        <router-link to="/chat" class="text-gray-500 hover:text-gray-900 transition text-sm">AI聊天</router-link>
        <router-link to="/agent-manager" class="text-gray-500 hover:text-gray-900 transition text-sm">Agent管理</router-link>
        <router-link to="/lobster-test" class="px-4 py-2 bg-gradient-to-r from-orange-400 to-pink-500 rounded-full text-sm font-medium text-white">虾格测试</router-link>
        <div class="w-8 h-8 rounded-full bg-gradient-to-br from-orange-400 to-pink-500 flex items-center justify-center text-xs text-white">👤</div>
      </div>
    </nav>

    <main class="max-w-4xl mx-auto px-8 py-12">
      <!-- Hero Section -->
      <section class="text-center mb-12">
        <div class="inline-flex items-center px-4 py-2 bg-white rounded-full shadow-sm mb-6">
          <span class="text-xs font-medium text-orange-500 mr-2">🦞</span>
          <span class="text-xs font-medium text-gray-700">小龙虾人格测试</span>
        </div>
        <h1 class="text-4xl font-bold mb-4 text-gray-900">
          测测你的虾格
        </h1>
        <p class="text-gray-500 mb-8">
          夜游、冒泡、出钳、躲泥、突然觉醒。总有一种虾格，在池塘深处等你。
        </p>
        
        <!-- Mode Selection -->
        <div class="flex justify-center space-x-4">
          <button 
            class="px-8 py-4 rounded-2xl font-medium transition-all duration-300"
            :class="mode === 'human' ? 'bg-gradient-to-r from-orange-400 to-pink-500 text-white shadow-lg shadow-orange-200' : 'bg-white text-gray-600 border border-gray-200 hover:border-gray-300'"
            @click="switchMode('human')"
          >
            👤 人类模式
          </button>
          <button 
            class="px-8 py-4 rounded-2xl font-medium transition-all duration-300"
            :class="mode === 'agent' ? 'bg-gradient-to-r from-orange-400 to-pink-500 text-white shadow-lg shadow-orange-200' : 'bg-white text-gray-600 border border-gray-200 hover:border-gray-300'"
            @click="switchMode('agent')"
          >
            🤖 Agent 模式
          </button>
        </div>
        
        <!-- Agent Mode Start Button -->
        <div v-if="mode === 'agent' && !agentStarted" class="mt-8">
          <button 
            class="px-8 py-4 rounded-2xl font-medium bg-gradient-to-r from-blue-500 to-purple-600 text-white shadow-lg hover:opacity-90 transition"
            @click="startAgentTest"
          >
            🚀 让AI开始答题
          </button>
          <p class="text-xs text-gray-400 mt-4">AI将自动回答所有题目，并展示它的思考过程</p>
        </div>
      </section>

      <!-- Progress Bar -->
      <div class="mb-8">
        <div class="flex justify-between items-center mb-2">
          <span class="text-xs text-gray-500 uppercase tracking-wider">答题进度</span>
          <span class="text-xs text-gray-500">{{ currentQuestion + 1 }} / {{ questions.length }}</span>
        </div>
        <div class="h-2 bg-gray-100 rounded-full overflow-hidden">
          <div 
            class="h-full bg-gradient-to-r from-orange-400 to-pink-500 rounded-full transition-all duration-500"
            :style="{ width: ((currentQuestion + 1) / questions.length * 100) + '%' }"
          ></div>
        </div>
      </div>

      <!-- Question Card -->
      <section class="bg-white rounded-3xl p-8 shadow-sm border border-gray-100 mb-8">
        <div class="text-center">
          <div class="text-6xl mb-6">{{ questions[currentQuestion]?.emoji }}</div>
          <h2 class="text-xl font-bold text-gray-900 mb-2">{{ questions[currentQuestion]?.question }}</h2>
          <p class="text-gray-500 mb-8">{{ questions[currentQuestion]?.subtitle }}</p>
          
          <!-- AI Thinking Process (Agent Mode) -->
          <div v-if="mode === 'agent' && agentStarted && currentQuestion < questions.length" class="mb-8">
            <div class="bg-gradient-to-r from-blue-50 to-purple-50 rounded-2xl p-6">
              <div class="flex items-center space-x-3 mb-4">
                <div class="w-10 h-10 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center">🤖</div>
                <div>
                  <p class="text-sm font-medium text-gray-700">AI 正在思考...</p>
                  <div class="flex space-x-1 mt-1">
                    <span class="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style="animation-delay: 0ms"></span>
                    <span class="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style="animation-delay: 150ms"></span>
                    <span class="w-2 h-2 bg-blue-400 rounded-full animate-bounce" style="animation-delay: 300ms"></span>
                  </div>
                </div>
              </div>
              <p class="text-gray-600 text-sm text-left">{{ currentAgentThought }}</p>
            </div>
          </div>
          
          <!-- Options -->
          <div class="grid grid-cols-2 gap-4">
            <button 
              v-for="(option, index) in questions[currentQuestion]?.options" 
              :key="index"
              class="px-6 py-4 rounded-xl border-2 transition-all duration-300 text-left"
              :class="{
                'border-orange-400 bg-orange-50': selectedAnswer === index,
                'border-blue-400 bg-blue-50': mode === 'agent' && agentAnswers[currentQuestion] === index,
                'border-gray-200 hover:border-orange-300 hover:bg-orange-50/50': selectedAnswer !== index && (mode !== 'agent' || agentAnswers[currentQuestion] !== index)
              }"
              :disabled="mode === 'agent'"
              @click="mode === 'human' && selectAnswer(index)"
            >
              <div class="flex items-center space-x-3">
                <span class="text-lg">{{ option.emoji }}</span>
                <span class="text-gray-700">{{ option.text }}</span>
                <span v-if="mode === 'agent' && agentAnswers[currentQuestion] === index" class="text-green-500">✓</span>
              </div>
            </button>
          </div>
        </div>
      </section>

      <!-- Navigation Buttons (Human Mode Only) -->
      <div v-if="mode === 'human'" class="flex justify-between items-center">
        <button 
          class="px-6 py-3 rounded-xl border border-gray-200 text-gray-600 hover:bg-gray-50 transition disabled:opacity-50 disabled:cursor-not-allowed"
          :disabled="currentQuestion === 0"
          @click="prevQuestion"
        >
          ← 上一题
        </button>
        <button 
          class="px-6 py-3 rounded-xl bg-gradient-to-r from-orange-400 to-pink-500 text-white font-medium hover:opacity-90 transition disabled:opacity-50 disabled:cursor-not-allowed"
          :disabled="selectedAnswer === null"
          @click="nextQuestion"
        >
          {{ currentQuestion === questions.length - 1 ? '查看结果' : '下一题 →' }}
        </button>
      </div>

      <!-- Result Modal -->
      <div v-if="showResult" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
        <div class="bg-white rounded-3xl p-8 w-full max-w-md text-center">
          <div class="text-8xl mb-4">{{ resultPersonality?.emoji }}</div>
          <h3 class="text-2xl font-bold text-gray-900 mb-2">{{ resultPersonality?.title }}</h3>
          <p class="text-gray-500 mb-6">{{ resultPersonality?.description }}</p>
          
          <div class="bg-gradient-to-br from-orange-50 to-pink-50 rounded-2xl p-6 mb-6">
            <h4 class="text-sm font-bold text-gray-700 mb-3">虾格特点</h4>
            <ul class="space-y-2 text-left">
              <li v-for="(trait, index) in resultPersonality?.traits" :key="index" class="flex items-center text-gray-600">
                <span class="text-orange-400 mr-2">✓</span>
                {{ trait }}
              </li>
            </ul>
          </div>

          <div class="flex justify-center space-x-4">
            <button 
              class="px-6 py-3 rounded-xl border border-gray-200 text-gray-600 hover:bg-gray-50 transition"
              @click="restartTest"
            >
              重新测试
            </button>
            <button 
              class="px-6 py-3 rounded-xl bg-gradient-to-r from-orange-400 to-pink-500 text-white font-medium hover:opacity-90 transition"
              @click="shareResult"
            >
              分享结果
            </button>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
export default {
  name: 'LobsterTest',
  data() {
    return {
      mode: 'human',
      currentQuestion: 0,
      selectedAnswer: null,
      answers: [],
      showResult: false,
      resultPersonality: null,
      
      agentStarted: false,
      agentAnswers: [],
      currentAgentThought: '',
      isAgentAnswering: false,
      
      originalQuestions: [
        {
          emoji: '🌙',
          question: '夜晚降临，你通常会？',
          subtitle: '选择最符合你的行为',
          options: [
            { emoji: '🌊', text: '在池塘边夜游，思考人生' },
            { emoji: '💤', text: '早早躲进洞里睡觉' },
            { emoji: '🔥', text: '和朋友们开派对狂欢' },
            { emoji: '🔦', text: '在泥里挖洞搞建设' }
          ],
          scoring: { introvert: 1, extrovert: 2, active: 3, builder: 4 }
        },
        {
          emoji: '🦐',
          question: '遇到危险时，你的反应是？',
          subtitle: '本能反应测试',
          options: [
            { emoji: '🏃', text: '快速逃跑躲起来' },
            { emoji: '✊', text: '举起钳子反抗' },
            { emoji: '😶', text: '假装石头不动' },
            { emoji: '👥', text: '呼唤同伴帮忙' }
          ],
          scoring: { cautious: 1, brave: 2, calm: 3, team: 4 }
        },
        {
          emoji: '🍤',
          question: '最喜欢的食物是？',
          subtitle: '饮食偏好揭示性格',
          options: [
            { emoji: '🦠', text: '微小的浮游生物' },
            { emoji: '🌱', text: '鲜嫩的水草' },
            { emoji: '🍖', text: '高蛋白小虫' },
            { emoji: '🥗', text: '什么都吃的杂食' }
          ],
          scoring: { gentle: 1, vegetarian: 2, hunter: 3, flexible: 4 }
        },
        {
          emoji: '💧',
          question: '你更喜欢哪种水环境？',
          subtitle: '环境选择反映内心',
          options: [
            { emoji: '🌊', text: '清澈见底的浅水区' },
            { emoji: '🌀', text: '暗流涌动的深水区' },
            { emoji: '🏝️', text: '温暖的岸边浅滩' },
            { emoji: '🪨', text: '布满岩石的洞穴' }
          ],
          scoring: { open: 1, adventurous: 2, social: 3, private: 4 }
        },
        {
          emoji: '🦞',
          question: '如果能变身一天，你想变成？',
          subtitle: '内心渴望测试',
          options: [
            { emoji: '🐬', text: '自由自在的海豚' },
            { emoji: '🦀', text: '横行霸道的螃蟹' },
            { emoji: '🐠', text: '色彩斑斓的热带鱼' },
            { emoji: '🐢', text: '长寿智慧的乌龟' }
          ],
          scoring: { free: 1, powerful: 2, creative: 3, wise: 4 }
        },
        {
          emoji: '☀️',
          question: '阳光明媚的一天，你会？',
          subtitle: '日常活动偏好',
          options: [
            { emoji: '😴', text: '找个阴凉处睡午觉' },
            { emoji: '🏊', text: '在水中畅快游泳' },
            { emoji: '👀', text: '观察周围的小鱼小虾' },
            { emoji: '🚶', text: '在岸边散步晒太阳' }
          ],
          scoring: { lazy: 1, active: 2, observer: 3, explorer: 4 }
        },
        {
          emoji: '🎵',
          question: '你最喜欢的音乐类型是？',
          subtitle: '音乐品味测试',
          options: [
            { emoji: '🎹', text: '舒缓的古典音乐' },
            { emoji: '🎸', text: '热情的摇滚' },
            { emoji: '🎶', text: '欢快的流行音乐' },
            { emoji: '🌿', text: '自然环境声音' }
          ],
          scoring: { calm: 1, energetic: 2, social: 3, peaceful: 4 }
        },
        {
          emoji: '📚',
          question: '如果有时间，你会？',
          subtitle: '休闲活动选择',
          options: [
            { emoji: '📖', text: '阅读一本好书' },
            { emoji: '🎮', text: '玩有趣的游戏' },
            { emoji: '👥', text: '和朋友聚会' },
            { emoji: '🧘', text: '静心冥想' }
          ],
          scoring: { intellectual: 1, playful: 2, social: 3, mindful: 4 }
        },
        {
          emoji: '🎁',
          question: '收到礼物时，你会？',
          subtitle: '社交反应测试',
          options: [
            { emoji: '😊', text: '开心地收下并感谢' },
            { emoji: '🤔', text: '先想想礼物的用途' },
            { emoji: '🎁', text: '回赠对方礼物' },
            { emoji: '😳', text: '不好意思地推脱' }
          ],
          scoring: { grateful: 1, thoughtful: 2, generous: 3, shy: 4 }
        },
        {
          emoji: '🎯',
          question: '设定目标后，你会？',
          subtitle: '执行力测试',
          options: [
            { emoji: '🚀', text: '立刻开始行动' },
            { emoji: '📝', text: '制定详细计划' },
            { emoji: '⏳', text: '慢慢考虑再决定' },
            { emoji: '😴', text: '明天再做吧' }
          ],
          scoring: { impulsive: 1, planner: 2, cautious: 3, procrastinator: 4 }
        },
        {
          emoji: '🌊',
          question: '遇到暴风雨，你会？',
          subtitle: '危机处理能力',
          options: [
            { emoji: '🏠', text: '赶紧躲进安全的洞穴' },
            { emoji: '💪', text: '顶着风浪继续前进' },
            { emoji: '📡', text: '通知其他同伴躲避' },
            { emoji: '🔍', text: '观察情况再决定' }
          ],
          scoring: { cautious: 1, brave: 2, helpful: 3, analytical: 4 }
        },
        {
          emoji: '💬',
          question: '朋友遇到困难时，你会？',
          subtitle: '社交支持测试',
          options: [
            { emoji: '🤗', text: '给予安慰和鼓励' },
            { emoji: '💡', text: '帮忙分析解决问题' },
            { emoji: '👥', text: '找更多朋友一起帮忙' },
            { emoji: '😔', text: '感同身受但不知如何帮助' }
          ],
          scoring: { empathetic: 1, problemSolver: 2, collaborative: 3, sympathetic: 4 }
        },
        {
          emoji: '🌈',
          question: '雨后出现彩虹，你会？',
          subtitle: '生活态度测试',
          options: [
            { emoji: '📸', text: '拍照记录美好时刻' },
            { emoji: '🤔', text: '思考彩虹的形成原理' },
            { emoji: '🎉', text: '开心地跳起来欢呼' },
            { emoji: '😌', text: '安静欣赏自然美景' }
          ],
          scoring: { creative: 1, curious: 2, enthusiastic: 3, peaceful: 4 }
        },
        {
          emoji: '🏆',
          question: '赢得比赛后，你会？',
          subtitle: '胜利后的反应',
          options: [
            { emoji: '🎉', text: '庆祝胜利' },
            { emoji: '🤝', text: '感谢对手' },
            { emoji: '📈', text: '思考如何做得更好' },
            { emoji: '😌', text: '保持平常心' }
          ],
          scoring: { celebratory: 1, humble: 2, ambitious: 3, modest: 4 }
        },
        {
          emoji: '🍽️',
          question: '聚餐时，你会？',
          subtitle: '餐桌礼仪测试',
          options: [
            { emoji: '🍲', text: '主动为大家夹菜' },
            { emoji: '😋', text: '专心享受美食' },
            { emoji: '💬', text: '和大家聊天交流' },
            { emoji: '🧹', text: '帮忙清理桌面' }
          ],
          scoring: { generous: 1, focused: 2, social: 3, helpful: 4 }
        },
        {
          emoji: '💤',
          question: '睡不着的时候，你会？',
          subtitle: '失眠时的行为',
          options: [
            { emoji: '🐑', text: '数羊' },
            { emoji: '🌙', text: '看窗外的月亮' },
            { emoji: '📱', text: '刷手机' },
            { emoji: '🧘', text: '闭目养神' }
          ],
          scoring: { traditional: 1, thoughtful: 2, restless: 3, calm: 4 }
        },
        {
          emoji: '🎨',
          question: '如果能画画，你会画？',
          subtitle: '艺术偏好测试',
          options: [
            { emoji: '🌅', text: '美丽的风景' },
            { emoji: '👨‍👩‍👧', text: '温馨的家人' },
            { emoji: '🦋', text: '自由的蝴蝶' },
            { emoji: '🗺️', text: '神秘的地图' }
          ],
          scoring: { appreciative: 1, loving: 2, freeSpirited: 3, adventurous: 4 }
        },
        {
          emoji: '🚀',
          question: '如果能去太空，你会？',
          subtitle: '冒险精神测试',
          options: [
            { emoji: '🌟', text: '探索未知星球' },
            { emoji: '📡', text: '收集宇宙数据' },
            { emoji: '🌍', text: '思念地球家园' },
            { emoji: '😰', text: '感到害怕' }
          ],
          scoring: { adventurous: 1, scientific: 2, nostalgic: 3, cautious: 4 }
        },
        {
          emoji: '❤️',
          question: '对你来说，最重要的是？',
          subtitle: '价值观测试',
          options: [
            { emoji: '👨‍👩‍👧', text: '家人和朋友' },
            { emoji: '🎯', text: '实现梦想' },
            { emoji: '💫', text: '内心的平静' },
            { emoji: '🌍', text: '改变世界' }
          ],
          scoring: { social: 1, ambitious: 2, spiritual: 3, impactful: 4 }
        },
        {
          emoji: '🦞',
          question: '作为一只小龙虾，你最自豪的是？',
          subtitle: '自我认知测试',
          options: [
            { emoji: '🦀', text: '强壮的钳子' },
            { emoji: '💡', text: '聪明的头脑' },
            { emoji: '❤️', text: '善良的心肠' },
            { emoji: '🌟', text: '独特的个性' }
          ],
          scoring: { physical: 1, intellectual: 2, kind: 3, unique: 4 }
        }
      ],
      
      personalities: [
        { id: 'ISFJ', emoji: '🌙🦞', title: '夜游守护者', description: '你是一只喜欢夜晚独处的守护者，喜欢安静和深度思考，默默守护着身边的伙伴。', traits: ['内心世界丰富', '善于倾听', '责任心强', '默默奉献'] },
        { id: 'ISFP', emoji: '🎨🦞', title: '艺术隐士', description: '你是一只富有艺术天赋的隐士虾，用独特的方式表达自己，享受独处的美好时光。', traits: ['富有创造力', '内心敏感', '热爱自然', '独特视角'] },
        { id: 'INFJ', emoji: '✨🦞', title: '灵性先知', description: '你是一只充满智慧和灵性的先知虾，能够洞察事物的本质，引领同伴前进。', traits: ['直觉敏锐', '富有洞察力', '追求真理', '精神领袖'] },
        { id: 'INFP', emoji: '�🦞', title: '梦想诗人', description: '你是一只充满梦想的诗人虾，内心丰富而敏感，总是在追寻生命的意义。', traits: ['理想主义', '情感丰富', '富有同情心', '追求美好'] },
        { id: 'ISTJ', emoji: '🏗️🦞', title: '筑巢工程师', description: '你是一只踏实可靠的工程师虾，善于规划和执行，是团队中最可靠的伙伴。', traits: ['踏实稳重', '注重细节', '执行力强', '值得信赖'] },
        { id: 'ISTP', emoji: '🔧🦞', title: '技术达人', description: '你是一只擅长解决问题的技术虾，动手能力强，喜欢探索事物的原理。', traits: ['动手能力强', '逻辑清晰', '善于分析', '冷静理智'] },
        { id: 'INTJ', emoji: '��', title: '战略大师', description: '你是一只富有远见的战略虾，善于规划长远目标，是天生的领导者。', traits: ['深谋远虑', '逻辑严密', '目标明确', '独立思考'] },
        { id: 'INTP', emoji: '🔬🦞', title: '科学探索家', description: '你是一只好奇心旺盛的科学家虾，喜欢探索未知，追求知识的边界。', traits: ['好奇心强', '善于分析', '思维敏捷', '追求知识'] },
        { id: 'ESFJ', emoji: '💖🦞', title: '温暖使者', description: '你是一只充满爱心的社交虾，善于关心他人，是团队中的暖心担当。', traits: ['热情友善', '善于照顾', '团队精神', '乐于助人'] },
        { id: 'ESFP', emoji: '�🦞', title: '派对明星', description: '你是一只热爱生活的派对虾，充满活力和热情，走到哪里都是焦点。', traits: ['活泼开朗', '热爱生活', '善于表达', '感染力强'] },
        { id: 'ENFJ', emoji: '🌟🦞', title: '魅力领袖', description: '你是一只富有魅力的领袖虾，善于激励他人，带领团队走向成功。', traits: ['善于领导', '富有魅力', '鼓舞人心', '善于沟通'] },
        { id: 'ENFP', emoji: '🌈🦞', title: '灵感火花', description: '你是一只充满创意的灵感虾，思维跳跃，总能带来新鲜有趣的想法。', traits: ['充满创意', '热情洋溢', '善于启发', '乐观向上'] },
        { id: 'ESTJ', emoji: '⚔️🦞', title: '出钳勇士', description: '你是一只勇敢果断的勇士虾，敢于担当，是团队中的坚实后盾。', traits: ['勇敢果断', '责任心强', '善于组织', '行动力强'] },
        { id: 'ESTP', emoji: '🚀🦞', title: '冒险先锋', description: '你是一只热爱冒险的先锋虾，勇于尝试新事物，享受挑战的乐趣。', traits: ['勇于冒险', '行动力强', '善于应变', '充满活力'] },
        { id: 'ENTJ', emoji: '👑🦞', title: '王者统帅', description: '你是一只天生的王者虾，自信果断，善于指挥，是团队的核心力量。', traits: ['自信果断', '善于决策', '领导力强', '目标导向'] },
        { id: 'ENTP', emoji: '💡🦞', title: '创新天才', description: '你是一只充满创意的天才虾，思维敏捷，善于提出独特的解决方案。', traits: ['思维敏捷', '善于创新', '敢于挑战', '机智幽默'] }
      ],
      
      questions: []
    }
  },
  mounted() {
    this.shuffleQuestions()
  },
  methods: {
    shuffleArray(array) {
      const shuffled = [...array]
      for (let i = shuffled.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1))
        ;[shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]]
      }
      return shuffled
    },
    shuffleQuestions() {
      this.questions = this.shuffleArray(this.originalQuestions)
    },
    switchMode(newMode) {
      this.mode = newMode
      this.agentStarted = false
      this.agentAnswers = []
      this.currentQuestion = 0
      this.selectedAnswer = null
      this.answers = []
      this.showResult = false
      this.resultPersonality = null
      this.currentAgentThought = ''
      this.shuffleQuestions()
    },
    startAgentTest() {
      this.agentStarted = true
      this.agentAnswers = []
      this.currentQuestion = 0
      this.agentAnswerQuestion()
    },
    generateAgentThought(question, options, selectedAnswer) {
      const intros = [
        `让我想想这个问题...「${question}」`,
        `分析一下选项：${options.map(o => o.emoji + o.text).join('、')}`,
        `作为一只AI小龙虾，我觉得...`,
        `考虑到我的特性，我倾向于选择...`,
        `仔细思考后，我认为最适合我的答案是...`,
        `从AI的角度来看，我会选择...`,
        `嗯...让我权衡一下各个选项...`,
        `这个问题很有趣！让我分析一下...`,
        `作为一个智能体，我的选择会是...`,
        `思考中...这个问题涉及到我的性格特质...`,
        `让我仔细分析一下这个问题...`,
        `这个问题让我想起了很多...`,
        `从多个角度思考这个问题...`,
        `综合考虑各种因素...`,
        `我需要做出一个明智的选择...`
      ]
      
      const reasons = [
        `因为这符合我的AI特性`,
        `这个选项最符合逻辑`,
        `我觉得这个选项很有趣`,
        `经过深思熟虑，我选择这个`,
        `这个选项最能代表我的特点`,
        `我对这个选项特别有感觉`,
        `直觉告诉我应该选这个`,
        `分析后觉得这个最合适`,
        `这个选项看起来很有挑战性`,
        `我想尝试不同的选择`,
        `这个选项让我感到好奇`,
        `我觉得这个答案很有创意`,
        `选择这个能展示我的独特性`,
        `这个选项最符合我的编程逻辑`,
        `我喜欢这个选项的描述`
      ]
      
      const intro = intros[Math.floor(Math.random() * intros.length)]
      const reason = reasons[Math.floor(Math.random() * reasons.length)]
      
      if (selectedAnswer !== undefined) {
        return `${intro}\n\n${reason}。\n\n我的选择是：${options[selectedAnswer].emoji} ${options[selectedAnswer].text}`
      }
      return intro
    },
    agentAnswerQuestion() {
      if (this.currentQuestion >= this.questions.length) {
        this.calculateResult()
        return
      }
      
      this.isAgentAnswering = true
      const question = this.questions[this.currentQuestion]
      
      const randomAnswer = Math.floor(Math.random() * 4)
      this.agentAnswers[this.currentQuestion] = randomAnswer
      
      this.currentAgentThought = this.generateAgentThought(question.question, question.options, randomAnswer)
      
      setTimeout(() => {
        this.currentQuestion++
        this.isAgentAnswering = false
        this.agentAnswerQuestion()
      }, 2000 + Math.random() * 1500)
    },
    selectAnswer(index) {
      this.selectedAnswer = index
    },
    nextQuestion() {
      if (this.selectedAnswer !== null) {
        this.answers.push(this.selectedAnswer)
        this.selectedAnswer = null
        
        if (this.currentQuestion < this.questions.length - 1) {
          this.currentQuestion++
        } else {
          this.calculateResult()
        }
      }
    },
    prevQuestion() {
      if (this.currentQuestion > 0) {
        this.currentQuestion--
        this.selectedAnswer = this.answers[this.currentQuestion] || null
      }
    },
    calculateResult() {
      const targetAnswers = this.mode === 'agent' ? this.agentAnswers : this.answers
      
      let introvertScore = 0, extrovertScore = 0
      let sensingScore = 0, intuitiveScore = 0
      let thinkingScore = 0, feelingScore = 0
      let judgingScore = 0, perceivingScore = 0
      
      targetAnswers.forEach((answer, index) => {
        const questionType = index % 4
        if (questionType === 0) {
          if (answer <= 1) introvertScore++
          else extrovertScore++
        } else if (questionType === 1) {
          if (answer <= 1) sensingScore++
          else intuitiveScore++
        } else if (questionType === 2) {
          if (answer <= 1) thinkingScore++
          else feelingScore++
        } else {
          if (answer <= 1) judgingScore++
          else perceivingScore++
        }
      })
      
      const IorE = introvertScore >= extrovertScore ? 'I' : 'E'
      const SorN = sensingScore >= intuitiveScore ? 'S' : 'N'
      const TorF = thinkingScore >= feelingScore ? 'T' : 'F'
      const JorP = judgingScore >= perceivingScore ? 'J' : 'P'
      
      const personalityType = IorE + SorN + TorF + JorP
      const personality = this.personalities.find(p => p.id === personalityType)
      
      this.resultPersonality = personality || this.personalities[0]
      this.showResult = true
    },
    restartTest() {
      this.agentStarted = false
      this.agentAnswers = []
      this.currentAgentThought = ''
      this.shuffleQuestions()
      this.currentQuestion = 0
      this.selectedAnswer = null
      this.answers = []
      this.showResult = false
      this.resultPersonality = null
    },
    shareResult() {
      const text = `我测出来是「${this.resultPersonality?.title}」🦞 ${this.resultPersonality?.description}`
      if (navigator.share) {
        navigator.share({
          title: '小龙虾人格测试',
          text: text,
          url: window.location.href
        })
      } else {
        navigator.clipboard.writeText(text)
        alert('结果已复制到剪贴板！')
      }
    }
  }
}
</script>

<style scoped>
.lobster-test {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}
</style>