import random
from odoo import fields, models, api
from dateutil.relativedelta import relativedelta
from datetime import date, timedelta
from odoo.exceptions import UserError  # <- agregado mínimo para UserError

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Propiedad'

    name = fields.Char(string="Título", required=True)
    description = fields.Text(string="Descripción")
    postcode = fields.Char(string="Código Postal")
    date_availability = fields.Date(string="Fecha disponibilidad",copy=False, default=lambda self: date.today() + timedelta(days=90))
    expected_price = fields.Float(string="Precio esperado")

    # muestra una advertencia si el precio esperado es menor a 10.000
    # 
    @api.onchange('expected_price')
    def _onchange_expected_price_warning(self):
        for rec in self:
            if rec.expected_price and rec.expected_price < 10000: # evita advertencia si el campo está vacío y
                return {
                    'warning': {
                        'title': "Precio bajo",
                        'message': "El precio esperado es menor a 10.000. Verifica si es correcto."
                    }
                }
        # Si no hay advertencia, no es necesario devolver nada

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

    # hace que al clickear en el checkbox de jardín, se complete automáticamente el área del jardín
    # si se desmarca, el área vuelve a 0
    @api.onchange('garden')
    def _onchange_garden(self):
        for rec in self:
            if rec.garden:
                rec.garden_area = 10
            else:
                rec.garden_area = 0

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

     # Punto 19: Campo computado para obtener todos los partners que hicieron ofertas
    offer_partner_ids = fields.Many2many(
        "res.partner",
        string="Ofertantes",
        compute="_compute_offer_partner_ids",
        store=True  # Opcional: si quieres que se guarde en la BD para búsquedas
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


    # Punto 19: Método para computar los partners que hicieron ofertas
    @api.depends('offer_ids.partner_id')
    def _compute_offer_partner_ids(self):
        for record in self:
            # Obtenemos todos los partners de las ofertas y eliminamos duplicados
            partners = record.offer_ids.mapped('partner_id')
            record.offer_partner_ids = partners

    def action_set_sold(self):
        for rec in self:
            if rec.state == 'cancelado':
                raise UserError("No se puede marcar como vendida una propiedad cancelada.")
            rec.state = 'vendido'

    def action_set_canceled(self):
        for rec in self:
            if rec.state == 'vendido':
                raise UserError("No se pueden cancelar propiedades ya vendidas.")
            rec.state = 'cancelado' 


    # ==================================================
    # Punto 22: restricción para eliminar propiedades
    # ==================================================
    @api.ondelete(at_uninstall=False)
    def _unlink_if_new_or_cancelled(self):
        """Solo permite eliminar propiedades en estado 'Nuevo' o 'Cancelado'"""
        for record in self:
            if record.state not in ['nuevo', 'cancelado']:
                raise UserError("No se pueden eliminar propiedades que no estén en estado 'Nuevo' o 'Cancelado'")
    # ==================================================



    # =================================================
    # Punto 21: botones en el encabezado de la propiedad

    def action_remove_all_tags(self):
        """Botón 'Sacar etiquetas': desvincula todas las etiquetas de la propiedad"""
        for record in self:
            record.tag_ids = [(5, 0, 0)]  # Comando Odoo para eliminar todas las etiquetas
        return True

    def action_add_all_tags(self):
        """Botón 'Cargar todas las etiquetas': vincula todas las etiquetas existentes"""
        all_tags = self.env['estate.property.tag'].search([])
        for record in self:
            record.tag_ids = [(6, 0, all_tags.ids)]  # Comando Odoo para reemplazar con todas las etiquetas
        return True

    def action_add_new_tag(self):
        """Botón 'A estrenar': crea y vincula la etiqueta 'A estrenar'"""
        tag_name = "A estrenar"
        
        # Buscar si ya existe la etiqueta
        tag = self.env['estate.property.tag'].search([('name', '=', tag_name)], limit=1)
        
        # Si no existe, crearla
        if not tag:
            tag = self.env['estate.property.tag'].create({'name': tag_name})
        
        # Agregar la etiqueta a la propiedad (sin quitar las existentes)
        for record in self:
            record.tag_ids = [(4, tag.id, 0)]  # Comando Odoo para agregar una etiqueta
        return True

    # =================================================

    def _get_random_partner(self, excluded_partners):
        """Devuelve un partner activo aleatorio que NO esté en la lista excluida."""
        domain = [('active', '=', True)]
        if excluded_partners:
            domain.append(('id', 'not in', excluded_partners.ids))
        partners = self.env['res.partner'].search(domain, limit=0)
        if not partners:
            return None
        return random.choice(partners)

    def action_generate_auto_offer(self):
        for prop in self:
            # 1) Precio = expected_price con variación aleatoria [-30%, +30%]
            if not prop.expected_price:
                raise UserError("La propiedad no tiene 'Precio esperado' para calcular la oferta.")
            variation = random.uniform(-0.3, 0.3)
            auto_price = prop.expected_price * (1 + variation)

            # redondeo “amigable” (opcional)
            auto_price = round(auto_price, 2)

            # 2) Obtener ofertantes ya usados
            # Preferimos offer_partner_ids (punto 19); si no existiera, lo derivamos de offer_ids
            excluded = getattr(prop, 'offer_partner_ids', self.env['res.partner'])
            if not excluded:
                excluded = prop.offer_ids.mapped('partner_id')

            # 3) Elegir partner aleatorio válido
            partner = self._get_random_partner(excluded)
            if not partner:
                raise UserError("No hay contactos activos disponibles que no hayan ofertado todavía.")

            # 4) Crear la oferta
            self.env['estate.property.offer'].create({
                'price': auto_price,
                'partner_id': partner.id,
                'property_id': prop.id,
            })
    
