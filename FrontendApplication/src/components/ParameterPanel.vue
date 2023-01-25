<template>
  <v-col style="background: #E6E6FA" class="rounded-xl mr-2">
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
</template>

<script>
import axios from "axios";
const api_gateway = 'http://localhost:3000' // Hardcoded, should use EnvironmentPlugin(['API_GATEWAY'])


export default {
  name: "ParameterPanel",
  data(){
    return{
      input_str: "",
      output_str: "",
    }
  },
  methods:{
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

<style scoped>

</style>