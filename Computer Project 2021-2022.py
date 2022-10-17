import mysql.connector
import os
import csv
import datetime

mydb=mysql.connector.connect(host='localhost',user='root',password='tiger')
mycursor=mydb.cursor()
if mydb.is_connected():
    print('success')
else:
    print ('could not connect')

try:
    mycursor.execute('Create database Library_Management')
except mysql.connector.errors.DatabaseError:
    print('Database exists')
mycursor.execute('Use Library_Management')

try:
    mycursor.execute('create table Library (Bcode varchar(5) primary key, Genre varchar(20), Title varchar(30), Author varchar(30), Publisher varchar(30), Price int(10), Mcode int(1))')
except:
    print("Table already exists")

try:
    mycursor.execute('create table Issue (Bcode varchar(5) primary key, Title varchar(30), Memcode int(1), Issuedate date)')
except:
    print("Table already exists")
    
try:
    mycursor.execute('create table Member (Memcode int(5) primary key, Name varchar(20), Address varchar(50), Phone int(10), Limit_books int(1), NOB int(2))')
except:
    print("Table already exists")
    
#To display all the tables created in the database    
mycursor.execute('show tables')
for k in mycursor:
    print(k)
    
#Writes all the data of the Library table into a csv file.
def writebook(elements):
    file= os.path.isfile("library.csv")
    with open("library.csv", "a", newline = "") as csvfile:
        cw= csv.writer(csvfile)   
        if not file:
            cw.writerow(['Bcode','Genre','Title','Author','Publisher','Price','Memcode','Issuedate'])
        cw.writerow(elements)
        
#Writes all the data of the Member table into a csv file.
def writemember(elements):
    file= os.path.isfile("member.csv")
    with open("member.csv", "a", newline = "") as csvfile:
        cw= csv.writer(csvfile)   
        if not file:
            cw.writerow(['Memcode','Name','Address','Phone','Limit_books','NOB'])
        cw.writerow(elements)

#Writes all the data of the Issue table into a csv file.
def writeissue(elements):
    file= os.path.isfile("issue.csv")
    with open("issue.csv", "a", newline = "") as csvfile:
        cw= csv.writer(csvfile)   
        if not file:
            cw.writerow(['Bcode','Title','Memcode','Issuedate'])
        cw.writerow(elements)

#1 Addition of records to the library table-
def add_lib():
    num=int(input("Enter the number of records:"))
    for i in range(num):
        Bcode=input("Enter bookcode:")
        Genre=input("Enter genre:")
        Title=input("Enter book name:")
        Author=input("Enter author:")
        Publisher=input("Enter publisher's name:")
        Price=int(input("Enter price of book:"))
        Mcode=int(input("Enter member code:"))
        inp="Insert into Library values(%s,%s,%s,%s,%s,%s,%s)"
        val=(Bcode,Genre,Title,Author,Publisher,Price,Mcode)
        lst=[Bcode,Genre,Title,Author,Publisher,Price,Mcode]
        mycursor.execute(inp,val)
        writebook(lst)
    mydb.commit()
    mycursor.execute('select * from Library')
    data=mycursor.fetchall()
    for row in data:
        print(row)

#2 Modification of records of library file-
def modify_lib():
    bc=input("Enter bookcode of the row you want to change:-")
    mycursor.execute("describe Library")
    data=mycursor.fetchall()
    for i in data:
        print(i[0], end=" ")
    print()
    mycursor.execute("select * from Library where Bcode= '"+ bc + "'")
    data=mycursor.fetchall()
    for i in data:
        for k in i:
            print(k,end=" ")
    print()
    t1 = input("Enter the field you want to change the value from:-")
    new_inp = input("Enter the new value:-")
    mycursor.execute("update Library set "+ t1 +" =  '" + new_inp + "' where Bcode = '" + bc + "'")
    mydb.commit()
    mycursor.execute("select * from Library")
    data=mycursor.fetchall()
    for i in data:
        print(i)

#3 Addition of records to member file-
def add_mem():
    num=int(input("Enter the number of records:"))
    for i in range(num):
        Memcode=int(input("Enter member code:"))
        Name=input("Enter name:")
        Address=input("Enter the address:")
        Phone=int(input("Enter phone number:"))
        Limit_books=int(input("Enter the maximum limit:"))
        NOB=int(input("Enter the number of books issued:"))
        inp="Insert into Member values(%s,%s,%s,%s,%s,%s)"
        val=(Memcode,Name,Address,Phone,Limit_books,NOB)
        lst=[Memcode,Name,Address,Phone,Limit_books,NOB]
        writemember(lst)
        mycursor.execute(inp,val)
    mydb.commit()
    mycursor.execute('select * from Member')
    data=mycursor.fetchall()
    for row in data:
          print(row)

#4 Modification of address and phone number of existing member in member file-
def modify_mem():
    m=input("Enter mcode of the row you want to change:-")
    mycursor.execute("describe Member")
    data=mycursor.fetchall()
    for i in data:
        print(i[0], end="   ")
    print()
    mycursor.execute("select * from Member where Memcode = '" + m + "'")
    data=mycursor.fetchall()
    for i in data:
        for k in i:
            print(k, end=" ")
    print()
    new_address = input("Enter the new address:-")
    new_phone = input("Enter the new phone number:-")
    mycursor.execute("update Member set Address = '" + new_address + "' where Memcode = '" + m + "'")
    mycursor.execute("update Member set Phone = '" + new_phone + "' where Memcode = '" + m + "'")
    mydb.commit()
    mycursor.execute("select * from Member")
    data=mycursor.fetchall()
    for i in data:
        print(i)

#5 Issue of Books-
def issue_books():
    #res(1,2)- result obtained
    res = ""
    res1 = ""
    memcode = int(input("Enter member code:-"))
    mycursor.execute("select * from Member where Memcode = '" + str(memcode) + "'")
    data = mycursor.fetchall()
    for i in data:
        res += str(i)
    limits = data[0][4]
    nob = data[0][5]
    if (res != ""):
        title_of_book = input("Enter the title of the book:-")
        mycursor.execute("select * from Library where Title = '" + str(title_of_book) + "'")
        data1 = mycursor.fetchall()
        # mc---->Member Code of the library table(showing if its issued or not issued)
        bc = data1[0][0]
        mc_of_lib = data1[0][6]
    for i in data1:
        res1 += str(i)
        if (res1 != ""):
            if (mc_of_lib == 0):
                if (limits > nob):
                    nob += 1
                    mycursor.execute(f"update Member set NOB = {nob} where Memcode = {memcode}")
                    mycursor.execute(f"update Library set Mcode = 1 where Bcode = {bc}")
                    Bcode = bc
                    Memcode = memcode
                    Title = title_of_book
                    Issuedate = datetime.date.today()
                    inp="Insert into Issue values(%s,%s,%s,%s)"
                    lst=[Bcode,Title,Memcode,Issuedate]
                    val=(Bcode,Title,Memcode,Issuedate)
                    writeissue(lst)
                    mycursor.execute(inp,val)
                    mydb.commit()
                    print("You have successfully issued the book.")
                    break
                else:
                    print("Member has already issued books to maximum limit")
                    break
            else:
                print("The book requested is already issued")
                break
        else:
            print("The book requested is not present in library")
            break
    else:
        print("Member code entered is invalid!")
        addmem=input('Do you want to be a member of this library? (y/n)')
        if addmem.upper == 'Y':
            add_mem()
        else:
            print ('Please register in order to issue books.')
    
    
#6 Return of Books-
def return_books():
    res2=""
    bc = int(input("Enter the bookcode of the book you want to return-"))
    mcode = int(input("Enter the member code-"))
    mycursor.execute("select * from Library where Bcode = '" + str(bc) + "'")
    data = mycursor.fetchall()
    for i in data:
        res2 += str(i)
    if (res2 != ""):
        fine = 0
        idays = int(input("Enter the number of days the book was issued:-"))
        if (idays == 0):
            fine = 0
        elif (idays <= 7):
            fine = idays * 0.5
        elif (idays <= 15):
            fine = idays * 1
        elif (idays > 15):
            fine = idays * 2
        else:
            pass
        if (idays > 0):
            print("Member has to pay a fine of " + str(fine))
        mycursor.execute("select * from Member where Memcode = '" + str(mcode) + "'")
        data1 = mycursor.fetchall()
        nob = data1[0][5]
        nob -= 1
        mycursor.execute("update Member set NOB = '" + str(nob) + "' where Memcode = '" + str(mcode) + "'")
        mycursor.execute("update Library set Mcode = 0 where Bcode = '" + str(bc) + "'")
        mycursor.execute("delete from Issue where Memcode = '" + str(mcode) + "'")
        mydb.commit()
    else:
        print("Bookcode not found")
        
#7 Searching for availability of a particular book-
def search_books():
    while True:
        mycursor.execute('select * from Library')
        data=mycursor.fetchall()
        title=input('Enter the title of the book-')
        for i in data:
            if title in i[2]:
                print(title,'exists in the library')
        ques=input("Do you want to search for another book? (y/n) ")
        if ques.upper()=='Y':
            continue
        else:
            break

#8 Reports-
def report():
    print("\tSubject wise book list-")
    mycursor.execute("select * from Library order by Genre")
    data = mycursor.fetchall()
    for i in data:
        print(i)
    print()
    
    print("\tList of books issued to members-")
    mycursor.execute("select Title from Issue")
    data1 = mycursor.fetchall()
    for i in data1:
        print(i)
    print()
    
    print("\tList of available books-")
    mycursor.execute("select * from Library where Mcode ='{}'".format(0))
    data2 = mycursor.fetchall()
    for i in data2:
        print(i)
    print()
    
    print("\tList of defaulters-")
    mycursor.execute("select Name as defaulters from Member where NOB>Limit_books")
    data3 = mycursor.fetchall()
    for i in data3:
        print(i)
    print()
    
    print("\tList of members in the library-")
    mycursor.execute("select Name from Member")
    data6 = mycursor.fetchall()
    for i in data6:
        print(i)
    print()

#Menu Driven-
print("\t\t\t{Library Management System}\n")
program=True
while program:
    print("(1) Addition of records to the library file:\n"
          "(2) Modification of records of library file:\n"
          "(3) Addition of records to member file:\n"
          "(4) Modification of address and phone number of existing member in member file:\n"
          "(5) Issue of books:\n"
          "(6) Return of books:\n"
          "(7) Searching for availability of a particular book:\n"
          "(8) Reports:\n"
             "\t(a) Subject wise book list-\n"
             "\t(b) List of books issued to members-\n"
             "\t(c) List of available books-\n"
             "\t(d) List of defaulters-\n"
             "\t(e) List of members in the library-")
    choice=int(input("Enter the number for the corresponding choice:"))
    if choice==1:
        add_lib()
    elif choice==2:
        modify_lib()
    elif choice==3:
        add_mem()
    elif choice==4:
        modify_mem()
    elif choice==5:
        issue_books()
    elif choice==6:
        return_books()
    elif choice==7:
        search_books()
    elif choice==8:
        report()
    else:
        print("Enter any one of the choices above(1,2,3,4,6,7,8)")
    
    choice=input("Do you want to continue, enter your choice: (Y) or (N)")
    
    if choice.upper()=='Y':
        continue
    else:
        program=False