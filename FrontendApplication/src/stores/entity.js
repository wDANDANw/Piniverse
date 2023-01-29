// Entity store

import { defineStore } from "pinia";
import { markRaw } from "vue";

import { useViewportStore } from "@/stores/viewport";

export class Entity {

    constructor (
        {
            name="default_name",
            obj_ref=null,
            properties = {},
            behaviors = {},
            psychologies = {},
            scale=[1, 1, 1],
            position=[0, 0, 0],
            draggable = false,
            is_visible = true,
            show_bounding_box=true,
        }) {

        // Static Semantics
        this.name = name;
        this.properties = properties;
        this.behaviors = behaviors;
        this.psychologies = psychologies;

        // Dynamic Semantics
        // this.behaviors = {};

        // Renderer Related
        this.is_visible = is_visible;

        if (this.obj_ref === null) {
            console.error("Must provide valid object reference when constructing the new entity " + name)
            return
        }

        this.obj_ref = obj_ref; // three js object in the scene
        this.obj_ref.geometry.computeBoundingBox();
        this.obj_ref.geometry.center();

        this.obj_ref.position.set(position[0], position[1], position[2])
        this.obj_ref.scale.set(scale[0], scale[1], scale[2])

        this.is_draggable = draggable;
        this.show_bounding_box = show_bounding_box;
        this.bounding_box_ref = null;

    }

    scale(x, y, z) {
        this.obj_ref.scale.set(x, y, z)
    }

    get_scale() {
        return this.obj_ref.scale
    }

    set_position(x, y, z) {
        this.obj_ref.position.set(x, y, z)
    }

    get_position() {
        return this.obj_ref.position
    }

    update_bounding_box() {
        this.bounding_box_ref.update()
    }

// TODO: Add getters and setters for 3D mesh, like position, rotation, etc. thru entity class
// TODO: Convert to getters & setters of property pattern (wrapper func)
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
        // Method to create a new entity from
        CREATE_ENTITY(
            {
                name,
                geometry,
                geometry_type="default_geometry_type",
                scale=[1, 1, 1],
                position=[0, 0, 0],
                draggable = false,
                properties = {},
                behaviors = {},
                psychologies = {},
                is_visible = true,
                show_bounding_box=true,
            }){

            const viewport_store = useViewportStore()

            let obj_ref;
            switch ( geometry_type ) {
                case "pc":
                    obj_ref = viewport_store.CREATE_PC_OBJECT(name, geometry)
                    break;
                default:
                    console.error("Got " + geometry_type + " in entity_store.CREATE_ENTITY. Type not supported. Check your params")
                    return null
            }

            // Create a New Entity
            return new Entity( {
                name: name,
                obj_ref: obj_ref,
                properties: properties,
                behaviors: behaviors,
                psychologies: psychologies,
                scale: scale,
                position: position,
                draggable: draggable,
                is_visible: is_visible,
                show_bounding_box: show_bounding_box,
            })
        },
        ADD_ENTITY(entity) {
            entity = markRaw(entity)
            const viewport_store = useViewportStore()
            this.entities.push(entity)
            if (entity.is_visible) {
                viewport_store.ADD_TO_SCENE(entity)
            }
            if (entity.is_draggable) {
                viewport_store.ADD_TO_DRAGGABLE(entity)
            }
            if (entity.show_bounding_box) {
                viewport_store.ADD_BOUNDING_BOX(entity)
            }
        },
        REMOVE_ENTITY(entity) {
            console.log("Not implemented: Remove entities in entity store for " + entity.name)
            // this.entities.remove(entity)
        }
    }

})

