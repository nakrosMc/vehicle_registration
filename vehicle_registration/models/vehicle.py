from odoo import models, fields, api
import requests
import logging
from odoo import _
from odoo import http, models
from odoo.http import request
import json
_logger = logging.getLogger(__name__)


class FleetVehicle(models.Model):
    _name = 'fleet.vehicle'
    _description = 'Vehículo'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'sequence desc'

    name = fields.Char(string='Placa', required=True, tracking=True)
    sequence = fields.Char(string='Referencia', readonly=True, copy=False, default='Nuevo')
    contact_id = fields.Many2one('res.partner', string='Propietario', required=True, tracking=True)
    photo = fields.Binary(string='Foto del Vehículo', tracking=True)
    brand = fields.Char(string='Marca', tracking=True)
    model = fields.Char(string='Modelo', tracking=True)
    year = fields.Integer(string='Año', tracking=True)
    color = fields.Char(string='Color', tracking=True)
    notes = fields.Text(string='Notas', tracking=True)
    active = fields.Boolean(string='Activo', default=True)
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('active', 'Activo'),
        ('maintenance', 'En Mantenimiento'),
        ('inactive', 'Inactivo'),
    ], string='Estado', default='draft', tracking=True)

    # Campo calculado
    is_available = fields.Boolean(
        string="Disponible",
        compute="_compute_is_available",
        store=True
    )

    @api.depends('state')
    def _compute_is_available(self):
        for rec in self:
            rec.is_available = rec.state == 'active'

    @api.model
    def create(self, vals):
        # Asignar secuencia si es nuevo
        if vals.get('sequence', 'Nuevo') == 'Nuevo':
            vals['sequence'] = self.env['ir.sequence'].next_by_code('fleet.vehicle') or 'Nuevo'
        
        # Forzar que el estado sea activo al crear
        if 'state' not in vals or vals['state'] == 'draft':
            vals['state'] = 'active'
        
        return super(FleetVehicle, self).create(vals)



    def action_set_active(self):
        self.write({'state': 'active'})

    def action_set_inactive(self):
        self.write({'state': 'inactive'})

    def action_set_maintenance(self):
        self.write({'state': 'maintenance'})
        
    other_vehicles_ids = fields.One2many(
        'fleet.vehicle',
        'contact_id',
        string='Otros Vehículos del Propietario',
        compute='_compute_other_vehicles',
        store=False
    )
        
    @api.depends('contact_id')
    def _compute_other_vehicles(self):
        for vehicle in self:
            if vehicle.contact_id and vehicle.id:
                vehicle.other_vehicles_ids = vehicle.search([
                    ('contact_id', '=', vehicle.contact_id.id),
                    ('id', '!=', vehicle.id)
                ])
            else:
                vehicle.other_vehicles_ids = self.env['fleet.vehicle']
                

    def action_send_to_api(self):
        """Enviar todos los vehículos del propietario a Node.js y mostrar notificación"""
        self.ensure_one()
        
        if not self.contact_id:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Error',
                    'message': 'Este vehículo no tiene un propietario asignado.',
                    'type': 'danger',
                    'sticky': True,
                }
            }

        # Buscar todos los vehículos activos del contacto
        vehicles = self.env['fleet.vehicle'].sudo().search([
            ('contact_id', '=', self.contact_id.id),
            ('active', '=', True)
        ])

        if not vehicles:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Sin vehículos',
                    'message': 'El contacto no tiene vehículos activos para enviar.',
                    'type': 'warning',
                    'sticky': False,
                }
            }

        # Preparar datos
        vehicle_data = []
        for v in vehicles:
            vehicle_data.append({
                'plate': v.name,
                'reference': v.sequence,
                'owner': v.contact_id.name,
                'brand': v.brand or '',
                'model': v.model or '',
                'year': v.year or '',
                'color': v.color or '',
                'state': v.state,
            })

        try:

            response = requests.post(
                'http://localhost:3000/api/vehicles',
                json=vehicle_data,
                headers={'Content-Type': 'application/json'},
                timeout=10
            )

            data = response.json()
            # Registrar log en Odoo
            self.env['api.log'].sudo().create({
                'status': str(response.status_code),
                'response_text': json.dumps(data, indent=2),
                'vehicle_data': json.dumps(vehicle_data, indent=2),
                'partner_id': self.contact_id.id,
                'vehicle_count': len(vehicle_data)
            })

            notify_type = 'success' if data.get('status') == 'ok' else 'danger'
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Resultado API',
                    'message': data.get('message', 'No hay mensaje de la API'),
                    'type': notify_type,
                    'sticky': False,
                }
            }

        except Exception as e:
            # Log de error
            self.env['api.log'].sudo().create({
                'status': 'Error de conexión',
                'response_text': str(e),
                'vehicle_data': json.dumps(vehicle_data, indent=2),
                'partner_id': self.contact_id.id,
                'vehicle_count': len(vehicle_data)
            })
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Error de Conexión',
                    'message': str(e),
                    'type': 'danger',
                    'sticky': True,
                }
            }
