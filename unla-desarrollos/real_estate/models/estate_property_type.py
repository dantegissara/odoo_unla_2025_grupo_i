from odoo import models, fields

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Tipo de propiedad"

    name = fields.Char(string="Nombre", required=True)

    # SQL Constraints - Punto 17
    _sql_constraints = [
        ('unique_type_name', 'UNIQUE(name)', 'El nombre del tipo de propiedad debe ser único')
    ]
    
    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "property_type_id")