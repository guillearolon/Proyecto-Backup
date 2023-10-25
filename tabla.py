import glob
import json

def procesar_archivo_json():
    ruta_archivo = glob.glob('C:/Users/guill/OneDrive/Escritorio/proyecto_backup/*.json')

    if not ruta_archivo:
        return []

    archivo_json = ruta_archivo[0]
    with open(archivo_json, 'r') as archivo:
        json_data = archivo.read()

    data = json.loads(json_data)

    campos = []
    for item in data['Report']:
        name = item.get('Name')
        name_tag = item.get('Tag')
        status_veeam = item.get('Status Veeam')
        job_name = item.get('Job Name')
        last_backup_date = item.get('Last Backup Date')

        if status_veeam in ['Warning', 'Failed', 'Success', 'Pending', 'InProgress', '-']:
            campos.append({
                'Name': name,
                'Name Tag': name_tag,
                'Status Veeam': status_veeam,
                'Job Name': job_name,
                'Last Backup Date': last_backup_date
            })

    return campos
