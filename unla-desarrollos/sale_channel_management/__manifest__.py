{
    'name': 'Gestión de Canales de Venta',
    'version': '18.0.1.0.0',
    'category': 'Sales',
    'summary': 'Gestión de canales de venta y grupos de crédito',
    'description': """
        Módulo para gestionar canales de venta, grupos de crédito y validaciones de límite de crédito.
    """,
    'author': 'Tu Nombre',
    'website': '',
    'depends': [
        'base', 
        'sale_management',
        'stock',
        'account',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_channel_views.xml',
        'views/account_move_show_journal.xml',
        'views/account_move_views.xml',
        'views/stock_picking_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
}