{
    'name': "Gestión de Flota de Vehículos",
    'version': '16.0.1.0.0',
    'author': "Leon Chacon",
    'category': 'Fleet',
    'summary': """
        Módulo para gestión de vehículos con integración API externa
        Incluye registro de vehículos, relación con contactos y logs de API
    """,
    'description': """
        Módulo de Gestión de Flota
        ==========================
        
        Características principales:
        • Registro completo de vehículos
        • Relación con contactos (propietarios)
        • Integración con API externa Node.js
        • Sistema de logs para respuestas de API
        • Secuencias automáticas para vehículos
        • Fotos de vehículos
        • Grupos de seguridad personalizados
    """,
    'depends': ['base','contacts','mail'],
    'data': [
        'security/fleet_security.xml',
        'security/ir.model.access.csv',
        'data/sequence_data.xml',
        'views/vehicle_views.xml',
        'views/partner_views.xml',
        'views/api_log_views.xml',
        'views/menu_views.xml',
    ],
    'demo': [
        'demo/vehicle_demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}