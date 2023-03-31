from models import *
from database import init_db, db_session
from datetime import datetime

class Twitter:
    """
    The menu to print once a user has logged in
    """
    def print_menu(self):
        print("\nPlease select a menu option:")
        print("1. View Feed")
        print("2. View My Tweets")
        print("3. Search by Tag")
        print("4. Search by User")
        print("5. Tweet")
        print("6. Follow")
        print("7. Unfollow")
        print("0. Logout")
    
    """
    Prints the provided list of tweets.
    """
    def print_tweets(self, tweets):
        for tweet in tweets:
            print("==============================")
            print(tweet)
        print("==============================")

    """
    Should be run at the end of the program
    """
    def end(self):
        print("Thanks for visiting!")
        db_session.remove()
    
    """
    Registers a new user. The user
    is guaranteed to be logged in after this function.
    """
    def register_user(self):
        
        while True:
            username = input("What would you like your username to be?: ")
            user_exists = db_session.query(User).where(User.username == username).first()
            if(user_exists != None):
                print("Username is already taken, please try again")
            else:
                break

        while True:
            password = input("What would you like your password to be?: ")
            password_2 = input("Please re-enter your password ")
            if (password != password_2):
                print("These passwords do not match, please try again.")
            else:
                break
            
        

    """
    Logs the user in. The user
    is guaranteed to be logged in after this function.
    """
    def login(self):
        username = input("Enter username: ")
        password = input("Enter password: ")
        user = db_session.query(User).filter_by(User.username == username, User.password == password).first()
        while (user == None):
            print("Invalid username or password")
            username = input("Enter username: ")
            password = input("Enter password: ")
        self.current_user = user



    
    def logout(self):
        self.current_user = None
        self.end

    """
    Allows the user to login,  
    register, or exit.
    """
    def startup(self):
        print("Welcome to ATCS twitter!")
        choice = int(input("Please select a menu option: \n1: Login \n2: Register User \n3: Exit\n"))
        if (choice == 1):
            self.login()
        elif (choice == 2):
            self.register_user()
        else:
            self.end()

    def follow(self):
        follow = input("Who would you like to follow?\n")
        for i in self.current_user.following:
            if(follow == i.username):
                print("You already follow" + follow)
                return
            
        self.currentuser.following.append(db_session.query(User.where(User.username == follow).first()))
        db_session.commit()
        print("You are now following " + follow)
    def unfollow(self):
        pass

    def tweet(self):
        pass
    
    def view_my_tweets(self):
        pass
    
    """
    Prints the 5 most recent tweets of the 
    people the user follows
    """
    def view_feed(self):
        pass

    def search_by_user(self):
        pass

    def search_by_tag(self):
        pass

    """
    Allows the user to select from the 
    ATCS Twitter Menu
    """
    def run(self):
        init_db()

        print("Welcome to ATCS Twitter!")
        self.startup()

        self.print_menu()
        option = int(input(""))

        if option == 1:
            self.view_feed()
        elif option == 2:
            self.view_my_tweets()
        elif option == 3:
            self.search_by_tag()
        elif option == 4:
            self.search_by_user()
        elif option == 5:
            self.tweet()
        elif option == 6:
            self.follow()
        elif option == 7:
            self.unfollow()
        else:
            self.logout()
        
        self.end()
