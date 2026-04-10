from odoo import api, fields, models


class SaleCommissionLine(models.Model):
    _name = "sale.commission.line"
    _description = "Sale Commission Line"
    _order = "id DESC"

    order_id = fields.Many2one(
        comodel_name="sale.order",
        string="Sale Order",
        required=True,
        ondelete="cascade",
    )
    rule_id = fields.Many2one(
        comodel_name="sale.commission.rule",
        string="Commission Rule",
        required=True,
    )
    user_id = fields.Many2one(
        related="rule_id.user_id",
        string="User",
        store=True,
        readonly=True,
    )
    commission_percent = fields.Float(
        related="rule_id.commission_percent",
        string="Commission Percentage",
        store=True,
        readonly=True,
        digits=(5, 2),
    )
    amount_untaxed = fields.Monetary(
        related="order_id.amount_untaxed",
        string="Untaxed Amount",
        store=True,
        readonly=True,
    )
    currency_id = fields.Many2one(
        related="order_id.currency_id",
        string="Currency",
        store=True,
        readonly=True,
    )
    commission_amount = fields.Monetary(
        string="Commission Amount",
        compute="_compute_commission_amount",
        store=True,
        currency_field="currency_id",
    )
    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("confirmed", "Confirmed"),
            ("paid", "Paid"),
        ],
        default="draft",
        string="State",
    )

    @api.depends("amount_untaxed", "commission_percent")
    def _compute_commission_amount(self):
        for line in self:
            line.commission_amount = line.amount_untaxed * line.commission_percent / 100
