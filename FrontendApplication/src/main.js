import {createApp} from "vue";
import App from './App.vue'
import vuetify from './plugins/vuetify'
import { loadFonts } from './plugins/webfontloader'
import { TroisJSVuePlugin } from 'troisjs';

loadFonts()

createApp(App)
  .use(vuetify, TroisJSVuePlugin)
  .mount('#app')
