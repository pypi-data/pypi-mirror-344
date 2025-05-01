import os
import re
import base64
import pandas as pd

from typing import List
from fastapi import UploadFile
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
from azure.ai.documentintelligence.models import AnalyzeResult, DocumentContentFormat

# Cargar las variables de entorno desde el archivo .env
load_dotenv(override=True)

def initialize_client():
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    key = os.getenv("AZURE_OPENAI_API_KEY")
    return DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))

def analyze_document_prebuilt_invoice(client, file_bytes: bytes, fields_to_extract: list) -> list:
    data = []
    try:
        poller = client.begin_analyze_document(
            "prebuilt-invoice", AnalyzeDocumentRequest(bytes_source=file_bytes)
        )
        invoices = poller.result()

        if invoices.documents:
            for idx, invoice in enumerate(invoices.documents):
                fields_data = {}
                missing_fields = []
                
                for field in fields_to_extract:
                    field_data = invoice.fields.get(field)
                    if field_data:
                        fields_data[field] = field_data.content
                    else:
                        fields_data[field] = "none"
                        missing_fields.append(field)
                
                data.append({
                    "extraction_number": idx + 1,
                    "fields": fields_data,
                    "missing_fields": missing_fields,
                    "error": "",
                    "source": "Document Intelligence"
                })
        else:
            data = [{
                    "extraction_number": 0,
                    "fields": {},
                    "missing_fields": [],
                    "error": "No se encontraron documentos en el archivo.",
                    "source": "Document Intelligence"
                }]
    
    except Exception as e:
        data = [{
                    "extraction_number": 0,
                    "fields": {},
                    "missing_fields": [],
                    "error": str(e),
                    "source": "Document Intelligence"
                }]
    
    return data

def extract_table_layout(file_bytes: bytes, header_ref: str = None) -> pd.DataFrame:

    def normalizar_header(header: str):
        if header:
            header = header.strip().lower()
            header = re.sub(r"[^\w\s]", "", header)  # elimina signos como º, ., etc.
            header = re.sub(r"\s+", "_", header)     # reemplaza espacios por _
        return header


    client = initialize_client()
    poller = client.begin_analyze_document(
        model_id="prebuilt-layout",
        body=file_bytes,
        output_content_format=DocumentContentFormat.MARKDOWN,
        content_type="application/pdf"
    )
    
    result: AnalyzeResult = poller.result()
    tablas_validas = []
    ref_error = 0
    ref_column_count = None
    header_detected = False
    header_columns = None

    for table_idx, table in enumerate(result.tables):
        print(f"Table # {table_idx} has {table.row_count} rows and {table.column_count} columns")

        table_data = []

        for row_idx in range(table.row_count):
            row_data = []
            for col_idx in range(table.column_count):
                cell = next((cell for cell in table.cells if cell.row_index == row_idx and cell.column_index == col_idx), None)
                row_data.append(cell.content if cell else None)
            table_data.append(row_data)

        df = pd.DataFrame(table_data)

        if header_ref:
            header_index = None
            for i, row in df.iterrows():
                if header_ref in row.values:
                    header_index = i
                    break

            if header_index is not None:
                # Se detectó el encabezado
                header_columns = [normalizar_header(col) for col in df.iloc[header_index]]
                ref_column_count = len(header_columns)
                header_detected = True

                df = df[header_index + 1:].reset_index(drop=True)
                df.columns = header_columns
                tablas_validas.insert(0, df)  # encabezado primero
            else:
                if not header_detected:
                    ref_error += 1
                    if ref_error == len(result.tables):
                        raise ValueError(f"D.I. Layout: No se encontró la columna '{header_ref}'.")
                continue
        else:
            if header_detected and df.shape[1] == ref_column_count:
                df.columns = header_columns
                tablas_validas.append(df)

    if not tablas_validas:
        raise ValueError("No se encontraron tablas válidas para concatenar.")

    tabla_final = pd.concat(tablas_validas, ignore_index=True)
    return tabla_final

def extract_table_custom_layout(file_bytes: bytes) -> pd.DataFrame:
    def normalizar_header(header: str):
        if header:
            header = header.strip().lower()
            header = re.sub(r"[^\w\s]", "", header)  # elimina signos como º, ., etc.
            header = re.sub(r"\s+", "_", header)     # reemplaza espacios por _
        return header


    load_dotenv()
    endpoint = os.getenv("AZURE_DOCUMENT_ENDPOINT")
    key = os.getenv("AZURE_DOCUMENT_KEY")
    model_id = os.getenv("AZURE_CUSTOM_MODEL_ID")

    client = DocumentIntelligenceClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    poller = client.begin_analyze_document(
        model_id=model_id,
        body=file_bytes,
        content_type="application/pdf"
    )
    result = poller.result()

    # Buscar tabla etiquetada como 'Datos_Sap'
    tabla = result.documents[0].fields.get("Datos_Sap")
    if tabla and tabla.type == "array":
        filas = []
        # Iterar sobre los registros de la tabla
        for fila in tabla.value_array:
            # Extraer cada valor de los campos
            n_doc = fila.value_object.get('N° doc', {}).get('valueString', '')
            clas = fila.value_object.get('Clas', {}).get('valueString', '')
            fecha_doc = fila.value_object.get('Fecha doc', {}).get('valueString', '')
            referencia = fila.value_object.get('Referencia', {}).get('valueString', '')
            fecha_base = fila.value_object.get('Fecha base', {}).get('valueString', '')
            vence_el = fila.value_object.get('Vence el', {}).get('valueString', '')
            impte_mon_extr = fila.value_object.get('Impte.mon.extr', {}).get('valueString', '')
            doc_comp = fila.value_object.get('Doc comp', {}).get('valueString', '')
            compens = fila.value_object.get('Compens', {}).get('valueString', '')
            
            # Agregar la fila extraída al listado de filas
            filas.append({
                'N° doc': n_doc,
                'Clas': clas,
                'Fecha doc': fecha_doc,
                'Referencia': referencia,
                'Fecha base': fecha_base,
                'Vence el': vence_el,
                'Impte.mon.extr': impte_mon_extr,
                'Doc comp': doc_comp,
                'Compens': compens
            })

        # Convertir la lista de filas a un DataFrame
        df = pd.DataFrame(filas)
        df.columns = [normalizar_header(col) for col in df.columns]
    return df
        
def process_base64_files(base64_files: list, fields_to_extract: list) -> list:
    client = initialize_client()
    final_results = {}

    for file_data in base64_files:
        file_name = file_data.get("file_name", "unknown")
        content = file_data.get("content", "")

        try:
            file_bytes = base64.b64decode(content)
            text_result = analyze_document_prebuilt_invoice(client, file_bytes, fields_to_extract)
            
            final_results[file_name] = {
                "invoice_number": text_result["invoice_number"],
                "fields": text_result["fields"],
                "missing_fields": text_result["missing_fields"],
                "error": text_result["error"],
                "source": "Document Intelligence"
            }

        except Exception as e:
            final_results[file_name] = {
                "invoice_number": 0,
                "fields": {},
                "missing_fields": [],
                "error": str(e),
                "source": "Document Intelligence"
            }
    
    return [final_results]

def process_uploaded_files(uploaded_files: List[UploadFile], fields_to_extract: List[str]) -> list:
    client = initialize_client()
    final_results = {}

    for file in uploaded_files:
        file_name = file.filename
        try:
            file_bytes = file.file.read()
            text_result = analyze_document_prebuilt_invoice(client, file_bytes, fields_to_extract)
            
            final_results[file_name] = {
                "invoice_number": text_result["invoice_number"],
                "fields": text_result["fields"],
                "missing_fields": text_result["missing_fields"],
                "error": text_result["error"],
                "source": "Document Intelligence"
            }
        except Exception as e:
            final_results[file_name] = {
                "invoice_number": 0,
                "fields": {},
                "missing_fields": [],
                "error": str(e),
                "source": "Document Intelligence"
            }
    
    return [final_results]

def process_binary_files(binary_files: list, fields_to_extract: list) -> list:
    client = initialize_client()
    final_results = {}

    for file_data in binary_files:
        file_name = file_data.get("file_name", "unknown")
        content = file_data.get("content", b"")

        try:
            text_result = analyze_document_prebuilt_invoice(client, content, fields_to_extract)
            
            final_results[file_name] = text_result

        except Exception as e:
            final_results[file_name] = [{
                "invoice_number": 0,
                "fields": {},
                "missing_fields": [],
                "error": str(e),
                "source": "Document Intelligence"
            }]
    
    return [final_results]
