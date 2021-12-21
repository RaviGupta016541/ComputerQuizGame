# computer quiz application using python tkinter
# mini project

from tkinter import *
from PIL import Image, ImageTk
import pymysql as py
import random
from threading import Thread
from time import sleep
from tkinter import messagebox
from datetime import datetime

db = py.connect(user="root",password="root",host="localhost",database="computerquiz")
mycursor = db.cursor()

root = Tk()
root.title("Computer quiz")
root.resizable(0,0)
root.geometry("700x600")
root.wm_iconbitmap('laptop.ico')

class ComputerQuiz:

    db = py.connect(user="root", password="root", host="localhost", database="computerquiz")
    mycursor = db.cursor()

    img1 = PhotoImage(file="compic.png")
    img2 = Image.open("start.png")
    img2 = img2.resize((100, 50), Image.ANTIALIAS)
    img22 = ImageTk.PhotoImage(img2)
    rule_img = Image.open("rulebutton.jpg")
    rule_img1 = rule_img.resize((90, 45), Image.ANTIALIAS)
    rule_img2 = ImageTk.PhotoImage(rule_img1)
    login_img = Image.open("login.png")
    login_img1 = login_img.resize((90, 45), Image.ANTIALIAS)
    login_img2 = ImageTk.PhotoImage(login_img1)
    register_img = Image.open("register2.png")
    register_img1 = register_img.resize((90, 45), Image.ANTIALIAS)
    register_img2 = ImageTk.PhotoImage(register_img1)
    back_img1 = Image.open("Back.jpg")
    back_img2 = back_img1.resize((90, 45), Image.ANTIALIAS)
    back_img3 = ImageTk.PhotoImage(back_img2)
    next_img1 = Image.open("Next1.png")
    next_img2 = next_img1.resize((90, 45), Image.ANTIALIAS)
    next_img3 = ImageTk.PhotoImage(next_img2)
    leaderbord_img1 = Image.open("leaderboard1.jpg")
    leaderbord_img2 = leaderbord_img1.resize((190, 55), Image.ANTIALIAS)
    leaderbord_img3 = ImageTk.PhotoImage(leaderbord_img2)

    userNameLoginvar = StringVar()
    userPassLoginvar = StringVar()
    userNameRegisterVar = StringVar()
    userPassword1RegisterVar = StringVar()
    userPassword2RegisterVar = StringVar()
    timerVar = IntVar()
    quesVar= StringVar()
    right = 0
    wrong = 0
    Game_score = 0
    listofquizid = []
    name = None
    stop_thread = False
    radiovar = StringVar()
    radiovar.set("L")
    times = 0
    run_once = 0
    quiz_type = None
    user_id=None
    score=None
    id=None
    count=1

    def next(self):

        self.ScoreFrame = Frame()
        self.ScoreFrame.place(x=0, y=0, width=700, height=600)
        self.ScoreFrame.configure(bg="light cyan")
        self.previous_score = 0
        self.attemp = self.right + self.wrong
        self.Game_score = self.right * 10
        self.Game_score = self.Game_score - (self.wrong * 2)
        try:  # if user not select any answer
            self.per = (self.right / self.attemp) * 100
        except:
            self.per = 0
        if self.per > 90:
            self.rating = "Excellent"
        elif self.per <= 90 and self.per > 80:
            self.rating = "Great"
        elif self.per <= 80 and self.per > 60:
            self.rating = "Very Good"
        elif self.per <= 60 and self.per > 40:
            self.rating = "Good"
        elif self.per <= 40 and self.per > 20:
            self.rating = "Not Good"
        else:
            self.rating = "Poor"

        self.backButton = Button(self.ScoreFrame, text="<-", image=self.back_img3, borderwidth=0, bg="light cyan", command=self.choose)
        self.backButton.place(x=2, y=3, width=50, height=20)
        self.credit_score = Label(self.ScoreFrame, text=self.rating + "! " + self.name.capitalize(), bg="light cyan", font=("", 30, 'bold'),
                             fg="purple3")
        self.credit_score.pack()
        self.score_ = Label(self.ScoreFrame, text=" YOURE SCORE ", bg="light cyan", fg="blue2", font=("Algerian", 30, "bold"))
        self.score_.pack(pady=25)
        self.total_attemp = Label(self.ScoreFrame, text="Total Attemp Questions -> " + str(self.attemp), fg="gray41", bg="light cyan",
                             font=("", 20))
        self.total_attemp.pack(pady=5)
        self.right_answers = Label(self.ScoreFrame, text="Right -> " + str(self.right), fg='green', bg="light cyan", font=("", 20))
        self.right_answers.pack(pady=5)
        self.wrong_answers = Label(self.ScoreFrame, text="Wrong -> " + str(self.wrong), fg='red', bg="light cyan", font=("", 20))
        self.wrong_answers.pack(pady=5)
        self.this_time_score = Label(self.ScoreFrame, text=" Your Game Score -> " + str(self.Game_score), fg="orange", bg="light cyan",
                                font=("", 20))
        self.this_time_score.pack(pady=7)

        self.sql = "select score from  players where user_id=%s"
        self.mycursor.execute(self.sql, (self.user_id,))
        self.alldata = self.mycursor.fetchall()
        for self.i in self.alldata:
            self.previous_score = self.i[0]
        self.total_score = self.previous_score + self.Game_score
        self.score = self.total_score
        self.sql2 = "update  players set score=%s where user_id=%s"
        self.mycursor.execute(self.sql2, (self.total_score, self.user_id))
        self.db.commit()
        self.tot_score = Label(self.ScoreFrame, text=" Now Your Total Score Is " + str(self.total_score), bg="light cyan", fg="orange red",
                          font=("", 22))
        self.tot_score.pack(pady=10)
        self.listofquizid.clear()

        self.right = 0
        self.wrong = 0
        self.run_once = 0
        self.currentTime = datetime.now()
        self.sql3 = "insert into  history (user_id,quiztype,score,date) values(%s,%s,%s,%s)"
        self.mycursor.execute(self.sql3, (self.user_id, self.quiz_type, self.Game_score, str(self.currentTime)))
        self.db.commit()

    def showhistory(self):
        self.historyFrame = Frame()
        self.historyFrame.place(x=0, y=0, width=700, height=600)
        self.historyFrame.configure(bg="light cyan")
        self.back_button = Button(self.historyFrame, text="<-", image=self.back_img3, borderwidth=0, bg="light cyan", command=self.choose,
                             width=50, height=20)

        self.back_button.grid(row=0, column=0, sticky='NW')
        self.historyLable = Label(self.historyFrame, text="     PLAY HISTORY", bg="light cyan", fg="blue2",
                             font=("Algerian", 22, "bold"),
                             width=13)
        self.historyLable.grid(row=0, column=1, pady=15)

        self.textLabelgametype = Label(self.historyFrame, text="  Game type", bg="light cyan", fg="purple2",
                                  font=("Engravers MT", 14, "bold"), width=10)
        self.textLabelgametype.grid(row=1, column=0, pady=7)

        self.textLabelscore = Label(self.historyFrame, text=" Score", bg="light cyan", fg="purple2",
                               font=("Engravers MT", 14, "bold"),
                               width=7)
        self.textLabelscore.grid(row=1, column=1)
        self.textLabelName = Label(self.historyFrame, text=" Date", bg="light cyan", fg="purple2",
                              font=("Engravers MT", 14, "bold"),
                              width=10)
        self.textLabelName.grid(row=1, column=2)
        self.sql = "select quiztype,score,date from  history where user_id=%s order by date"
        self.mycursor.execute(self.sql, (self.user_id,))
        self.record = self.mycursor.fetchall()
        self.index = 1
        for self.i in self.record:
            Label(self.historyFrame, text=self.i[0], font=("consolas", 12), bg="light cyan", fg="gray40").grid(row=self.index + 1,
                                                                                                     column=0)
            Label(self.historyFrame, text=self.i[1], font=("consolas", 12), bg="light cyan", fg="gray40").grid(
                row=self.index + 1, column=1)
            Label(self.historyFrame, text=self.i[2], font=("consolas", 12), bg="light cyan", fg="gray40").grid(row=self.index + 1,
                                                                                                     column=2)
            self.index = self.index + 1

    def timer(self):
        self.timer_secounds = 100
        while (self.timer_secounds >= 0):
            if self.timer_secounds > 0:
                self.timerVar.set(self.timer_secounds)
            elif (self.timer_secounds == 0):
                self.next()
            self.timer_secounds = self.timer_secounds - 1
            sleep(1)
            global stop_thread
            if self.stop_thread:
                self.stop_thread = False
                break
        self.timerVar.set("")

    def randomquiz(self):
        text = str(self.count) + "/10"
        print(text)
        self.quesVar.set(text)
        self.count = self.count + 1
        while (len(self.listofquizid) < 10):
            self.id = random.randrange(1, 15)
            if self.id in self.listofquizid:
                continue
            else:
                self.listofquizid.append(self.id)
                return self.id

        self.stop_thread = True
        self.next()

    def selected(self,SelectedRadioButton):
        self.SelectedRadioButton=SelectedRadioButton

        if self.times == 0:
            self.check = 0

            self.x = self.radiovar.get()
            self.t = int(self.x)
            self.sql = "select * from " + self.quiz_type + "  where ques_id=%s"
            self.mycursor.execute(self.sql, (self.id,))
            for self.i in self.mycursor.fetchall():
                self.rightans = self.i[6]
                if self.rightans == self.i[self.t + 1]:
                    self.check = 1

            if self.check == 1:
                self.right = self.right + 1
                self.SelectedRadioButton.configure(background="green2")

            else:
                self.wrong = self.wrong + 1
                self.SelectedRadioButton.configure(background="red")
        else:
            pass
        self.times += 1


    def question(self, quiz_type):
        self.quiz_type = quiz_type

        self.mt = Thread(target=self.timer)
        self.k = 1
        while self.k:
            if self.run_once == 0:
                self.mt.start()
                self.run_once = 2
            else:
                self.run_once = 2
            self.k = 0
        self.times = 0
        self.quizFrame = Frame()
        self.quizFrame.place(x=0, y=0, width=700, height=600)
        self.quizFrame.configure(bg="light cyan")
        self.quiz = None
        self.answer1 = None
        self.answer2 = None
        self.answer3 = None
        self.answer4 = None
        self.id = self.randomquiz()
        self.sql = "select * from " + self.quiz_type + " where ques_id=%s"
        self.mycursor.execute(self.sql, (self.id,))
        for self.i in self.mycursor.fetchall():
            self.quiz = self.i[1]
            self.answer1 = self.i[2]
            self.answer2 = self.i[3]
            self.answer3 = self.i[4]
            self.answer4 = self.i[5]
        self.questionq = Label(self.quizFrame, text=self.quiz, font=("consolas", 18), width=700, bg="light cyan", justify="center",
                          wraplength=500)
        self.questionq.pack(pady=5)
        self.radioButtonOption1 = Radiobutton(self.quizFrame, text=self.answer1, font=("Times", 14), bg="light cyan",
                                         variable =self.radiovar, value=1,
                                         command=lambda: self.selected( self.radioButtonOption1))
        self.radioButtonOption2 = Radiobutton(self.quizFrame, text=self.answer2, font=("Times", 14), bg="light cyan",variable=self.radiovar, value=2,
                                         command=lambda: self.selected( self.radioButtonOption2))
        self.radioButtonOption3 = Radiobutton(self.quizFrame, text=self.answer3, font=("Times", 14), bg="light cyan",
                                         variable=self.radiovar, value=3,
                                         command=lambda: self.selected( self.radioButtonOption3 ))
        self.radioButtonOption4 = Radiobutton(self.quizFrame, text=self.answer4, font=("Times", 14), bg="light cyan",
                                         variable=self.radiovar, value=4,
                                         command=lambda: self.selected( self.radioButtonOption4 ))
        self.radioButtonOption1.pack()
        self.radioButtonOption2.pack()
        self.radioButtonOption3.pack()
        self.radioButtonOption4.pack()

        self.questionremain = Label(self.quizFrame, text="Question remaing :-", bg="light cyan", font=("consolas", 14))
        self.questionremain.place(x=210, y=560, width=200, height=50)
        self.questionEntry = Entry(self.quizFrame, textvariable=self.quesVar, font=("consolas", 17))
        self.questionEntry.place(x=415, y=572, width=74, height=26)

        self.timeremain = Label(self.quizFrame, text="Time remaing :-", bg="light cyan", font=("consolas", 14))
        self.timeremain.place(x=10, y=465, width=150, height=50)
        self.TimerEntry = Entry(self.quizFrame, textvariable=self.timerVar, font=("consolas", 17))
        self.TimerEntry.place(x=175, y=475, width=43, height=28)

        self.nextbutton = Button(self.quizFrame, text="next", image=self.next_img3, borderwidth=0, bg="light cyan",
                            command=lambda: self.question(self.quiz_type))
        self.nextbutton.place(x=500, y=460, width=90, height=50)
        self.radiovar.set(0)

    def leaderboard(self):
        self.leaderboard_ = Frame()
        self.leaderboard_.configure(bg="light cyan")
        self.leaderboard_.place(x=0, y=0, width=700, height=600)
        self.back_button = Button(self.leaderboard_, text="<-", image=self.back_img3, borderwidth=0, bg="light cyan", command=self.choose,
                             width=50, height=20)
        self.back_button.grid(row=0, column=0, sticky='NW')
        self.leaderbo = Label(self.leaderboard_, text="LEADERBOARD", bg="light cyan", fg="blue2", font=("Algerian", 30, "bold"),
                         width=12)
        self.leaderbo.grid(row=0, column=2, pady=15)
        self.textLabelposition = Label(self.leaderboard_, text="Rank", bg="light cyan", fg="purple2",
                                  font=("Engravers MT", 16, "bold"), width=10)
        self.textLabelposition.grid(row=1, column=0, pady=7)
        self.textLabelName = Label(self.leaderboard_, text="Name", bg="light cyan", fg="purple2",
                              font=("Engravers MT", 16, "bold"), width=10)
        self.textLabelName.grid(row=1, column=2)
        self.textLabelscore = Label(self.leaderboard_, text="Score", bg="light cyan", fg="purple2",
                               font=("Engravers MT", 16, "bold"), width=7)
        self.textLabelscore.grid(row=1, column=4)
        self.sql = "select user,score from  players order by score DESC "
        self.mycursor.execute(self.sql)
        self.record = self.mycursor.fetchall()
        self.index = 1
        for self.i in self.record:
            Label(self.leaderboard_, text=self.index, font=("consolas", 17), bg="light cyan", fg="gray40").grid(row=self.index + 1,
                                                                                                      column=0)
            Label(self.leaderboard_, text=self.i[0].capitalize(), font=("consolas", 17), bg="light cyan", fg="gray40").grid(
                row=self.index + 1, column=2)
            Label(self.leaderboard_, text=self.i[1], font=("consolas", 17), bg="light cyan",
                  fg="gray40").grid(row=self.index + 1, column=4)
            self.index = self.index + 1

    def choose(self):
        self.count=1
        self.f5 = Frame()
        self.f5.configure(bg="light cyan")
        self.f5.place(x=0, y=0, width=700, height=600)
        self.show_name = Label(self.f5, text=self.name.capitalize(), font=("comic sans MS", 25, "bold",), bg="light cyan",
                          fg="dark violet")
        self.show_name.place(x=5, y=5)
        self.show_score = Label(self.f5, text=self.score, font=("comic sans MS", 25, "bold"), bg="light cyan", fg="dark violet")
        self.show_score.place(x=600, y=5)
        self.show_leaderboard = Button(self.f5, text="LEADERBOARD", image=self.leaderbord_img3, borderwidth=0, bg="light cyan",
                                  command=self.leaderboard)
        self.show_leaderboard.place(x=255, y=5, width=190, height=50)
        self.show_history = Button(self.f5, text="HISTORY", font=("georgia", 14), fg="blue", bg="cyan", command=self.showhistory)
        self.show_history.place(x=297, y=60, width=100, height=35)
        self.basiccomputerquizButton = Button(self.f5, text="Basic \n Computer Quiz", font=("georgia", 28, "bold"), bg="cyan",
                                         fg="blue", command=lambda: self.question("basicquiz"))
        self.basiccomputerquizButton.place(x=10, y=100, width=335, height=240)
        self.pythonbutton = Button(self.f5, text="Python Quiz", font=("georgia", 28, "bold"), bg="cyan", fg="blue",
                              command=lambda: self.question("python"))
        self.pythonbutton.place(x=355, y=100, width=335, height=240)
        self.javaButton = Button(self.f5, text="Java Quiz", font=("georgia", 28, "bold"), bg="cyan", fg="blue",
                            command=lambda: self.question("Java"))
        self.javaButton.place(x=10, y=350, width=335, height=240)
        self.CButton = Button(self.f5, text="C Quiz", font=("georgia", 28, "bold"), bg="cyan", fg="blue",
                         command=lambda: self.question("cquiz"))
        self.CButton.place(x=355, y=350, width=335, height=240)

    def insertdata(self):
        self.username = self.userNameRegisterVar.get()
        self.password1 = self.userPassword1RegisterVar.get()
        self.password2 = self.userPassword2RegisterVar.get()
        if self.username=="" or self.password1=="":
            messagebox.showerror("Registration failed.", "username or password must not be empty.")
        elif self.password1 != self.password2:
            messagebox.showerror("Registration failed.", "Password and confirm Password does not match.")
            self.userPassword1RegisterVar.set("")
            self.userPassword2RegisterVar.set("")

        else:
            self.tupleNamepass = (self.username, self.password1)
            self.sqlform = "insert into players (user,userpass) values(%s,%s)"
            self.mycursor.execute(self.sqlform, self.tupleNamepass)
            self.db.commit()
            messagebox.showinfo("Hello! " + self.username, "Registration successfull.\nNow Login to your account .")
            self.login()

    def log(self):
        self.check = 1
        self.username = self.userNameLoginvar.get()
        self.userpass = self.userPassLoginvar.get()
        self.sqlform = "select * from players"
        self.mycursor.execute(self.sqlform)
        self.alldata = self.mycursor.fetchall()
        for i in self.alldata:
            if i[1] == self.username and i[2] == self.userpass:
                self.user_id = i[0]
                self.score = i[3]
                self.check = 0
        if self.check == 0:
            messagebox.showinfo("Welcome", "successfully login")
            self.name = self.username
            self.choose()
        else:
            messagebox.showerror("Login failed", "Username or password did not match. \nplease enter valid id and password .")
            self.userNameLoginvar.set("")
            self.userPassLoginvar.set("")

    def login(self):
        self.loginFrame = Frame()
        self.loginFrame.configure(bg="light cyan")
        self.loginFrame.place(x=0, y=0, width=700, height=600)
        self.loginLabel = Label(self.loginFrame, fg="blue2", bg="light cyan", justify="center", text="ACCOUNT  LOGIN ",
                           font=("Algerian", 25, "bold"))
        self.loginLabel.pack(pady=30)
        self.enterLabel = Label(self.loginFrame, bg="light cyan", text="Enter Name", fg="purple2", font=("Arial", 20))
        self.enterLabel.place(x=175, y=150)
        self.EnterName = Entry(self.loginFrame, font=("Arial", 20), textvariable=self.userNameLoginvar)
        self.EnterName.place(x=400, y=155, height=30, width=170)
        self.passwordLabel = Label(self.loginFrame, bg="light cyan", text="Enter password", fg="purple2", font=("Arial", 20))
        self.passwordLabel.place(x=175, y=250)
        self.enterpassword = Entry(self.loginFrame, font=("Arial", 20), show='*', textvariable=self.userPassLoginvar)
        self.enterpassword.place(x=400, y=255, height=30, width=170)
        self.loginButton = Button(self.loginFrame, image=self.login_img2, borderwidth=0, bg="light cyan", text="login", command=self.log)
        self.loginButton.place(x=310, y=370, width=100, height=40)
        self.Backbutton = Button(self.loginFrame, text="<-", image=self.back_img3, borderwidth=0, bg="light cyan", command=self.page)
        self.Backbutton.place(x=2, y=3, width=50, height=20)

    def reg(self):
        self.registerFrame = Frame()
        self.registerFrame.place(x=0, y=0, width=700, height=600)
        self.registerFrame.configure(bg="light cyan")
        self.registereLabel = Label(self.registerFrame, fg="blue2", bg="light cyan", justify="center", text="ACCOUNT REGISTER",
                               font=("Algerian", 25, "bold"))
        self.registereLabel.pack(pady=30)
        self.EnterLabel = Label(self.registerFrame, bg="light cyan", text="Enter Name", fg="purple2", font=("Arial", 20))
        self.EnterLabel.place(x=135, y=150)
        self.EntryName = Entry(self.registerFrame, font=("Arial", 18), textvariable=self.userNameRegisterVar)
        self.EntryName.place(x=400, y=155, height=30, width=200)
        self.PasswordLabel = Label(self.registerFrame, text="Enter password", bg="light cyan", fg="purple2", font=("Arial", 20))
        self.PasswordLabel.place(x=135, y=215)
        self.passwordEntry1 = Entry(self.registerFrame, font=("Arial", 16), show='*', textvariable=self.userPassword1RegisterVar)
        self.passwordEntry1.place(x=400, y=220, height=30, width=200)
        self.confirmpassword = Label(self.registerFrame, text="Confirm password", bg="light cyan", fg="purple2",
                                font=("Arial", 20))
        self.confirmpassword.place(x=135, y=280)
        self.passwordEntry2 = Entry(self.registerFrame, font=("Arial", 16), show='*', textvariable=self.userPassword2RegisterVar)
        self.passwordEntry2.place(x=400, y=285, height=30, width=200)
        self.RegisterButton = Button(self.registerFrame, text="Register", bg="light cyan", image=self.register_img2, borderwidth=0,
                                command=self.insertdata)
        self.RegisterButton.place(x=320, y=380, width=100, height=40)
        self.BackButton = Button(self.registerFrame, text="<-", command=self.page, image=self.back_img3, borderwidth=0, bg="light cyan", )
        self.BackButton.place(x=2, y=3, width=50, height=20)

    def page(self):
        self.secondPage = Frame()
        self.secondPage.place(x=0, y=0, width=700, height=600)
        self.secondPage.configure(bg="light cyan")
        self.Loginlable = Label(self.secondPage, fg="blue", text="Welcome\n please login to your account", bg="light cyan",
                           justify="center", font=("comic sans MS", 20))
        self.Loginlable.pack(pady=50)
        self.loginButton = Button(self.secondPage, text="login", image=self.login_img2, borderwidth=0, bg="light cyan", command=self.login)
        self.loginButton.place(x=290, y=150, width=100, height=40)
        self.registerlable = Label(self.secondPage, fg="blue", text="Don't have an account? \n create account", bg="light cyan",
                              justify="center", font=("comic sans MS", 20))
        self.registerlable.pack(pady=80)
        self.registerButton = Button(self.secondPage, text="register", image=self.register_img2, borderwidth=0, bg="light cyan",
                                command=self.reg)
        self.registerButton.place(x=290, y=350, width=100, height=40)

    def home(self):
        def rules():
            labeltext = Label(self.home_frame,
                text="Each quiz contain 10 questions \n you will get 100 sec to solve a quiz \n once you select a option that will be a final choice \n you will get 10 score for every right  and -2 for wrong answer.",
                font=("comic sans MS", 15), bg="black", fg="white")
            labeltext.place(x=0, y=470, height=130, width=700)

        def about():
            labelabout = Label(self.home_frame,
                        text="hello user! \n This is a Simple Computer Quiz Game ,\n Made by Ravi Shankar Gupta and Uma Shankar.\n Play and enjoy \U0001f600.",
                        font=("comic sans MS", 15), bg="black", fg="white")
            labelabout.place(x=0, y=470, height=130, width=700)

        self.home_frame = Frame()
        self.home_frame.place(x=0, y=0, width=700, height=600)
        self.home_frame.config(bg="white")
        self.lableimage = Label(self.home_frame, image=self.img1, bg="white")
        self.lableimage.place(x=250, y=15)
        self.labletext = Label(self.home_frame, fg="blue", text="Computer quiz", font=("comic sans MS", 30, "bold"), bg="white")
        self.labletext.place(x=220, y=255)
        self.btnstart = Button(self.home_frame, image=self.img22, borderwidth=0, bg="white", command=self.page)
        self.btnstart.place(x=300, y=370, height=50, width=100)
        self.btnrules = Button(self.home_frame, image=self.rule_img2, bg="white", borderwidth=0, command=rules)
        self.btnrules.place(x=305, y=420, height=45, width=90)
        self.btnrules = Button(self.home_frame, text="About us", fg="black", borderwidth=0, command=about)
        self.btnrules.place(x=0, y=0, height=20, width=70)

    def __init__(self):
        self.home()

user = ComputerQuiz()
root.mainloop()