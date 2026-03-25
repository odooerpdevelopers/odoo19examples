{
    "name": "Sale Commission",
    "version": "19.0.1.0.0",
    "summary": "Comisiones de vendedor sobre pedidos de venta",
    "author": "TrotonLabs",
    "website": "https://trotonlabs.com",
    "category": "Sales",
    "license": "LGPL-3",
    "depends": ["sale"],
    "data": [
        "security/ir.model.access.csv",
        "views/sale_commission_rule_views.xml",
        "views/sale_order_views.xml",
    ],
    "installable": True,
    "application": False,
}
