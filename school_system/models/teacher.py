from odoo import fields, models,  api

class Guru(models.Model):
    _name = 'sekolah.guru'
    _description = 'Data Guru'
    _rec_name = 'nm_guru'

    nip = fields.Char(string='NIP', required=True, copy=False)
    nm_guru = fields.Char(string='Nama Guru', required=True)
    jns_kelamin = fields.Selection([
        ('L', 'Laki-laki'),
        ('P', 'Perempuan'),
    ], string='Jenis Kelamin', required=True)
    tgl_lahir = fields.Date(string='Tanggal Lahir')
    tgi_badan = fields.Integer(string='Tinggi Badan (cm)')
    usia = fields.Integer(string='Usia', compute='_compute_usia', store=True)
    no_telp = fields.Char(string='No. Telepon')
    alamat = fields.Text(string='Alamat')
    pendidikan_terakhir = fields.Selection([
        ('SMA', 'SMA'),
        ('D3', 'D3'),
        ('S1', 'S1'),
        ('S2', 'S2'),
        ('S3', 'S3'),
    ], string='Pendidikan Terakhir')
    jurusan = fields.Char(string='Jurusan')
    tahun_lulus = fields.Integer(string='Tahun Lulus')

    @api.depends('tgl_lahir')
    def _compute_usia(self):
        for rec in self:
            rec.usia = (fields.Date.today() - rec.tgl_lahir).days // 365 if rec.tgl_lahir else 0