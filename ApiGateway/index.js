const express = require('express')
const axios = require('axios')
const cors = require('cors')
const app = express()

// Get the quotes api from the environment(refer docker-compose.yml)
const QUOTES_API_GATEWAY = process.env.QUOTES_API
const PREPROCESSING_API_GATEWAY = process.env.PREPROCESSING_API

// Use CORS to prevent Cross-Origin Requets issue
app.use(cors())
app.use(express.json());

// Get the status of the API
app.get('/api/status', (req, res) => {
    return res.json({status: 'ok'})
})

// Returns a random quote from the quote api
app.get('/api/randomquote',async (req, res) => {
    try {
        const url = QUOTES_API_GATEWAY + '/api/quote'
        const quote = await axios.get(url)
        return res.json({
            time: Date.now(),
            quote: quote.data
        })
    } catch (error) {
        console.log(error)
        res.status(500)
        return res.json({
            message: "Internal server error",
        })
    }
    
})

// Demo
app.post('/api/resolve_entity', async (req, res) => {
    try {
        const url = PREPROCESSING_API_GATEWAY + '/api/resolve_entity'
        const data = req.body
        console.log(data)
        const resolved = await axios.post(url, data)

        console.log(resolved.data)

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




// Handle any unknown route
app.get('*', (req, res) => {
    res.status(404)
    return res.json({
        message: 'Resource not found'
    })
});

// starts the app
app.listen(3000, () => {
    console.log('API Gateway is listening on port 3000!')
})
