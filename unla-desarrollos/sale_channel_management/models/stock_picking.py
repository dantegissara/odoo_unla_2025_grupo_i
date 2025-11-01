from odoo import models, fields

class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    # Campo para el canal de venta
    sale_channel_id = fields.Many2one(
        'sale.channel',
        string='Canal de Venta',
        related='sale_id.sale_channel_id',  # ← Se obtiene de la orden de venta
        store=True,  # ← Se guarda en BD para poder filtrar/agrupar
        help='Canal de venta de la orden de venta asociada'
    )