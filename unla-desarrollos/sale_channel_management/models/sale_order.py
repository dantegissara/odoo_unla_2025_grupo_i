# sale_channel_management/models/sale_order.py
from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = "sale.order"

    sale_channel_id = fields.Many2one(
        comodel_name="sale.channel",   
        string="Canal de venta",
        required=True
    )

    @api.onchange("sale_channel_id")
    def _onchange_sale_channel_id_set_warehouse(self):
        """
        Al elegir canal, si el canal tiene depósito configurado,
        actualizar el warehouse de la orden.
        """
        for order in self:
            channel = order.sale_channel_id
            if channel and channel.warehouse_id:
                order.warehouse_id = channel.warehouse_id

    # --- Opcional pero MUY útil: cubrir casos no-UI (importes, RPC, automatizaciones) ---
    def _apply_channel_warehouse(self, vals):
        """Helper: decide warehouse a partir del canal (solo si no viene seteado a mano)."""
        channel_id = vals.get("sale_channel_id")
        warehouse_in_vals = "warehouse_id" in vals
        if channel_id and not warehouse_in_vals:
            channel = self.env["sale.channel"].browse(channel_id)
            if channel.warehouse_id:
                vals["warehouse_id"] = channel.warehouse_id.id
        return vals

    @api.model
    def create(self, vals):
        vals = self._apply_channel_warehouse(vals.copy())
        return super().create(vals)

    def write(self, vals):
        # Si cambian el canal en una SO existente y no fijan warehouse explícitamente,
        # alineamos el warehouse con el del canal.
        self._apply_channel_warehouse(vals)
        return super().write(vals)