from odoo import models, fields

class Attendance(models.Model):
    _name = 'api.attendance'
    _description = 'Attendance Record'

    name = fields.Char(required=True)
    datetime = fields.Datetime(required=True)
    type = fields.Selection([
        ('check_in', 'Check In'),
        ('check_out', 'Check Out')
    ], required=True)
    longitude = fields.Float(digits=(10, 7))
    latitude = fields.Float(digits=(10, 7))