import pandas as pd

from io import BytesIO
from sqlalchemy import and_
from app.controller.mail import DATE_FORMAT
from app.models.products import Products
from app.models.subscriptions import Subscriptions
from app.models.transactions import Transactions
from app.models.user import Users
from app.config.database import SessionLocal
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime


def get_db():                                                                                                                                                                                                                   
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
class Automation:


    @staticmethod
    def get_transactions(db: Session, twenty_four_hours_ago: datetime):
        try:
            recent_data = db.query(
                Transactions.id_user,
                Transactions.created_at,
                Users.num_document,
                Products.name.label('product_name'),
                Products.price.label('product_price')
            ).join(
                Users, Transactions.id_user == Users.id
            ).join(
                Products, Transactions.products == Products.id
            ).filter(
                and_(
                    Transactions.created_at >= twenty_four_hours_ago,
                    Transactions.status == "APPROVED"
                )
            ).all()

    

            transactions_data = []
            documento_numero = 1
            for transaction in recent_data:
                transactions_data.append({
                    "Encab: Empresa": "SAFE COMERCIAL ZONA FRANCA SAS",
                    "Encab: Tipo Documento": "FV",
                    "Encab: Prefijo": "SAFE",
                    "Encab: Documento Número": documento_numero,
                    "Fecha Creación": transaction.created_at.strftime("%Y-%m-%d"),
                    "Encab: Tercero Interno": "900123456",
                    "Encab: Nit o Cc Cliente": str(transaction.num_document),
                    "Encab: Nota": "Factura por suscripcion",
                    "Encab: FormaPago": "Contado",
                    "Encab: Fecha Entrega": "23/12/2023",
                    "Detalle: Bodega": transaction.product_name,
                    "Detalle: UnidadDeMedida": "Und.",
                    "Detalle: Cantidad": 1,
                    "Detalle: IVA": "0.19",
                    "Precio del Producto": transaction.product_price,
                    "Detalle: Descuento": 0,
                    "Detalle: Vencimiento": "23/04/2023",
                    "Detalle: Nota": "",
                    "Detalle: Centro costos": "",
                    "Detalle: Personalizado1": "",
                    "Detalle: Personalizado2": "",
                    "Detalle: Personalizado3": "",
                    "Detalle: Personalizado4": "",
                    "Detalle: Personalizado5": "",
                    "Detalle: Personalizado6": "",
                    "Detalle: Personalizado7": "",
                    "Detalle: Personalizado8": "",
                    "Detalle: Personalizado9": "",
                    "Detalle: Personalizado10": "",
                    "Detalle: Personalizado12": "",
                    "Detalle: Personalizado13": "",
                    "Detalle: Personalizado14": "",
                    "Detalle: Personalizado15": "",
                    "Detalle: Código Centro Costos": ""
                })
                documento_numero += 1


            df = pd.DataFrame(transactions_data)
            output = BytesIO()
            df.to_excel(output, index=False)
            output.seek(0)

            return {"éxito": True, "archivo": output}

        except SQLAlchemyError as error:
            print(f"Error al recuperar transacciones: {error}")
            return {"éxito": False, "error": str(error)}

    @staticmethod
    def terceros(db: Session, twenty_four_hours_ago: datetime):
        try:
            recent_data = db.query(
                Transactions.type_document.label('type_document'),
                Transactions.num_document.label('num_document'),
                Transactions.full_name.label('full_name'),
                Transactions.phone_number.label('phone_number'),
                Transactions.city_shipping.label('city_shipping'),
                Transactions.region_shipping.label('region_shipping'),
                Transactions.phone_number_shipping.label('phone_number_shipping'),
                Transactions.customer_email.label('customer_email'),
                Transactions.created_at.label('created_at'),
                Users.name.label('user_name'),
                Users.lastname.label('user_lastname'),
                Users.type_person.label('user_type_person')
            ).join(
                Users, Transactions.id_user == Users.id
            ).filter(
                and_(
                    Transactions.created_at >= twenty_four_hours_ago,
                    Transactions.status == "APPROVED"
                )
            ).all()


            grouped_data = {}
            for data in recent_data:
                if data.num_document not in grouped_data:
                    tipo_direccion = "Empresa/Oficina" if data.type_document == "nit" else "Casa"
                    fecha_creacion = data.created_at.strftime("%Y-%m-%d ") if data.created_at else ""
                    grouped_data[data.num_document] = {
                        "Tipo Identificación": data.type_document,
                        "No. Identificación": str(data.num_document),
                        "Ciudad Identificación": data.city_shipping,
                        "1er. Nombre o Razón Social ": data.user_name.split(' ', 1)[0],
                        "2do. Nombre": data.user_name.split(' ', 1)[1] if len(data.user_name.split(' ', 1)) > 1 else "",
                        "1re. Apellido": data.user_lastname.split(' ', 1)[0],
                        "2do.Apellido": data.user_lastname.split(' ', 1)[1] if len(data.user_lastname.split(' ', 1)) > 1 else "",
                        "Propiedad Activa": "Cliente;",
                        "Activos": -1,
                        "Propiedad Retención": data.user_type_person,
                        "Fecha Creación": fecha_creacion,
                        "Plazo": 0,
                        "Clasificación Dian": "Normal",
                        "Actividad Económica": "",
                        "Matricula": "",
                        "Tipos_Responsabilidades": "",
                        "Aplica ReteIca": "",
                        " % Ica": "",
                        "Tipo Dirección": tipo_direccion,
                        "Ciudad Dirección": data.city_shipping,
                        "Dirección Principal": "-1",
                        "Teléfonos": str(data.phone_number_shipping),
                        "Código Postal": "",
                        "Fax ": "",
                        "Movil 1": "",
                        "Movil 2": "",
                        "Correo Electrónico": data.customer_email,
                        "E_Mail 2": "",
                        "E_Mail 3": "",
                        "Página Web": "",
                        "Observaciones": "",
                        "Sucursal": ""
                    }
                else:
                    grouped_data[data.num_document]["Activos"] -= 1

            users_data = list(grouped_data.values())

            df = pd.DataFrame(users_data)
            output = BytesIO()
            df.to_excel(output, index=False)
            output.seek(0)

            return {"éxito": True, "archivo": output}

        except SQLAlchemyError as error:
            print(f"Error al recuperar terceros: {error}")
            return {"éxito": False, "error": str(error)}
        
    @staticmethod
    def inventario_(db: Session, twenty_four_hours_ago: datetime):
        try:
            recent_transactions = db.query(
                Transactions,
                Products.name.label('product_name'),
                Products.descr.label('product_descr'),
                Products.price.label('product_price')
            ).join(
                Products, Transactions.products  == Products.id
            ).filter(
                and_(
                    Transactions.created_at >= twenty_four_hours_ago,
                    Transactions.status == "APPROVED"
                )
            ).all()

            transactions_data = {}

            for transaction in recent_transactions:
                product_code = transaction.product_name
                product_descr = transaction.product_descr
                product_price = transaction.product_price

                if product_code not in transactions_data:
                    transactions_data[product_code] = {
                        "Código": product_code,
                        "Descripción": product_descr,
                        "Activo": -1,  # Comienza con -1
                        "Exis. Máxima": "0",
                        "Exis. Mínima": "0",
                        "Unid. Medida": "Und.",
                        "Precio 1":  str(product_price),
                        "Precio 2": "0",
                        "Precio 3": "0",
                        "Precio 4": "0",
                        "Grupo Uno": "SERVICIOS",
                        "Iva": "0.19",
                        "Tipo Iva": "Gravado",
                        "Clasificación": "Servicio",
                        "Clasificación Niif": "Servicio",
                        "Facturar sin Existen.": "-1",
                        "Centro Costos": "0"
                    }
                else:
                    transactions_data[product_code]["Activo"] -= 1

            transactions_list = list(transactions_data.values())


            df = pd.DataFrame(transactions_list)
            output = BytesIO()
            df.to_excel(output, index=False)
            output.seek(0)

            return {"éxito": True, "archivo": output}

        except SQLAlchemyError as error:
            print(f"Error al recuperar transacciones: {error}")
            return {"éxito": False, "error": str(error)}
    