from odoo import models, fields,api
from datetime import date, timedelta


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Oferta sobre propiedad"

    price = fields.Float(string="Precio", required=True)
    status = fields.Selection(
        selection=[
            ("accepted", "Aceptada"),
            ("refused", "Rechazada"),
        ],
        string="Estado",
    )
    partner_id = fields.Many2one(
        "res.partner",
        string="Ofertante",
        required=True,
    )
    property_id = fields.Many2one(
        "estate.property",
        string="Propiedad",
        required=True,
        ondelete="cascade",
    )

    validity = fields.Integer(
        string="Validez(dias)",
        default=7,
        store=True,
    )

    date_deadline = fields.Date(
        string="Fecha limite",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        store=True,
    )

    # Campo relacionado al tipo de propiedad
    # "related" apunta al campo property_type_id del modelo estate.property
    # "store=True" hace que se guarde en la base de datos (sirve para filtrar/ordenar en vistas y reportes)
    property_type = fields.Many2one(          # El modelo relacionado
        string="Tipo Propiedad",
        related="property_id.property_type_id",
        store=True,
    )

    @api.depends('validity', 'create_date')
    def _compute_date_deadline(self):
        for rec in self:
            base = (rec.create_date or fields.Datetime.now()).date()
            rec.date_deadline = base + timedelta(days=rec.validity or 0)

    def _inverse_date_deadline(self):
        for rec in self:
            if rec.date_deadline and rec.create_date:
                rec.validity = (rec.date_deadline - rec.create_date.date()).days