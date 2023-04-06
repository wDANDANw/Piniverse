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
        @click="analysis_sentence"
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
const api_gateway = process.env.VUE_APP_API_SERVER_GATEWAY

// Viewport related
import { mapActions } from 'pinia'
import { useEntityStore } from "@/stores/entity";
import * as viewport from "@/stores/viewport";



//import * as querystring from "querystring";
//import { utils } from "@/utils/utils";

// CONSTANTS
//const PC_SCALE_CONST = 100 // Point cloud mesh too small. Scale x100

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

    ...mapActions(useEntityStore, ["CREATE_ENTITY", "ADD_ENTITY"]),

    clearFields(){
      this.query_str = "";
      this.output_str = "";
    },

    async analysis_sentence() {
      let temp_string = this.query_str;
      fetch("http://localhost:12333/api/parse_text_to_entities/", {
        method: "post",
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        //make sure to serialize your JSON body
        body: JSON.stringify({
          input_str: temp_string
        })
      }).then( (response) => {
        return response.json()
      }).then((json)=>{
        console.log("Response:")
        console.log(json)
        let noun_array = json.output;
        for (let i = 0; i < noun_array.length; i++) {
          this.send_query(noun_array[i].nouns[0])
        }
      })
    },

    async send_query(object) {

      this.output_str = "Generating ...";
      const resolver_api = "/api/text_to_model";
      const url = api_gateway + resolver_api;
      await axios.post(url, {query: object}).then((res) => {
        //console.log(res.data);
        viewport.useViewportStore().SHOW_LINES(res.data.geometry);
        this.output_str = "Generated the model for \"" + res.data.query + "\"" + res.data.geometry;
      });
    },
    async test() {
      this.output_str = "Generating ...";
      const resolver_api = "/api/text_to_model";
      const url = api_gateway + resolver_api;
      await axios.post(url, {query: "apple"}).then((res) => {
        console.log(res.data.geometry);
        this.output_str = "Generated the model for \"" + res.data.query + "\"" + res.data.geometry
      });
    },

    // async story_to_scene() {
    //   this.output_str = "Generating Story to Scene";
    //   const resolver_api = "/api/story_to_scene";
    //   const url = api_gateway + resolver_api;
    //   let vm = this;
    //   // let generated_geometry = null;
    //   await axios.post(url, {query: vm.query_str}).then((res) => {
    //     // vm.output_str = JSON.stringify(res.data)
    //     vm.output_str = "Generated the model for \"" + res.data.query + "\""
    //
    //     const entities = res.data.entities;
    //     const scene = res.data.scene;
    //     const events = res.data.events;
    //     const logics = res.data.logics;
    //
    //     vm.output_str += "\n\nDEBUGGING: You can check console for parsed entities, scene, events, and logics"
    //     console.log("Entities\n", entities)
    //     console.log("Scene\n", scene)
    //     console.log("Events\n", events)
    //     console.log("Logics\n", logics)
    //
    //     // Create entities out of each entity_name and entity_ontologies pair
    //     let new_entity = null;
    //     const local_entities_hash_map = {};
    //     Object.entries(entities).forEach(([e_name, e_ontos]) => {
    //       e_name = utils.toTitleCase(e_name)
    //       new_entity = this.CREATE_ENTITY({
    //         name: e_name,
    //         geometry: e_ontos.Geometry,
    //         geometry_type: "pc",
    //         scale: [100, 100, 100],
    //         position: [100, 100, 0],
    //         draggable: true,
    //         properties: e_ontos.Properties,
    //         behaviors: e_ontos.Behaviors,
    //         psychologies: e_ontos.Psychologies,
    //         is_visible: true,
    //         show_bounding_box: true,
    //       })
    //       if (new_entity === null || new_entity === undefined) {
    //         console.error("Failed to create entity " + e_name + " from params " + e_ontos)
    //         // return;
    //       } else {
    //         local_entities_hash_map[e_name] = new_entity
    //         this.ADD_ENTITY(new_entity)
    //       }
    //     })
    //
    //     // For each scene node
    //     const traverse_scene = (children_tree) => {
    //       Object.entries(children_tree).forEach( ([node_name, node_value]) => {
    //
    //         // If valid node, do some processing
    //         if (node_value["name"] !== undefined && node_value["name"] !== null) {
    //
    //           const title_case_node_name = utils.toTitleCase(node_name)
    //
    //           // If this entity is registered
    //           if (Object.keys(local_entities_hash_map).includes(title_case_node_name)) {
    //
    //             // Use Scene Info to update entity
    //
    //             // Position
    //             if (Array.isArray(node_value.world_position) && node_value.scale.length === 3) {
    //               local_entities_hash_map[title_case_node_name].set_position(
    //                   node_value.world_position[0] * PC_SCALE_CONST,
    //                   node_value.world_position[1] * PC_SCALE_CONST,
    //                   node_value.world_position[2] * PC_SCALE_CONST
    //               )
    //             }
    //
    //             // Scaling
    //             if (Array.isArray(node_value.scale) && node_value.scale.length === 3) {
    //               local_entities_hash_map[title_case_node_name].scale(
    //                   node_value.scale[0] * PC_SCALE_CONST,
    //                   node_value.scale[1] * PC_SCALE_CONST,
    //                   node_value.scale[2] * PC_SCALE_CONST
    //               )
    //             }
    //
    //             // TODO: Support relative position rather than world position
    //           }
    //
    //           // TODO: If not registered
    //           else {
    //             // console.log("not implemented")
    //           }
    //
    //           // Check if children. If so, traverse
    //           if (typeof node_value["children"] === 'object' && node_value["children"] !== null) {
    //             traverse_scene(node_value["children"])
    //           }
    //
    //         }
    //       })
    //     }
    //     // Simple Scene Handling
    //     traverse_scene({Scene: scene})
    //
    //     console.log("Succeeded task story to scene")
    //   });
    // }
  }
}
</script>

<style scoped>

</style>
