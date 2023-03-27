import io
import xlsxwriter
import pymysql


def db_connector():
    """
    db_connector is used to connect to the database for CRUD operations
    used by the respective definitions.
    """
    my_sql_con = pymysql.connect(
        host="iesl-dev-db-syd.cdiah0tmq8hx.ap-southeast-2.rds.amazonaws.com",
        user="admin",
        password="Cp35jYibiHkydS2JxvKS",
        db="myfarm-investor-dev",
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor,
        port=3306
    )
    return my_sql_con

def fetch_table_data():

    # fetch details from the database using mysql query.
    conn = db_connector()
    cursor = conn.cursor()
    sql = 'select * from users_details'
    q = cursor.execute(sql)
    header = [row[0] for row in cursor.description]
    rows = cursor.fetchall()
    # Closing connection
    conn.close()


    return header, rows

def export():


    # Create an new Excel file and add a worksheet.
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet('MENU')
    workbook = xlsxwriter.Workbook('file.xlsx')

    # Create style for cells
    header_cell_format = workbook.add_format({'bold': True, 'border': True, 'bg_color': 'yellow'})
    body_cell_format = workbook.add_format({'border': True})
    header, rows = fetch_table_data()
    row_index = 0
    column_index = 0
    # Create header for border
    for column_name in header:
        worksheet.write(row_index, column_index, column_name, header_cell_format)
        column_index += 1

    row_index += 1
    # insert data into excel file
    for i in rows:
        column_index = 0
        for key, value in i.items():
            worksheet.write(row_index, column_index, value, body_cell_format)
            column_index += 1
        row_index += 1
    print(str(row_index) + ' rows written successfully to ' + workbook.filename)

    # Closing workbook
    workbook.close()
    output.seek(0)
    # xlsx_data = output.getvalue()
    # print(xlsx_data)



export()

