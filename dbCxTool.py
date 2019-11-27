from . import dbsqlite3

def get一省内的县市(codePrex):
    conn, cursor = dbsqlite3.connToDB('/Users/cx/Desktop/sj/csAllTList')
    sql = "SELECT `areaname` FROM area WHERE `areacode` LIKE '%d%%' AND `areacode` <> '%d0000'" % (codePrex, codePrex)
    cursor.execute(sql)
    result = []
    for row in cursor:
        areaname = row[0]
        result.append(areaname)
    conn.close()
    return result

def set学校地区前缀(areaname):
    conn, cursor = dbsqlite3.connToDB('/Users/cx/Desktop/sj/csAllTList')
    sql = "SELECT `ID`, `name` FROM school WHERE `name` LIKE '%s%%'" % areaname
    cursor.execute(sql)
    newData = []
    for row in cursor:
        ID = row[0]
        schoolName = row[1]
        newData.append({
            'ID':ID,
            'schoolName':schoolName,
            'prefix':areaname
        })
    for item in newData:
        updateSql = "UPDATE school SET key1='%s' WHERE ID=%d" % (item['prefix'], item['ID'])
        cursor.execute(updateSql)
    conn.commit()
    conn.close()
    return

def setArea湖南():
    地区列表 = get一省内的县市(43)
    地区列表.append('宁乡县')
    地区列表.append('望城县')
    for 地区名 in 地区列表:
        set学校地区前缀(地区名)

def set附属():
    conn, cursor = dbsqlite3.connToDB('/Users/cx/Desktop/sj/csAllTList')
    sql = "SELECT ID FROM school WHERE name LIKE '%附属%' OR name LIKE '%附中%' OR name LIKE '%附小%'"
    cursor.execute(sql)
    newData = []
    for row in cursor:
        ID = row[0]
        newData.append({
            'ID':ID,  
        })
    for item in newData:
        updateSql = "UPDATE school SET key2='附属' WHERE ID=%d" % (item['ID'])
        cursor.execute(updateSql)
    conn.commit()
    conn.close()
    return

def set附属():
    conn, cursor = dbsqlite3.connToDB('/Users/cx/Desktop/sj/csAllTList')
    sql = "SELECT ID FROM school WHERE name LIKE '%附属%' OR name LIKE '%附中%' OR name LIKE '%附小%'"
    cursor.execute(sql)
    newData = []
    for row in cursor:
        ID = row[0]
        newData.append({
            'ID':ID,  
        })
    for item in newData:
        updateSql = "UPDATE school SET key2='附属' WHERE ID=%d" % (item['ID'])
        cursor.execute(updateSql)
    conn.commit()
    conn.close()
    return

def set数字中小学(中or小):
    conn, cursor = dbsqlite3.connToDB('/Users/cx/Desktop/sj/csAllTList')
    sql = "SELECT ID, name FROM school WHERE name LIKE '%%%s%%'" % (中or小)
    cursor.execute(sql)
    newData = []
    for row in cursor:
        ID = row[0]
        name = row[1]
        index = name.find(中or小)
        char = name[index-1]
        if 中or小 == '中' and len(name) > index+1 and name[index+1] != "学":
            if name.find("中路") == index or name.find("中心小学") == index:
                continue
        
        if char in ['一','二','三','四','五','六','七','八','九','十']:
            newData.append({
                'ID':ID,  
            })
        else:
            index = name.find("中心小学")
            if index > 0 and name[index-1] in ['一','二','三','四','五','六','七','八','九','十']:
               newData.append({
                   'ID':ID,
                }) 
    for item in newData:
        updateSql = "UPDATE school SET `数字%s学`='数' WHERE ID=%d" % (中or小, item['ID'])
        cursor.execute(updateSql)
    conn.commit()
    conn.close()
    return
