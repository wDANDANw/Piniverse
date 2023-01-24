
<template>
  <v-app id="inspire" align="center" style="background: #FFCCCC">
    <v-main>
<!--      align="center" style="background: #CCFFFF" cols="11"-->
    <v-col md="11">
<!--      Top of the page-->
      <v-col align="center" style="background: #CCFFFF" class="rounded-xl mb-4">
        <v-toolbar-title style="font-size: 30px; font-family: 'Comic Sans MS',serif">Game Creation Engine</v-toolbar-title>
      </v-col>

      <v-row class="pa-4">
<!--        Left side of the page-->
        <v-col style="background: #CCFFFF" class="rounded-xl mr-2">
          <v-toolbar-title style="font-size: 20px; font-family: 'Comic Sans MS',serif">Parameters</v-toolbar-title>
          <v-textarea
              name="input"
              label="Input"
              v-model="input_str"
              style="font-family: 'Comic Sans MS', serif"
          ></v-textarea>
          <v-btn
              block
              elevation="2"
              outlined
              rounded
              class="mt-5"
              @click="demo_generate"
              style="font-family: 'Comic Sans MS', serif"
          >Generate
          </v-btn>
          <v-btn
              block
              elevation="2"
              outlined
              rounded
              class="mt-5"
              style="font-family: 'Comic Sans MS', serif"
              @click="clearFields"
          >Clear
          </v-btn>
          <v-textarea
              ref = "OutputBox"
              name="output"
              v-model="output_str"
              class="mt-5"
              readonly
              style="font-family: 'Comic Sans MS', serif"
          ></v-textarea>
        </v-col>
<!--        Right side of the page-->
        <v-col style="background: #CCFFFF" class="rounded-xl ml-2">
          <v-toolbar-title style="font-size: 20px; font-family: 'Comic Sans MS',serif">3D Viewer</v-toolbar-title>
          <v-file-input
              label="Manual Upload Model Files"
              type="file"
              id="file"
              ref="myFiles"
              class="custom-file-input mt-4 mr-4"
              accept=".obj"
              @change="previewFiles"
              multiple="true"
              style="font-family: 'Comic Sans MS', serif"
          ></v-file-input>
          <vue3dLoader
              backgroundAlpha="0.3"
              id="viewer"
              ref="myViewer"
              :filePath="filePath"
              :cameraPosition="{ x: 1, y: -5, z: -20 }"
              :height="350"
          />
        </v-col>
      </v-row>
    </v-col>
    </v-main>
  </v-app>

</template>


<script setup>
import {vue3dLoader} from "vue-3d-loader";

</script>

<script>
import axios from "axios"
const api_gateway = 'http://localhost:3000' // Hardcoded, should use EnvironmentPlugin(['API_GATEWAY'])

 export default {

   name: 'App',
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
     clearFields(){
       this.input_str = "";
       this.output_str = "";
     },

    async demo_generate() {
      this.output_str = "Generating ...";
      const resolver_api = "/api/resolve_ner";
      const url = api_gateway + resolver_api;
      let vm = this;
      await axios.post(url, {input_str: vm.input_str}).then((res) => vm.output_str = JSON.stringify(res.data));
    }
  }
 }
</script>
