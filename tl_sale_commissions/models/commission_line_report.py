from odoo import api, models


class CommissionLineReport(models.AbstractModel):
    _name = "report.tl_sale_commissions.commission_line_report"
    _description = "Sale Commissions Report"

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env["sale.commission.line"].browse(docids)
        docs = docs.sorted(key=lambda l: (l.user_id.name or "", l.id))

        group_data = []
        current_user = None
        current_lines = self.env["sale.commission.line"]

        for line in docs:
            if line.user_id != current_user:
                if current_lines:
                    group_data.append(
                        {
                            "user": current_user,
                            "lines": current_lines,
                            "total_untaxed": sum(
                                current_lines.mapped("amount_untaxed")
                            ),
                            "total_commission": sum(
                                current_lines.mapped("commission_amount")
                            ),
                            "count": len(current_lines),
                        }
                    )
                current_user = line.user_id
                current_lines = self.env["sale.commission.line"]
            current_lines += line

        if current_lines:
            group_data.append(
                {
                    "user": current_user,
                    "lines": current_lines,
                    "total_untaxed": sum(current_lines.mapped("amount_untaxed")),
                    "total_commission": sum(current_lines.mapped("commission_amount")),
                    "count": len(current_lines),
                }
            )

        grand_untaxed = sum(docs.mapped("amount_untaxed"))
        grand_commission = sum(docs.mapped("commission_amount"))

        return {
            "doc_ids": docids,
            "doc_model": "sale.commission.line",
            "docs": docs,
            "group_data": group_data,
            "grand_untaxed": grand_untaxed,
            "grand_commission": grand_commission,
            "grand_count": len(docs),
        }
