from odoo import api, fields, models
import base64
import qrcode
from io import BytesIO

class Siswa(models.Model):
    _name = 'sekolah.siswa'
    _description = 'Data Siswa'
    _rec_name = 'nm_siswa'
    _order = 'nis'

    nis = fields.Char(string='NIS', required=True, copy=False)
    nm_siswa = fields.Char(string='Nama Siswa', required=True)
    jns_kelamin = fields.Selection([
        ('L', 'Laki-laki'),
        ('P', 'Perempuan'),
    ], string='Jenis Kelamin', required=True)
    tgl_lahir = fields.Date(string='Tanggal Lahir')
    usia = fields.Integer(string='Usia', compute='_compute_usia', store=True)
    foto = fields.Binary(string='Foto')
    agama = fields.Char(string='Agama')
    nm_ayah = fields.Char(string='Nama Ayah')
    nm_ibu = fields.Char(string='Nama Ibu')
    alamat = fields.Text(string='Alamat')

    kelas_id = fields.Many2one('sekolah.kelas', string='Kelas', required=True)

  
    foto = fields.Binary(string='Foto', attachment=True)
    qr_code = fields.Binary(string='QR Code', compute='_generate_qr', store=True, attachment=True)
    foto_pdf = fields.Binary(string='Foto for PDF', compute='_compute_foto_pdf', store=True, attachment=True)

    @api.depends('tgl_lahir')
    def _compute_usia(self):
        for rec in self:
            rec.usia = (fields.Date.today() - rec.tgl_lahir).days // 365 if rec.tgl_lahir else 0

    @api.depends('nis')
    def _generate_qr(self):
        for rec in self:
            if rec.nis:
                qr = qrcode.make(rec.nis)
                buffer = BytesIO()
                qr.save(buffer, format='PNG')
                rec.qr_code = base64.b64encode(buffer.getvalue())
            else:
                rec.qr_code = False 
    @api.depends('foto')
    def _compute_foto_pdf(self):
        for rec in self:
            if rec.foto:
                try:
                    # Buat decode, soalnya saya ada image yang pakai webp
                    image_data = base64.b64decode(rec.foto)
                    image = Image.open(io.BytesIO(image_data))

                    if image.mode in ('RGBA', 'LA', 'P'):
                        background = Image.new('RGB', image.size, (255, 255, 255))
                        if image.mode == 'P':
                            image = image.convert('RGBA')
                        background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
                        image = background
                    elif image.mode != 'RGB':
                        image = image.convert('RGB')

                    # pilihan ini antara save as nya sebagai PEG or PNG
                    buffer = io.BytesIO()
                    image.save(buffer, format='JPEG', quality=90)  
                    rec.foto_pdf = base64.b64encode(buffer.getvalue())
                except Exception as e:
                    rec.foto_pdf = rec.foto  
                    # _logger.warning("Failed to convert foto to JPEG: %s", e)
            else:
                rec.foto_pdf = False