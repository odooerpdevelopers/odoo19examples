from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = ["sale.order"]

    commission_rule_id = fields.Many2one(
        comodel_name="sale.commission.rule",
        string="Regla de comisión",
        compute="_compute_commission_rule_id",
        store=True,
        readonly=False,
    )
    commission_percent = fields.Float(
        string="% Comisión",
        compute="_compute_commission_fields",
        store=True,
        digits=(5, 2),
    )
    commission_amount = fields.Monetary(
        string="Importe comisión",
        compute="_compute_commission_fields",
        store=True,
        currency_field="currency_id",
    )
    commission_line_ids = fields.One2many(
        comodel_name="sale.commission.line",
        inverse_name="order_id",
        string="Líneas de comisión",
    )

    @api.depends("user_id")
    def _compute_commission_rule_id(self):
        for order in self:
            rule = self.env["sale.commission.rule"].search(
                [
                    ("user_id", "=", order.user_id.id),
                    ("active", "=", True),
                ],
                limit=1,
            )
            order.commission_rule_id = rule

    @api.depends("commission_rule_id", "amount_total")
    def _compute_commission_fields(self):
        for order in self:
            if order.commission_rule_id:
                order.commission_percent = order.commission_rule_id.commission_percent
                order.commission_amount = (
                    order.amount_total
                    * order.commission_rule_id.commission_percent
                    / 100
                )
            else:
                order.commission_percent = 0.0
                order.commission_amount = 0.0

    def action_confirm(self):
        res = super().action_confirm()
        for order in self:
            if order.commission_rule_id:
                existing = order.commission_line_ids.filtered(
                    lambda line: line.rule_id == order.commission_rule_id
                )
                if not existing:
                    self.env["sale.commission.line"].create(
                        {
                            "order_id": order.id,
                            "rule_id": order.commission_rule_id.id,
                            "state": "confirmed",
                        }
                    )
        return res
