import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Dashboard from '../views/Dashboard.vue'
import Chat from '../views/Chat.vue'
import Browser from '../views/Browser.vue'
import Settings from '../views/Settings.vue'
import VoiceCall from '../views/VoiceCall.vue'
import AgentManager from '../views/AgentManager.vue'
import LobsterTest from '../views/LobsterTest.vue'
import ScheduleManager from '../views/ScheduleManager.vue'
import TableManager from '../views/TableManager.vue'
import Analytics from '../views/Analytics.vue'
import FileManager from '../views/FileManager.vue'
import Team from '../views/Team.vue'
import Monitor from '../views/Monitor.vue'
import Ecommerce from '../views/Ecommerce.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard
  },
  {
    path: '/chat',
    name: 'Chat',
    component: Chat
  },
  {
    path: '/browser',
    name: 'Browser',
    component: Browser
  },
  {
    path: '/voice-call',
    name: 'VoiceCall',
    component: VoiceCall
  },
  {
    path: '/settings',
    name: 'Settings',
    component: Settings
  },
  {
    path: '/agent-manager',
    name: 'AgentManager',
    component: AgentManager
  },
  {
    path: '/lobster-test',
    name: 'LobsterTest',
    component: LobsterTest
  },
  {
    path: '/schedule-manager',
    name: 'ScheduleManager',
    component: ScheduleManager
  },
  {
    path: '/table-manager',
    name: 'TableManager',
    component: TableManager
  },
  {
    path: '/analytics',
    name: 'Analytics',
    component: Analytics
  },
  {
    path: '/file-manager',
    name: 'FileManager',
    component: FileManager
  },
  {
    path: '/team',
    name: 'Team',
    component: Team
  },
  {
    path: '/monitor',
    name: 'Monitor',
    component: Monitor
  },
  {
    path: '/ecommerce',
    name: 'Ecommerce',
    component: Ecommerce
  }
]

const router = new VueRouter({
  mode: 'hash',
  base: '/',
  routes
})

export default router