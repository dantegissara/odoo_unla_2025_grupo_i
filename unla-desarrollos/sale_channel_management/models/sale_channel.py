from odoo import models, fields, api

class SaleChannel(models.Model):
    _name = 'sale.channel'
    _description = 'Canal de Venta'
    
    name = fields.Char(
        string='Nombre', 
        required=True,
        help='Nombre identificativo del canal'
    )
    
    code = fields.Char(
        string='Código', 
        required=True,
        help='Código identificativo del canal'
    )
    
    # COMENTAR TEMPORALMENTE hasta instalar dependencias
    warehouse_id = fields.Many2one(
         'stock.warehouse',
         string='Depósito',
         help='Almacén de donde se debe despachar la mercadería'
    )
    
    journal_id = fields.Many2one(
         'account.journal',
         string='Diario de Factura',
         domain=[('type', '=', 'sale')],
         help='Diario contable para facturas asociadas a las órdenes'
    )
    
    # SQL Constraints
    _sql_constraints = [
        ('unique_code', 'UNIQUE(code)', 'El código del canal debe ser único en el sistema.')
    ]