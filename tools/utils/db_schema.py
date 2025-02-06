from database.engine import get_table_desc



def get_db_schema_string(db, db_psycopg2, TABLES_TO_EXCLUDE, VIEWS_TO_INCLUDE):

    tables = db.get_usable_table_names()
    tables = tables + VIEWS_TO_INCLUDE
    schema = ""
    for table in tables:
        if table not in TABLES_TO_EXCLUDE:
            schema += "\n" + "*"*10 + "\n" + get_table_desc(table, db_psycopg2)

    return schema