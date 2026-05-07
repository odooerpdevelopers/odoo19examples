{
    "name": "TL Sale Commissions",
    "version": "19.0.1.0.0",
    "category": "Sales",
    "author": "TrotonLabs",
    "license": "LGPL-3",
    "depends": ["sale"],
    "data": [
        "security/ir.model.access.csv",
        "views/sale_commission_views.xml",
        "views/sale_commission_line_views.xml",
        "views/sale_order_views.xml",
    ],
    "installable": True,
    "application": False,
}
