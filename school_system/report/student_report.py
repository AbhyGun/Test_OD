from odoo import models, api
import logging
_logger = logging.getLogger(__name__)

class ReportKartuSiswa(models.AbstractModel):
    _name = 'report.school_system.report_kartu_siswa_template'
    _description = 'Kartu Siswa'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['sekolah.siswa'].browse(docids)
        _logger.warning("DocIDs: %s", docids)
        _logger.warning("Docs: %s", docs.mapped('nm_siswa'))
        return {
            'doc_ids': docs.ids,
            'doc_model': 'sekolah.siswa',
            'docs': docs,
        }