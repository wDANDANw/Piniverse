import { markRaw } from "vue";
import { defineStore } from "pinia";
import { OrbitControls } from "three/addons/controls/OrbitControls";
import { DragControls } from "@/stores/custom_modules/DragControls";
import { TransformControls } from "@/stores/custom_modules/TransformControls";
import {
    AmbientLight ,
    BufferGeometry ,
    Color ,
    // CylinderGeometry,
    DirectionalLight ,
    FogExp2 ,
    Line ,
    LineBasicMaterial,
    // Mesh,
    // MeshPhongMaterial,
    PerspectiveCamera ,
    Scene ,
    Vector3 ,
    WebGLRenderer ,
} from "three";

// Point Cloud Related
import {
    Points,
    PointsMaterial,
    // BufferAttribute,
    Float32BufferAttribute,
} from "three";

// Debug related
import Stats from 'three/addons/libs/stats.module.js';
import {
    BoxHelper,
    Mesh,
    BoxGeometry,
    SphereGeometry,
    MeshStandardMaterial
    // MeshNormalMaterial,
    // MeshBasicMaterial,
} from "three";
const DEBUG = true

// Entity Related
import { Entity, useEntityStore } from "@/stores/entity";


// TODO: Reorganize the order of functions
export const useViewportStore = defineStore("scene", {
    state: () => {
        return {
            width: 0,
            height: 0,
            camera: null,
            active_control: null,
            controls: {
                c_cam: null,
                c_drag: null,
                c_trans: null,
            },
            scene: null,
            renderer: null,
            axisLines: [],
            point_size: 10,
            movable_objects: markRaw([]),
            bounding_boxes: markRaw({}),
            entities: markRaw([]),
            stats: null,
        };
    },
    getters: {
        CAMERA_POSITION: (state) => {
            return state.camera ? state.camera.position : null;
        },
        SCENE: (state) => {
            return state.scene
        }
    },
    actions: {
        SET_VIEWPORT_SIZE(width, height) {
            this.width = width;
            this.height = height;
        },
        INITIALIZE_RENDERER(el) {
            const renderer = new WebGLRenderer({ antialias: true });
            renderer.setPixelRatio(window.devicePixelRatio);
            renderer.setSize(this.width, this.height);
            el.appendChild(renderer.domElement);

            this.renderer = markRaw(renderer);

            if (DEBUG) {
                const container = document.createElement( 'div' );
                el.appendChild( container );

                this.stats = new Stats();
                container.appendChild( this.stats.dom );
            }

        },
        INITIALIZE_CAMERA() {
            const camera = new PerspectiveCamera(
                // 1. Field of View (degrees)
                60,
                // 2. Aspect ratio
                this.width / this.height,
                // 3. Near clipping plane
                1,
                // 4. Far clipping plane
                3000
            );
            camera.position.z = 500;

            this.camera = camera;
        },
        INITIALIZE_CONTROLS() {

            // Multiple Controls Example
            // Reference: https://sbcode.net/threejs/multi-controls-example/

            // Camera Controls
            const camera_control = new OrbitControls(
                this.camera,
                this.renderer.domElement
            );
            camera_control.rotateSpeed = 1.0;
            camera_control.zoomSpeed = 1.2;
            camera_control.panSpeed = 0.8;
            camera_control.noZoom = false;
            camera_control.noPan = false;
            camera_control.staticMoving = true;
            camera_control.dynamicDampingFactor = 0.3;
            camera_control.keys = [65, 83, 68];

            this.controls.c_cam = markRaw(camera_control);
            this.active_control = camera_control;

            // Drag Control
            const drag_controls = new DragControls(this.movable_objects, this.camera, this.renderer.domElement)
            drag_controls.addEventListener('dragstart', function (event) {
                event.object.material.opacity = 0.33
            })
            drag_controls.addEventListener('dragend', function (event) {
                event.object.material.opacity = 1
            })
            drag_controls.enabled = false; // Default to disabled

            this.controls.c_drag = markRaw(drag_controls);

            // Transform Controls
            const transform_controls = new TransformControls(this.movable_objects, this.camera, this.renderer.domElement)
            this.controls.c_trans = markRaw(transform_controls);
            transform_controls.enabled = false;

            // Fly Controls
            // TODO: Add fly controls funcs

            // Control Switches
            // TODO: Switch window to vue element
            // TODO: Generate controls on the fly
            // TODO: Refactor to generate the controls on the fly (based on conditions) and remove them
            //  once switches mode so the controls wouldn't watch listeners all the time
            window.addEventListener("keydown", event => {
                switch ( event.key.toLowerCase() ) {
                    case 'd':
                        if (this.active_control === drag_controls) {
                            this.active_control.enabled = false;
                            camera_control.enabled = true;
                            this.active_control = camera_control;
                        } else {
                            this.active_control.enabled = false;
                            drag_controls.enabled = true;
                            this.active_control = drag_controls;
                        }
                        if (DEBUG) console.log("Drag Control set to" + drag_controls.enabled)
                        break;
                    case 'w':
                        if (this.active_control === transform_controls) {
                            if (transform_controls.getMode() === "translate") {
                                this.active_control.enabled = false;
                                camera_control.enabled = true;
                                this.active_control = camera_control;
                                this.scene.remove(transform_controls)
                            } else {
                                this.active_control.setMode("translate")
                            }
                        } else {
                            this.active_control.enabled = false;
                            transform_controls.enabled = true;
                            transform_controls.setMode("translate");
                            this.active_control = transform_controls;
                            this.scene.add(transform_controls)
                        }
                        if (DEBUG) {
                            console.log("Translate Control Enabled: " + transform_controls.enabled)
                            console.log("Translate Control Latest Mode: " + transform_controls.getMode())
                        }
                        break;
                    case 'e':
                        if (this.active_control === transform_controls) {
                            if (transform_controls.getMode() === "rotate") {
                                this.active_control.enabled = false;
                                camera_control.enabled = true;
                                this.active_control = camera_control;
                                this.scene.remove(transform_controls)
                            } else {
                                this.active_control.setMode("rotate")
                            }
                        } else {
                            this.active_control.enabled = false;
                            transform_controls.enabled = true;
                            transform_controls.setMode("rotate");
                            this.active_control = transform_controls;
                            this.scene.add(transform_controls)
                        }
                        if (DEBUG) {
                            console.log("Translate Control Enabled: " + transform_controls.enabled)
                            console.log("Translate Control Latest Mode: " + transform_controls.getMode())
                        }
                        break;
                    case 'r':
                        if (this.active_control === transform_controls) {
                            if (transform_controls.getMode() === "scale") {
                                this.active_control.enabled = false;
                                camera_control.enabled = true;
                                this.active_control = camera_control;
                                this.scene.remove(transform_controls)
                            } else {
                                this.active_control.setMode("scale")
                            }
                        } else {
                            this.active_control.enabled = false;
                            transform_controls.enabled = true;
                            transform_controls.setMode("scale");
                            this.active_control = transform_controls;
                            this.scene.add(transform_controls)
                        }
                        if (DEBUG) {
                            console.log("Translate Control Enabled: " + transform_controls.enabled)
                            console.log("Translate Control Latest Mode: " + transform_controls.getMode())
                        }
                        break;

                }
            })

        },
        DISABLE_ALL_CONTROLS(exception=null) {
            for (const ctrl in this.controls) {
                if (ctrl !== exception)
                    ctrl.enabled = false;
            }
        },
        UPDATE_CONTROLS() {
            for (const ctrl in this.controls) {
                ctrl.update();
            }
        },
        INITIALIZE_SCENE() {
            const scene = new Scene();
            scene.background = markRaw(new Color(0xcccccc));
            scene.fog = markRaw(new FogExp2(0xcccccc, 0.002));

            // // Pyramids
            // this.pyramids = [];
            // var pyramidGeometry = new CylinderGeometry(0, 10, 30, 4, 1);
            // var pyramidMaterial = new MeshPhongMaterial({
            //     color: 0xffffff,
            //     flatShading: true,
            // });
            // for (var i = 0; i < 500; i++) {
            //     var mesh = new Mesh(pyramidGeometry, pyramidMaterial);
            //     mesh.position.x = (Math.random() - 0.5) * 1000;
            //     mesh.position.y = (Math.random() - 0.5) * 1000;
            //     mesh.position.z = (Math.random() - 0.5) * 1000;
            //     mesh.updateMatrix();
            //     mesh.matrixAutoUpdate = false;
            //     this.pyramids.push(markRaw(mesh));
            // }
            // // scene.add(...this.pyramids); // Do not show pyramids at the beginning

            // lights
            var lightA = new DirectionalLight(0xffffff);
            lightA.position.set(1, 1, 1);
            scene.add(markRaw(lightA));
            var lightB = new DirectionalLight(0x002288);
            lightB.position.set(-1, -1, -1);
            scene.add(markRaw(lightB));
            var lightC = new AmbientLight(0x222222);
            scene.add(markRaw(lightC));

            // Axis Line 1
            const axisLine1Material = new LineBasicMaterial({ color: 0x0000ff });
            const axisLine1Points = [];
            axisLine1Points.push(new Vector3(0, 0, 0));
            axisLine1Points.push(new Vector3(0, 1000, 0));
            let axisLine1Geometry = new BufferGeometry().setFromPoints(
                axisLine1Points
            );
            let axisLine1 = new Line(axisLine1Geometry, axisLine1Material);
            this.axisLines.push(markRaw(axisLine1));

            // Axis Line 2
            const axisLine2Material = new LineBasicMaterial({ color: 0x00ff00 });
            const axisLine2Points = [];
            axisLine2Points.push(new Vector3(0, 0, 0));
            axisLine2Points.push(new Vector3(1000, 0, 0));
            let axisLine2Geometry = new BufferGeometry().setFromPoints(
                axisLine2Points
            );
            let axisLine2 = new Line(axisLine2Geometry, axisLine2Material);
            this.axisLines.push(markRaw(axisLine2));

            // Axis 3
            const axisLine3Material = new LineBasicMaterial({ color: 0xff0000 });
            const axisLine3Points = [];
            axisLine3Points.push(new Vector3(0, 0, 0));
            axisLine3Points.push(new Vector3(0, 0, 1000));
            let axisLine3Geometry = new BufferGeometry().setFromPoints(
                axisLine3Points
            );
            let axisLine3 = new Line(axisLine3Geometry, axisLine3Material);
            this.axisLines.push(markRaw(axisLine3));

            scene.add(...this.axisLines);
            this.scene = markRaw(scene);
        },
        RESIZE(width, height) {
            this.width = width;
            this.height = height;
            this.camera.aspect = width / height;
            this.camera.updateProjectionMatrix();
            this.renderer.setSize(width, height);
            this.controls.c_cam.handleResize();
            this.RENDER();
        },
        SET_CAMERA_POSITION(x, y, z) {
            if (this.camera) {
                this.camera.position.set(x, y, z);
            }
        },
        RESET_CAMERA_ROTATION() {
            if (this.camera) {
                this.camera.rotation.set(0, 0, 0);
                this.camera.quaternion.set(0, 0, 0, 1);
                this.camera.up.set(0, 1, 0);
                this.controls.c_cam.target.set(0, 0, 0);
            }
        },
        HIDE_AXIS_LINES() {
            this.scene.remove(...this.axisLines);
            this.RENDER();
        },
        SHOW_AXIS_LINES() {
            this.scene.add(...this.axisLines);
            this.RENDER();
        },
        // HIDE_PYRAMIDS() {
        //     this.scene.remove(...this.pyramids);
        //     this.RENDER();
        // },
        // SHOW_PYRAMIDS() {
        //     this.scene.add(...this.pyramids);
        //     this.RENDER();
        // },
        INITIALIZE_DEBUG_SCENE() {
            // Debug Cube
            const c_geometry = new BoxGeometry()
            const c_material = new MeshStandardMaterial({ transparent: true, color:"pink" })
            const cube = new Mesh(c_geometry, c_material)

            const c_debug_entity = new Entity( {
                name: "cube",
                obj_ref: cube,
                position: [-100,100,0],
                scale: [100, 100, 100],
                draggable: true,
                show_bounding_box: true
            })
            useEntityStore().ADD_ENTITY(c_debug_entity)

            // Debug Sphere
            const s_geometry = new SphereGeometry(1, 32, 16);
            const s_material = new MeshStandardMaterial({
                color: 0xffff00,
                wireframe: true,
            });
            const sphere = new Mesh(s_geometry, s_material);

            const s_debug_entity = new Entity( {
                name: "sphere",
                obj_ref: sphere,
                scale: [50, 50, 50],
            })
            s_debug_entity.is_draggable = true
            s_debug_entity.show_bounding_box = true
            s_debug_entity.set_position(100, 100, 0)
            useEntityStore().ADD_ENTITY(s_debug_entity)

        },
        INIT(width, height, el) {
            return new Promise((resolve) => {
                this.SET_VIEWPORT_SIZE(width, height);
                this.INITIALIZE_RENDERER(el);
                this.INITIALIZE_CAMERA();
                this.INITIALIZE_CONTROLS();
                this.INITIALIZE_SCENE();
                this.INITIALIZE_DEBUG_SCENE();

                // Initial scene rendering
                this.RENDER();

                // Add an event listener that will re-render
                // the scene when the controls are changed
                this.controls.c_cam.addEventListener("change", () => {
                    this.RENDER();
                });

                resolve();
            });
        },
        RENDER() {
            this.renderer.render(this.scene, this.camera);
        },
        UPDATE_DEBUG(){
            if (DEBUG) {
                this.stats.update();

                if (Object.keys(this.bounding_boxes).length > 0) {
                    Object.values(this.bounding_boxes).forEach(entity => entity.update_bounding_box())
                }
            }
        },
        ANIMATE() {
            window.requestAnimationFrame(this.ANIMATE);

            this.RENDER();
            this.UPDATE_DEBUG();

        },
        ADD_TO_SCENE(entity) {
            this.scene.add(entity.obj_ref)
            // this.RENDER() // Probably unnecessary since updating each frame
        },
        REMOVE_FROM_SCENE (entity) {
            this.scene.remove(entity.obj_ref)
            // this.RENDER() // Probably unnecessary since updating each frame
        },
        ADD_TO_DRAGGABLE (entity) {
            this.movable_objects.push(entity.obj_ref)
        },
        REMOVE_FROM_DRAGGABLE (entity) {
            // TODO
            // Use index of or filter
            console.log(entity)
        },
        ADD_BOUNDING_BOX (entity) {
            // Bounding Box
            // Reference 1: PC Bounding Box: https://discourse.threejs.org/t/how-to-plot-bounding-box-with-respect-to-a-point-cloud/37366/11
            // Reference 2: https://threejs.org/docs/?q=Points#api/en/core/BufferGeometry => Comes with a bounding box!
            // https://threejs.org/docs/#api/en/helpers/BoxHelper

            const bounding_box = new BoxHelper(entity.obj_ref, 0xffff00);
            entity.bounding_box_ref = bounding_box;
            this.scene.add(bounding_box)
            this.bounding_boxes[entity.obj_ref.uuid] = entity
        },
        REMOVE_BOUNDING_BOX (entity) {
            // TODO
            console.log(entity)
        },
        CREATE_PC_OBJECT(name, geometry) {
            /***
             *  Creates a point three js cloud object and return it
             *  name: name of the model
             *  geometry: {coords, colors}
             *  @return: point cloud object
             */

            // References
            // Reference: https://stackoverflow.com/questions/66225871/how-to-give-each-point-its-own-color-in-threejs
            // Reference 2: OFFICIAL PCD LOADER: https://github.com/mrdoob/three.js/blob/master/examples/jsm/loaders/PCDLoader.js

            // Constants
            const PC_CORRECTION = 1 // Correct the coords to center at 0, 0, 0

            // Calculate centroid
            let center_x, center_y, center_z = 0
            let num_of_points = geometry.coords.length

            // Point Cloud Construction
            // Coords
            let object_geometry = new BufferGeometry();
            const positions = []
            const colors = []

            let centroid = [0, 0, 0]

            let vertex, vx, vy, vz, color;
            for (let i = 0; i < geometry.coords.length; i ++ ) {
                vertex = geometry.coords[i]
                vx = vertex[0] * PC_CORRECTION - PC_CORRECTION/2
                vy = vertex[1] * PC_CORRECTION - PC_CORRECTION/2
                vz = vertex[2] * PC_CORRECTION - PC_CORRECTION/2

                center_x += vx
                center_y += vy
                center_z += vz

                positions.push(vx, vy, vz)

                color = geometry.colors[i]
                colors.push(color[0], color[1], color[2])
            }

            centroid = [center_x/num_of_points, center_y/num_of_points, center_z/num_of_points]

            object_geometry.setAttribute( 'position', new Float32BufferAttribute( positions, 3 ) );
            object_geometry.setAttribute( 'color', new Float32BufferAttribute( colors, 3 ) );

            // Material
            const material = new PointsMaterial({
                size: this.point_size,
                sizeAttenuation: false,
                vertexColors: true
            });

            console.log(centroid)

            // Return Point Cloud Object
            return new Points(object_geometry, material);
        },



    },
});
