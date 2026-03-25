# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SaleCommissionRule(models.Model):
    _name = "sale.commission.rule"
    _description = "Regla de Comisión de Venta"
    _order = "user_id, id"

    name = fields.Char(
        string="Nombre",
        required=True,
    )
    user_id = fields.Many2one(
        comodel_name="res.users",
        string="Usuario",
        required=True,
        domain=[("internal", "=", True)],
        help="Usuario interno asignado a esta regla de comisión",
    )
    commission_percent = fields.Float(
        string="Porcentaje de Comisión",
        required=True,
        digits=(5, 2),
        help="Porcentaje de comisión a aplicar",
    )
    active = fields.Boolean(
        string="Activo",
        default=True,
    )
    commission_line_ids = fields.One2many(
        comodel_name="sale.commission.line",
        inverse_name="rule_id",
        string="Líneas de Comisión",
        copy=False,
    )

    _sql_constraints = [
        (
            "unique_user_active",
            "UNIQUE(user_id, active) WHERE active = true",
            "Solo puede haber una regla activa por usuario",
        ),
    ]

    @api.constrains("commission_percent")
    def _check_commission_percent(self):
        """Validar que el porcentaje sea positivo"""
        for record in self:
            if record.commission_percent < 0:
                raise models.ValidationError(
                    "El porcentaje de comisión no puede ser negativo"
                )
