from odoo import models, fields

class AccountMove(models.Model):
    _inherit = 'account.move'
    
    # d. Trasladar canal a facturas
    sale_channel_id = fields.Many2one(
        'sale.channel',
        string='Canal de Venta',
        store =True,
        help='Canal de venta asociado a esta factura'
    )