import xml.etree.ElementTree as ET
import glob
import json
from funciones import pdf_to_csv, dict_from_csv, validacion_facturas_y_json_a_cargar

# pdf_to_csv(a_convertir=r'Tarea 1\lista_precios.pdf',
#            destino=r'Tarea 1\lista_precios.csv',
#            paginas="all")

# dict_from_csv(csv=r'Tarea 1\lista_precios.csv')

ruta = r'Tarea 1\Facturas\*.xml'
lista_facturas_xml = glob.glob(ruta)

lista_facturas = []

facturas = {}

for factura in lista_facturas_xml:

    tree = ET.parse(factura)

    root = tree.getroot()

    namespace = {
        'cac': "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
        'cbc': "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",

    }

    id_factura = root.find('cbc:ID', namespace)
    fecha = root.find('cbc:IssueDate', namespace)

    lista_facturas.append(f'{id_factura.text}')
    facturas[f'{id_factura.text}'] = []

    for x in root.findall('cac:InvoiceLine', namespace):

        for item in x.findall('cac:Item', namespace):

            nombre = item.find('cbc:Description', namespace)

            for seller_id in item.findall('cac:SellersItemIdentification', namespace):
                id_seller = seller_id.find('cbc:ID', namespace)

        for valor in x.findall('cac:Price', namespace):

            valor_item = valor.find('cbc:UnitPrice', namespace)
            cantidad_item = valor.find('cbc:BaseQuantity', namespace)

            valor = float(valor_item.text)
            cantidad = float(cantidad_item.text)

        subtotal = valor*cantidad
        facturas[f'{id_factura.text}'].append({'fecha': fecha.text,
                                               'id_seller': id_seller.text,
                                               'nombre': nombre.text,
                                               'valor': valor,
                                               'cantidad': cantidad,
                                               'subtotal': subtotal})

        with open(r'Tarea 1\facturas.json', 'w') as file:
            json.dump(facturas, file, indent=4)

dic_facturas = {}
with open(r'Tarea 1\facturas.json') as data_file:
    dic_facturas = json.load(data_file)

lista_bool_nombre = []
lista_bool_valor = []
facturas_carga = {}
facturas_erroneas = []

for factura in lista_facturas:

    facturas_carga[f'{factura}'] = []

    for key, value in dic_facturas.items():

        if factura == key:
            for key in dic_facturas[f'{factura}']:
                # print(factura, key['nombre'], key['valor'])
                if key['nombre'] in [keyd for keyd in dict_from_csv(csv=r'Tarea 1\lista_precios.csv').keys()]:
                    lista_bool_nombre.append(True)

                    if key['valor'] in [keyv for keyv in dict_from_csv(csv=r'Tarea 1\lista_precios.csv').values()]:

                        subtotal_verificador = key['valor']*key['cantidad']

                        if key['subtotal'] == subtotal_verificador:
                            lista_bool_valor.append(True)

            if len(lista_bool_nombre) == len(lista_bool_valor):

                print(f"valores ok en la factura {factura}")

                for key in dic_facturas[f'{factura}']:

                    facturas_carga[f'{factura}'].append({'fecha': key['fecha'],
                                                         'id_seller': key['id_seller'],
                                                         'nombre': key['nombre'],
                                                         'valor': key['valor'],
                                                         'cantidad': key['cantidad'],
                                                         'subtotal': key['subtotal']},)
            else:
                print(f"valores erroneos en la factura {factura}")
                facturas_erroneas.append(factura)
            with open(r'Tarea 1\facturas_a_cargar.json', 'w') as file:
                json.dump(facturas_carga, file, indent=4)
            lista_bool_valor.clear()
            lista_bool_nombre.clear()

dic_facturas_a_cargar = {}
with open(r'Tarea 1\facturas_a_cargar.json') as data_file:
    dic_facturas_a_cargar = json.load(data_file)

for key, value in dic_facturas_a_cargar.items():

    if value != []:
        id = key
        fecha = [value['fecha'] for value in dic_facturas_a_cargar[f'{id}']]
        dia = str(fecha[0])[8::1]
        mes = str(fecha[0])[5:7:1]
        año = str(fecha[0])[0:4:1]
        print(key, dia, mes, año)

        for value in dic_facturas_a_cargar[f'{id}']:

            id_seller = value['id_seller']
            nombre = value['nombre']
            valor = int(value['valor'])
            cantidad = str(value['cantidad']).replace('.', ',')
            subtotal = int(value['subtotal'])

            print(id_seller, nombre, valor, cantidad, subtotal)
