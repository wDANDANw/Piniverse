
<template>
  <v-app id="inspire" align="center" style="background: #EACECE">
    <v-main>
<!--      align="center" style="background: #CCFFFF" cols="11"-->
    <v-col md="11">
<!--      Top of the page-->
      <v-col align="center" style="background: #E6E6FA" class="rounded-xl mb-4">
        <v-toolbar-title style="font-size: 30px; font-family: 'Comic Sans MS',serif">Game Creation Engine</v-toolbar-title>
      </v-col>

      <v-row class="pa-4">
<!--        Left side of the page-->
        <ParameterPanel></ParameterPanel>
<!--        Right side of the page-->
        <v-col style="background: #E6E6FA" class="rounded-xl ml-2">
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
          <viewport class="view">

          </viewport>
            <div class="options" align="right">
              <v-menu
                  v-model="menu"
                  :close-on-content-click="false"
                  location="end"
                  align="center">
                <template v-slot:activator="{ props }">
                  <v-btn
                      color="indigo"
                      v-bind="props"
                      icon
                  >
                    <v-icon>
                      mdi-cog
                    </v-icon>

                  </v-btn>
                </template>
                    <panel></panel>
              </v-menu>
            </div>
<!--          TODO: DO NOT DELETE THE FOLLOWING COMMENTS!!!!-->
<!--          <v-expansion-panels>-->
<!--            <v-expansion-panel>-->
<!--              <v-expansion-panel-title>-->
<!--                Options-->
<!--              </v-expansion-panel-title>-->
<!--              <v-expansion-panel-text>-->
<!--                <panel></panel>-->
<!--              </v-expansion-panel-text>-->
<!--            </v-expansion-panel>-->
<!--          </v-expansion-panels>-->

        </v-col>

      </v-row>


    </v-col>
    </v-main>
  </v-app>




</template>



<script>

import viewPort from "@/components/ViewPort.vue";
import controlPanel from "@/components/ControlPanel.vue";
import ParameterPanel from "@/components/ParameterPanel";

 export default {

   name: 'App',
   components: {
     viewport: viewPort,
     ParameterPanel,
     panel: controlPanel,
   },
   data() {
     return {
       filePath: ['model/test.dae'],
       files: [],
       dialog: false,
       fav: true,
       menu: false,
       message: false,
       hints: true,
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

.options{
  margin-top: -5rem;
  margin-right: 0.5rem;
}

.view{
  margin-bottom: 2rem;
}
</style>

<!--          <vue3dLoader-->
<!--              backgroundAlpha="0.3"-->
<!--              id="viewer"-->
<!--              ref="myViewer"-->
<!--              :filePath="filePath"-->
<!--              :cameraPosition="{ x: 1, y: -5, z: -20 }"-->
<!--              :height="350"-->
<!--          />-->