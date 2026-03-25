# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SaleCommissionLine(models.Model):
    _name = 'sale.commission.line'
    _description = 'Línea de Comisión de Venta'
    _order = 'order_id, id'

    order_id = fields.Many2one(
        comodel_name='sale.order',
        string='Pedido',
        required=True,
        ondelete='cascade',
        help='Pedido de venta asociado',
    )
    rule_id = fields.Many2one(
        comodel_name='sale.commission.rule',
        string='Regla de Comisión',
        required=True,
        ondelete='cascade',
        help='Regla de comisión aplicada',
    )
    user_id = fields.Many2one(
        related='rule_id.user_id',
        string='Usuario',
        store=True,
        readonly=True,
    )
    commission_percent = fields.Float(
        related='rule_id.commission_percent',
        string='Porcentaje',
        store=True,
        readonly=True,
    )
    amount_total = fields.Monetary(
        related='order_id.amount_total',
        string='Total Pedido',
        store=True,
        readonly=True,
    )
    commission_amount = fields.Monetary(
        string='Monto Comisión',
        compute='_compute_commission_amount',
        store=True,
        readonly=True,
    )
    currency_id = fields.Many2one(
        related='order_id.currency_id',
        string='Moneda',
        store=True,
        readonly=True,
    )
    state = fields.Selection(
        selection=[
            ('draft', 'Borrador'),
            ('confirmed', 'Confirmado'),
            ('paid', 'Pagado'),
        ],
        string='Estado',
        default='draft',
    )

    @api.depends('amount_total', 'commission_percent')
    def _compute_commission_amount(self):
        """Calcular monto de comisión"""
        for record in self:
            record.commission_amount = (
                record.amount_total * record.commission_percent / 100
            )
