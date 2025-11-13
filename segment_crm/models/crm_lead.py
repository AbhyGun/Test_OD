from odoo import api, fields, models

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    is_new_customer = fields.Boolean(string='Pelanggan Baru')
    customer_segment = fields.Selection([
        ('konstruksi', 'Konstruksi'),
        ('perbankan', 'Perbankan'),
        ('pemerintah', 'Pemerintah'),
        ('bumd_bumn', 'BUMD/BUMN'),
        ('kementrian', 'Kementrian'),
        ('swasta_lainnya', 'Swasta Lainnya'),
    ], string='Segment Pelanggan')
    customer_segment_other = fields.Char(string='Segment Pelanggan Lainnya')
    product_segment_id = fields.Many2one('product.segment', string='Segment Product')
    task_progress_ids = fields.One2many('crm.task.progress', 'lead_id', string='Task Progress')

    @api.onchange('customer_segment')
    def _onchange_customer_segment(self):
        if self.customer_segment != 'swasta_lainnya':
            self.customer_segment_other = False


class CrmTaskProgress(models.Model):
    _name = 'crm.task.progress'
    _description = 'CRM Task Progress'

    lead_id = fields.Many2one('crm.lead', string='Lead')
    task = fields.Char(string='Task')
    deadline = fields.Date(string='Deadline')
    status = fields.Selection([
        ('to_do', 'To Do'),
        ('progress', 'Progress'),
        ('done', 'Done'),
    ], string='Status', default='to_do')