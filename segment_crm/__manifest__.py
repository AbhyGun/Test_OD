{
    'name': 'CRM Segment Customization',
    'version': '16.0.1.0.0',
    'category': 'CRM',
    'summary': 'Add customer segment and product segment fields to CRM',
    'author': 'PT Matrica Consulting Service',
    'depends': ['crm'],
    'data': [
        'security/ir.model.access.csv',
        'views/crm_lead_views.xml',
        'views/product_segment_views.xml',
    ],
    'installable': True,
    'application': False,
}