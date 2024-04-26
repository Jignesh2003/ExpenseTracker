from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
import mysql.connector 
from tkcalendar import Calendar
import datetime
import tkinter.font as font
con = None
#==============================
try:
	con = mysql.connector.connect(host="localhost",user="root",password="",database="expensetracker")
	cur = con.cursor()
	window = Tk()
	window.title("ExpenseTracker")
	class User:  #used to store the user logged in data
		def setId(self,id):
			self.id = id
		def setName(self,name):
			self.name = name
		def getId(self):
			return self.id
		def getName(self):
			return self.name
	userLoggedIn = User()
	#start of program
	loginFrame = Frame(master=window, width=350, height=400)
	loginFrame.pack(fill=BOTH,expand=True)

	#Register Frame Methods
	def handle_submit(event):
		pass1 = confirmPassRegTxt.get()
		pass2 = passRegTxt.get()
		if pass1 == pass2:
			cur.execute("insert into user(name,password) values('{}','{}');".format(nameRegTxt.get(),pass1))
			if cur.rowcount == 1:
				con.commit()
				cur.execute('select * from user where id = (select max(id) from user);')
				result = cur.fetchall()
				messagebox.showinfo("Sign up successfully","Welocome to expense tracker system. Your account number is {}".format(result[0][0]))
				RegisterationFrame.pack_forget()
				userLoggedIn.setId(result[0][0])
				userLoggedIn.setName(result[0][1])
				MainMenuFrame()	

		else:
			messagebox.showerror("Incorect password","Both password entered do not match")	

	def handle_clearRegBtn(event):
		nameRegTxt.delete(0,END)
		passRegTxt.delete(0,END)
		confirmPassRegTxt.delete(0,END)

	def handle_LoginBtn(event):
		RegisterationFrame.pack_forget()
		loginFrame.pack()

	def RegisterFrame():
		RegisterationFrame.pack(fill=BOTH,expand=True)

	RegisterationFrame = Frame(master=window, width=370, height=400)
	#registration frame components
	Label(master=RegisterationFrame,text="Register Yourself ",font=("Calibri",35,"bold","italic"),foreground="royalblue").place(x=15,y=30)
	Label(master=RegisterationFrame,text="Name:",font=("Arial",11,"bold")).place(x=50,y=150)
	Label(master=RegisterationFrame,text="Password:",font=("Arial",11,"bold")).place(x=50,y=200)
	Label(master=RegisterationFrame,text="Re Password:",font=("Arial",11,"bold")).place(x=50,y=250)
	nameRegTxt = Entry(master=RegisterationFrame)
	nameRegTxt.place(x=180,y=150)
	passRegTxt = Entry(master=RegisterationFrame,show="*")
	passRegTxt.place(x=180,y=200)
	confirmPassRegTxt = Entry(master=RegisterationFrame,show="*")
	confirmPassRegTxt.place(x=180,y=250)
	submitBtn = Button(master=RegisterationFrame,text="Sign up")
	submitBtn.bind("<Button-1>",handle_submit)
	submitBtn.place(x=75,y=300)
	clearRegBtn = Button(master=RegisterationFrame,text="Clear")
	clearRegBtn.bind("<Button-1>",handle_clearRegBtn)
	clearRegBtn.place(x=205,y=300)
	LoginBtn = Button(master=RegisterationFrame,text="Log in")
	LoginBtn.bind("<Button-1>",handle_LoginBtn)
	LoginBtn.place(x=140,y=350)


	#Main Frame Methods
	def handle_addIncome(event):
		MenuFrame.pack_forget()
		addIncomeFrameInstance.pack(fill=BOTH,expand=True)

	def handle_addExpense(event):
		MenuFrame.pack_forget()
		addExpenseFrameInstance.pack(fill=BOTH,expand=True)

	def handle_viewChart(event):
		MenuFrame.pack_forget()
		createPiechart()	

	def MainMenuFrame():
		MenuFrame.pack(fill=BOTH,expand=True)
		WelocomeLbl["text"]="Welcome {},".format(userLoggedIn.getName())
		
	# Main Menu components
	MenuFrame = Frame(master=window, width=370, height=400)
	WelocomeLbl = Label(master=MenuFrame,text="",font=("Calibri",30,"bold","italic"),foreground="royalblue")
	WelocomeLbl.place(x=50,y=50)
	addIncomeBtn = Button(master=MenuFrame,text="Add Income")
	addIncomeBtn.bind("<Button-1>",handle_addIncome)
	addIncomeBtn.place(x=50,y=150)
	addExpenseBtn = Button(master=MenuFrame,text="Add Expense")
	addExpenseBtn.bind("<Button-1>",handle_addExpense)
	addExpenseBtn.place(x=50,y=200)
	viewChartBtn = Button(master=MenuFrame,text="View Chart")
	viewChartBtn.bind("<Button-1>",handle_viewChart)
	viewChartBtn.place(x=50,y=250)

	#Add Income Frame
	def handle_addIncome_event(event):
		amount = incomeAmountTxt.get()
		if amount.isdigit() and int(incomeAmountTxt.get()) > 0:
			amount = int(amount)
			cur = con.cursor()
			month, day , year = incomeCal.get_date().split('/')
			year = '20'+year
			cur.execute("insert into income values({},{},'{}','{}-{}-{}');".format(userLoggedIn.getId(),amount,incomeSource.get(),year,month,day))
			if cur.rowcount == 1:
				messagebox.showinfo("Income registered","The record is successfully recorded.")
				con.commit()
				addIncomeFrameInstance.pack_forget()
				MenuFrame.pack(fill=BOTH,expand=True)
		else:
			messagebox.showerror("Incorect amount","There is some error in the amount entered")

	def handle_incomeBack_event(event):
		addIncomeFrameInstance.pack_forget()
		MenuFrame.pack(fill=BOTH,expand=True)

	#Add Income Components
	addIncomeFrameInstance = Frame(master=window,width=450, height=500)
	Label(master=addIncomeFrameInstance,text="Add Income ",font=("Calibri",30,"bold","italic"),foreground="royalblue").place(x=50,y=50)
	Label(master=addIncomeFrameInstance,text="Amount: ",font=("Arial",11,"bold")).place(x=50,y=150)
	Label(master=addIncomeFrameInstance,text="Date: ",font=("Arial",11,"bold")).place(x=50,y=200)
	Label(master=addIncomeFrameInstance,text="Income Source: ",font=("Arial",11,"bold")).place(x=50,y=400)
	incomeAmountTxt = Entry(master=addIncomeFrameInstance,text="")
	incomeAmountTxt.place(x=180,y=150)
	current_time = datetime.datetime.now()
	incomeCal = Calendar(master=addIncomeFrameInstance, selectmode = 'day',year = int(current_time.year), month = int(current_time.month),day = int(current_time.day))
	incomeCal.place(x=180,y=200)
	n = StringVar()
	incomeSource = Combobox(addIncomeFrameInstance, width = 27, 
	                            textvariable = n)  
	# Adding combobox drop down list
	incomeSource['values'] = (  'Active', 
	                          'Passive',
	                          'Diversification',
	                          'Earned Income',
	                          'Profit Income',
	                          'Interest Income', 
	                          'Dividend Income', 
	                          'Rental Income', 
	                          'Capital Gains Income', 
	                          'Royalty Income',
	                          'Other Income')
	incomeSource.place(x=180,y=400)
	incomeSource.current(0) 
	incomeSubmitBtn = Button(master=addIncomeFrameInstance,text="Submit")
	incomeSubmitBtn.bind("<Button-1>",handle_addIncome_event)
	incomeSubmitBtn.place(x=75,y=450)
	incomeBackBtn = Button(master=addIncomeFrameInstance,text="Back")
	incomeBackBtn.bind("<Button-1>",handle_incomeBack_event)
	incomeBackBtn.place(x=205,y=450)

	#Expense Frame Methods
	def handle_addExpense_event(event):
		try:
			amount = expenseAmountTxt.get()
			if amount.isdigit() and int(expenseAmountTxt.get()) > 0:
				cur = con.cursor()
				cur.execute('select sum(amount) from income where id={}'.format(userLoggedIn.getId()))
				result = cur.fetchall()
				totalIncome	= int(result[0][0])
				cur.execute('select sum(amount) from expense where id={}'.format(userLoggedIn.getId()))
				result = cur.fetchall()
				if result[0][0]==None:
					totalExpense = 0
				else:
					totalExpense = int(result[0][0])
				if int(amount) <= (totalIncome-totalExpense):
					amount = int(amount)
					cur = con.cursor()
					month, day , year = expenseCal.get_date().split('/')
					year = '20'+year
					cur.execute("insert into expense values({},{},'{}','{}-{}-{}');".format(userLoggedIn.getId(),amount,expenseCategory.get(),year,month,day))
					if cur.rowcount == 1:
						messagebox.showinfo("Expense registered","The record is successfully recorded.")
						con.commit()
						addExpenseFrameInstance.pack_forget()
						MenuFrame.pack(fill=BOTH,expand=True)
				else:
					messagebox.showerror("Low Balance","Expense is more than total income")
			else:
				messagebox.showerror("Incorect amount","There is some error in the amount entered")
		except:
			messagebox.showerror("Low Balance","Expense is more than total income")
	def handle_expenseBack_event(event):
		addExpenseFrameInstance.pack_forget()
		MenuFrame.pack(fill=BOTH,expand=True)

	#Expense Frame components
	addExpenseFrameInstance = Frame(master=window,width=450, height=500)
	Label(master=addExpenseFrameInstance,text="Add Expense ",font=("Calibri",30,"bold","italic"),foreground="royalblue").place(x=50,y=50)
	Label(master=addExpenseFrameInstance,text="Amount: ",font=("Arial",11,"bold")).place(x=50,y=150)
	Label(master=addExpenseFrameInstance,text="Date: ",font=("Arial",11,"bold")).place(x=50,y=200)
	Label(master=addExpenseFrameInstance,text="Expense Category: ",font=("Arial",11,"bold")).place(x=40,y=400)
	expenseAmountTxt = Entry(master=addExpenseFrameInstance,text="")
	expenseAmountTxt.place(x=180,y=150)
	current_time = datetime.datetime.now()
	expenseCal = Calendar(master=addExpenseFrameInstance, selectmode = 'day',year = int(current_time.year), month = int(current_time.month),day = int(current_time.day))
	expenseCal.place(x=180,y=200)
	n = StringVar()
	expenseCategory = Combobox(addExpenseFrameInstance, width = 27, 
	                            textvariable = n)  
	# Adding combobox drop down list
	expenseCategory['values'] = (  'Mortgage or rent payments', 
	                          'Loans',
	                          'Insurance',
	                          'Daycare',
	                          'Tuition',
	                          'Utilities', 
	                          'Groceries', 
	                          'Eating at restaurants', 
	                          'Clothing', 
	                          'Entertainment',
	                          'Travel',
	                          'Hobbies',
	                          'Gifts',
	                          'Other expense')
	expenseCategory.place(x=180,y=400)
	expenseCategory.current(0) 
	expenseSubmitBtn = Button(master=addExpenseFrameInstance,text="Submit")
	expenseSubmitBtn.bind("<Button-1>",handle_addExpense_event)
	expenseSubmitBtn.place(x=75,y=450)
	expenseBackBtn = Button(master=addExpenseFrameInstance,text="Back")
	expenseBackBtn.bind("<Button-1>",handle_expenseBack_event)
	expenseBackBtn.place(x=205,y=450)

	#Pie chart methods
	def handle_createPieChart(event):
		try:
			monthOfYear = month.get()
			cur = con.cursor()
			cur.execute("select sum(amount) from income where id = {} and monthname(date) = '{}' and year(date) = {};".format(userLoggedIn.getId(),monthOfYear,year.get()))
			result = cur.fetchall()
			if result[0][0]>=0:
				totalChartIncome = int(result[0][0])
			cur.execute("select sum(amount),category from expense where id = {} and monthname(date) = '{}' and year(date) = {};".format(userLoggedIn.getId(),monthOfYear,year.get()))
			result = cur.fetchall()
			if result[0][0]>=0:
				totalChartExpense = int(result[0][0])
			cur.execute("select sum(amount),category from expense where id = {} and monthname(date) = '{}' and year(date) = {} group by category;".format(userLoggedIn.getId(),monthOfYear,year.get()))
			result = cur.fetchall()
			canvas = Canvas(master=PieChartFrame,width=190,height=190)
			canvas.place(x=70,y=180)
			colorCategoryMap = {'Mortgage or rent payments': "gray",'Loans': "silver",'Insurance' : "maroon",'Daycare': "red",'Tuition': "purple",'Utilities' : "blue2",'Groceries' : "gray35",'Eating at restaurants' : "DeepSkyBlue2",'Clothing' : "olive",'Entertainment': "violet",'Travel' : "navy",'Hobbies' : "blue",'Gifts' : "teal",'Other expense': "aqua","Savings":"green"}
			begin = 360*0/totalChartIncome
			save = totalChartIncome - totalChartExpense
			if save == 1:
				save=0
			for row in result:
				e = 360*int(row[0])/totalChartIncome
				canvas.create_arc((2,10,140,150),fill=colorCategoryMap[row[1]],outline="black",start=begin,extent=e)
				begin += e
				if result[len(result)-1][1] == row[1] and save != 0:
				 	canvas.create_arc((2,10,140,150),fill=colorCategoryMap["Savings"],outline="black",start=begin,extent=360*save/totalChartIncome)
			i=180
			if len(labelList)>0:
				for label in labelList:
					label.destroy()
			for row in result:
				i += 15
				percent = int(row[0])/totalChartIncome*100
				str = row[1] + " {0:.2f}%".format(percent)
				labelList.append(Label(PieChartFrame,text=str,foreground=colorCategoryMap[row[1]]))
				labelList[len(labelList)-1].place(x=250,y=i) 
			i+=15
			percent = save/totalChartIncome*100
			labelList.append(Label(PieChartFrame,text="Savings {0:.2f}%".format(percent),foreground=colorCategoryMap['Savings']))
			labelList[len(labelList)-1].place(x=250,y=i)
		
		except:
			messagebox.showerror("No data","No data is there of the entered month and year")
	def handle_goBackPieChart(event):
		PieChartFrame.pack_forget()
		MenuFrame.pack()
	#Pie chart Frame Components
	def createPiechart():
		PieChartFrame.pack(fill=BOTH,expand=True)

	PieChartFrame = Frame(master=window, width=450, height=400)
	Label(master=PieChartFrame,text="Monthly chart ",font=("Calibri",30,"bold","italic"),foreground="royalblue").place(x=50,y=30)
	Label(master=PieChartFrame,text="Select the Month",font=("Arial",11,"bold")).place(x=50,y=100)
	Label(master=PieChartFrame,text="Select the Year",font=("Arial",11,"bold")).place(x=50,y=150)
	n = StringVar()
	month = Combobox(PieChartFrame, width = 10, 
	                            textvariable = n)  
	# Adding combobox drop down list
	month['values'] = ('January',
					   'February',
					   'March',
					   'April',
					   'May',
					   'June',
					   'July',
					   'August',
					   'September',
					   'October',
					   'November',				   
					   'December')
	month.place(x=180,y=100)
	month.current(0) 
	year = Entry(PieChartFrame,text="2021",width=13)
	year.insert(0,"{}".format(datetime.datetime.now().year))
	year.place(x=180,y=150)
	createBtn = Button(PieChartFrame, text="Create")
	createBtn.place(x=300,y=100)
	createBtn.bind("<Button-1>",handle_createPieChart)
	GoBackBtn = Button(PieChartFrame, text="Go Back")
	GoBackBtn.place(x=300,y=150)
	GoBackBtn.bind("<Button-1>",handle_goBackPieChart)
	labelList = []

	#Login Frame Methods
	def handle_clearBtn(event):
		accNoTxt.delete(0,END)
		passTxt.delete(0,END)
	def handle_loginBtn(event):
		AccountNumber = accNoTxt.get()
		Password = passTxt.get()
		#Checking acc ount number valid or not
		if AccountNumber.isdecimal():
			cur = con.cursor()
			cur.execute("select * from user where id={};".format(AccountNumber))
			result = cur.fetchall()
			if result:
				if result[0][2] == Password:
					messagebox.showinfo("Login Successful","Welocome to expense tracker system")
					loginFrame.pack_forget()
					userLoggedIn.setId(result[0][0])
					userLoggedIn.setName(result[0][1])
					MainMenuFrame()	
				else:
					messagebox.showerror("Login Unsuccessful","Invalid account number or password")	
			else:
				messagebox.showerror("Login Unsuccessful","Invalid account number or password")	

		else:
			messagebox.showerror("Incorrect Account number","Account number does not contain characters or special characters")
	def handle_registerBtn(event):
		loginFrame.pack_forget()
		RegisterFrame()
	#Login Frame Components
	Label(master=loginFrame,text="Expense Tracker",font=("Calibri",35,"bold","italic"),foreground="royalblue").place(x=15,y=30)
	Label(master=loginFrame,text="Account Number:",font=("Arial",11,"bold")).place(x=50,y=147)
	Label(master=loginFrame,text="Password:",font=("Arial",11,"bold")).place(x=50,y=197)
	accNoTxt = Entry(master=loginFrame)
	accNoTxt.place(x=180,y=150)
	passTxt = Entry(master=loginFrame,show="*")
	passTxt.place(x=180,y=200)
	loginBtn = Button(master=loginFrame,text="Login")
	loginBtn.bind("<Button-1>",handle_loginBtn)
	loginBtn.place(x=75,y=250)
	clearBtn = Button(master=loginFrame,text="Clear")
	clearBtn.bind("<Button-1>",handle_clearBtn)
	clearBtn.place(x=205,y=250)
	registerBtn = Button(master=loginFrame,text="Sign up")
	registerBtn.bind("<Button-1>",handle_registerBtn)
	registerBtn.place(x=140,y=300)
	window.mainloop()

except:
  	if con:
  		print("Some error occured")
  	else:
  		messagebox.showerror("Unable to connect to database","Check your network connections")
finally:
	if con:
		con.close()