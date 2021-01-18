class MenuItem:

    def __init__(self, text, number):
        self.text = text
        self.number = number


    def display(self):
        return f"{self.number}- {self.text}"

class Menu():

    def __init__(self, header, menuItems):   #Gelen liste obje olarak döndüğünde adresi dönüyor-sor
        self.header = header
        self.menuItems = list(menuItems)
        
    def display(self, display_header):
        if display_header == True:
            print(self.header)
            print(self.menuItems)

        else:
            print(self.menuItems)

    def add_menu_item(self,text , number):
        add_item = MenuItem(text,number)
        self.menuItems.append(add_item.display())



class User():

    menu_items = []
    menu = Menu("",menu_items)

    def __init__(self, name, password):
        self.name = name
        self.password = password

        User.menu_items=[]

    def get_name(self):
        return self.name
    def get_password(self):
        return self.password
    def who_user(self):
        if isinstance(self,Admin):
            return 'admin'
        elif isinstance(self, Student):
            return 'student'


    def display(self):
        return f"Name : {self.name}  Password: {self.password}"

    def menu_builder(self):
        if isinstance(self, Admin):
            for i,x in enumerate(self.menu_items,1):
                print(i,x)

        elif isinstance(self, Student):
            for i,x in enumerate(self.menu_items,1):
                print(i,x)




class Admin(User):
    menu_items = ["List books", "Create a book", "Delete a book", "Search for a book",
                   "List Users", "Create User", "Delete User", "Exit"]
    menu = Menu("Welcome to admin menu.",menu_items)



    def __init__(self,name, password,role = "admin"):
        super().__init__(name, password)

        self.role = role


class Student(User):

    menu_flag = False
    menu_items = ["Search for a book", "Add a book to my book list", "delete a book from my book list",
                   "Exit"]
    menu = Menu("Welcome to student menu.", menu_items)


    def __init__(self,name, password,role = "student"):
        super().__init__(name, password)

        self.role = role
        


class UserDB:

    example_users = {'Ahmet': ['1234', 'student'], 'Ayse': ['4321', 'student'], "admin": ["0000", 'admin']}
    users_object = {}
    
    def __init__(self,example_users_flag = True):
        UserDB.users_object={}
        self.example_users_flag = example_users_flag
        if example_users_flag == True:
            self.create_example_users()
        else:
            pass

    def add_user(self, name, password, role):
        if role == "student":
           std = Student(name,password)
           UserDB.users_object[name] = [password, role]

        elif role == "admin":
            adm = Admin(name,password)
            UserDB.users_object[name] = [password, role]

    def create_example_users(self):
        for x in UserDB.example_users:
            UserDB.add_user(self, x, UserDB.example_users[x][0], UserDB.example_users[x][1])

    def remove_user(self,name):
        UserDB.users_object.pop(name)
        print(self.list_user())
        return f"{name} is deleted."
        

    def list_user(self):
        student_users=[]
        for x,y in self.users_object.items():
            student_users.append(x)
        return student_users

    def validate_user(self,uid,password):

        try:
            if(self.users_object[uid][0] == password):

                print("Correct password.")
                if self.users_object[uid][1]=="admin":
                    _user=Admin(uid,self.users_object[uid][0],"admin")
                    return _user
                elif self.users_object[uid][1]=="student":
                    _user=Student(uid,self.users_object[uid][0],"student")  
                    return _user
                
            else:
                print("Wrong password.")
                return False
        except KeyError:
            print("User doesn't exist.")
            return False 

class Book:

    def __init__(self, bid, name, no_of_copies, list_of_authors):
        self.bid = bid
        self.name = name
        self.no_of_copies = no_of_copies
        self.list_of_authors = [list_of_authors]

    def display(self):
        return f"Book ID: {self.bid}, Book name: {self.name}, Number of copies: {self.no_of_copies}, Author list{self.list_of_authors}"


class Library:
    example_books = {"001": ["Biology", 2, ["Alice", "Bob"]],
                     "002": ["Chemistry", 3, ["Alice"]]
                     }
    author_to_books = {}
    book_objects = {}

    def __init__(self, example_books_flag= True):
        self.example_books_flag = example_books_flag

        if (example_books_flag==True):
            self.create_example_books()

    def create_example_books(self):
        for x in self.example_books:
            self.add_book(x,self.example_books[x][0],self.example_books[x][1],self.example_books[x][2])

    def add_book(self, bid, name, copies, authors):
        Library.book_objects[bid] = [name,copies,authors]
        Library.author_to_books[tuple(authors)] = [bid,name,copies]


    def remove_book(self):
        print(self.list_book())
        book_to_del = input("Select book to delete: ")
        for x,y in self.author_to_books.items():
            #print(x,y)
            if(y[1]==book_to_del):
                print(y[1],book_to_del)
                self.author_to_books[x] = []

        print("--->",self.author_to_books)
            

    def list_book(self):
        list_of_books= []
        for i in Library.book_objects:
            list_of_books.append(str(i)+" "+str(Library.book_objects[i][0])+" "+str(Library.book_objects[i][1])+" "+str(Library.book_objects[i][2]))
        return list_of_books

    def search_book(self):
        find_book = input("Select book to search: ")
        for i,j in Library.book_objects.items():
            if(find_book == j[0]):
               print("Found book:",j[0],j[1],j[2])


class Main:
    
    wants_to_exit=False
    def __init__(self):
        self.library=Library(True)
        self.userdb=UserDB(True)
        self.current_user=None
        self.login()

    def login(self):
        username=""
        password=""
        durum=""
        while self.wants_to_exit==False:
            print(self.userdb.list_user())
            self.username=input("Username: ")
            self.password=input("Password: ")
            print("user validating..")
            _user=self.userdb.validate_user(self.username,self.password)
            if _user!=False:
                if _user.role=="student":
                    self.show_student_menu()
                elif _user.role =="admin":
                    self.show_admin_menu()
            
    def show_admin_menu(self):
       
        admin = Admin(self.username, self.password)
        admin.menu.display(True)
        while True:
            print(admin.menu_builder())
            number = int(input("Choose an option: "))
            if number == 1:
                print(self.library.list_book())
            elif number == 2:
                bid=input("Book ID: ")
                name=input("Name: ")
                copies=input("Copies: ")
                authors=input("Authors: ")
                self.library.add_book(bid, name, copies,[authors])
                print(self.library.list_book())
                #print(self.library.create_example_books())
            elif number == 3:
                print(self.library.list_book())
                print(self.library.remove_book())
            elif number == 4:
                print(self.library.search_book())
            elif number == 5:
                print(self.userdb.list_user())
            elif number == 6:
                name=input("Name:")
                password=input("Password: ")
                role=input("Role: ")
                self.userdb.add_user(name, password, role)
                print(self.userdb.list_user())
            elif number == 7:
                print(self.userdb.list_user())
                user_to_del = input("Select user to delete: ")
                self.userdb.remove_user(user_to_del)
            else:
                print("Program ending...")
                self.wants_to_exit=True
                break


    def show_student_menu(self):


        student = Student(self.username, self.password)
        student.menu.display(True)
        while True:
            student.menu_builder()
            number = int(input("Choose an option: "))
            if number == 1:
                self.library.search_book()
            elif number == 2:
                bid=input("Book ID: ")
                name=input("Name: ")
                copies=input("Copies: ")
                authors=input("Authors: ")
                self.library.add_book(bid, name, copies,[authors])
                print(self.library.list_book())
            elif number == 3:
                self.library.remove_book()
            else:
                print("Program ending...")
                self.wants_to_exit=True
                break


main=Main()
