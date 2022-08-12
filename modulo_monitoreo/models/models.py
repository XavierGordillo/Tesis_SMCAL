from odoo import fields, models, api
import requests
from datetime import datetime
from odoo.exceptions import ValidationError


class ResUser(models.Model):
    _inherit = "res.users"
    es_administrador = fields.Boolean(string='Es Administrador', store=True)
    
class Horario(models.Model):
    _name = "mo.horario"
    _description = "Horario de Ejecución del Monitoreo"

    name = fields.Selection(
        selection=[("lunes", "Lunes"), ("martes", "Martes"),
                   ("miercoles", "Miércoles"), ("jueves", "Jueves"), ("viernes", "Viernes"),
                   ("sabado", "Sábado"), ("domingo", "Domingo")], required=True,
        string="Día")
    hora_desde = fields.Float(string='Hora Desde', required=True)
    hora_hasta = fields.Float(string='Hora Hasta', required=True)

    estacion_ids = fields.Many2one("mo.estacion",
                                  string="Estación",
                                  ondelete='cascade')


class Estacion(models.Model):
    _name = "mo.estacion"
    _description = "Estación"

    name = fields.Char(string="Nombre de la Estación", required=True)
    temperatura = fields.Float(string="Temperatura")
    humedad = fields.Float(string="Húmedad")
    co2 = fields.Float(string="Nivel de CO2")
    tvoc = fields.Float(string="TVOC")

    url_servicio = fields.Char(string="Url del servicio", required=True)

    validar = fields.Boolean(default=False, string="Validar Servicio")

    estado = fields.Boolean(default=False, string="Estado")

    horario_id = fields.One2many("mo.horario", "estacion_ids")




    _sql_constrainst = [
        ('name_unique', 'unique (name)',
         "El Nombre de Estación ya Existe")
    ]

    def validarURL(self):
        #Temperatura-Húmedad-Nivel de CO2-TVOC
        url = str(self.url_servicio)
        data = requests.get(url)
        valores = data.text
        aux_seperar = valores.split('-')
        if len(aux_seperar) > 3:
            self.temperatura = aux_seperar[0]
            self.humedad = aux_seperar[1]
            self.co2 = aux_seperar[2]
            self.tvoc = aux_seperar[3]

    def monitorear(self):
        estaciones = self.env["mo.estacion"].search([])
        print("Si entra")
        for estacion in estaciones:
            print(estacion.horario_id.name)
            print("--")
            print(datetime.today().strftime('%A'))
            if str(estacion.horario_id.name) == str(datetime.today().strftime('%A')):
                print("SI entra")
                hora1 = datetime.strptime(estacion.horario_id.hora_desde, "%X").time()
                hora2 = datetime.strptime(estacion.horario_id.hora_hasta, "%X").time()
                hora_act = datetime.now().time()
                print(hora1)
                print(hora2)
                print(hora_act)
                if hora2 > hora1:
                    if hora_act > hora1 and hora_act < hora2:
                        print("Hola")

                #docente.write({'plan_id': plan})
                #self.env.cr.commit()

        



