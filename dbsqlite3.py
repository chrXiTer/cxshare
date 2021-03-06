import sqlite3
from . import file as cxfile
#import file as cxfile

def connToDB(dbpath): # 'test.db'
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    return conn, cursor

def createTable(conn, cur):
    cur.execute('''CREATE TABLE IF NOT EXISTS webpc (url TEXT primary key, 
        time varchar(100),
        title TEXT,
        contentOri TEXT,
        contentText TEXT,
        contentJson TEXT,
        type integer)''') # 1 身份证  10 手机号  100 qq邮箱  1000 qq  10000 邮箱

def insertDataToDb(conn, cur, tableName, colNameList, dataList):
    strT1 = ", ".join(colNameList)
    for data in dataList:
        strT2 = ", ".join(['"%s"' % data[colNameList[i]] for i in range(len(colNameList))])
        sqlStr = 'INSERT INTO `%s` (%s) VALUES (%s);' % (tableName, strT1, strT2)
        cur.execute(sqlStr)
    conn.commit()

def reduceDBDataByIDNo2(conn, cursor, tableName): # 将表中id去重然后存入 tmp2 表
    cursor.execute('SELECT  id  FROM %s GROUP BY id' % tableName)
    aa = []
    for row in cursor:
        IDNo = row[0]
        aa.append(IDNo)
    for IDNo in aa:
        insertDataToDb(conn, cursor, 'tmp2', ['id'], [{'id':IDNo}])

def updateID(conn, cursor, tableName):  # 修改 身份证 字段，去掉第一个字符
    cursor.execute('SELECT  ID, `身份证`  FROM %s' % tableName)
    aa = []
    for row in cursor:
        ID = row[0]
        sfz = row[1]
        if(sfz[0] == "'"):
            aa.append([ID,sfz])
    for item in aa:
        ID = item[0]
        sfz = item[1][1:]
        sql = "UPDATE %s set `身份证`='%s' where ID=%s;" % (tableName, sfz , ID)
        cursor.execute(sql)
    conn.commit()

def reduceDBDataByIDNo(conn, cursor, tableName):
    cursor.execute('''
        SELECT `身份证`, `ID`, * FROM %s WHERE `身份证` IN (
                SELECT `身份证` FROM %s GROUP BY `身份证` HAVING COUNT(`身份证`) >=2
        ) ORDER BY `身份证`
    ''' % (tableName,tableName))
    tmpData = dict()
    colNameList = [tuple[0] for tuple in cursor.description]
    for row in cursor: # 将查到的数据安装 身份证号 分组
        IDNo = row[0]
        tmpData[IDNo]= tmpData.get(IDNo) or []
        tmpData[IDNo].append(list(row))

    
    def reduceRecord(idsNeedDelete, records):
        IDToDelete = records[0][1]
        for i in range(len(records[0])):
            v0 = records[0][i]
            v1 = records[1][i]
            if v0 == None or v0 == 'nan' or v0 == '':
                records[0][i] = records[1][i]
            elif v0 == None or v0 == 'nan' or v0 == '':
                records[1][i] = v0
            elif v1 != v0 and colNameList[i] != "ID":  # 两天记录该项不一致
                if colNameList[i] == "其它":    #其它项，进行合并
                    records[0][i] = v0 + "$" + v1
                    records[1][i] = v0 + "$" + v1
                else:
                    IDToDelete = -1  # 两条记录不删除
                    break
        if IDToDelete != -1:
            idsNeedDelete.append(IDToDelete)
            records.remove(records[0])
            if len(records) > 1:
                reduceRecord(idsNeedDelete, records) 

    idsNeedDelete = []
    for IDNo in tmpData:
        records = tmpData[IDNo]
        reduceRecord(idsNeedDelete, records)
    
    for IDNo in tmpData:
        records = tmpData[IDNo]
        for record in records:
            updateDataToDB(conn, cursor, tableName, colNameList[2:], record[2:])
    for ID in idsNeedDelete:
        deleteDataFromDB(conn, cursor, tableName, ID)
    
def updateDataToDB(conn, cursor, tableName, colNameList, record):
    strs = []
    ID = None
    for i in range(len(colNameList)):
        recordValue = str(record[i])
        if type(record[i]).__name__ == 'str':
            recordValue = "'" + record[i] + "'"
        elif colNameList[i] == 'ID':
            ID = recordValue
        elif type(record[i]).__name__ == 'NoneType':
            recordValue = 'null'
        strs.append("`" + colNameList[i] + "` = " + recordValue)
    strT = ", ".join(strs)
    cursor.execute('UPDATE %s set %s where ID=%s;' % (tableName, strT, ID))
    conn.commit()

def deleteDataFromDB(conn, cursor, tableName, ID):
    cursor.execute('DELETE FROM %s WHERE ID=%s;' % (tableName, ID))
    conn.commit()


if __name__ == "__main__":
    pass

