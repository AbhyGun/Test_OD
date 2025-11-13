from odoo import fields, models

class Kelas(models.Model):
    _name = 'sekolah.kelas'
    _description = 'Data Kelas'
    _rec_name = 'nm_kelas'

    nm_kelas = fields.Char(string='Nama Kelas', required=True)
    jurusan = fields.Char(string='Jurusan')
    wali_kelas_id = fields.Many2one('sekolah.guru', string='Wali Kelas')