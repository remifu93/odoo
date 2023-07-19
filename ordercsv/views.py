import csv
from django.db import connection
from django.shortcuts import render
from .forms import UploadCSVForm



def get_csv_order_values(csv_file, order_column_name):
    columns_values = []

    file_data = csv_file.read().decode('utf-8')
    csv_files = file_data.splitlines()

    reader_csv = csv.reader(csv_files)

    column_names = next(reader_csv)
    column_index = column_names.index(order_column_name)

    for fila in reader_csv:
        columns_values.append(fila[column_index])

    return column_names, columns_values


def upload_csv(request):
    """
        Vista DJANGO para Suvir CSV y ver estados de Ordenes.

        Esta vista se podria abstraer y hacer con mucho menos codigo utilizando class based views y los modelos django.
        Pero entiendo que el objetivo es comprobar mi nivel de compresion general tanto en python como en SQL.

        Por lo que entendi, el modulo web deberia ser capaz de recibir un fichero csv, leer su contenido el cual en una columna traeria
        los "nombres de orders", en este caso utilice ORDER ID para identificar una orden.

        Por lo tanto al momento de crear ordenes se le auto asigna el campo ID que es auto increment, podria implementarse a estos modulos,
        que dicho ORDEN ID llegue en el JSON al momento de registrar la orden.

        El usuario debe proporsionar un CSV y el nombre de columna que contiene el ORDER ID de las filas

        CSV ejemplo, en el modulo web se carga el fichero con este formato y se indicaria order en columna, ademas de los estados que se quieren ver

        amount,customer,city,order
        5000,2023-01-01,Empresa 1,1
        1000,2023-01-01,Empresa 2,2
        1500,2023-01-01,Empresa 3,3

        Este modulo devuelve las ordenes con el estado indicado
    """
    if request.method == 'POST':
        form = UploadCSVForm(request.POST, request.FILES)

        if form.is_valid():
            # des del form html
            csv_file = form.cleaned_data['csv_file']
            orders_column_name = form.cleaned_data['column']
            status = form.cleaned_data['status']

            try:
                # intento procesar el csv para obtener sus columnas y valores de filas
                csv_colum_names, cvs_values = get_csv_order_values(csv_file, orders_column_name)
            except:
                form.add_error('column', f"Verifique el csv o el nombre de columna indicado")
            else:
                # genero el listado de orders para generar la consulta y le quito comillas para prevenir sql inject
                placeholders = ",".join(cvs_values).replace("'", " ")

                with connection.cursor() as cursor:
                    query = f"""
                        SELECT store_order.id, store_customer.companyName, store_order.status 
                        FROM store_order
                        LEFT JOIN store_customer ON store_order.customer_id = store_customer.id
                        WHERE store_order.id IN ({placeholders})
                        AND store_order.status = %s
                    """
                    cursor.execute(query, (status,))
                    results = cursor.fetchall()

                    rows = [{"id": row[0], "customer": row[1], "status": row[2]} for row in results]

                return render(request, 'csv_detail.html', {'orders': rows})
    else:
        form = UploadCSVForm()

    return render(request, 'upload_csv.html', {"form": form})
