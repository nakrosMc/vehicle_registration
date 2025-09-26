from odoo import _, api, fields, models, tools
import json

class APILog(models.Model):
    _name = 'api.log'
    _description = 'Log de API'
    _order = 'create_date desc'
    _rec_name = 'date'

    date = fields.Datetime(string='Fecha', default=fields.Datetime.now, readonly=True)
    status = fields.Char(string='Estado', readonly=True)
    response_text = fields.Text(string='Respuesta', readonly=True)
    vehicle_data = fields.Text(string='Datos Enviados', readonly=True)
    partner_id = fields.Many2one('res.partner', string='Contacto', readonly=True)
    vehicle_count = fields.Integer(string='Vehículos Enviados', readonly=True)

    @api.model
    def create_log(self, status, response_data, vehicle_data, partner_id=None):
        """Helper para crear logs. vehicle_data debe ser lista de dicts"""
        vehicle_json = json.dumps(vehicle_data) if isinstance(vehicle_data, list) else str(vehicle_data)
        count = len(vehicle_data) if isinstance(vehicle_data, list) else 0
        return self.create({
            'status': status,
            'response_text': response_data,
            'vehicle_data': vehicle_json,
            'partner_id': partner_id,
            'vehicle_count': count
        })
