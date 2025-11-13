{
    'name': 'Sale & Purchase Reporting',
    'version': '1.0',
    'category': 'Reporting',
    'summary': 'Wizard to generate Excel report of product sales/purchases',
    'author': 'PT Matrica Consulting Service',
    'depends': ['sale', 'purchase'],
    'data': [
        'views/sale_purchase_report_views.xml',
    ],
    'installable': True,
    'application': False,
}