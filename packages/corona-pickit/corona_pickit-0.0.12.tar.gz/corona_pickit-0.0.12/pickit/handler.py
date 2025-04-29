# -*- coding: utf-8 -*-
import logging
import datetime

from pickit.connector import Connector, ConnectorException
from pickit.settings import api_settings

logger = logging.getLogger(__name__)


class PickitHandler:
    """
        Handler to connect with Pickit
    """

    def __init__(self,
        base_url=api_settings.PICKIT['BASE_URL'],
        api_key=api_settings.PICKIT['API_KEY'],
        token=api_settings.PICKIT['TOKEN'],
        verify=True, **kwargs):
    
        self.base_url = kwargs.pop('base_url', base_url)
        self.api_key = kwargs.pop('api_key', api_key)
        self.token = kwargs.pop('token', token)
        self.verify = kwargs.pop('verify', verify)
        
        headers = {
            'apiKey': self.api_key,
            'token': self.token,
            'Content-Type': 'application/json'
        }

        self.connector = Connector(headers=headers, verify_ssl=self.verify)

    def get_shipping_label(self):
        raise NotImplementedError(
            'get_shipping_label is not a method implemented for PickitHandler')

    def get_default_payload(self, instance):
        split_name = instance.customer.full_name.split()
        rut, _ = instance.customer.rut.split('-')
        first_name = split_name[0]
        last_name = split_name[1] if len(split_name) > 1 else ''
        
        products = []

        for item in instance.items:  # O si es un dict: instance.get('items', [])
            product = {
                "name": item.name,
                "weight": {
                    "amount": 1001,
                    "unit": "g"
                },
                "length": {
                    "amount": 0,
                    "unit": "cm"
                },
                "height": {
                    "amount": 0,
                    "unit": "cm"
                },
                "width": {
                    "amount": 0,
                    "unit": "cm"
                },
                "price": int(float(item.quantity) * float(item.price)),
                "sku": item.sku,
                "amount": int(item.quantity),
                "useSerialNumber": False,
                "serialNumber": "",
                "image": None
            }
        products.append(product)
        
        payload = {
            "budgetPetition": {
                "serviceType": "PP",
                "workflowTag": "dispatch",
                "operationType": 1,
                "retailer": {
                    "tokenId": api_settings.PICKIT['TOKEN']
                },
                "products": products,
                "sla": {
                    "id": 1
                },
                "customer": {
                    "name": first_name,
                    "lastName": last_name,
                    "pid": rut,
                    "email": instance.customer.email or "EMAIL@PICKIT.COM",
                    "phone": instance.customer.phone,
                    "address": {
                        "address": instance.address.street,
                        "streetNumber": instance.address.number,
                        "province": instance.region.name,
                        "postalCode": instance.commune.zone_code,
                        "city": instance.location.name,
                        "department": "",
                        "neighborhood": "",
                        "floor": "",
                        "apartment": instance.address.unit or "",
                        "country": "Chile",
                        "latitude": "",
                        "longitude": "",
                        "observations": ""
                    }
                },
                "pointId": int(instance.agency_id)  # Reemplazar con valor dinámico si aplica
            },
            "trakingInfo": {
                "order": instance.reference,
                "shipment": instance.reference
            },
            "firstState": 1,
            "packageAmount": 1,
            "observations": ""
        }

        return payload

    def create_shipping(self, data):
        """
        This method generates a Pickit shipping.
        """
        url = f'{self.base_url}'
        headers = {
            'Content-Type': 'application/json',
            'apiKey': self.api_key,
            'token': self.token,
        }
        try:
            response = self.connector.post(url, data, headers=headers)
            logger.info(response)

            if 'message' in response and 'context' in response:
                raise ConnectorException(
                    response.get('message', 'Unknown error'),
                    str(response.get('context', '')),
                    400
                )

            response.update({
                'tracking_number': int(response['pickitCode']),
                'tracking_url': int(response['urlTracking']),
            })
            return response

        except ConnectorException as error:
            logger.error(error)
            raise ConnectorException(error.message, error.description, error.code) from error

    def get_tracking(self, identifier):
        raise NotImplementedError(
            'get_tracking is not a method implemented for PickitHandler')

    def get_events(self, raw_data):
        """
            This method obtain array events.
            structure:
            {
                "codigo":227569,
                "ubicacionActual":"326",
                "numeroOrdenFlete":959284399,
                "folio":724175058,
                "tipoDocumento":4,
                "estadoMicro":3,
                "estadoMacro":2,
                "nombreEstadoHomologado":"RECIBIDO EN PICKIT",
                "reIntentoWebhook":0,
                "codCiudadDestino":266,
                "tripulacion":null,
                "rutEmpresa":76499449,
                "maquina":null,
                "urlImagen":"",
                "ciudadDestino":"SANTIAGO",
                "estadoEnReparto":0,
                "encargosTotales":1,
                "fechaHoraEvento":1632754923322,
                "codigoEstadoHomologado":"RECIBIDO EN PICKIT",
                "descripcionEstado":"RECIBIDO EN PICKIT",
                "latitud":"0",
                "longitud":"0",
                "rutRecibe":0,
                "dvRecibe":null,
                "nombreRecibe":null,
                "tipoDevolucion":null,
                "codigoInternoEstado":2,
                "codigoAgenciaDestino":1053,
                "intePersonalizada":0,
                "inteBeetrack":0,"inteWebhook":1,
                "reIntentoPersonalizada":0,
                "reIntentoBeetrack":0,
                "saludAcusoPersonalizada":0,
                "saludAcusoBeetrack":0,
                "saludAcusoWebhook":0,
                "ctacteNumero":"41966"
            }
            return [{
                'city': 'Santiago',
                'state': 'RM',
                'description': 'Llego al almacén',
                'date': '12/12/2021'
            }]
        """
        date = datetime.datetime.now()
        return [{
                'city': '',
                'state': '',
                'description': raw_data.get('descripcionEstado'),
                'date': date.strftime('%d/%m/%Y')
            }]

    def get_status(self, raw_data):
        """
            This method returns the status of the order and "is_delivered".
            structure:
            {
                "codigo":227569,
                "ubicacionActual":"326",
                "numeroOrdenFlete":959284399,
                "folio":724175058,
                "tipoDocumento":4,
                "estadoMicro":3,
                "estadoMacro":2,
                "nombreEstadoHomologado":"RECIBIDO EN PICKIT",
                "reIntentoWebhook":0,
                "codCiudadDestino":266,
                "tripulacion":null,
                "rutEmpresa":76499449,
                "maquina":null,
                "urlImagen":"",
                "ciudadDestino":"SANTIAGO",
                "estadoEnReparto":0,
                "encargosTotales":1,
                "fechaHoraEvento":1632754923322,
                "codigoEstadoHomologado":"RECIBIDO EN PICKIT",
                "descripcionEstado":"RECIBIDO EN PICKIT",
                "latitud":"0",
                "longitud":"0",
                "rutRecibe":0,
                "dvRecibe":null,
                "nombreRecibe":null,
                "tipoDevolucion":null,
                "codigoInternoEstado":2,
                "codigoAgenciaDestino":1053,
                "intePersonalizada":0,
                "inteBeetrack":0,"inteWebhook":1,
                "reIntentoPersonalizada":0,
                "reIntentoBeetrack":0,
                "saludAcusoPersonalizada":0,
                "saludAcusoBeetrack":0,
                "saludAcusoWebhook":0,
                "ctacteNumero":"41966"
            }

            status : ['EN BODEGA CLIENTE', 'RECIBIDO EN PICKIT', 'EN TRANSITO A DESTINO', 'RECIBIDO EN AGENCIA DESTINO',
                       'EN REPARTO A DOMICILIO', 'ENTREGADO', 'NO ENTREGADO', 'PENDIENTE', 'CERRADO CON EXCEPCION',
                       'REDESTINADO', 'ANULADO']
            response: ('ENTREGADO', True)
        """

        status = raw_data.get('nombreEstadoHomologado')
        is_delivered = False

        if status.upper() == 'ENTREGADO':
            is_delivered = True

        return status, is_delivered
