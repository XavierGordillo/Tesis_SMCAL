from odoo import fields, models, api
import requests
from datetime import datetime, timedelta
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
            #periodos = self.env['mo.horario'].search([('id', 'in', estacion.horario_id)])
            for periodo in estacion.horario_id:
                print(periodo.name)
                print("--")
                print(datetime.today().strftime('%A'))
                if str(periodo.name) == str(datetime.today().strftime('%A')):
                    print("SI entra")
                    aux_hora1 = str(periodo.hora_desde).replace(".", ":")
                    aux_hora2 = str(periodo.hora_hasta).replace(".", ":")
                    print(aux_hora1)
                    print(aux_hora2)
                    hora1 = datetime.strptime(aux_hora1+":00", "%X").time()
                    hora2 = datetime.strptime(aux_hora2+":00", "%X").time()
                    hora_act = datetime.now().time()
                    print(hora1)
                    print(hora2)
                    print(hora_act)
                    if hora2 > hora1:
                        print("mayor")
                        if hora_act > hora1 and hora_act < hora2:
                            print("tambien")
                            self.refrescarSensor(estacion)


    def refrescarSensor(self, estacion):
        print("maosada")
        url = str(estacion.url_servicio)
        print(url)
        data = requests.get(url)
        valores = data.text
        aux_seperar = valores.split('-')
        if len(aux_seperar) > 3:
            estacion.write({'temperatura': aux_seperar[0]})
            estacion.write({'humedad': aux_seperar[1]})
            estacion.write({'co2': aux_seperar[2]})
            estacion.write({'tvoc': aux_seperar[3]})
            estacion.env.cr.commit()


    def notificar(self):
        print("Entra a notificar")
        estaciones = self.env["mo.estacion"].search([])
        for estacion in estaciones:
            if estacion.co2 > 700 and estacion.humedad>=50 and  estacion.humedad<=60 \
                    and estacion.temperatura>=17 and estacion.temperatura<=24:
                print("Posiblemente exista covid")
            else:
                print("Todo bn")


