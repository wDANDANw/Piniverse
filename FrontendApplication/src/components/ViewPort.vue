<script setup>
import {ref, onMounted} from "vue";
import { useViewportStore } from "@/stores/viewport";
let height = 0;
let width = 0;
const store = useViewportStore();
const viewport = ref(null);
const { INIT, ANIMATE, RESIZE } = store;
onMounted(() => {
  // height = viewport.value.offsetHeight;
  height = 500; // TODO: Placeholder
  width = viewport.value.offsetWidth;

store.SHOW_LINES();
  INIT(width, height, viewport.value).then(() => {
    ANIMATE();
    window.addEventListener(
        "resize",
        () => {
          RESIZE(viewport.value.offsetWidth, viewport.value.offsetHeight);
        },
        true
    );
  });
});
</script>

<template>
  <div class="viewport" ref="viewport"></div>
</template>

