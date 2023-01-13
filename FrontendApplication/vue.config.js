const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,

  pluginOptions: {
    vuetify: {
			// https://github.com/vuetifyjs/vuetify-loader/tree/next/packages/vuetify-loader
		},
  },

  // References: 1: Invalid Host header => https://stackoverflow.com/questions/51084089/vuejs-app-showing-invalid-host-header-error-loop
  // 2: Webpack new api: https://www.cnblogs.com/byx1024/p/16777744.html
  devServer: {
    allowedHosts: 'all'
  }

})
