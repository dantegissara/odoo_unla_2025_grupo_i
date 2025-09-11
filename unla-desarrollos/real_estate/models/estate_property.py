from odoo import fields, models, api
from dateutil.relativedelta import relativedelta
from datetime import date, timedelta

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Propiedad'

    name = fields.Char(string="Título", required=True)
    description = fields.Text(string="Descripción")
    postcode = fields.Char(string="Código Postal")
    date_availability = fields.Date(string="Fecha disponibilidad",copy=False, default=lambda self: date.today() + timedelta(days=90))
    expected_price = fields.Float(string="Precio esperado")
    selling_price = fields.Float(string="Precio de venta",copy=False)
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
    state = fields.Selection(
        [
            ("nuevo", "Nuevo"),
            ("oferta_recibida", "Oferta Recibida"),
            ("oferta_aceptada", "Oferta Aceptada"),
            ("vendido", "Vendido"),
            ("cancelado", "Cancelado"),
        ],
        string="Estado",
        required=True,
        default="nuevo",
        copy=False
    )