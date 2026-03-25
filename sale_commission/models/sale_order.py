# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    commission_rule_id = fields.Many2one(
        comodel_name='sale.commission.rule',
        string='Regla de Comisión',
        compute='_compute_commission_rule_id',
        store=True,
        readonly=False,
    )
    commission_percent = fields.Float(
        string='Porcentaje Comisión',
        compute='_compute_commission_percent',
        store=True,
        readonly=True,
    )
    commission_amount = fields.Monetary(
        string='Monto Comisión',
        compute='_compute_commission_amount',
        store=True,
        readonly=True,
    )
    commission_line_ids = fields.One2many(
        comodel_name='sale.commission.line',
        inverse_name='order_id',
        string='Líneas de Comisión',
        copy=False,
    )

    @api.depends('user_id')
    def _compute_commission_rule_id(self):
        """Obtener regla de comisión por usuario"""
        for order in self:
            if order.user_id:
                rule = self.env['sale.commission.rule'].search(
                    [
                        ('user_id', '=', order.user_id.id),
                        ('active', '=', True),
                    ],
                    limit=1,
                )
                order.commission_rule_id = rule
            else:
                order.commission_rule_id = False

    @api.depends('commission_rule_id')
    def _compute_commission_percent(self):
        """Obtener porcentaje de comisión"""
        for order in self:
            order.commission_percent = (
                order.commission_rule_id.commission_percent
                if order.commission_rule_id
                else 0.0
            )

    @api.depends('amount_total', 'commission_percent')
    def _compute_commission_amount(self):
        """Calcular monto de comisión"""
        for order in self:
            order.commission_amount = (
                order.amount_total * order.commission_percent / 100
            )

    def action_confirm(self):
        """Generar línea de comisión al confirmar"""
        result = super().action_confirm()
        self._create_commission_lines()
        return result

    def _create_commission_lines(self):
        """Crear líneas de comisión"""
        CommissionLine = self.env['sale.commission.line']
        for order in self:
            # Eliminar líneas existentes
            order.commission_line_ids.unlink()
            # Crear nueva línea si hay regla
            if order.commission_rule_id:
                CommissionLine.create(
                    {
                        'order_id': order.id,
                        'rule_id': order.commission_rule_id.id,
                        'state': 'confirmed',
                    }
                )
