import pymysql
db=pymysql.connect(host='localhost',user='root',password='',database='samarth')
cursor=db.cursor()
class project_123:
    def insert_record(self):
        self.Name=input("Enter the ID: ")
        self.Mobile_Number=int(input("Enter the Mobile number: "))
        self.Email_ID=int(input("Enter the Email ID:"))
        self.PASSWORD=int(input("Enter the Country Name:"))
        self.Date_of_Birth=input("Enter the Date of Birth:")
        insert_query="INSERT INTO customer_details values(%s,%s,%s,%s,%s)"
        try:
            cursor.execute(insert_query,(self.Name,self.Mobile_Number,self.Email_ID,self.PASSWORD,self.Date_of_Birth))
            result=cursor.rowcount
            if result:
                print("Data inserted succesfully\n")
                db.commit()
            else:
                print("There was an error inserting the data")
                db.rollback()
        except Exception as e:
            print(f"There was an error: {e}")
            db.rollback()
    def fetch_record(self):
        choice=int(input("Enter your choice: \n1.Fetch all records.\n2.Fetch record based on ID\n"))
        if choice==1:
            select_query="SELECT * FROM project_123"
            cursor.execute(select_query)
            result=cursor.fetchall()
            if result:
                print("Printing all records\n")
                for i in result:
                    print(i)
            else:
                print("No records found\n")
        elif choice==2:
            self.Mobile_Number=int(input("Enter the Mobile_Number of the User: "))
            select_query="SELECT * FROM project_123 WHERE Mobile_number=%s"
            try:
                cursor.execute(select_query,(self.Mobile_Number))
                result=cursor.fetchone()
                if result:
                    print("Printing the details for the User\n")
                    print(result)
                else:
                    print("No record found of the Mobile_Number\n")
            except Exception as e:
                print(f"There was an error fetching the records{e}")
        else:
            print("Invalid choice")
    def update_record(self):
        Mobile_Number=int(input("Enter the Mobile_Number: "))
        cursor.execute("SELECT * FROM project_123 WHERE Mobile_Number=%s",Mobile_Number)
        fetch_result=cursor.fetchone()
        if fetch_result:
            print("RECORD TO UPDATE\n")
            print(fetch_result)
            self.Name=input("Enter the new name of the User: ")
            self.Email_ID=int(input("Enter the New Email Id:"))
            self.PASSWORD=int(input("Enter the New Password:"))
            self.Date_of_Birth=input("Enter the Date Of Birth:")
            update_query="UPDATE project_123 SET Name=%s,Email_ID=%s,PASSWORD=%s,Date_of_Birth=%s WHERE Mobile_Number=%s"
            try:
                cursor.execute(update_query,(self.Name,self.Email_ID,self.PASSWORD,self.Date_of_Birth,Mobile_Number))
                update_result=cursor.rowcount
                if update_result:
                    print("DATA UPDATED SUCCESFULLY")
                    db.commit()
                else:
                    print("THERE WAS AN ERROR UPDATING THE DATA")
                    db.rollback()
            except Exception as e:
                print(f"There was en error {e}")
                db.rollback()
        else:
            print("THIS ID DOES NOT EXIST\n")

if __name__=="__main__":
    e=project_123()
    while True:
        choice=int(input("Enter your choice: \n1.Insert New Record.\n2.Fetch Records.\n3.Update Record\n4. Exit.\n"))
        if choice==1:
            e.insert_record()
        elif choice==2:
            e.fetch_record()
        elif choice==3:
            e.update_record()
        elif choice==4:
            break
        else:
            print("Please select a valid option")