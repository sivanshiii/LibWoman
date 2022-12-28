import mysql.connector
import pandas as pd

loggedin = False;    
user = ""
pas = ""
member = ["MemberId","FirstName","LastName","DOJ"]
books = ["BookID", "ISBN", "Title", "LendedTo"]
bookslender = ["BookID", "ISBN", "Title", "LendeeID","LendeeName"]
def execSQL(cursor, statement):
    cursor.reset(True);
    cursor.execute(statement)

def login(usern, passw):
    global user
    global pas
    try:
        cnx = mysql.connector.connect(user=usern,passwd=passw,host="localhost") 
        cursor = cnx.cursor()
    except:
        print("Incorrect Login")
        return False;
    execSQL(cursor,"show databases")
   
    if (('library',) in cursor):
        print("DATABASE FOUND")
        cnx = mysql.connector.connect(user=usern,passwd=passw,host="localhost",database='library') 
        cursor = cnx.cursor()
        execSQL(cursor, "show tables")
        if (('books',) in cursor and ('members',) in cursor):
            print("TABLES FOUND")
            user = usern
            pas = passw
            return True;
        else:
            print("CREATING TABLES...")
            execSQL(cursor, "CREATE TABLE 'library'.'members' (  'MemberID' INT NOT NULL AUTO_INCREMENT, 'FirstName' VARCHAR(45) NULL,  'LastName' VARCHAR(45) NULL,  'DOJ' DATE NULL,  PRIMARY KEY ('MemberID'));")
            execSQL(cursor,"CREATE TABLE 'books' (  'BookID' BIGINT(25) NOT NULL AUTO_INCREMENT,  'ISBN' INT NOT NULL DEFAULT 00000,'Title' VARCHAR(100) NOT NULL DEFAULT '--nobook--','LendedTo' INT NOT NULL DEFAULT -1,PRIMARY KEY ('BookID'));")
            user = usern
            pas = passw
            return True;
    else:
        print("CREATING DATABASE...")
        execSQL(cursor, "CREATE DATABASE library;")
        cnx = mysql.connector.connect(user=usern,passwd=passw,host="localhost",database='library')
        cursor = cnx.cursor()
        print("CREATING TABLES...")
        execSQL(cursor,"CREATE TABLE 'members' ('MemberID' INT NOT NULL AUTO_INCREMENT, 'FirstName' VARCHAR(45) NULL, 'LastName' VARCHAR(45) NULL, 'DOJ' DATE NULL, PRIMARY KEY ('MemberID'));")
        execSQL(cursor,"CREATE TABLE 'books' (  'BookID' BIGINT(25) NOT NULL AUTO_INCREMENT,  'ISBN' INT NOT NULL DEFAULT 00000,'Title' VARCHAR(100) NOT NULL DEFAULT '--nobook--','LendedTo' INT NOT NULL DEFAULT -1,PRIMARY KEY ('BookID'));")
        user = usern
        pas = passw
        return True;
        
def parseCommand(stat = str):
    cnx = mysql.connector.connect(user=user,passwd=pas,host="localhost",database='library') 
    cursor = cnx.cursor()
    if (stat.lower().startswith("user")):
        if (stat.lower().startswith("user add")):
            if ("(" not in stat or ")" not in stat or "," not in stat):
                commandFailedFormatError()
            else:
                args = stat[stat.index("(")+1:stat.index(")")].split(",")
                execSQL(cursor, "INSERT INTO members values(default ,'"+args[0]+"','"+args[1]+"', date(now()));")
                success()
        elif (stat.lower().startswith("user info")):
            if ("(" not in stat or ")" not in stat):
                commandFailedFormatError()
            else:
                args = stat[stat.index("(")+1:stat.index(")")]
                execSQL(cursor, "SELECT * FROM members WHERE MemberID = " + args)
                temp = []
                for x in cursor:
                    temptemp = []  
                    for y in x:
                      temptemp.append(y)
                    temp.append(temptemp) 
                try:
                    df = pd.DataFrame(data = temp, columns = member )      
                    print(df)   
                    success()
                except:
                    commandFailedNoRecords()
        elif (stat.lower().startswith("user search")):
            if ("(" not in stat or ")" not in stat):
                commandFailedFormatError()
            else:
                args = stat[stat.index("(")+1:stat.index(")")]
                execSQL(cursor, f"SELECT * FROM members WHERE CONCAT(FirstName, ' ', LastName) like '%{args}%'" )
                temp = []
                for x in cursor:
                    temptemp = []  
                    for y in x:
                      temptemp.append(y)
                    temp.append(temptemp)   
                try:
                    df = pd.DataFrame(data = temp, columns = member )     
                    print(df)   
                    success()
                except:
                    commandFailedNoRecords()
             
    elif (stat.lower().startswith("book")):
        if (stat.lower().startswith("book add")):
            if ("(" not in stat or ")" not in stat or "," not in stat):
                commandFailedFormatError()
            else:
                args = stat[stat.index("(")+1:stat.index(")")].split(",")
                execSQL(cursor, "INSERT INTO books values(default ,"+args[0]+",'"+args[1]+"', default);")
                success()
        elif (stat.lower().startswith("book info")):
            if ("(" not in stat or ")" not in stat):
                commandFailedFormatError()
            else:
                args = stat[stat.index("(")+1:stat.index(")")]
                execSQL(cursor, "SELECT * FROM books WHERE bookid = " + args)
                temp = []
                for x in cursor:
                    temptemp = []  
                    for y in x:
                      temptemp.append(y)
                    temp.append(temptemp) 
                try:
                    df = pd.DataFrame(data = temp, columns = books )      
                    print(df)  
                    success() 
                except:
                    commandFailedNoRecords()     
        elif (stat.lower().startswith("book searchisbn")):
            if ("(" not in stat or ")" not in stat):
                commandFailedFormatError()
            else:
                args = stat[stat.index("(")+1:stat.index(")")]
                execSQL(cursor, f"SELECT * FROM books WHERE ISBN like '{args}%'" )
                temp = []
                for x in cursor:
                    temptemp = []  
                    for y in x:
                      temptemp.append(y)
                    temp.append(temptemp)   
                try:
                    df = pd.DataFrame(data = temp, columns = books )     
                    print(df)   
                    success()
                except:
                    commandFailedNoRecords()             
        elif (stat.lower().startswith("book search")):
            if ("(" not in stat or ")" not in stat):
                commandFailedFormatError()
            else:
                args = stat[stat.index("(")+1:stat.index(")")]
                execSQL(cursor, f"SELECT * FROM books WHERE Title like '%{args}%'" )
                temp = []
                for x in cursor:
                    temptemp = []  
                    for y in x:
                      temptemp.append(y)
                    temp.append(temptemp)   
                try:
                    df = pd.DataFrame(data = temp, columns = books )     
                    print(df)   
                    success()
                except:
                    commandFailedNoRecords()       
        elif (stat.lower().startswith("book lend")):
            if ("(" not in stat or ")" not in stat or "," not in stat):
                commandFailedFormatError()
            else:
                args = stat[stat.index("(")+1:stat.index(")")].split(",")
                execSQL(cursor, f"SELECT LendedTo FROM books WHERE BookID = {args[0]};" )
                lendstatus = -2
                for x in cursor:
                        lendstatus = x
                if(lendstatus != (-1,)):
                    print("Book has already been lended to memberID #" + str(lendstatus[0]))
                else:
                    try:
                        execSQL(cursor, f"UPDATE books SET LendedTo = {args[1]} WHERE BookID = {args[0]};" )
                        success()
                    except:
                        commandFailedNoRecords()
        elif (stat.lower().startswith("book return")):
            if ("(" not in stat or ")" not in stat):
                commandFailedFormatError()
            else:
                args = stat[stat.index("(")+1:stat.index(")")]
                try:
                    execSQL(cursor, f"UPDATE books SET LendedTo = default WHERE BookID = {args};" )
                    success()
                except:
                    commandFailedNoRecords()
        elif (stat.lower().startswith("book liid")):
            if ("(" not in stat or ")" not in stat):
                commandFailedFormatError()
            else:
                args = stat[stat.index("(")+1:stat.index(")")]
                execSQL(cursor, f"SELECT books.BookID, books.ISBN, books.Title, ifnull(members.MemberID, '-1') as LendeeID, ifnull(concat(members.FirstName, ' ', members.LastName), '--not lended--') as LendeeName FROM books LEFT JOIN members ON books.LendedTo = members.MemberID WHERE BookID = '{args}';" )
                temp = []
                for x in cursor:
                    temptemp = []  
                    for y in x:
                      temptemp.append(y)
                    temp.append(temptemp) 
                try:
                    df = pd.DataFrame(data = temp, columns = bookslender )      
                    print(df)  
                    success() 
                except:
                    commandFailedNoRecords()   
        elif (stat.lower().startswith("book liisbn")):
            if ("(" not in stat or ")" not in stat):
                commandFailedFormatError()
            else:
                args = stat[stat.index("(")+1:stat.index(")")]
                execSQL(cursor, f"SELECT books.BookID, books.ISBN, books.Title, ifnull(members.MemberID, '-1') as LendeeID, ifnull(concat(members.FirstName, ' ', members.LastName), '--not lended--') as LendeeName FROM books LEFT JOIN members ON books.LendedTo = members.MemberID WHERE ISBN = '{args}';" )
                temp = []
                for x in cursor:
                    temptemp = []  
                    for y in x:
                      temptemp.append(y)
                    temp.append(temptemp) 
                try:
                    df = pd.DataFrame(data = temp, columns = bookslender )      
                    print(df)  
                    success() 
                except:
                    commandFailedNoRecords()     
        elif (stat.lower().startswith("book lititle")):
            if ("(" not in stat or ")" not in stat):
                commandFailedFormatError()
            else:
                args = stat[stat.index("(")+1:stat.index(")")]
                execSQL(cursor, f"SELECT books.BookID, books.ISBN, books.Title, ifnull(members.MemberID, '-1') as LendeeID, ifnull(concat(members.FirstName, ' ', members.LastName), '--not lended--') as LendeeName FROM books LEFT JOIN members ON books.LendedTo = members.MemberID WHERE Title like '%{args}%';" )
                temp = []
                for x in cursor:
                    temptemp = []  
                    for y in x:
                      temptemp.append(y)
                    temp.append(temptemp) 
                try:
                    df = pd.DataFrame(data = temp, columns = bookslender )      
                    print(df)  
                    success() 
                except:
                    commandFailedNoRecords()  
   
    else:
        print("Command Failed, incorrect syntax") 
        help()            
    cnx.commit()
    return True

def help():
    helps = """Commands:

NOTE: All arguments have to be passed in the "(arg1,arg2,...)" format.
-> Logging in:
  -> Provide the database username and password as "username,password".
-> User Commands:
  -> user add (first_name,last_name): Adds a member to the library system.
  -> user info (member_id): Gets all user data associated with the given member_id.
  -> user search (query): Searches for a member based on first or last name.
-> Book Commands:
  -> book add (ISBN_no,title): Adds a book (with an ISBN number and Title) to the
                               library system.
  -> book info (book_id): Returns all information about a given book based on the
                          book_id.
  -> book search (title): Searches for all books with a similar title and returns
                          all information associated with the book.
  -> book searchisbn (ISBN_no): Searches for all books with the given ISBN_no and 
                                returns all information associated with the book.
  -> book lend (book_id,member_id): Used to lend a book to a library member.
  -> book return (book_id): Used to mark a book as returned to the library.
  -> book liid (book_id): Returns all information about the lending status of a
                          book based on book_id.
  -> book liisbn (ISBN_no): Returns all information about the lending status of a
                            book(s) based on ISBN_no.
  -> book lititle (title): Returns all information about the lending status of a
                           book(s) based on its title.         
                           """
    print(helps)                     
    
def commandFailedFormatError():
    print("Command failed, please provide input in specified format")
    help()
                
def commandFailedNoRecords():
    print("No such records exist.")
    
def success():
    print("Command executed successfully!")
      
while True:
    statement = ""
    if(not loggedin):
       statement = input("Enter Username and Password separated by a comma (username,password): \nLibMan> ")
       if(statement.lower() not in ["exit", "help"]):
           if("," in statement):
              userpass = statement.split(",");
              loggedin = login(str(userpass[0]).strip(), str(userpass[1]).strip())
              if(loggedin):
                  print("LibMan: A fast library management solution by Rayan Madan")
              pass
                  
    if(loggedin):
        statement = input("LibMan> ")
        if(statement.lower() not in ["exit", "help"]):
            parseCommand(statement)
                        
    if(statement == "help"):
        help()
        pass      
    if(statement == "exit"):
        print("Goodbye!")
        break