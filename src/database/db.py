import mysql.connector
from mysql.connector import Error

from . import cred

# in cred file should be one line
# p = 'password'


def save_res_to_db(time, cpu, mem, avg_pt):
    try:
        con = mysql.connector.connect(user='Ury3EhU5sM', password=cred.p,
                                      host='remotemysql.com',
                                      port=3306,
                                      database='Ury3EhU5sM')
        c = con.cursor()
        c.execute(
            "INSERT INTO res (time,cpu,mem,avg_pt) VALUES (%s,%s,%s,%s);",
            (time, cpu, mem, avg_pt)
        )
        con.commit()
        print(c.rowcount, "record inserted successfully into table")

    except Error as e:
        print("Error reading data from MySQL table", e)
    finally:
        if (con.is_connected()):
            con.close()
            c.close()
            print("MySQL connection is closed")


def get_statistic(time, cpu, mem, avg_pt):
    res_stat = []
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
            ) as no_mem,
            (
                SELECT count(*) from res
                WHERE avg_pt > %s
            ) as no_avg_pt,
            (
                SELECT count(*) from res
                WHERE ts >= DATE_SUB(current_timestamp(), INTERVAL 60 MINUTE)
            ) as no_all_last,
            (
                SELECT count(*) from res
                WHERE time > %s
                AND ts >= DATE_SUB(current_timestamp(), INTERVAL 60 MINUTE)
            ) as no_time_last,
            (
                SELECT count(*) from res
                WHERE cpu > %s
                AND ts >= DATE_SUB(current_timestamp(), INTERVAL 60 MINUTE)
            ) as no_cpu_last,
            (
                SELECT count(*) from res
                WHERE mem > %s
                AND ts >= DATE_SUB(current_timestamp(), INTERVAL 60 MINUTE)
            ) as no_mem_last,
            (
                SELECT count(*) from res
                WHERE avg_pt > %s
                AND ts >= DATE_SUB(current_timestamp(), INTERVAL 60 MINUTE)
            ) as no_avg_pt_last
        FROM DUAL;
        """,
            (time, cpu, mem, avg_pt, time, cpu, mem, avg_pt)
        )
        records = c.fetchall()
        no_all = records[0][0]
        no_time = records[0][1]
        no_cpu = records[0][2]
        no_mem = records[0][3]
        no_avg_pt = records[0][4]
        no_all_last = records[0][5]
        no_time_last = records[0][6]
        no_cpu_last = records[0][7]
        no_mem_last = records[0][8]
        no_avg_pt_last = records[0][9]

        perc_time = int(((no_time/no_all))*100)
        perc_cpu = int(((no_cpu/no_all))*100)
        perc_mem = int(((no_mem/no_all))*100)
        perc_avg_pt = int((1-(no_avg_pt/no_all))*100)

        perc_time_last = int(((no_time_last/no_all_last))*100)
        perc_cpu_last = int(((no_cpu_last/no_all_last))*100)
        perc_mem_last = int(((no_mem_last/no_all_last))*100)
        perc_avg_pt_last = int((1-(no_avg_pt_last/no_all_last))*100)
        # order of field:
        # ####
        # no_all, no_all_last,
        # time, perc_time, perc_time_last,
        # cpu, perc_cpu, perc_cpu_last,
        # mem, perc_mem, perc_mem_last,
        # avg_pt, perc_avg_pt, perc_avg_pt_last,
        # ####
        res_stat = [
            no_all, no_all_last,
            time, perc_time, perc_time_last,
            cpu, perc_cpu, perc_cpu_last,
            mem, perc_mem, perc_mem_last,
            avg_pt, perc_avg_pt, perc_avg_pt_last
        ]

    except Error as e:
        print("Error reading data from MySQL table", e)
    finally:
        if (con.is_connected()):
            con.close()
            c.close()
    return res_stat

# save_res_to_db(78068, 25, 557441024, 10000)
# save_res_to_db(81000, 26, 570000000, 9100)
# get_statistic(78068, 25, 557441024, 10000)
# get_statistic(80000, 25, 560000000, 9400)
