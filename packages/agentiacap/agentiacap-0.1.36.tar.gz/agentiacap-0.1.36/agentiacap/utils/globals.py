from typing_extensions import Annotated, TypedDict
from pydantic import BaseModel, Field
from typing import Optional
from typing import List

### Clases reutilizables ###
class MailSchema(TypedDict):
    cuerpo_original:str
    asunto:Annotated[str, ...]
    cuerpo:Annotated[str, ...]
    adjuntos:Annotated[list, ...]
    categoria:Annotated[str, ...]
    extracciones:Annotated[list, ...]
    tokens:Annotated[int, ...]
    
class Result(TypedDict):
    categoria:Annotated[str, ...]
    extractions:Annotated[list, ...]
    tokens:Annotated[int, ...]

# Schemas de entrada y salida
class InputSchema(TypedDict):
    asunto:Annotated[str, ...]
    cuerpo:Annotated[str, ...]
    adjuntos:Annotated[list, ...]

class OutputSchema(TypedDict):
    result: Annotated[dict, ...]

class Retencion(TypedDict):
    es_nota_modelo: bool
    datos_completos: bool
    datos: str
    firmada: bool


class SapReg(BaseModel):

    invoice: Optional[str] = Field(
        description='Dato ubicado en la columna "Referencia" y cumple con ser un numero con el formato ddddAdddddddd'
    )
    date: Optional[str] = Field(
        description='Dato ubicado en la columna "FechaDoc" y cumple con ser una fecha formato dd.MM.yyyy'
    )
    due_date: Optional[str] = Field(
        description='Dato ubicado en la columna "Vence El" y cumple con ser una fecha formato dd.MM.yyyy'
    )
    purchase_number: Optional[str] = Field(
        description='Dato ubicado en la columna "Nº doc." y cumple con ser un numero de 10 digitos'
    )
    op_date: Optional[str] = Field(
        description='Dato ubicado en la columna "Fecha doc." y representa la fecha de purchase_number'
    )
    comp_doc: Optional[str] = Field(
        description='Dato ubicado en la columna "Doc. comp." y representa la fecha de purchase_number'
    )
    comp_date: Optional[str] = Field(
        description='Dato ubicado en la columna "Compens." y representa la fecha de purchase_number'
    )
    found: Optional[bool] = Field(
        description='Indica si se encontró el purchase_number. Por defecto es False'
    )
    overdue: Optional[bool] = Field(
        description='Indica si True si la fecha actual es mayor a la fecha de due_date. Por defecto es False'
    )

class SapTable(BaseModel):
    """
    A class representing a table of invoices with multiple rows.
    
    Attributes:
        invoices: A list of Invoice objects.
    """
    invoices: List[SapReg]

    @staticmethod
    def example():
        """
        Creates an empty example InvoiceTable object.

        Returns:
            InvoiceTable: An empty InvoiceTable object with no invoices.
        """
        return SapTable(invoices=[])

### Variables Globales ###

categories = [
    "Categoría: Alta de usuario, Descripción: Se suele pedir explícitamente en el asunto o en el cuerpo del mail. Sujeto a palabras claves dentro del contexto de la generación o gestión de un nuevo usuario.",
    "Categoría: Error de registración, Descripción: el reclamo siempre es por fechas de vencimiento mal aplicadas. Sujeto al contexto en que el proveedor reclama una mala asignación de la fecha de vencimiento de su factura en el sistema.", 
    "Categoría: Impresión de NC/ND, Descripción: Ahora se llama “Multas”. Sujeto a palabras clave relacionadas con Multas. Sujeto al contexto en que se reclama o consulta por diferencias en el pago . ", 
    "Categoría: Impresión de OP y/o Retenciones, Descripción: Suele ser una solicitud o pedido de ordenes de pago (OP) o retenciones. Suele estar explicito en el asunto o en el cuerpo del mail un mensaje pidiendo retenciones/OP.",
    "Categoría: Pedido devolución retenciones, Descripción: Suele estar explicito en el asunto o cuerpo del mail. Sujeto a palabras clave relacionadas con una devolución o reintegro de una retención. También se suele hacer mención con frecuencia que se envía una nota o se adjunta una nota solicitando a la devolución del monto retenido.",
    "Categoría: Problemas de acceso, Descripción: Sujeto al contexto en que se reclama por no poder acceder a facturar u obtener información de una factura. No se solicita información de una factura solo se reclama el acceso al sistema.", 
    "Categoría: Otras consultas, Descripción: Consultas generales que no encajan en ninguna de las categorías."
    "Categoría: Estado de facturas, Descripción: Consultas sobre estado de facturas, facturas pendientes, facturas vencidas, facturas impagas, facturas no cobradas, facturas rechazadas (o que se haga alguna mención a algún tipo de rechazo) o que puede estar rechazadas (Sujeto a contexto en que se pide motivo del rechazo de una factura), validar el estado de presentación de una factura para saber si se encuentra bien cargada o aún no se efectuó este paso.",
    "Categoría: Estado de cuenta, Descripción: Se consulta y/o informa el estado de la cuenta para conocer deudas o saldos a favor."
]

fields_to_extract = [
    "VendorName",
    "CustomerName",
    "CustomerTaxId",
    "CustomerCodSap",
    "VendorTaxId",
    "CustomerAddress",
    "InvoiceId",
    "InvoiceDate",
    "InvoiceTotal",
    "PurchaseOrderNumber",
    "Signed"
]

lista_sociedades = [
    {'Nombre Soc SAP': '', 'Código SAP': '', 'Estado': '', 'CUIT': '', 'Nombre en AFIP': ''}, 
    {'Nombre Soc SAP': 'A - EVANGELISTA S.A.', 'Código SAP': '478', 'Estado': 'Activa', 'CUIT': '30685218190', 'Nombre en AFIP': 'A EVANGELISTA S A'}, 
    {'Nombre Soc SAP': 'AESA', 'Código SAP': '478', 'Estado': 'Activa', 'CUIT': '30685218190', 'Nombre en AFIP': 'A EVANGELISTA S A'}, 
    {'Nombre Soc SAP': 'YPF GAS SOCIEDAD ANONIMA', 'Código SAP': '522', 'Estado': 'Activa', 'CUIT': '30515488479', 'Nombre en AFIP': 'YPF GAS SOCIEDAD ANONIMA'}, 
    {'Nombre Soc SAP': 'YACIMIENTO LA VENTANA YPF S.A.', 'Código SAP': '571', 'Estado': 'Activa', 'CUIT': '30652671418', 'Nombre en AFIP': 'YACIMIENTO LA VENTANA YPF SA SINOPEC ARGENTINA EXPLORATION AND PRODUCTION INC UTE'}, 
    {'Nombre Soc SAP': 'YPF SA IATE SA UTE', 'Código SAP': '575', 'Estado': 'Activa', 'CUIT': '30656820477', 'Nombre en AFIP': 'YPF S.A IATE S.A UTE          '}, 
    {'Nombre Soc SAP': 'YPF S.A.', 'Código SAP': '620', 'Estado': 'Activa', 'CUIT': '30546689979', 'Nombre en AFIP': 'YPF SOCIEDAD ANONIMA'},
    {'Nombre Soc SAP': 'OPESSA', 'Código SAP': '680', 'Estado': 'Activa', 'CUIT': '30678774495', 'Nombre en AFIP': 'OPERADORA DE ESTACIONES DE SERVICIO SOCIEDAD ANONIMA'}, 
    {'Nombre Soc SAP': 'ACUER DE OPER CONJUN EL LIMITE', 'Código SAP': '781', 'Estado': 'Activa', 'CUIT': '30687155242', 'Nombre en AFIP': 'ACUERDO DE OPERAC CONJUNTAS EL LIMITE'}, 
    {'Nombre Soc SAP': 'FUNDACION YPF', 'Código SAP': '789', 'Estado': 'Activa', 'CUIT': '30691548054', 'Nombre en AFIP': 'FUNDACION YPF'}, 
    {'Nombre Soc SAP': 'LLANCANELO', 'Código SAP': '797', 'Estado': 'Activa', 'CUIT': '30707293809', 'Nombre en AFIP': 'CONTRATO DE UNION TRANSITORIA DE EMPRESAS - AREA LLANCANELO U.T.E.'}, 
    {'Nombre Soc SAP': 'GAS Y PETROLEO DEL NQ SA CON PART', 'Código SAP': '918', 'Estado': 'Activa', 'CUIT': '30712188061', 'Nombre en AFIP': 'GAS Y PETROLEO DEL NEUQUEN SOCIEDAD ANONIMA CON PARTICIPACION ESTATAL MAYORITARIA-YPF S.A.-TOTAL AUSTRAL SA SUC ARG-ROVELLA ENERGIA SA-AREA CERRO LAS MINAS UTE'}, 
    {'Nombre Soc SAP': 'UTE ZAMPAL OESTE - YPF SA -', 'Código SAP': '1046', 'Estado': 'Activa', 'CUIT': '30709441945', 'Nombre en AFIP': 'YPF S.A EQUITABLE RESOURCES ARGENTINA COMPANY S.A - ZAMPAL OESTE UTE'}, 
    {'Nombre Soc SAP': 'AESA PERU', 'Código SAP': '1143', 'Estado': 'Activa', 'CUIT': 'EXTERIOR', 'Nombre en AFIP': 'AESA PERU'}, 
    {'Nombre Soc SAP': 'ENERGIA ARGENTINA S.A. - YPF S.A. -', 'Código SAP': '1153', 'Estado': 'Activa', 'CUIT': '30711435227', 'Nombre en AFIP': 'ENERGIA ARGENTINA S.A. - YPF S.A. - PROYECTO GNL ESCOBAR - UTE'}, 
    {'Nombre Soc SAP': 'UTE RINCON DEL MANGRULLO', 'Código SAP': '1160', 'Estado': 'Activa', 'CUIT': '30714428469', 'Nombre en AFIP': 'YPF S.A - PAMPA ENERGIA S.A.. UNION TRANSITORIA DE EMPRESAS - RINCON DEL MANGRULLO'}, 
    {'Nombre Soc SAP': 'YPF SA KILWER SA AREA CHACHAHUEN', 'Código SAP': '1164', 'Estado': 'Activa', 'CUIT': '30716199025', 'Nombre en AFIP': 'YPF S.A.-KILWER S.A.-KETSAL S.A.-ENERGIA MENDOCINA S.A. AREA CHACHAHUEN UNION TRANSITORIA DE EMPRESAS'}, 
    {'Nombre Soc SAP': 'YPF S.A. - PETRONAS E&P ARGENTINA S', 'Código SAP': '1167', 'Estado': 'Activa', 'CUIT': '30714869759', 'Nombre en AFIP': 'YPF S.A. - PETRONAS E&P ARGENTINA S.A.'}, 
    {'Nombre Soc SAP': 'YPF S.A.- PBB POLISUR S.A., AREA', 'Código SAP': '1169', 'Estado': 'Activa', 'CUIT': '30715142658', 'Nombre en AFIP': 'YPF S.A.- PBB POLISUR S.A., AREA EL OREJANO UTE'}, 
    {'Nombre Soc SAP': 'COMPANIA DE HIDROCARBURO NO CONVENC', 'Código SAP': '1171', 'Estado': 'Activa', 'CUIT': '30714124427', 'Nombre en AFIP': 'COMPAÑIA DE HIDROCARBURO NO CONVENCIONAL S.R.L.'}, 
    {'Nombre Soc SAP': 'AESA BOLIVIA', 'Código SAP': '1457', 'Estado': 'Activa', 'CUIT': 'EXTERIOR', 'Nombre en AFIP': 'AESA BOLIVIA'}, 
    {'Nombre Soc SAP': 'YPF PESA POSA  AREA RIO NEUQUEN POR', 'Código SAP': '1471', 'Estado': 'Activa', 'CUIT': '30716137119', 'Nombre en AFIP': 'YPF, PESA, POSA - AREA RIO NEUQUEN UTE'}, 
    {'Nombre Soc SAP': 'YPF SA EQUINOR ARGENTINA AS', 'Código SAP': '1474', 'Estado': 'Activa', 'CUIT': '30716788683', 'Nombre en AFIP': 'YPF S.A. - EQUINOR ARGENTINA AS SUCURSAL ARGENTINA- AREA CAN 102 UTE'}, 
    {'Nombre Soc SAP': 'GAS Y PETROLEO DEL NEUQUEN SA.', 'Código SAP': '1477', 'Estado': 'Activa', 'CUIT': '30714224960', 'Nombre en AFIP': 'GAS Y PETROLEO DEL NEUQUEN SOCIEDAD ANONIMA -YPF S.A.-PLUSPETROL S.A AREA LAS TACANAS UTE'}, 
    {'Nombre Soc SAP': 'UTE LOMA CAMPANA', 'Código SAP': '1480', 'Estado': 'Activa', 'CUIT': '30714335614', 'Nombre en AFIP': 'YPF S.A - COMPAÑIA DE HIDROCARBURO NO CONVENCIONAL SRL AREA LOMA CAMPANA UTE'}, 
    {'Nombre Soc SAP': 'EXXON MOBIL EXPLORATION ARGENTINA S', 'Código SAP': '1484', 'Estado': 'Activa', 'CUIT': '30715683152', 'Nombre en AFIP': 'EXXON MOBIL EXPLORATION ARGENTINA SRL YPF SA AREA LOMA DEL MOLLE UTE'}, 
    {'Nombre Soc SAP': 'YPF TECNOLOGIA SA', 'Código SAP': '1600', 'Estado': 'Activa', 'CUIT': '30713748508', 'Nombre en AFIP': 'YPF TECNOLOGIA S.A.'}, 
    {'Nombre Soc SAP': 'COMPAÑIA DE DESARROLLO NO CONVENCIO', 'Código SAP': '1603', 'Estado': 'Activa', 'CUIT': '30714412651', 'Nombre en AFIP': 'COMPA IA DE DESARROLLO NO CONVENCIONAL SRL'}, 
    {'Nombre Soc SAP': 'YPF SA CIA DE DESARROLLO NO CONVENC', 'Código SAP': '1604', 'Estado': 'Activa', 'CUIT': '30714739235', 'Nombre en AFIP': 'YPF S.A- COMPAÑIA DE DESARROLLO NO CONVENCIONAL S.R.L AREA CHIHUIDO DE LA SIERRA NEGRA SUDESTE- NARAMBUENA UNION TRANSITORIA DE EMPRESAS'}, 
    {'Nombre Soc SAP': 'UTE BAJO DEL TORO I S.R.L.', 'Código SAP': '1606', 'Estado': 'Activa', 'CUIT': '30715890751', 'Nombre en AFIP': 'BAJO DEL TORO I S.R.L. - YPF S.A. - AREA BAJO DEL TORO UTE'}, 
    {'Nombre Soc SAP': 'UTE BANDURRIA SUR', 'Código SAP': '1607', 'Estado': 'Activa', 'CUIT': '30715884344', 'Nombre en AFIP': 'YPF S.A. - SPM ARGENTINA S.A. - AREA BANDURRIA SUR UTE'}, 
    {'Nombre Soc SAP': 'OLEODUCTO LOMA CAMPANA LAGO PELLEGR', 'Código SAP': '1610', 'Estado': 'Activa', 'CUIT': '30715995413', 'Nombre en AFIP': 'OLEODUCTO LOMA CAMPANA - LAGO PELLEGRINI SA'}, 
    {'Nombre Soc SAP': 'YPF VENTURES SAU', 'Código SAP': '1613', 'Estado': 'Activa', 'CUIT': '33716225289', 'Nombre en AFIP': 'YPF VENTURES SAU'}, 
    {'Nombre Soc SAP': 'YPF LITIO S.A.U.', 'Código SAP': '1614', 'Estado': 'Activa', 'CUIT': '33717818399', 'Nombre en AFIP': 'YPF LITIO SAU'}, 
    {'Nombre Soc SAP': 'YPF DIGITAL', 'Código SAP': '1615', 'Estado': 'Activa', 'CUIT': '33718163809', 'Nombre en AFIP': 'YPF DIGITAL SAU'}, 
    {'Nombre Soc SAP': 'VMOS S.A.U.', 'Código SAP': '1617', 'Estado': 'Activa', 'CUIT': '30718713354', 'Nombre en AFIP': 'VMOS SAU'}, 
    {'Nombre Soc SAP': 'MOBIL ARGENTINA S.A.', 'Código SAP': '1619', 'Estado': 'Activa', 'CUIT': '30658473499', 'Nombre en AFIP': 'MOBIL ARGENTINA SOCIEDAD ANONIMA'}
]

socs = [soc["Nombre Soc SAP"] for soc in lista_sociedades] + [soc["Nombre en AFIP"] for soc in lista_sociedades]
cods_soc = [soc["Código SAP"] for soc in lista_sociedades]
cuits = [soc["CUIT"] for soc in lista_sociedades]

relevant_categories = [
    "Estado de facturas", 
    # "Pedido devolución retenciones", 
    "Impresión de OP y/o Retenciones"
]

def obtener_valor_por_prioridad(extractions, campo, fuentes_prioritarias):
    for fuente in fuentes_prioritarias:
        #extractions es una lista con objetos por cada tipo de extraccion
        for extraccion in extractions:
            if extraccion["source"] == fuente:
                #extraccion["extractions"] es una lista de objetos por cada documento procesado
                for documents in extraccion["extractions"]:
                    #document es una lista de objetos por cada pagina extraida
                    for document in documents:
                        document_data = documents[document]
                        for page in document_data:
                            value = page["fields"].get(campo, None)
                            if value:
                                value = value.strip() 
                                if value.lower() not in ["none", "", "-", "null"]:
                                    return value  # Retorna el primer valor válido

    return None  # Si no encuentra nada válido, retorna None

def obtener_facturas(extractions):
    nulos = ["null", "none", "-", "", None]
    facturas = []
    ids_vistos = set()
    fecha_monto_vistos = set()
    fuentes_facturas = ["Document Intelligence", "Vision"]

    for fuente in fuentes_facturas:
        for extraccion in extractions:
            if extraccion["source"] == fuente:
                for documents in extraccion["extractions"]:
                    for document in documents:
                        document_data = documents[document]
                        for page in document_data:
                            fields = page["fields"]
                            invoice_id = fields.get("InvoiceId", None)
                            invoice_date = fields.get("InvoiceDate", None)
                            invoice_total = fields.get("InvoiceTotal", None)

                            if invoice_id and invoice_id not in ids_vistos:
                                if invoice_id not in nulos and invoice_date not in nulos:
                                    facturas.append({"Factura": invoice_id, "Fecha": invoice_date, "Monto": invoice_total})
                                    ids_vistos.add(invoice_id)
                            elif invoice_date not in nulos and invoice_total not in nulos:
                                clave = (invoice_date, invoice_total)
                                if clave not in fecha_monto_vistos:
                                    facturas.append({"Factura": "", "Fecha": invoice_date, "Monto": invoice_total})
                                    fecha_monto_vistos.add(clave)

    for extraccion in extractions:
        if extraccion["source"] == "Mail":
            for documents in extraccion["extractions"]:
                for document in documents:
                    document_data = documents[document]
                    for page in document_data:
                        fields = page["fields"]
                        invoice_id = fields.get("InvoiceId", [])
                        invoice_date = fields.get("InvoiceDate", [])
                        invoice_total = fields.get("InvoiceTotal", [])

                        if not invoice_id: invoice_id = []
                        if not invoice_date: invoice_date = []
                        if not invoice_total: invoice_total = []

                        max_length = max(len(invoice_id), len(invoice_date), len(invoice_total))
                        for i in range(max_length):
                            invoice = invoice_id[i] if i < len(invoice_id) else ""
                            fecha = invoice_date[i] if i < len(invoice_date) else ""
                            monto = invoice_total[i] if i < len(invoice_total) else ""

                            if invoice not in nulos:
                                if invoice not in ids_vistos:
                                    facturas.append({"Factura": invoice, "Fecha": fecha, "Monto": monto})
                                    ids_vistos.add(invoice)
                            elif fecha not in nulos and monto not in nulos:
                                clave = (fecha, monto)
                                if clave not in fecha_monto_vistos:
                                    facturas.append({"Factura": "", "Fecha": fecha, "Monto": monto})
                                    fecha_monto_vistos.add(clave)

    return facturas


def generar_resumen(datos):
    extractions = datos.get("extracciones", [])
    fuentes_prioritarias = ["Mail", "Document Intelligence", "Vision"]
    customer = obtener_valor_por_prioridad(extractions, "CustomerName", fuentes_prioritarias)
    cod_soc = obtener_valor_por_prioridad(extractions, "CustomerCodSap", fuentes_prioritarias)
    resume = {
        "CUIT": obtener_valor_por_prioridad(extractions, "VendorTaxId", fuentes_prioritarias),
        "Proveedor": obtener_valor_por_prioridad(extractions, "VendorName", fuentes_prioritarias),
        "Sociedad": customer,
        "Cod_Sociedad": cod_soc,
        "Facturas": obtener_facturas(extractions)
    }

    return resume
