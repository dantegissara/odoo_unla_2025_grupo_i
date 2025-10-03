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

        # 🔹 Many2one - Tipo Propiedad
    property_type_id = fields.Many2one(
        "estate.property.type",
        string="Tipo Propiedad"
    )

    # 🔹 Many2one - Comprador (res.partner)
    buyer_id = fields.Many2one(
        "res.partner",
        string="Comprador"
    )

    # 🔹 Many2one - Vendedor (res.users)
    salesman_id = fields.Many2one(
        "res.users",
        string="Vendedor",
        default=lambda self: self.env.user,  # usuario logueado
        copy=False  # no copiar al duplicar registro
    )

    # 🔹 Many2many - Etiquetas
    tag_ids = fields.Many2many(
        comodel_name="estate.property.tag",
        string="Etiquetas",
    )

    offer_ids = fields.One2many(
    comodel_name="estate.property.offer",
    inverse_name="property_id",
    string="Ofertas",
    )

    total_area = fields.Float(
        string="Superficie total",
        compute="_compute_total_area",
        store=True
    )

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for rec in self:
            rec.total_area = rec.living_area + rec.garden_area

    best_offer = fields.Float(
        string="Mejor oferta",
        compute="_compute_best_offer"
    )

    def _compute_best_offer(self):
        for rec in self:
            offers = rec.offer_ids.mapped("price")
            rec.best_offer = max(offers) if offers else 0