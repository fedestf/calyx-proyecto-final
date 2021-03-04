import xml.etree.ElementTree as ET
import glob
import json

ruta = r'Tarea 1\Facturas\*.xml'
lista_xml = glob.glob(ruta)

lista_facturas = []
lista_diccionarios = []
facturas = {}


for factura in lista_xml:

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

        subtotal = float(valor_item.text)*float(cantidad_item.text)

        facturas[f'{id_factura.text}'].append({'id_seller': f'{id_seller.text}', 'nombre': f'{nombre.text}',
                                               'valor': f'{float(valor_item.text)}', 'cantidad': f'{float(cantidad_item.text)}', 'subtotal': f'{subtotal}'})

        # print(id_seller.text, nombre.text,
        #     float(valor_item.text), float(cantidad_item.text), subtotal)

dic_prueba = {}
with open('data.json') as data_file:
    dic_prueba = json.load(data_file)

for key, value in dic_prueba.items():
    print(key, value)
    print("\n")
