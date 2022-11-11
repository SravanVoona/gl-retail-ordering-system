import pandas as pd
import mysql.connector

class Table_to_Csv:
    
    def conversion():
        db = mysql.connector.connect(user = 'root', passwd = 'root', database = 'grocart')
        cursor = db.cursor()

        query = "SELECT fname,lname,password FROM grocart.user;"
        cursor.execute(query)

        myallData = cursor.fetchall()

        fname,lname,password = [],[],[]
        #address,city,state,country,zipcode,email,phone,isadmin = [],[],[],[],[],[],[],[]
        for  fn,ln,pw in myallData:
            fname.append(fn)
            lname.append(ln)
            password.append(pw)

        #we need to store this data to CSV
        dic = {'first_name' : fname , 'last_name' : lname, 'password' : password}
        df = pd.DataFrame (dic)
        path = r'C:\Users\sudheer varma\Capstone_Project\user_to_csv.csv' #Path where the table is to be saved.
        df_csv = df.to_csv(path)

    


