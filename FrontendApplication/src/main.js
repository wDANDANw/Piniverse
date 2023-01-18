import {createApp} from "vue";
import App from './App.vue'
import vuetify from './plugins/vuetify'
import { loadFonts } from './plugins/webfontloader'
import vue3dLoader from 'vue-3d-loader';

loadFonts()

createApp(App)
  .use(vuetify, vue3dLoader)
  .mount('#app')
