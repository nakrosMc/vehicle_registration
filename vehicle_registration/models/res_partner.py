from odoo import models, fields, api
import requests
import json
from odoo import _

class ResPartner(models.Model):
    _inherit = 'res.partner'

    vehicle_ids = fields.One2many('fleet.vehicle', 'contact_id', string='Vehículos')
    vehicle_count = fields.Integer(string='Total Vehículos', compute='_compute_vehicle_count')

    @api.depends('vehicle_ids')
    def _compute_vehicle_count(self):
        for partner in self:
            partner.vehicle_count = len(partner.vehicle_ids)

    def action_view_vehicles(self):
        self.ensure_one()
        return {
            'name': 'Vehículos del Contacto',
            'type': 'ir.actions.act_window',
            'res_model': 'fleet.vehicle',
            'view_mode': 'tree,form',
            'domain': [('contact_id', '=', self.id)],
            'target': 'current',
        }

    def action_send_to_api(self):
        """Enviar todos los vehículos activos de este contacto a Node.js y mostrar notificación"""
        self.ensure_one()

        # Buscar vehículos activos
        vehicles = self.env['fleet.vehicle'].sudo().search([
            ('contact_id', '=', self.id),
            ('active', '=', True)
        ])

        if not vehicles:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Sin vehículos',
                    'message': 'Este propietario no tiene vehículos activos para enviar.',
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
                'partner_id': self.id,
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
            # Registrar error en log
            self.env['api.log'].sudo().create({
                'status': 'Error de conexión',
                'response_text': str(e),
                'vehicle_data': json.dumps(vehicle_data, indent=2),
                'partner_id': self.id,
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

