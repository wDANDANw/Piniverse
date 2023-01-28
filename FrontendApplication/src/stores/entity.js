// Entity store

import { defineStore } from "pinia";

import { useViewportStore } from "@/stores/viewport";

export class Entity {

    constructor({name="default_name", obj_ref=null}) {

        // Static Semantics
        this.name = name;
        this.ontologies = {}; // Entity Ontology / Adjs

        // Dynamic Semantics
        // this.behaviors = {};

        // Renderer Related
        this.is_visible = true;
        this.obj_ref = obj_ref; // Renderable object in the scene
        this.is_draggable = false;
        this.show_bounding_box = true;
        this.bounding_box_ref = null;
        this.scale = [1, 1, 1]
        this.position = [1, 1, 1]
    }

}

export const useEntityStore = defineStore("entity_store", {
    state: () => {
        return {
            entities: [],
        }
    },
    getters: {
        ENTITIES: (state) => {
            return state.entities
        },
    },
    actions: {
        ADD_ENTITY(entity) {
            const store = useViewportStore()
            this.entities.push(entity)
            if (entity.is_visible) {
                store.ADD_TO_SCENE(entity)
            }
            if (entity.is_draggable) {
                store.ADD_TO_DRAGGABLE(entity)
            }
            if (entity.show_bounding_box) {
                store.ADD_BOUNDING_BOX(entity)
            }
        },
        REMOVE_ENTITY(entity) {
            this.entities.remove(entity)
        },
    }

})
