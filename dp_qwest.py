import sqlite3
import os

con = sqlite3.connect("qwest.db")
cursor = con.cursor()

try:
    cursor.execute("""CREATE TABLE qwest
                   (№ INTEGER PRIMARY KEY AUTOINCREMENT,
                   image_qwest TEXT,
                   image_answer TEXT,
                   info_image TEXT,
                   answer TEXT,
                   true INTEGER,
                   false INTEGER,
                   total INTEGER)
               """)
except:
    pass

folder_path = 'data/image'
file_names = os.listdir(folder_path)
COUNT = len(file_names) // 3
#print(file_names)


def lol():
    for i in range(1, COUNT+1):
        file_qwest = f'{i}.JPG'
        file_info = f'{i}_.JPG'
        if f'{i}_t.JPG' in file_names:
            file_answer =f'{i}_t.JPG'
        else:
            file_answer = f'{i}_f.JPG'
        answer = file_answer[-5]
        if answer == 'f':
            answer = 'False'
        else:
            answer = 'True'
        data = [file_qwest, file_answer, file_info, answer, 0, 0]
        cursor.execute(
            "INSERT INTO qwest (image_qwest, image_answer, info_image, answer,true, false) VALUES (?,?,?,?,?,?)",
            data)
        con.commit()

#lol()