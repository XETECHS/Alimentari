# -*- encoding: UTF-8 -*-
##############################################################################

{
	'name': 'Reporte de Ventas y Compras',
	'summary': """Reporte de Ventas y Compras""",
	'version': '15.',
	'description': """Permite Generar Reporte de Ventas y Compras de IVA""",
	'author': 'Luis Aquino --> laquino@xetechs.com',
	'maintainer': 'Github: @juancacorps',
	'website': 'https://www.xetechs.odoo.com',
	'category': 'account',
	'depends': ['account', 'account_reports'],
	'license': 'AGPL-3',
	'assets': {
		'web.assets_common': [
            'reporte_ventas_compras/static/src/css/**/*',
            'reporte_ventas_compras/static/src/less/**/*'
        ]
	},
	'data': [
		'data/paperformat_data.xml',
		'views/product_template_view.xml',
		'views/account_invocie_view.xml',
		'views/views.xml',
		'wizard/wizard_ventas_compras_view.xml',
		'views/ab_reports.xml',
		'views/report_purchase_book_template.xml',
		'views/report_sale_book_template.xml',
	],
	'demo': [],
	'installable': True,
	'auto_install': False,
}
