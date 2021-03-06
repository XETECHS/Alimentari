# -*- coding: utf-8 -*-
{
    'name': "alimentari",

    'summary': """
       Aplicación Alimentari""",

    'description': """
       Contiene las funcionalidades adicionales que requiere Alimentari.
    """,

    'author': "Xetechs",
    'website': "https://xetechs.com/",
    'license': "LGPL-3",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','stock','account','sale','purchase'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        # 'views/views.xml',
        # 'views/templates.xml',
        'views/sale_report_templates_inherit.xml',
        'views/report_invoice_inherit.xml',
        'views/product_template_view_inherit.xml',
        'views/account_move_view_inherit.xml',
        'views/purchase_order_view_inherit.xml',    
        'views/stock_picking_view_inherit.xml',
        'views/product_category_form.xml',
        'views/account_invoice_alcochol_inherit.xml',
        
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
