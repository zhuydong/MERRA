import pymysql
# import MySQLdb 这个包和上面包都可以使用，用那个包，下面的包名要和使用的一致
import time

DataBaseName = 'MERRA_400'
try:
    conn = pymysql.connect(host='localhost',
                           user='root',
                           password='123456',
                           )  # db='ModisTem20'  这个可以放在前面的括号里面，同时把后面的第二、三行删除即可，就是直接选择数据库，不用创建数据库
    cursor = conn.cursor()
    # cursor.execute('CREATE DATABASE  IF NOT EXISTS '+DataBaseName +' CHARACTER SET=utf8mb4')
    cursor.execute(
        """CREATE DATABASE %s""" % DataBaseName + """ CHARACTER SET=utf8mb4;""")  # 'CREATE DATABASE  IF NOT EXISTS ModisTem20 CHARACTER SET=utf8mb4;'
    conn.select_db(DataBaseName)
    print('数据库创建连接成功！')
except Exception as e:
    print('数据库创建连接失败!', e)


def obtain_name():
    """
        建立数据库表名
    """
    lev_list = [400]
    return (('T03_' + str(x).zfill(3)) for x in lev_list)


def create_table(tb_name, con):
    """
        循环建表
    """
    begin = time.perf_counter()
    cursor = con.cursor()
    for name in tb_name:
        sql_createTb = f"""CREATE TABLE {name}(
                        id mediumint(8) unsigned NOT NULL AUTO_INCREMENT,

                        date date DEFAULT NULL,
                        lon float DEFAULT NULL,
                        lat float DEFAULT NULL,
                        TO3 float DEFAULT NULL,
                        Var_TO3 float DEFAULT NULL,

                        COSC float DEFAULT NULL,

                        PRIMARY KEY(id)
                        );
                        """
        cursor.execute(sql_createTb)
    con.commit()
    cursor.close()
    con.close()
    print('耗时%.2f秒' % (time.perf_counter() - begin))


if __name__ == "__main__":
    tb_name = obtain_name()
    create_table(tb_name, conn)

