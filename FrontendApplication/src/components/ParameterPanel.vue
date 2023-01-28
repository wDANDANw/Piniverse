<template>
  <v-col style="background: #E6E6FA" class="rounded-xl mr-2">
    <v-toolbar-title style="font-size: 20px; font-family: 'Comic Sans MS',serif">Parameters</v-toolbar-title>
    <v-textarea
        name="input"
        label="Input"
        v-model="query_str"
        style="font-family: 'Comic Sans MS', serif"
    ></v-textarea>
    <v-btn
        block
        elevation="2"
        outlined
        rounded
        class="mt-5"
        @click="send_query"
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
</template>

<script>
import axios from "axios";
const api_gateway = 'http://localhost:12333' // Hardcoded, should use EnvironmentPlugin(['API_GATEWAY'])

// Viewport related
import { mapActions } from 'pinia'
import { useViewportStore } from "@/stores/viewport";

// Options API
export default {
  name: "ParameterPanel",
  data(){
    return{
      query_str: "",
      output_str: "",
    }
  },
  methods:{

    ...mapActions(useViewportStore, ["ADD_OBJECT_PC"]),

    clearFields(){
      this.query_str = "";
      this.output_str = "";
    },

    async send_query() {
      this.output_str = "Generating ...";
      const resolver_api = "/api/text_to_model";
      const url = api_gateway + resolver_api;
      let vm = this;
      // let generated_geometry = null;
      await axios.post(url, {query: vm.query_str}).then((res) => {
        // vm.output_str = JSON.stringify(res.data)
        vm.output_str = "Generated the model for \"" + res.data.query + "\""
        this.ADD_OBJECT_PC("test_model_name", JSON.parse(res.data.geometry))
      });


    }
  }
}
</script>

<style scoped>

</style>
