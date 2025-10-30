# sale_channel_management/models/sale_order.py
from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = "sale.order"

    sale_channel_id = fields.Many2one(
        comodel_name="sale.channel",   
        string="Canal de venta",
        required=True
    )
