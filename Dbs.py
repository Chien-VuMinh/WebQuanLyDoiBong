import mysql.connector

# ket noi toi dbs
db = mysql.connector.connect(user = 'root', password = '123456', host = 'localhost')

# tao csdl
code = "CREATE SCHEMA `quan_ly_giai_bong_da` ;"


# create table
create_cau_thu_table = "CREATE TABLE `quan_ly_giai_bong_da`.`cau_thu` (`ma_cau_thu` VARCHAR(3) NOT NULL, `ten` NVARCHAR(100) NOT NULL, `ngay_sinh` DATE NOT NULL,  `loai_cau_thu` NVARCHAR(45) NOT NULL, `ghi_chu` NVARCHAR(100) NULL, PRIMARY KEY (`ma_cau_thu`));"


# them noi dung vao csdl
add_content_to_cau_thu_table = "INSERT INTO `quan_ly_giai_bong_da`.`cau_thu` (`ma_cau_thu`, `ten`, `ngay_sinh`, `loai_cau_thu`, `ghi_chu`) VALUES (%s, %s, %s, %s, %s);" 
var = [
    ['002', 'nguyen van a', '2000-12-2', 'hau ve', 'trong nuoc'], 
    ('003', 'nguyen van b', '2003-2-25', 'hau ve canh trai', 'ngoai quoc')
]                             

# chay doan code 
mycursor = db.cursor()
for item in var:
    mycursor.execute(add_content_to_cau_thu_table, item)


# update db
db.commit()

# xoa csdl
# code = "drop schema `cauthu` ;"
# mycursor = cau_thu_db.cursor()
# mycursor.execute(code)