import { createApp } from 'vue';//创建 Vue 应用实例
import App from './App.vue'; //应用的入口组件。
import router from './router'; //管理应用的路由配置和导航行为
import piniaStore from './store'; //管理应用的全局状态。

import bootstrap from './core/bootstrap';
import '/@/styles/reset.less';
import '/@/styles/index.less';
import Antd from 'ant-design-vue';//在应用中使用 Ant Design Vue 组件库

const app = createApp(App);//函数创建一个 Vue 应用实例，并将根组件 App 传递给它。

app.use(Antd);
app.use(router);//注册路由实例
app.use(piniaStore);
app.use(bootstrap)
app.mount('#app');// Vue 应用实例挂载到 HTML 中的 #app 元素上，启动应用。
