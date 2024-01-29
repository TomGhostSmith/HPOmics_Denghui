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

const app = createApp(App)
// installElementPlus(app)
for (let i in Icons)
{
    app.component(i, Icons[i])
}
app.use(ElementPlus)
app.use(store).use(router).mount('#app')
// app.use(store).use(router).use(router).mount('#app')