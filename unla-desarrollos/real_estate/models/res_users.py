from odoo import models, fields


# ==================================================
# Punto 24: Extender el modelo res.users
# ==================================================
class ResUsers(models.Model):
    _inherit = "res.users"
    
    # Campo One2many inverso al salesman_id de estate.property
    property_ids = fields.One2many(
        comodel_name="estate.property",
        inverse_name="salesman_id",
        string="Propiedades asignadas",
        help="Propiedades inmobiliarias asignadas a este vendedor"
    )