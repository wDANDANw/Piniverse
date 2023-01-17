
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
          ></v-textarea>
          <v-btn
              block
              elevation="2"
              outlined
              rounded
              class="mt-5"
          >Generate
          </v-btn>
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
import { vue3dLoader } from "vue-3d-loader";
</script>

<script>

 export default {

   name: 'App',
   data() {
     return {
       filePath: ['model/teat.dae'],
       files: [],
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

     }
   }
 }
</script>
