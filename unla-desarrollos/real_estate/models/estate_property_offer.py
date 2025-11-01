from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import date, timedelta

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Oferta sobre propiedad"

    _sql_constraints = [
        ('unique_offer_per_partner_per_property',
         'UNIQUE(partner_id, property_id)',
         'Una persona no puede hacer más de una oferta por propiedad')
    ]

    price = fields.Float(string="Precio", required=True)
    status = fields.Selection(
        selection=[
            ("accepted", "Aceptada"),
            ("refused", "Rechazada"),
        ],
        string="Estado",
    )
    partner_id = fields.Many2one("res.partner", string="Ofertante", required=True)
    property_id = fields.Many2one("estate.property", string="Propiedad", required=True, ondelete="cascade")

    validity = fields.Integer(string="Validez(dias)", default=7, store=True)

    date_deadline = fields.Date(
        string="Fecha limite",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        store=True,
    )

    property_type = fields.Many2one(
        string="Tipo Propiedad",
        related="property_id.property_type_id",
        store=True,
    )


    # ==================================================
    #  Punto 23: Sobrescribir el método create
    # ==================================================
    @api.model
    def create(self, vals):
        # Validación a: Precio mayor a la mejor oferta existente
        property_id = vals.get('property_id')
        price = vals.get('price')
        
        if property_id and price:
            property_obj = self.env['estate.property'].browse(property_id)
            
            # Obtener la mejor oferta actual
            existing_offers = property_obj.offer_ids.mapped('price')
            best_offer = max(existing_offers) if existing_offers else 0
            
            if price <= best_offer:
                raise UserError(f"El precio ofertado (${price}) debe ser mayor a la mejor oferta actual (${best_offer})")
            
            # Validación b: Estado de la propiedad debe ser "Nuevo" u "Oferta recibida"
            valid_states = ['nuevo', 'oferta_recibida']
            if property_obj.state not in valid_states:
                raise UserError(f"Solo se pueden crear ofertas para propiedades en estado 'Nuevo' u 'Oferta recibida'. Estado actual: {property_obj.state}")
        
        # Crear la oferta
        offer = super().create(vals)
        
        # c: Cambiar estado de la propiedad a "Oferta recibida"
        if property_id:
            property_obj.write({'state': 'oferta_recibida'})
        
        return offer
    # ==================================================


    @api.depends('validity', 'create_date')
    def _compute_date_deadline(self):
        for rec in self:
            base = (rec.create_date or fields.Datetime.now()).date()
            rec.date_deadline = base + timedelta(days=rec.validity or 0)

    def _inverse_date_deadline(self):
        for rec in self:
            if rec.date_deadline and rec.create_date:
                rec.validity = (rec.date_deadline - rec.create_date.date()).days

    # 🔹 Botón "Aceptar" en la lista de ofertas (Punto 16)
    def action_accept_offer(self):
        for offer in self:
            prop = offer.property_id
            if not prop:
                raise UserError("La oferta no tiene propiedad asociada.")

            # Rechazar las demás ofertas de la misma propiedad
            (prop.offer_ids - offer).write({'status': 'refused'})

            # Cargar datos en la propiedad
            vals_prop = {
                'buyer_id': offer.partner_id.id,
                'selling_price': offer.price,
                # Ajustá este estado a tu selection real del modelo estate.property
                'state': 'oferta_aceptada',
            }
            prop.write(vals_prop)

            # Marcar esta oferta como aceptada
            offer.status = 'accepted'
