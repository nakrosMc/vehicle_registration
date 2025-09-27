# 🚗 Vehicle Registration Project

Módulo personalizado de **Odoo 16** para la gestión de vehículos, con integración a una **API Node.js** para enviar información de los vehículos y registrar logs de respuesta.

---

## 📂 Contenido del proyecto

- `vehicle_registration`: Módulo principal de Odoo para registrar vehículos y asociarlos a contactos.
- `vehicle_api`: API Node.js que recibe los datos de los vehículos enviados desde Odoo y registra la respuesta.
- `vehicle_registration_project`: Carpeta contenedora de ambos módulos.

---

## ⚙️ Requisitos

- **Odoo 16** (instalación local)
- **Node.js** (v14 o superior)
- **Python 3.10+**
- **PostgreSQL**
- **Git**

> ⚠️ **Nota:** Para ver el módulo en Odoo, primero debes asignar los permisos correspondientes a los usuarios. Si no, el módulo no será visible.

---

## 🏎 Uso del módulo en Odoo

### Registro de Vehículos

1. Ir a **Flota → Vehículos**.
2. Crear un nuevo vehículo y asociarlo a un contacto.
3. Completar los campos obligatorios: **foto, marca, modelo, año y color**.
4. Guardar el registro.

### Smart Button en Contactos

- Al abrir un contacto, puedes ver un botón que muestra todos los vehículos asociados a ese contacto.

### Enviar vehículos a la API

1. Seleccionar un contacto con vehículos activos.
2. Presionar el botón **Enviar a API**.
3. Odoo enviará los vehículos a la API Node.js y mostrará un mensaje con el resultado.
4. Las respuestas se registran en el módulo **Logs API**.

---

## 📊 Registro de Logs

- Todas las respuestas de la API se registran en Odoo bajo **Logs API**.
- Campos registrados:
  - Fecha de respuesta
  - Estado (status)
  - Texto de la respuesta
  - Número de vehículos enviados
  - Datos enviados

---

## 🔢 Secuencias

- El módulo utiliza secuencias para numerar automáticamente los vehículos (`VEH/0001`, `VEH/0002`, ...).

---

## 👥 Permisos de usuario

- Los **Usuarios de Flota** solo pueden ver y enviar sus propios vehículos.
- El botón **Enviar a API** solo es visible para los usuarios con rol de **Administrador de Flota**.
- Todos los campos importantes están disponibles en el historial de cambios (**tracking**) para auditoría.

---

## 🖥 API Node.js

### Instalación y ejecución

1. Abrir la terminal y moverse a la carpeta de la API:

```bash
cd vehicle_registration_project/vehicle_api
Instalar dependencias:

npm install
Iniciar el servidor:
node server.js
Por defecto, correrá en: http://localhost:3000

Funcionalidad
Endpoint: POST /api/vehicles

Recibe un array de vehículos desde Odoo.

Imprime los datos en la consola y devuelve una respuesta JSON:

{
  "status": "ok",
  "message": "Recibidos X vehiculos"
}
Cada envío se registra en Logs API en Odoo.

Ejemplo de server.js

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
```
---

## 📝 Datos Demo

El módulo incluye datos demo para facilitar las pruebas iniciales.

Al instalar el módulo, se crean ejemplos de:

- Contactos

- Vehículos asociados a esos contactos

- Logs de envío a la API

Esto permite probar el flujo completo sin necesidad de crear registros manualmente.

---

## 📌 Notas adicionales
Es obligatorio seleccionar un contacto al crear un vehículo.

La creación de vehículos cuenta con secuencia propia.

Se puede adjuntar una foto del vehículo.

Todos los campos y botones están ubicados de manera coherente y estructurada dentro de las vistas de Odoo.

Logs y historial (tracking) están habilitados para todos los cambios importantes.

🔗 Repositorio
GitHub: https://github.com/nakrosMc/vehicle_registration
