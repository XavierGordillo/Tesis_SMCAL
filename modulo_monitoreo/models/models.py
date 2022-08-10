from odoo import fields, models, api
from odoo.exceptions import ValidationError


class ResUser(models.Model):
    _inherit = "res.users"
    es_administrador = fields.Boolean(string='Es Administrador', store=True)

class Estacion(models.Model):
    _name = "mo.estacion"
    _description = "Estación"

    name = fields.Char(string="Nombre de la EStación", required=True)
    temperatura = fields.Float(string="Temperatura")
    humedad = fields.Float(string="Húmedad")
    co2 = fields.Float(string="Nivel de CO2")
    tvoc = fields.Float(string="TVOC")

    url_servicio = fields.Char(string="Url del servicio", required=True)

    validar = fields.Boolean(default=False, string="Validar Servicio")

    estado = fields.Boolean(default=False, string="Estado")

    _sql_constrainst = [
        ('name_unique', 'unique (name)',
         "El Nombre de Estación ya Existe")
    ]

