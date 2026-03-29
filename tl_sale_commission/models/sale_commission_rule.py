from odoo import fields, models


class SaleCommissionRule(models.Model):
    _name = "sale.commission.rule"
    _description = "Sale Commission Rule"

    name = fields.Char(
        string="Name",
        required=True,
    )
    user_id = fields.Many2one(
        comodel_name="res.users",
        string="User",
        required=True,
        domain=[("share", "=", False)],
    )
    commission_percent = fields.Float(
        string="Commission Percentage",
        required=True,
        digits=(5, 2),
    )
    active = fields.Boolean(
        default=True,
    )
    commission_line_ids = fields.One2many(
        comodel_name="sale.commission.line",
        inverse_name="rule_id",
        string="Commission Lines",
    )

    _unique_user = models.Constraint(
        "UNIQUE(user_id, active)",
        "User Commission Rule must be unique when active!",
    )
