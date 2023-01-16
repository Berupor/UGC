from vertica_python import connect

vt_client = connect(
    host='127.0.0.1',
    port=5433,
    user='dbadmin',
    password='',
    database='docker',
    autocommit=True,
)
