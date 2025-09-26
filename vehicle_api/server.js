// server.js
const express = require('express');
const bodyParser = require('body-parser');
const morgan = require('morgan');

const app = express();
const PORT = 3000;

// Middlewares
app.use(bodyParser.json());
app.use(morgan('dev'));

// Endpoint para recibir vehículos
app.post('/api/vehicles', (req, res) => {
    const vehicles = req.body;
    console.log('Vehículos recibidos desde Odoo:');
    console.log(JSON.stringify(vehicles, null, 2));

    res.status(200).json({ status: 'ok', message: `Recibidos ${vehicles.length} vehiculos` });
});

// Iniciar servidor
app.listen(PORT, () => {
    console.log(`Servidor Node.js escuchando en http://localhost:${PORT}`);
});
