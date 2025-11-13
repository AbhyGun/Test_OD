import logging
import json
from odoo import http
from odoo.http import request
from odoo.exceptions import AccessError
import hmac
import hashlib
import time

_logger = logging.getLogger(__name__)

API_SECRET = "school_system_api_secret_2025"
TOKEN_EXPIRY = 3600  

def generate_token():
    timestamp = str(int(time.time()))
    token = hmac.new(
        API_SECRET.encode(),
        timestamp.encode(),
        hashlib.sha256
    ).hexdigest()
    return f"{timestamp}:{token}"

def verify_token(token):
    try:
        timestamp_str, sig = token.split(':', 1)
        timestamp = int(timestamp_str)
        now = int(time.time())
        if now - timestamp > TOKEN_EXPIRY:
            return False
        expected_sig = hmac.new(
            API_SECRET.encode(),
            timestamp_str.encode(),
            hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(sig, expected_sig)
    except Exception:
        return False
class SimpleTest(http.Controller):
    @http.route('/api/hello', auth='none', csrf=False)
    def hello(self):
        return http.Response(json.dumps({"hello": "world"}), mimetype='application/json')
class AttendanceAPI(http.Controller):

    @http.route('/api/attendance', type='http', auth='none', methods=['GET'], csrf=False)
    def get_attendance(self, **kwargs):
        token = request.httprequest.headers.get('X-API-TOKEN')
        if not token or not verify_token(token):
            return request.make_response(
                json.dumps({'error': 'Invalid or missing token'}),
                headers={'Content-Type': 'application/json'},
                status=401
            )

        start_date = kwargs.get('start_date')
        end_date = kwargs.get('end_date')
        if not start_date or not end_date:
            return request.make_response(
                json.dumps({'error': 'start_date and end_date required'}),
                headers={'Content-Type': 'application/json'},
                status=400
            )

        domain = [
            ('datetime', '>=', start_date),
            ('datetime', '<=', end_date)
        ]
        records = request.env['api.attendance'].sudo().search(domain)
        data = [{
            'id': r.id,
            'name': r.name,
            'datetime': r.datetime.isoformat(),
            'type': r.type,
            'longitude': r.longitude,
            'latitude': r.latitude
        } for r in records]

        return request.make_response(
            json.dumps({'data': data}),
            headers={'Content-Type': 'application/json'}
        )

    @http.route('/api/attendance', type='http', auth='none', methods=['POST'], csrf=False)
    def create_attendance(self, **kwargs):
        token = request.httprequest.headers.get('X-API-TOKEN')
        if not token or not verify_token(token):
            return request.make_response(
                json.dumps({'error': 'Invalid or missing token'}),
                headers={'Content-Type': 'application/json'},
                status=401
            )

        try:
            data = json.loads(request.httprequest.data)
        except Exception:
            return request.make_response(
                json.dumps({'error': 'Invalid JSON'}),
                headers={'Content-Type': 'application/json'},
                status=400
            )

        required = ['name', 'datetime', 'type']
        for field in required:
            if field not in data:
                return request.make_response(
                    json.dumps({'error': f'Missing field: {field}'}),
                    headers={'Content-Type': 'application/json'},
                    status=400
                )

        try:
            record = request.env['api.attendance'].sudo().create({
                'name': data['name'],
                'datetime': data['datetime'],
                'type': data['type'],
                'longitude': data.get('longitude', 0.0),
                'latitude': data.get('latitude', 0.0),
            })
            return request.make_response(
                json.dumps({'id': record.id, 'status': 'success'}),
                headers={'Content-Type': 'application/json'},
                status=201
            )
        except Exception as e:
            return request.make_response(
                json.dumps({'error': str(e)}),
                headers={'Content-Type': 'application/json'},
                status=500
            )

    @http.route('/api/token', type='http', auth='none', methods=['GET'], csrf=False)
    def get_token(self):
        """Endpoint bantu: generate token (hanya untuk dev/test)"""
        token = generate_token()
        return request.make_response(
            json.dumps({'token': token}),
            headers={'Content-Type': 'application/json'}
        )
    @http.route('/api/test', auth='none', methods=['GET'], csrf=False)
    def test(self):
        return http.Response(
            json.dumps({"status": "Controller is WORKING!"}),
            headers={'Content-Type': 'application/json'}
        )