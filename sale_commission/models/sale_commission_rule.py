from odoo import fields, models


class SaleCommissionRule(models.Model):
    _name = "sale.commission.rule"
    _description = "Regla de comisión de vendedor"
    _order = "user_id, id"

    name = fields.Char(
        string="Nombre",
        required=True,
    )
    user_id = fields.Many2one(
        comodel_name="res.users",
        string="Vendedor",
        required=True,
        domain=[("share", "=", False)],
    )
    commission_percent = fields.Float(
        string="Porcentaje (%)",
        required=True,
        digits=(5, 2),
    )
    active = fields.Boolean(
        string="Activo",
        default=True,
    )
    commission_line_ids = fields.One2many(
        comodel_name="sale.commission.line",
        inverse_name="rule_id",
        string="Histórico de comisiones",
    )

    _sql_constraints = [
        models.Constraint(
            "unique_user_active",
            "UNIQUE(user_id, active)",
            "Ya existe una regla activa para este vendedor.",
        ),
    ]
