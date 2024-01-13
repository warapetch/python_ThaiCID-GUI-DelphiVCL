"""
    Data reader
    ไฟล์ประกอบของการอ่านข้อมูลบัตรประชาชน
    วรเพชร  เรืองพรวิสุทธิ์
    09/01/2567
"""

from enum import Enum

"""
    DataType ประเภทของข้อมูล
    เพื่อจำแนก ในการจัดการ ตัดเครื่องหมายคั่นฟิลด์ '#'
"""

class SaveType(Enum):
    NONE = 1
    FILE = 2
    CLIPBOARD = 3


class ThaiCIDDataType(Enum):
    TEXT = 1
    NAME = 2
    GENDER = 3
    DATE = 4
    ADDRESS = 5
    RELIGION = 6
    DOCNUMBER = 7
    
# Lookup Data    
GENDER = ['-','ชาย','หญิง']    
RELIGION = ['-','พุทธ','อิสลาม','คริสต์','พราหมณ์-ฮินดู','ซิกข์','ยิว','เชน','โซโรอัสเตอร์','บาไฮ','ไม่นับถือศาสนา','ไม่ทราบ']


"""
    Package 1
    สำหรับ ติดต่อ+อ่าน โดยระบุข้อมูลบัตร { TH}

    # Read-Binary command format
    # Command	    Class	INS	    P1	    P2	    Lc	                Data In	    Le
    # Read-Binary	0xFF	0xB0	MSB	    LSB	    Length of Data In	Data	    Length expected    
    
    # Command   Description 
    # Class	    call Class (CLA) 
    # INS	    call Method
    # P1	    Paramer 1    
    # P2	    Paramer 2
    # Lc	    ขนาดของข้อมูล ที่ส่งเข้าไป (Length of Data In)
    # Data In	ข้อมูลที่ส่งเข้าไป (Data In)   
    # Le        ขนาดของข้อมูล ที่ต้องการ (Response Data Out)
    
    Response
    # Data out, SW1, SW2
   
"""


APDU_SELECT = [0x00, 0xA4, 0x04, 0x00, 0x08]
APDU_THAI_CARD = [0xA0, 0x00, 0x00, 0x00, 0x54, 0x48, 0x00, 0x01]



"""
    Package 2
    สำหรับอ่าน คอลัมน์ที่ต้องการ
    request ไปแล้วบัตรจะส่งข้อมูลกลับมา เราต้อง ACK กลับไป
    # Application Protocol Data Unit (APDU)
"""

APDU_DATA=[
    {
        'key':'APDU_CID', 
        'id':'CID',
        'desc': 'เลขบัตรประชาชน',
        'apdu':[0x80, 0xb0, 0x00, 0x04, 0x02, 0x00, 0x0d],
        'type': ThaiCIDDataType.TEXT
    },

    {
        'key':'APDU_THFULLNAME',  
        'id':'FULLNAME-TH',
        'desc': 'ชื่อ-นามสุกล(TH)',
        'apdu':[0x80, 0xb0, 0x00, 0x11, 0x02, 0x00, 0x64],
        'type': ThaiCIDDataType.NAME
    },
    {
        'key':'APDU_ENFULLNAME', 
        'id':'FULLNAME-EN',
        'desc': 'ชื่อ-นามสุกล(EN)',
        'apdu':[0x80, 0xb0, 0x00, 0x75, 0x02, 0x00, 0x64],
        'type': ThaiCIDDataType.NAME
        },
    {
        'key':'APDU_BIRTH', 
        'id':'BIRTH',
        'desc': 'วันเดือนปีเกิด',
        'apdu': [0x80, 0xb0, 0x00, 0xD9, 0x02, 0x00, 0x08],
        'type': ThaiCIDDataType.DATE
        },
    {
        'key':'APDU_GENDER', 
        'id':'GENDER',
        'desc': 'เพศ',
        'apdu': [0x80, 0xb0, 0x00, 0xE1, 0x02, 0x00, 0x01],
        'type': ThaiCIDDataType.GENDER
        },
    {
        'key':'APDU_ISSUER', 
        'id':'ISSUER',
        'desc': 'ผู้ออกบัตร',
        'apdu': [0x80, 0xb0, 0x00, 0xF6, 0x02, 0x00, 0x64],
        'type': ThaiCIDDataType.TEXT
        },
    {
        'key':'APDU_ISSUE', 
        'id':'ISSUE',
        'desc': 'บัตร-วันเริ่มใช้',
        'apdu': [0x80, 0xb0, 0x01, 0x67, 0x02, 0x00, 0x08],
        'type': ThaiCIDDataType.DATE
        },
    {
        'key':'APDU_EXPIRE', 
        'id':'EXPIRE',
        'desc': 'บัตร-วันหมดอายุ',
        'apdu':[0x80, 0xb0, 0x01, 0x6F, 0x02, 0x00, 0x08],
        'type': ThaiCIDDataType.DATE
        },
    {
        'key':'APDU_ADDRESS', 
        'id':'ADDRESS',
        'desc': 'ที่อยู่',
        'apdu':[0x80, 0xb0, 0x15, 0x79, 0x02, 0x00, 0x64],
        'type': ThaiCIDDataType.ADDRESS
        },

    # {
    #     'key':'APDU_RELIGION', 
    #     'id':'RELIGION',
    #     'desc': 'ศาสนา',
    #     'apdu':[0x80, 0xb0, 0x01, 0x77, 0x02, 0x00, 0x02],
    #     'type': ThaiCIDDataType.RELIGION
    #     },

    {
        'key':'APDU_DOCNO', 
        'id':'DOCNO',
        'desc': 'เลขใต้บัตร',
        'apdu':[0x80, 0xb0, 0x16, 0x19, 0x02, 0x00, 0x0E],
        'type': ThaiCIDDataType.DOCNUMBER
        },
      

]




APDU_PHOTO = [
    # Part 1/20
    {
        'key':'APDU_PHOTO1', 
        'apdu':[0x80, 0xb0, 0x01, 0x7B, 0x02, 0x00, 0xFF] },
    # Part 2/20
    {
        'key':'APDU_PHOTO2', 
        'apdu':[0x80, 0xb0, 0x02, 0x7A, 0x02, 0x00, 0xFF] },
    # Part 3/20
    {
        'key':'APDU_PHOTO3', 
        'apdu':[0x80, 0xb0, 0x03, 0x79, 0x02, 0x00, 0xFF] },
    # Part 4/20
    {
        'key':'APDU_PHOTO4', 
        'apdu':[0x80, 0xb0, 0x04, 0x78, 0x02, 0x00, 0xFF] },    
    # Part 5/20
    {
        'key':'APDU_PHOTO5', 
        'apdu':[0x80, 0xb0, 0x05, 0x77, 0x02, 0x00, 0xFF] },
    # Part 6/20
    {   
        'key':'APDU_PHOTO6', 
        'apdu':[0x80, 0xb0, 0x06, 0x76, 0x02, 0x00, 0xFF] },
    # Part 7/20
    {
        'key':'APDU_PHOTO7', 
        'apdu':[0x80, 0xb0, 0x07, 0x75, 0x02, 0x00, 0xFF] },
    # Part 8/20
    {
        'key':'APDU_PHOTO8', 
        'apdu':[0x80, 0xb0, 0x08, 0x74, 0x02, 0x00, 0xFF] },
    # Part 9/20
    {
        'key':'APDU_PHOTO9', 
        'apdu':[0x80, 0xb0, 0x09, 0x73, 0x02, 0x00, 0xFF] },
    # Part 10/20
    {
        'key':'APDU_PHOTO10', 
        'apdu':[0x80, 0xb0, 0x0A, 0x72, 0x02, 0x00, 0xFF] },
    # Part 11/20
    {
        'key':'APDU_PHOTO11', 
        'apdu':[0x80, 0xb0, 0x0B, 0x71, 0x02, 0x00, 0xFF] },
    # Part 12/20
    {
        'key':'APDU_PHOTO12', 
        'apdu':[0x80, 0xb0, 0x0C, 0x70, 0x02, 0x00, 0xFF] },
    # Part 13/20
    {
        'key':'APDU_PHOTO13', 
        'apdu':[0x80, 0xb0, 0x0D, 0x6F, 0x02, 0x00, 0xFF] },
    # Part 14/20
    {
        'key':'APDU_PHOTO14', 
        'apdu':[0x80, 0xb0, 0x0E, 0x6E, 0x02, 0x00, 0xFF] },
    # Part 15/20
    {
        'key':'APDU_PHOTO15', 
        'apdu':[0x80, 0xb0, 0x0F, 0x6D, 0x02, 0x00, 0xFF] },
    # Part 16/20
    {
        'key':'APDU_PHOTO16', 
        'apdu':[0x80, 0xb0, 0x10, 0x6C, 0x02, 0x00, 0xFF] },
    # Part 17/20
    {
        'key':'APDU_PHOTO17', 
        'apdu':[0x80, 0xb0, 0x11, 0x6B, 0x02, 0x00, 0xFF] },
    # Part 18/20
    {
        'key':'APDU_PHOTO18', 
        'apdu':[0x80, 0xb0, 0x12, 0x6A, 0x02, 0x00, 0xFF] },
    # Part 19/20
    {
        'key':'APDU_PHOTO19', 
        'apdu':[0x80, 0xb0, 0x13, 0x69, 0x02, 0x00, 0xFF] },
    # Part 20/20
    {
        'key':'APDU_PHOTO20', 
        'apdu':[0x80, 0xb0, 0x14, 0x68, 0x02, 0x00, 0xFF] },

]