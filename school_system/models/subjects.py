from odoo import fields, models

class MataPelajaran(models.Model):
    _name = 'sekolah.mata_pelajaran'
    _description = 'Mata Pelajaran'
    _rec_name = 'nm_mata_pelajaran'

    nm_mata_pelajaran = fields.Char(string='Nama Mata Pelajaran', required=True)
    jurusan = fields.Char(string='Jurusan')
    guru_id = fields.Many2one('sekolah.guru', string='Guru Pengampu')