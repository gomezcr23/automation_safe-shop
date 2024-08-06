import os
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from app.controller import mail
from app.config.database import SessionLocal
from app.controller.automation import Automation
from apscheduler.triggers.interval import IntervalTrigger

# Configurar variables de entorno
USER_NAME_RPT = os.getenv("USER_NAME_RPT")
USER_EMAIL_RPT_1 = os.getenv("USER_EMAIL_RPT_1")
USER_EMAIL_RPT_2 = os.getenv("USER_EMAIL_RPT_2")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally: 
        db.close()

def interval_task_test():
    try:
        print("Iniciando intervalo de tarea...")
        db = next(get_db())
        twenty_four_hours_ago = datetime.now() - timedelta(hours=24)

        result_transactions = Automation.get_transactions(db, twenty_four_hours_ago)
        result_terceros = Automation.terceros(db, twenty_four_hours_ago)
        result_inventario = Automation.inventario_(db, twenty_four_hours_ago)

        if result_transactions["éxito"] and result_terceros["éxito"] and result_inventario["éxito"]:
            print("Generando archivos...")
            files = {
                "documentos_ventasWO_SFI.xlsx": result_transactions["archivo"],
                "tercerosWO_SFI.xlsx": result_terceros["archivo"],
                "inventarioWO_SFI.xlsx": result_inventario["archivo"]
            }
            mail.send_email_with_attachments(user_email=USER_EMAIL_RPT_1, user_name=USER_NAME_RPT, files=files)
            mail.send_email_with_attachments(user_email=USER_EMAIL_RPT_2, user_name=USER_NAME_RPT, files=files)
        else:
            print("No se pudieron generar los archivos Excel.")
    except Exception as e:
        print(f"Error en interval_task_test: {e}")

def cron_task_test():
    print('cron task is run...')

if __name__ == "__main__":
    scheduler = BackgroundScheduler()

    # scheduler.add_job(interval_task_test, IntervalTrigger(minutes=1))
    scheduler.add_job(cron_task_test, CronTrigger(hour=23, minute=45))
    scheduler.add_job(cron_task_test, CronTrigger(hour=3, minute=30))

    print("Iniciando el programador de tareas...")
    # Iniciar el programador de tareas
    scheduler.start()

    try:
        # Mantener el programa en ejecución
        while True:
            pass
    except (KeyboardInterrupt, SystemExit):
        print("Deteniendo el programador de tareas...")
        scheduler.shutdown()
