from odoo import api, fields, models


class SaleCommissionLine(models.Model):
    _name = "sale.commission.line"
    _description = "Línea de comisión generada"
    _order = "order_id desc"

    order_id = fields.Many2one(
        comodel_name="sale.order",
        string="Pedido de venta",
        required=True,
        ondelete="cascade",
    )
    rule_id = fields.Many2one(
        comodel_name="sale.commission.rule",
        string="Regla aplicada",
        required=True,
    )
    user_id = fields.Many2one(
        comodel_name="res.users",
        string="Vendedor",
        related="rule_id.user_id",
        store=True,
    )
    commission_percent = fields.Float(
        string="% Aplicado",
        related="rule_id.commission_percent",
        store=True,
    )
    amount_total = fields.Monetary(
        string="Base (importe pedido)",
        related="order_id.amount_total",
        store=True,
    )
    commission_amount = fields.Monetary(
        string="Importe comisión",
        compute="_compute_commission_amount",
        store=True,
    )
    currency_id = fields.Many2one(
        related="order_id.currency_id",
        store=True,
    )
    state = fields.Selection(
        selection=[
            ("draft", "Borrador"),
            ("confirmed", "Confirmada"),
            ("paid", "Pagada"),
        ],
        string="Estado",
        default="draft",
        required=True,
    )

    @api.depends("amount_total", "commission_percent")
    def _compute_commission_amount(self):
        for line in self:
            line.commission_amount = line.amount_total * line.commission_percent / 100
