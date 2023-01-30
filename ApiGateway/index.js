const express = require('express')
const axios = require('axios')
const cors = require('cors')
const app = express()

// Get the quotes api from the environment(refer docker-compose.yml)
// const PREPROCESSING_API_GATEWAY =
const PREPROCESSING_API_GATEWAY = process.env.PREPROCESSING_API
const MODEL_GENERATOR_API_GATEWAY = process.env.MODEL_GENERATOR_API_GATEWAY
const STORY_ANALYZER_API_GATEWAY = process.env.STORY_ANALYZER_API_GATEWAY
const PORT = process.env.PORT

// Use CORS to prevent Cross-Origin Requets issue
app.use(cors())
app.use(express.json());

// Get the status of the API
app.get('/api/status', (req, res) => {
    return res.json({status: 'ok'})
})

// Demo
app.post('/api/resolve_entity', async (req, res) => {
    try {
        const url = PREPROCESSING_API_GATEWAY + '/api/resolve_entity'
        const data = req.body
        const resolved = await axios.post(url, data)

        return res.json({
            time: Date.now(),
            raw: resolved.data.raw,
            resolved: resolved.data.sequences
        })
    } catch (error) {
        // console.log(error)
        res.status(500)
        return res.json({
            message: "Internal server error",
        })
    }
})

// Demo
app.post('/api/resolve_ner', async (req, res) => {
    try {
        // TODO: Make this a middleware
        console.log("Callling /api/resolve_ner")

        const url = PREPROCESSING_API_GATEWAY + '/api/resolve_ner'
        const data = req.body
        const resolved = await axios.post(url, data)

        console.log(resolved)

        return res.json({
            time: Date.now(),
            input: resolved.data.input,
            output: resolved.data.output
        })
    } catch (error) {
        // console.log(error)
        res.status(500)
        return res.json({
            message: "Internal server error",
        })
    }
})


// Get Mesh
app.post('/api/text_to_model', async (req, res) => {
    try {
        // TODO: Make this logging a middle ware
        console.log("Calling /api/text_to_mesh")

        const url = MODEL_GENERATOR_API_GATEWAY + '/api/text_to_model'
        const data = req.body
        const resolved = await axios.post(url, data)

        return res.json({
            time: Date.now(),
            query: resolved.data.query,
            geometry: resolved.data.geometry
        })
    } catch (error) {
        // console.log(error)
        res.status(500)
        return res.json({
            message: "Internal server error",
        })
    }
})

// Story to scene
app.post('/api/story_to_scene', async (req, res) => {
    try {
        // TODO: Make this logging a middle ware
        console.log("Calling /api/story_to_scene")

        // First analyze the story

        const analyze_story_url = STORY_ANALYZER_API_GATEWAY + '/api/analyze_story'
        const data = req.body
        const response = await axios.post(analyze_story_url, data)

        if (response.status === 500) {
            res.status(500)
            return res.json({
                message: "Internal server error: Analyze Story Failed",
            })
        }

        const entities = JSON.parse(response.data.entities)
        const scene = JSON.parse(response.data.scene)
        const events = JSON.parse(response.data.events)
        const logics = JSON.parse(response.data.logics)

        // Generate Geometries for Entities
        const model_generation_url = MODEL_GENERATOR_API_GATEWAY + '/api/text_to_model';
        let query, geo_res = "";
        for ( const [name, ontologies] of Object.entries(entities) ) {
            query = JSON.stringify([name, ontologies])
            console.log("Generating geometry for " + query)
            geo_res = await axios.post(model_generation_url, {query: query})
            if (geo_res.data.geometry) {
                entities[name]["Geometry"] = JSON.parse(geo_res.data.geometry)
                console.log("Generated geometry for " + query)
            } else {
                console.log("No valid geometry when trying to generate model for " + query)
            }

        }

        // The front end can directly use the objects as they are passed in json
        // It seems that the frontend will automatically unpack it
        return res.json({
            time: Date.now(),
            query: req.body.query,
            entities: entities,
            scene: scene,
            events: events,
            logics: logics,
        })
    } catch (error) {
        console.log("Got Error: " + error)
        res.status(500)
        return res.json({
            message: "Internal server error",
        })
    }
})


// Handle any unknown route
app.get('*', (req, res) => {
    res.status(404)
    return res.json({
        message: 'Resource not found'
    })
});

// starts the app
app.listen(PORT, () => {
    console.log('API Gateway is listening on port ' + PORT)
})
