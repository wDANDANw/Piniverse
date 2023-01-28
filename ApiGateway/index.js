const express = require('express')
const axios = require('axios')
const cors = require('cors')
const app = express()

// Get the quotes api from the environment(refer docker-compose.yml)
// const PREPROCESSING_API_GATEWAY = process.env.PREPROCESSING_API
const PREPROCESSING_API_GATEWAY = "http://localhost:12334"
const MODELGENERATOR_API_GATEWAY = "http://localhost:12335"
const PORT = 12333

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
        console.log("Callling /api/text_to_mesh")

        const url = MODELGENERATOR_API_GATEWAY + '/api/text_to_model'
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
