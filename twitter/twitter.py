from models import *
from database import init_db, db_session
from datetime import datetime

class Twitter:
    """
    The menu to print once a user has logged in
    """
    def __init__(self):
        self.current_user = None

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
        count = 0
        while(count == 0):
            #Gets inputs from user
            uname = input("What would you like your username to be?: ")
            password = input("Enter a password: ")
            verify = input("Re-enter your password: ")

            #Checks if username is already in database
            if db_session.query(User).where(User.username == uname).count() > 0:
                print("Username is already taken, please try again")
            #checks if password is equal to the verification password
            elif (password != verify):
                print("Passwords don't match, please try again")
            else:
                #adds new user to database with inputs
                user = User(username = uname, password = password, following = [], followers = [])
                db_session.add(user)
                db_session.commit()
                print("Welcome to ATCS Twitter!")
                self.current_user = user
                break






        
            
        

    """
    Logs the user in. The user
    is guaranteed to be logged in after this function.
    """
    def login(self):
        #gets inputs from user to login
        username = input("Enter username: ")
        password = input("Enter password: ")
        user = db_session.query(User).where((User.username == username)&(User.password == password)).first()
        #checks if the inputs already in database
        while (user == None):
            print("Invalid username or password")
            username = input("Enter username: ")
            password = input("Enter password: ")
            user = db_session.query(User).where((User.username == username)&(User.password == password)).first()
        self.current_user = user



    
    def logout(self):
        #logouts user
        self.current_user = None
        self.end

    """
    Allows the user to login,  
    register, or exit.
    """
    def startup(self):
        print("Welcome to ATCS twitter!")
        #prints each option to do
        choice = int(input("Please select a menu option: \n1: Login \n2: Register User \n3: Exit\n"))
        if (choice == 1):
            self.login()
        elif (choice == 2):
            self.register_user()
        else:
            self.end()

    def follow(self):
        #follow another user in the database
        account = input("Who would you like to follow? ")
        #iterates through the users following list to see if they follow that person
        for i in self.current_user.following:
            if(account == i.username):
                print("You already follow" + account)
                return
            
        #gets all of the users
        all = db_session.query(User).all()
        #adds the user to the other users following list
        for i in all:
            if i.username == account:
                self.current_user.following.append(db_session.query(User).where(User.username == account).first())
                db_session.commit()
                print("You are now following " + account)
                return
            print("User not found")

    
    def unfollow(self):
        account = input("Who would you like to unfollow? ")
        #iterates through their following to see if they are following that person
        for i in self.current_user.following:
            if(account == i.username):
                #removes person from the following list
                self.current_user.following.remove(db_session.query(User).where(User.username == account).first())
                db_session.commit()
                print("You no longer follow " + account)
                return
        #if they don't follow that person returns this
        print("You don't follow " + account)


    def tweet(self):
        #gets tweet info
        content = input("Enter your tweet: ")
        tags = input("Enter the tags, seperate by spaces: ")
        lst = tags.split()
        tags2 = []

        #adds the tags and the tweet content to the database
        for tag in lst:
            tags2.append(tag)
        timestamp = datetime.now()
        twt = Tweet(content = content, username = self.current_user.username, timestamp = timestamp)
        db_session.add(twt)
        db_session.commit()

        temp = None
        for i in range(len(tags2)):
            #checks if tag exists and if doesn't adds it to the database
            if db_session.query(Tag).where(Tag.content == tags2[i]).count() == 0:
                temp = Tag(content = tags2[i])
                db_session.add(temp)
                twt.tags.append(temp)
            else:
                #if tweet exists, add tags to list of tags
                temp = db_session.query(Tag).where(Tag.content == tags2[i]).first()
                temp2 = db_session.query(Tweet).where(Tweet.timestamp == timestamp).first()
                temp.tweets.append(temp2)
        db_session.commit()

    
    def view_my_tweets(self):
        #views users tweets
        t = self.current_user.tweets
        self.print_tweets(t)
    
    """
    Prints the 5 most recent tweets of the 
    people the user follows
    """
    def view_feed(self):
        #sets variables
        following = []
        feed = []
        count = 0
        #gets usernames in following 
        for user in self.current_user.following:
            following.append(user.username)
        #gets all the tweets
        all_tweets = db_session.query(Tweet).order_by(Tweet.timestamp.desc()).all()
        for i in all_tweets:
            #sets the tweet amount to only 5
            if(count == 5):
                break
            #only gets it if user is following the user 
            if(i.username in following):
                feed.append(i)
                count = count + 1
        #prints tweets
        self.print_tweets(feed)

            
            


    def search_by_user(self):
        use = input("Who would you like to search for? ")
        #sees if user is in database
        if db_session.query(User).where(User.username == use).count() == 0:
            print("There is no user by that name")
        else:
            #if user is prints the tweets of the user
            twts = db_session.query(Tweet).where(Tweet.username == use).all()
            self.print_tweets(twts)

    def search_by_tag(self):
        tg = input("What tag would you like to search for? ")
        #checks if tag exists
        if db_session.query(Tag).where(Tag.content == tg).count() == 0:
            print("There are no tweets with this tag")
        else:
            #if tag exists gets all the tweets from the tag and prints the tweets
            twts = []
            total = db_session.query(Tweet).order_by(Tweet.timestamp.desc()).all()
            for i in total:
                for tags in i.tags:
                    if(tg == tags.content):
                        twts.append(i)
            self.print_tweets(twts)


    """
    Allows the user to select from the 
    ATCS Twitter Menu
    """
    def run(self):
        #runs program
        init_db()
        count = 0
        print("Welcome to ATCS Twitter!")
        self.startup()

        while(count == 0):
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
                count = count + 1

            
        self.end()
