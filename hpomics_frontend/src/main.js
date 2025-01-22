import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
// import './plugins/element.js'
// import installElementPlus from './plugins/element'
import ElementPlus from "element-plus"
import "element-plus/dist/index.css"
import 'element-plus/theme-chalk/index.css'
import * as Icons from '@element-plus/icons-vue'

const axios = require('axios')
axios.default.baseURL = '/api'
const app = createApp(App)
// installElementPlus(app)
for (let i in Icons)
{
    app.component(i, Icons[i])
}
app.use(ElementPlus)
app.use(store).use(router).mount('#app')
app.config.globalProperties.$axios = axios
// app.config.globalProperties.$backend = 'http://localhost:8081'
app.config.globalProperties.$backend = 'http://10.117.51.125:8081'
// app.use(store).use(router).use(router).mount('#app')
