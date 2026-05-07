from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    commission_id = fields.Many2one(
        comodel_name="sale.commission",
        string="Commission Rule",
        compute="_compute_commission_id",
        store=True,
        precompute=True,
        readonly=False,
    )
    commission_percent = fields.Float(
        string="Commission (%)",
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
    def _compute_commission_id(self):
        for order in self:
            if order.user_id:
                commission = self.env["sale.commission"].search(
                    [("user_id", "=", order.user_id.id), ("active", "=", True)],
                    limit=1,
                )
                order.commission_id = commission
            else:
                order.commission_id = False

    @api.depends("commission_id")
    def _compute_commission_percent(self):
        for order in self:
            if order.commission_id:
                order.commission_percent = order.commission_id.commission_percent
            else:
                order.commission_percent = 0.0

    @api.depends("amount_untaxed", "commission_percent")
    def _compute_commission_amount(self):
        for order in self:
            order.commission_amount = (
                order.amount_untaxed * order.commission_percent / 100
            )

    def action_confirm(self):
        res = super().action_confirm()
        for order in self:
            if order.commission_id:
                self.env["sale.commission.line"].create(
                    {
                        "order_id": order.id,
                        "commission_id": order.commission_id.id,
                        "state": "confirmed",
                    }
                )
        return res
