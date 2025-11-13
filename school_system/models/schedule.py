from odoo import fields, models

class Jadwal(models.Model):
    _name = 'sekolah.jadwal'
    _description = 'Jadwal Pelajaran'
    _rec_name = 'hari'

    hari = fields.Selection([
        ('Senin', 'Senin'),
        ('Selasa', 'Selasa'),
        ('Rabu', 'Rabu'),
        ('Kamis', 'Kamis'),
        ('Jumat', 'Jumat'),
        ('Sabtu', 'Sabtu'),
    ], string='Hari', required=True)
    jam = fields.Float(string='Jam Ke')
    kelas_id = fields.Many2one('sekolah.kelas', string='Kelas', required=True)
    mata_pelajaran_id = fields.Many2one('sekolah.mata_pelajaran', string='Mata Pelajaran', required=True)