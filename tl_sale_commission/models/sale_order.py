from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = ["sale.order"]

    commission_rule_id = fields.Many2one(
        comodel_name="sale.commission.rule",
        string="Commission Rule",
        compute="_compute_commission_rule_id",
        store=True,
        precompute=True,
        readonly=False,
    )
    commission_percent = fields.Float(
        string="Commission Percentage",
        compute="_compute_commission_percent",
        store=True,
        digits=(5, 2),
    )
    commission_amount = fields.Monetary(
        string="Commission Amount",
        compute="_compute_commission_amount",
        store=True,
        currency_field="currency_id",
    )
    commission_line_ids = fields.One2many(
        comodel_name="sale.commission.line",
        inverse_name="order_id",
        string="Commission Lines",
    )

    @api.depends("user_id")
    def _compute_commission_rule_id(self):
        for order in self:
            if order.user_id:
                commission_rule = self.env["sale.commission.rule"].search(
                    [
                        ("user_id", "=", order.user_id.id),
                        ("active", "=", True),
                    ],
                    limit=1,
                )
                order.commission_rule_id = commission_rule
            else:
                order.commission_rule_id = False

    @api.depends("commission_rule_id")
    def _compute_commission_percent(self):
        for order in self:
            if order.commission_rule_id:
                order.commission_percent = order.commission_rule_id.commission_percent
            else:
                order.commission_percent = 0.0

    @api.depends("amount_total", "commission_percent")
    def _compute_commission_amount(self):
        for order in self:
            c_percent = order.commission_percent
            order.commission_amount = order.amount_untaxed * c_percent / 100

    def action_confirm(self):
        result = super().action_confirm()
        for order in self:
            if order.commission_rule_id:
                self.env["sale.commission.line"].create(
                    [
                        {
                            "order_id": order.id,
                            "rule_id": order.commission_rule_id.id,
                            "state": "confirmed",
                        }
                    ]
                )
        return result
