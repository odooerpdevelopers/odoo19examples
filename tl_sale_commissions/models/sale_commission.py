from odoo import fields, models


class SaleCommission(models.Model):
    _name = "sale.commission"
    _description = "Sale Commission Rule"
    _order = "name"

    name = fields.Char(required=True)
    user_id = fields.Many2one(
        comodel_name="res.users",
        string="Salesperson",
        required=True,
        domain=[("share", "=", False)],
    )
    commission_percent = fields.Float(
        string="Commission (%)",
        required=True,
        digits=(5, 2),
    )
    active = fields.Boolean(default=True)
    commission_line_ids = fields.One2many(
        comodel_name="sale.commission.line",
        inverse_name="commission_id",
        string="Commission Lines",
    )

    _unique_user = models.Constraint(
        "UNIQUE(user_id, active)",
        "An active commission rule already exists for this salesperson!",
    )
