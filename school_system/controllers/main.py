from odoo import http
from odoo.http import request
import base64

class SekolahController(http.Controller):

    @http.route('/school/image/<model("sekolah.siswa"):student>/<string:field>',
                type='http', auth='public', methods=['GET'])
    def student_image(self, student, field, **kw):
        """ field can be 'foto_pdf' or 'qr_code' """
        bin_data = student[field] or b''
        headers = [
            ('Content-Type', 'image/png' if field == 'qr_code' else 'image/jpeg'),
            ('Content-Length', len(bin_data))
        ]
        return request.make_response(bin_data, headers)