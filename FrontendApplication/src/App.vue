
<template>
  <v-app id="inspire">
    <v-app-bar app>
      <v-toolbar-title>Game Creation Engine</v-toolbar-title>
    </v-app-bar>

    <v-main>
      <v-container fluid>
        <v-col
            cols="12"
            md="6"
            class="">
          <v-textarea
              name="input-7-1"
              label="Input"
              v-model="input_str"
          ></v-textarea>
          <v-btn
              block
              elevation="2"
              outlined
              rounded
              class="mt-5"
              @click="demo_generate"
          >Generate
          </v-btn>
          {{"TODO: Make this output prettier"}}
          <h3 > Output: {{output_str}} </h3>
          <v-btn
              block
              elevation="2"
              outlined
              rounded
              class="mt-5"
          >Clear
          </v-btn>
          <v-btn
              block
              elevation="2"
              outlined
              rounded
              class="mt-5"
              @click="previewFiles"
              type="file" id="file" ref="myFiles" accept=".obj"
          >Select Model File

          </v-btn>
          <input type="file" id="file" ref="myFiles" class="custom-file-input" accept=".obj"
                 @change="previewFiles" multiple>
        </v-col>
        <v-col
            cols="12"
            md="6"
        >
        </v-col>

      </v-container>
      <v-container>
        <viewport></viewport>
        <panel></panel>
      </v-container>

    </v-main>
  </v-app>

</template>

<script>
import axios from "axios"
const api_gateway = 'http://localhost:3000' // Hardcoded, should use EnvironmentPlugin(['API_GATEWAY'])

import viewPort from "@/components/ViewPort.vue";
import controlPanel from "@/components/ControlPanel.vue";

 export default {

   name: 'App',
   components: {
     viewport: viewPort,
     panel: controlPanel,
   },
   data() {
     return {
       filePath: ['model/teat.dae'],
       files: [],
       input_str: "",
       output_str: ""
     }
   },
   methods: {
     previewFiles() {
       console.log(this.filePath)
       this.files = this.$refs.myFiles.files;
       let temp = '';
       for (const file of this.files) {
         temp += `${file.name}`;
         temp = 'model/' + temp;
         this.filePath = [temp];
         console.log(this.filePath)
       }
     },

    async demo_generate() {
      this.output_str = "Generating ..."
      const resolver_api = "/api/resolve_ner"
      const url = api_gateway + resolver_api
      let vm = this
      await axios.post(url, {input_str: vm.input_str}).then((res) => vm.output_str = JSON.stringify(res.data))
    }
  }
 }
</script>

<style scoped>
html,
body {
  width: 100%;
  height: 100%;
  overflow: hidden;
}
body {
  margin: 0px;
}
canvas {
  position: relative;
}
#app {
  height: 100%;
}
</style>
