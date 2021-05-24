import tkinter as tk
from tkinter import *
import tkinter.font as tkFont
import tkinter.messagebox
import mysql.connector
import requests
import json


def exitProtocol(self):
    exitOption = tkinter.messagebox.askquestion("Exit?", "Are you sure you want to exit?")

    if exitOption == "no":
        pass
    else:
        app.destroy()


class setUp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        global currentTimeline
        currentTimeline = tk.StringVar()
        currentTimeline.set("1775 - 1861")
        global numquestions
        numquestions = tk.IntVar()
        numquestions.set(15)
        global questionsAnswered
        questionsAnswered = tk.IntVar()
        questionsAnswered.set(1)
        global questionsCorrect
        questionsCorrect = tk.IntVar()
        questionsCorrect.set(0)
        global percentCorrect
        percentCorrect = tk.StringVar()
        percentCorrect.set("0.0")
        global requestmade
        requestmade=False

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (startPage, settingsPage, questionsPage, pausePage, resultsPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(startPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()





class startPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        exitButton = Button(self, text="Exit", width=10, height=1, padx=10, pady=10, command=lambda:exitProtocol(self))
        exitButton.pack(side=LEFT, anchor=NW)

        settingsButton = Button(self, text="Settings", width=10, height=1, padx=10, pady=10,
                                command=lambda:controller.show_frame(settingsPage))
        settingsButton.pack(side=RIGHT, anchor=NE)

        fontStyle = tkFont.Font(family="Lucida Grande", size=15)
        startButton = Button(self, text="Start", width=20, height=2, font=fontStyle, bg="blue", fg="white",
                             command=lambda:controller.show_frame(questionsPage))
        startButton.pack(side=BOTTOM)

        fontStyle = tkFont.Font(family="Lucida Grande", size=35)
        title = Label(self, text="Time Line History Quiz", width=50, height=2, font=fontStyle)
        title.pack(side=TOP)

        fontStyle = tkFont.Font(family="Lucida Grande", size=12, slant="italic")
        description = Label(self, text="This program is meant to test your knowledge of the timelines of various "
                                       "periods of history.\n To change your time period, select settings in the top "
                                       "right corner. Once you have confirmed your correct time period, select start "
                                       "to begin the test.", font=fontStyle, height=10)
        description.pack(side=TOP)


class settingsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        def savechanges():
            global currentTimeline
            currentTimeline.set(clicked1.get())
            global numquestions
            numquestions.set(clicked2.get())

            if numquestions.get() >= 40:
                numareyousure = tkinter.messagebox.askquestion("Are you sure?",
                                                               "You have selected the option to have over 40 questions."
                                                               " This may take you a long time to complete. "
                                                               "Are you sure that this is the correct number "
                                                               "of questions?")
                if numareyousure == "yes":
                    pass
                else:
                    numquestions.set(15)
                    clicked2.set(numQuestionsOptions[2])

        homeButton = Button(self, text="Home", width=10, height=1, padx=10, pady=10,
                            command=lambda: controller.show_frame(startPage))
        homeButton.pack(side=LEFT, anchor=NW)

        fontStyle = tkFont.Font(family="Lucida Grande", size=35)
        title = Label(self, text="Settings", height=3, font=fontStyle)
        title.pack(side=TOP)

        fontStyle = tkFont.Font(family="lucida Grande", size=16)
        TPlabel = Label(self, text="Time Period", font=fontStyle)
        TPlabel.pack(side=TOP)

        fontStyle = tkFont.Font(family="lucida Grande", size=10, slant="italic")
        TP2label = Label(self, text="This will change the time period that you are asked questions and tested on",
                         font=fontStyle)
        TP2label.pack(side=TOP)

        timePeriodOptions = ["1775 - 1861",
                             "1862 - 1914",
                             "1915 - 1945",
                             "1946 - 1968",
                             "1969 - Present"]

        clicked1 = StringVar()
        clicked1.set(timePeriodOptions[0])

        drop1 = OptionMenu(self, clicked1, *timePeriodOptions)
        drop1.pack(side=TOP)

        fontStyle = tkFont.Font(family="lucida Grande", size=16)
        NQlabel = Label(self, text="Number of Questions", font=fontStyle)
        NQlabel.pack(side=TOP)

        fontStyle = tkFont.Font(family="lucida Grande", size=10, slant="italic")
        NQ2label = Label(self, text="This will change the total number of questions of the overall test",
                         font=fontStyle)
        NQ2label.pack(side=TOP)

        numQuestionsOptions = ["5","10","15","20","25","30","35","40","45","50"]

        clicked2 = StringVar()
        clicked2.set(numQuestionsOptions[2])

        drop2 = OptionMenu(self, clicked2, *numQuestionsOptions)
        drop2.pack(side=TOP)

        fontStyle = tkFont.Font(family="lucida Grande", size=12)
        selectButton = Button(self, text="Save Changes", bg="blue", fg="white", width=20, height=2, font=fontStyle,
                              command=savechanges)
        selectButton.pack(side=BOTTOM)


class Question:
  def __init__(self, text, date):
    self.text = tk.StringVar()
    self.text.set(text)
    self.date = tk.StringVar()
    self.date.set(date)


class questionsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)


        def homeProtocol():
            exitOption = tkinter.messagebox.askquestion("Exit To Home?", "Are you sure you want to quit the test? "
                                                                         "All progress will be lost")

            if exitOption == "no":
                pass
            else:
                global questionsAnswered
                questionsAnswered.set(1)
                controller.show_frame(startPage)

        def conversion(change):
            if change == "1st":
                return 1
            elif change == "2nd":
                return 2
            elif change == "3rd":
                return 3
            else:
                return 4

        def checkCorrect():
            ans1 = conversion(clicked1.get())
            ans2 = conversion(clicked2.get())
            ans3 = conversion(clicked3.get())
            ans4 = conversion(clicked4.get())

            answersConverted = [ans1, ans2, ans3, ans4]

            questions1 = question1txt.date.get()
            questions2 = question2txt.date.get()
            questions3 = question3txt.date.get()
            questions4 = question4txt.date.get()

            questions = [questions1, questions2, questions3, questions4]
            questionsSorted = sorted(questions)

            for i in range(0, 4):
                if answersConverted[i] == questionsSorted.index(questions[i]) + 1:
                    pass
                else:
                    return False
            return True

        def updatequestions():
            global requestmade
            request = {}
            request = requests.get("http://flip3.engr.oregonstate.edu:6952/query")
            requestmade = True
            response = request.json()
            question1txt.text.set(response[0]['name'])
            question1txt.date.set(response[0]['date'])
            question2txt.text.set(response[1]['name'])
            question2txt.date.set(response[1]['date'])
            question3txt.text.set(response[2]['name'])
            question3txt.date.set(response[2]['date'])
            question4txt.text.set(response[3]['name'])
            question4txt.date.set(response[3]['date'])

            clicked1.set(Answers[0])
            clicked2.set(Answers[0])
            clicked3.set(Answers[0])
            clicked4.set(Answers[0])

        def updateServer():
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd="Celticsbasketball2001.",
                database="mainbase"
            )

            cur = db.cursor()

            global numquestions
            global questionsCorrect
            global percentCorrect


            cur.execute("INSERT INTO finaltab (numbercorrect, numberofquestions, percentage) VALUES (%s, %s, %s)",
                        (questionsCorrect.get(), numquestions.get(), percentCorrect.get()))
            db.commit()
            controller.show_frame(resultsPage)

        def endTest():
            global numquestions
            global questionsAnswered
            global percentCorrect
            global questionsCorrect
            questionsAnswered.set(questionsAnswered.get() + 1)
            correct = checkCorrect()
            if correct:
                questionsCorrect.set(questionsCorrect.get() + 1)

            if questionsAnswered.get() > numquestions.get():
                questionsAnswered.set(1)
                percentCorrect.set(str((questionsCorrect.get() / numquestions.get()) * 100) + "%")
                updateServer()

            else:
                updatequestions()
                pass


        homeButton = Button(self, text="Home", width=10, height=1, padx=10, pady=10, command=homeProtocol)
        homeButton.pack(side=LEFT, anchor=NW)

        pauseButton = Button(self, text="Pause", width=10, height=1, padx=10, pady=10,
                             command=lambda:controller.show_frame(pausePage))
        pauseButton.pack(side=RIGHT, anchor=NE)


        global currentTimeline
        fontStyle = tkFont.Font(family="lucida Grande", size=18)
        timeperiodlabel = Label(self, textvariable=currentTimeline, font=fontStyle)
        timeperiodlabel.pack(side=TOP)

        QuestionFrame = Frame(self)
        AnswersFrame = Frame(self)
        nextframe = Frame(self)
        questionframe = Frame(self)
        QuestionFrame.place(relx=.05, rely=.4, anchor=W)
        AnswersFrame.place(relx=.8, rely=.4, anchor=E)
        questionframe.place(relx=.1, rely=1, anchor=S)
        nextframe.place(relx=.95, rely=1, anchor=S)

        question1txt = Question("", 0)
        question1 = Label(QuestionFrame, textvariable=question1txt.text, font=fontStyle)
        question1.pack()
        spacer1 = Label(QuestionFrame, text="")
        spacer1.pack()

        question2txt = Question("", 0)
        question2 = Label(QuestionFrame, textvariable=question2txt.text, font=fontStyle)
        question2.pack()
        spacer2 = Label(QuestionFrame, text="")
        spacer2.pack()

        question3txt = Question("", 0)
        question3 = Label(QuestionFrame, textvariable=question3txt.text, font=fontStyle)
        question3.pack()
        spacer3 = Label(QuestionFrame, text="")
        spacer3.pack()

        question4txt = Question("", 0)
        question4 = Label(QuestionFrame, textvariable=question4txt.text, font=fontStyle)
        question4.pack()

        Answers = ["1st",
                   "2nd",
                   "3rd",
                   "4th"]

        clicked1 = StringVar()
        clicked1.set(Answers[0])
        drop1 = OptionMenu(AnswersFrame, clicked1, *Answers)
        drop1.pack(side=TOP)
        spacer21 = Label(AnswersFrame, text="")
        spacer21.pack()
        clicked2 = StringVar()
        clicked2.set(Answers[0])
        drop2 = OptionMenu(AnswersFrame, clicked2, *Answers)
        drop2.pack(side=TOP)
        spacer22 = Label(AnswersFrame, text="")
        spacer22.pack()
        clicked3 = StringVar()
        clicked3.set(Answers[0])
        drop3 = OptionMenu(AnswersFrame, clicked3, *Answers)
        drop3.pack(side=TOP)
        spacer23 = Label(AnswersFrame, text="")
        spacer23.pack()
        clicked4 = StringVar()
        clicked4.set(Answers[0])
        drop4 = OptionMenu(AnswersFrame, clicked4, *Answers)
        drop4.pack(side=TOP)

        global numquestions
        global questionsAnswered
        fontStyle = tkFont.Font(family="lucida Grande", size=20)
        CurQuestion = Label(questionframe, textvariable=questionsAnswered, font=fontStyle)
        spacerlabel = Label(questionframe, text="/", font=fontStyle)
        totalQuestions = Label(questionframe, textvariable=numquestions, font=fontStyle)
        CurQuestion.pack(side=LEFT)
        spacerlabel.pack(side=LEFT)
        totalQuestions.pack(side=LEFT)

        NextButton = Button(nextframe, text="Next", font=fontStyle, bg = "Orange", command=endTest)
        NextButton.pack(side=RIGHT)

        global requestmade
        request = {}
        if requestmade == False:
            request = requests.get("http://flip3.engr.oregonstate.edu:6952/query")
            requestmade = True
        response = request.json()
        question1txt.text.set(response[0]['name'])
        question1txt.date.set(response[0]['date'])
        question2txt.text.set(response[1]['name'])
        question2txt.date.set(response[1]['date'])
        question3txt.text.set(response[2]['name'])
        question3txt.date.set(response[2]['date'])
        question4txt.text.set(response[3]['name'])
        question4txt.date.set(response[3]['date'])


class pausePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        def homeProtocol():
            exitOption = tkinter.messagebox.askquestion("Exit To Home?", "Are you sure you want to quit the test? "
                                                                         "All progress will be lost")

            if exitOption == "no":
                pass
            else:
                global questionsAnswered
                questionsAnswered.set(1)
                controller.show_frame(startPage)

        homeButton = Button(self, text="Home", width=10, height=1, padx=10, pady=10, command=homeProtocol)
        homeButton.pack(side=LEFT, anchor=NW)

        fontStyle = tkFont.Font(family="Lucida Grande", size=15)
        ResumeButton = Button(self, text="Resume", width=20, height=2, font=fontStyle, bg="blue", fg="white",
                              command=lambda: controller.show_frame(questionsPage))
        ResumeButton.pack(side=BOTTOM)

        fontStyle = tkFont.Font(family="Lucida Grande", size=20)
        PausedLabel = Label(self, pady=30, text="The Test Has Been Paused", font=fontStyle)
        PausedLabel.pack(side=TOP)

        curansweredlbl = Frame(self)
        curansweredlbl.place(relx=.5, rely=.5, anchor="center")

        global questionsAnswered
        qnumlbl = Label(curansweredlbl, text="Question Number: ", font=fontStyle)
        curQuestion = Label(curansweredlbl, textvariable=questionsAnswered, font=fontStyle)
        qnumlbl.pack(side=LEFT)
        curQuestion.pack(side=LEFT)


class resultsPage(tk.Frame):
    def __init__(self, parent, controller):

        def percentfinished():
            global numquestions
            global questionsCorrect

            total = (questionsCorrect.get() / numquestions.get()) * 100
            return total


        tk.Frame.__init__(self,parent)
        exitButton = Button(self, text="Exit", width=10, height=1, padx=10, pady=10, command=lambda: exitProtocol(self))
        exitButton.pack(side=LEFT, anchor=NW)

        fontStyle = tkFont.Font(family="Lucida Grande", size=12)
        startButton = Button(self, text="Home", width=20, height=2, font=fontStyle, bg="blue", fg="white",
                             command=lambda: controller.show_frame(startPage))
        startButton.pack(side=BOTTOM)

        fontStyle = tkFont.Font(family="lucida Grande", size=18)
        timeperiodlabel = Label(self, textvariable=currentTimeline, font=fontStyle)
        timeperiodlabel.pack(side=TOP)

        fontStyle = tkFont.Font(size=24)
        finishedlabel = Label(self, text="Finished! Here's The Results", font=fontStyle)
        finishedlabel.pack(side=TOP)

        keyframe = Frame(self)
        resultframe = Frame(self)
        keyframe.place(relx=.40, rely=.5)
        resultframe.place(relx=.60, rely=.5)

        global questionsCorrect
        global numquestions
        global percentCorrect
        fontStyle = tkFont.Font(size=16)
        numCorrect = Label(keyframe, text="Total Correct:", font=fontStyle)
        numCorrect.pack()
        CurQuestion = Label(resultframe, textvariable=questionsCorrect, font=fontStyle)
        spacerlabel = Label(resultframe, text="/", font=fontStyle)
        totalQuestions = Label(resultframe, textvariable=numquestions, font=fontStyle)
        percentCorrectlbl = Label(keyframe, text="Percent Correct:", font=fontStyle)
        percentCorrectlbl.pack()
        PercentLabel = Label(resultframe, textvariable=percentCorrect, font=fontStyle)
        PercentLabel.pack(side=BOTTOM)
        CurQuestion.pack(side=LEFT)
        spacerlabel.pack(side=LEFT)
        totalQuestions.pack(side=LEFT)


app = setUp()
app.title("Time Line Test")



app.mainloop()