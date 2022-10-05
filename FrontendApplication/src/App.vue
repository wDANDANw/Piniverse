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
            <v-textarea
                filled
                name="input-7-4"
                label="Output"
            ></v-textarea>
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
export default {
  data: () => ({ drawer: null }),
}
</script>