import mysql.connector
from mysql.connector import Error
import cred


def save_res_to_db(time, cpu, mem):
    try:
        con = mysql.connector.connect(user='Ury3EhU5sM', password=cred.p,
                                      host='remotemysql.com',
                                      port=3306,
                                      database='Ury3EhU5sM')
        c = con.cursor()
        c.execute(
            "INSERT INTO res (time,cpu,mem) VALUES (%s,%s,%s);",
            (time, cpu, mem)
        )
        con.commit()
        print(c.rowcount, "record inserted successfully into results table")

    except Error as e:
        print("Error reading data from MySQL table", e)
    finally:
        if (con.is_connected()):
            con.close()
            c.close()
            print("MySQL connection is closed")


def get_statistic(time, cpu, mem):
    try:
        con = mysql.connector.connect(user='Ury3EhU5sM', password=cred.p,
                                      host='remotemysql.com',
                                      port=3306,
                                      database='Ury3EhU5sM')
        c = con.cursor()
        c.execute(
            """
        SELECT
            (
                SELECT count(*) from res
            ) as no_all,
            (
                SELECT count(*) from res
                WHERE time > %s
            ) as no_time,
            (
                SELECT count(*) from res
                WHERE cpu > %s
            ) as no_cpu,
            (
                SELECT count(*) from res
                WHERE mem > %s
            ) as no_mem
        FROM DUAL;
        """,
            (time, cpu, mem)
        )
        records = c.fetchall()
        no_all = records[0][0]
        no_time = records[0][1]
        no_cpu = records[0][2]
        no_mem = records[0][3]

        print(
            no_all,
            no_time/no_all,
            no_cpu/no_all,
            no_mem/no_all,
        )

    except Error as e:
        print("Error reading data from MySQL table", e)
    finally:
        if (con.is_connected()):
            con.close()
            c.close()
            print("MySQL connection is closed")


save_res_to_db(1002, 23.3, 23132)
get_statistic(1002, 23.3, 23132)
