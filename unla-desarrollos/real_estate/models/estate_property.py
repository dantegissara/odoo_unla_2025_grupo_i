from odoo import fields, models, api
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Propiedad'

    name = fields.Char(string="Título", required=True)
    description = fields.Text(string="Descripción")
    postcode = fields.Char(string="Código Postal")
    date_availability = fields.Date(string="Fecha disponibilidad")
    expected_price = fields.Float(string="Precio esperado")
    selling_price = fields.Float(string="Precio de venta")
    bedrooms = fields.Integer(string="Habitaciones", default=2)
    living_area = fields.Integer(string="Superficie cubierta")
    facades = fields.Integer(string="Fachadas")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Jardín")
    garden_orientation = fields.Selection(
        selection=[
            ("north", "Norte"),
            ("south", "Sur"),
            ("east", "Este"),
            ("west", "Oeste"),
        ],
        default="north",
        string="Orientación del jardín",
    )
    garden_area = fields.Integer(string="Superficie jardín")