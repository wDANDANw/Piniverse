<!--<script setup>-->

<!--const store = useViewportStore();-->
<!--let axisLinesVisible = true;-->
<!--let pyramidsVisible = true;-->
<!--function togglePyramids() {-->
<!--  if (pyramidsVisible) {-->
<!--    store.HIDE_PYRAMIDS();-->
<!--    pyramidsVisible = false;-->
<!--  } else {-->
<!--    store.SHOW_PYRAMIDS();-->
<!--    pyramidsVisible = true;-->
<!--  }-->
<!--}-->
<!--function toggleAxisLines() {-->
<!--  if (axisLinesVisible) {-->
<!--    store.HIDE_AXIS_LINES();-->
<!--    axisLinesVisible = false;-->
<!--  } else {-->
<!--    store.SHOW_AXIS_LINES();-->
<!--    axisLinesVisible = true;-->
<!--  }-->
<!--}-->
<!--function resetCameraPosition() {-->
<!--  store.SET_CAMERA_POSITION(0, 0, 500);-->
<!--  store.RESET_CAMERA_ROTATION();-->
<!--}-->
<!--</script>-->

<template>

  <v-card>
    <v-card-text>

      <div class="checkbox">
        <v-checkbox
            label="axis-lines"
            v-model="axisLinesVisible"
            @click="toggleAxisLines">
        </v-checkbox>
      </div>

      <br>
      <br>
      <div class="camera">Camera Position</div>

      <div class="text">
        X: <span>{{ store.CAMERA_POSITION.x }}</span>
      </div>

      <div class="text">
        Y: <span>{{ store.CAMERA_POSITION.y }}</span>
      </div>

      <div class="text">
        Z: <span>{{ store.CAMERA_POSITION.z }}</span>
      </div>

      <br>

      <div class="buttons">
        <v-btn
            @click="resetCameraPosition"
        >
          Reset Camera
        </v-btn>
      </div>

      <v-container class="icons">
        <v-row>
          <v-col>
            <v-btn
                href="https://github.com/SRLabs/Vue-Three-Demo"
                target="_blank"
                class="links"
                icon>
              <v-icon>
                mdi-github
              </v-icon>
            </v-btn>
          </v-col>
          <v-col>
            <v-btn
                href="https://threejs.org/examples/?q=controls#misc_controls_trackball"
                target="_blank"
                class="links"
                icon>
              <v-icon>
                mdi-backup-restore
              </v-icon>
            </v-btn>
          </v-col>
        </v-row>
      </v-container>

    </v-card-text>
  </v-card>
</template>

<script>
import * as viewport from "@/stores/viewport";
export default {
  name: 'ControlPanel',
  data() {
    return {
      store: viewport.useViewportStore(),
      axisLinesVisible: true
    }
  },
  methods: {
    toggleAxisLines() {
      if (this.axisLinesVisible) {
        this.store.HIDE_AXIS_LINES();
        this.axisLinesVisible = false;
      } else {
        this.store.SHOW_AXIS_LINES();
        this.axisLinesVisible = true;
      }
    },
    resetCameraPosition() {
      this.store.SET_CAMERA_POSITION(0, 0, 500);
      this.store.RESET_CAMERA_ROTATION();
    }
  }
}
</script>

<style>
.checkbox{
  margin-top: -1rem;
  margin-bottom: -3rem;
  color: #7b34e6;
}

.text{
  text-align: left;
  font-size: 15px;
  margin-top: 8px;
}

.camera{
  font-size: 20px;
  /*margin-top: 1.5rem;*/
}

.buttons{
  font-size: 16px;
  /*margin-top: 1rem;*/
  /*margin-bottom: -1rem;*/
}

.links{
  /*margin-top: 1.5rem;*/
  text-align: center;
}

.icons{

}
</style>
