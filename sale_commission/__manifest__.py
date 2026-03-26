{
    "name": "Comisiones de Venta",
    "version": "1.0.0",
    "category": "Sales",
    "summary": "Gestión de comisiones de vendedores",
    "description": "Módulo para gestionar comisiones de vendedores en pedidos",
    "author": "Your Company",
    "depends": ["sale"],
    "data": [
        "security/ir.model.access.csv",
        "views/sale_commission_rule_views.xml",
        "views/sale_commission_line_views.xml",
        "views/sale_order_views.xml",
    ],
    "installable": True,
    "application": False,
    "license": "LGPL-3",
}
