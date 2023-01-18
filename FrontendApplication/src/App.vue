
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

          <v-file-input
              label="Manual Upload Model Files"
              type="file"
              id="file"
              ref="myFiles"
              class="custom-file-input"
              accept=".obj"
              @change="previewFiles"
              multiple="true"
          ></v-file-input>
        </v-col>

      </v-container>
<!--      This is the 3D model viewer-->
<!--          Support: obj, dae, json...-->
<!--          Left mouse to rotate-->
<!--          Right mouse to move-->
<!--          Scroll to zoom in/out-->
      <vue3dLoader
          id="viewer"
          ref="myViewer"
          :filePath="filePath"
          :cameraPosition="{ x: 1, y: -5, z: -20 }"
          :height="350"
      />
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
