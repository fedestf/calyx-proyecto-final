import xml.etree.ElementTree as ET

tree = ET.parse(r'Tarea 1\Facturas\factura_uno.xml')

root = tree.getroot()

namespace = {
    'cac': "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2",
    'cbc': "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2"

}
# ejemplo de busqueda trae las id de las boletas

# for x in root.findall('cac:InvoiceLine', namespace):
#     id = x.find('cbc:ID', namespace)

#     print(id.text)


def quitar_punto_string(cantidad):
    s = cantidad
    sin_punto = s.replace(".", "")

    return int(sin_punto)


for x in root.findall('cac:InvoiceLine', namespace):

    id_pedido = x.find('cbc:ID', namespace)
    cantidad = x.find('cbc:InvoicedQuantity', namespace)

    for item in x.findall('cac:Item', namespace):
        nombre = item.find('cbc:Description', namespace)

        for seller_id in item.findall('cac:SellersItemIdentification', namespace):
            id_seller = seller_id.find('cbc:ID', namespace)

        for valor in item.findall('cac:AdditionalItemProperty', namespace):
            valor_item = valor.find('cbc:Value', namespace)
            subtotal = valor.find('cbc:Value', namespace)

    print(id_pedido.text, id_seller.text, nombre.text,
          valor_item.text, quitar_punto_string(cantidad.text), subtotal.text)
