from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Etiqueta de propiedad"

    name = fields.Char(string="Nombre", required=True)

    # SQL Constraints - Punto 17
    _sql_constraints = [
        ('unique_tag_name', 'UNIQUE(name)', 'El nombre de la etiqueta debe ser único')
    ]
    
    name = fields.Char(required=True)
    color = fields.Integer()