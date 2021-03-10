# -*- coding: utf-8 -*-
"""
@Time ： 2021/3/7 10:38
@Auth ： Twinzo1
@File ：qxc.py
@IDE ：PyCharm
@Motto：ABC(Always Be Coding)
"""
import sqlite3
import qixing


class qxc(object):
    def __init__(self, db_name="./qxc.db", table_name="STARS"):
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()
        self.db_name = db_name
        self.table_name = table_name

    def create_table(self):
        self.cur.execute('''CREATE TABLE %s
            (ID INT PRIMARY KEY     NOT NULL,
            SUMS            INT     NOT NULL,
            THOUS           INT     NOT NULL,
            HUNS            INT     NOT NULL,
            TENS            INT     NOT NULL,
            ONES            INT     NOT NULL,
            B_HUNS          INT     NOT NULL,
            B_TENS          INT     NOT NULL,
            B_ONES          INT     NOT NULL);''' % self.table_name)

    def check_table(self):
        self.cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tab_names = [row[0] for row in self.cur.fetchall() if row]
        if self.table_name in tab_names:
            return True
        else:
            return False

    def check_key(self, key):
        self.cur.execute("SELECT id FROM %s" % self.table_name)
        ids = [row[0] for row in self.cur.fetchall()]
        if int(key) in ids:
            return True
        else:
            return False

    def insert(self, data_list):
        self.cur.execute('INSERT INTO %s VALUES(?,?,?,?,?,?,?,?,?)' % self.table_name, data_list)

    # 强制更新
    def force_update_by_id(self, key):
        self.cur.execute("DELETE from %s where ID=%s" % (self.table_name, key))

    def get_by_id(self, key):
        cursor = self.cur.execute("SELECT * from %s where ID='%s'" % (self.table_name, key))
        all_code = [row for row in cursor]
        return all_code

    def get_all(self):
        cursor = self.cur.execute("SELECT * from %s" % self.table_name)
        all_code = []
        for row in cursor:
            all_code.append(list(row))
        return all_code

    def close(self):
        self.conn.commit()
        self.conn.close()


if __name__ == "__main__":
    # 获取期数列表
    period_list = qixing.get_lottery_num(60, False)
    qxc = qxc(table_name="STARS")
    if not qxc.check_table():
        qxc.create_table()
    # 查找数据库，是否已经存取
    for per in period_list:
        if not qxc.check_key(int(per)):
            da = qixing.get_lottery_by_id(per)
            qxc.insert(da)

    pic_pra = qxc.get_all()
    print(pic_pra[-10::1])

    qxc.close()
    import rea

    rea.data2pic(pic_pra)
