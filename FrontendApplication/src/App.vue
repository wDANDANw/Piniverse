<template>
  <v-app id="inspire">
    <v-navigation-drawer
        v-model="drawer"
        app
    >
      <!--  -->
      <v-btn
          block
          elevation="2"
          outlined
          rounded
      >Primary Page</v-btn>
    </v-navigation-drawer>

    <v-app-bar app>
      <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>

      <v-toolbar-title>Game Creation Engine</v-toolbar-title>
    </v-app-bar>

    <v-main>
      <v-container fluid>
        <v-row>
          <v-col
              cols="12"
              md="6"
          >
            <v-textarea
                name="input-7-1"
                label="Input"
                v-model="input_str"
            ></v-textarea>
          </v-col>
          <v-col
              cols="12"
              md="6"
          >
            <v-btn
                class="ma-lg-2"
                block
                elevation="2"
                outlined
                rounded
                @click="demo_generate"
            >Generate</v-btn>
            <v-btn
                class="ma-lg-2"
                block
                elevation="2"
                outlined
                rounded
            >Clear</v-btn>
          </v-col>
          <v-col
              cols="12"
              md="6"
          >
            {/* Should this be textarea?? */}
            {{output_str}}
            <v-textarea 
                filled
                name="input-7-4"
                label="Output"
                v-model="output_str"
            >{{output_str}}</v-textarea>
          </v-col>
          <v-col
              cols="12"
              md="6"
          >

          </v-col>
        </v-row>
      </v-container>
      <!--  -->
    </v-main>
  </v-app>
</template>

<script>

import axios from "axios"
const api_gateway = 'http://localhost:3000' // Hardcoded, should use EnvironmentPlugin(['API_GATEWAY'])

export default {
  data: () => ({ 
    drawer: null,
    input_str: "",
    output_str: ""
  }),
  methods: {
    async demo_generate() {
      this.output_str = "Generating ..."
      const resolver_api = "/api/resolve_entity" 
      const url = api_gateway + resolver_api
      let vm = this
      await axios.post(url, {input_str: vm.input_str}).then((res) => vm.output_str = JSON.stringify(res.data))
    }
  }
}
</script>