from functools import partial
import json
import tkinter as tk
from tkinter import StringVar, ttk
import os.path
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
import random
import string
from datetime import datetime as dt


class UserInfo(tk.Toplevel):
	def __init__(self, parent, user):
		super().__init__(parent)

		self.geometry('350x200')
		self.title('User Info')

		self.user_info = user
		self.usernamestr = StringVar()
		self.passstr = StringVar()
		self.emailstr = StringVar()
		self.ignstr = StringVar()
		self.usernamestr.set(self.user_info.get('Username', ''))
		self.passstr.set(self.user_info.get('Password', ''))
		self.emailstr.set(self.user_info.get('Email', ''))
		self.ignstr.set(self.user_info.get('ign', ''))
		ttk.Label(self, text="Account Information").grid(row=0, column=1)
		ttk.Label(self, text="IGN").grid(row=1,column=0)
		ttk.Entry(self, textvariable=self.ignstr).grid(row=1, column=2)
		ttk.Label(self, text="Username").grid(row=2,column=0)
		ttk.Entry(self, textvariable=self.usernamestr, state="readonly").grid(row=2, column=2)
		ttk.Label(self, text="Password").grid(row=3,column=0)
		ttk.Entry(self, textvariable=self.passstr, state="readonly").grid(row=3, column=2)
		ttk.Label(self, text="Email").grid(row=4,column=0)
		ttk.Entry(self, textvariable=self.emailstr, state="readonly").grid(row=4, column=2)

		ttk.Button(self, text="Save", command=self.save).grid(row=6, column=2)

	def save(self):
		with open('./valo acc.json', 'r') as infile:
			data = json.loads(infile.read())
		data[self.usernamestr.get()]['ign'] = self.ignstr.get()
		with open('./valo acc.json', 'w') as outfile:
			outfile.write(json.dumps(data))
			outfile.close()

class CreateAccount(tk.Toplevel):
	def __init__(self, parent):
		super().__init__(parent)

		self.geometry('400x200')
		self.title('Create Account')
		self.usernamestr = StringVar()
		self.passstr = StringVar()
		self.emailstr = StringVar()
		self.ignstr = StringVar()
		ttk.Label(self, text="Account Information").grid(row=0, column=1)
		ttk.Label(self, text="Account Name*").grid(row=1,column=0)
		ttk.Entry(self, textvariable=self.ignstr).grid(row=1, column=2)
		ttk.Label(self, text="Username").grid(row=2,column=0)
		ttk.Entry(self, textvariable=self.usernamestr).grid(row=2, column=2)
		ttk.Label(self, text="Password").grid(row=3,column=0)
		ttk.Entry(self, textvariable=self.passstr).grid(row=3, column=2)
		ttk.Label(self, text="Email").grid(row=4,column=0)
		ttk.Entry(self, textvariable=self.emailstr).grid(row=4, column=2)
		
		ttk.Button(self, text='Create Account', command= self.createUser).grid(row=5,column=1)
	
	def randomUserInfoGen(self):
		char = string.ascii_letters
		size = 10
		self.username = ''.join(random.choice(char) for _ in range(size))
		self.email = self.username.lower() + '@gmail.com'
		self.password = 'valo1234'
	
	def getUserInput(self):
		self.username = self.usernamestr.get() or self.username
		self.email = self.emailstr.get() or self.email
		self.password = self.passstr.get() or self.password
		self.ign = self.ignstr.get() or 'NULL'
		self.usernamestr.set("")
		self.emailstr.set("")
		self.passstr.set("")
		self.ignstr.set("")

	def webCode(self):
		url = 'https://signup.euw.leagueoflegends.com/en/signup/index#/'
		options = webdriver.ChromeOptions()
		options.add_argument("--start-maximized")
		options.add_argument('--log-level=3')
		options.add_argument('--no-sandbox')
		
		# Provide the path of chromedriver present on your system.
		driver = webdriver.Chrome(executable_path="./chromedriver", chrome_options=options)
		driver.set_window_size(1920, 1080)
		driver.get(url)
		time.sleep(3)

		# Page 1 (Email entry)
		driver.find_element_by_name('email').send_keys(self.email)
		driver.find_element_by_css_selector('.next-button button').click()
		time.sleep(3)
		

		# Page 2 (DOB)
		daySelect = Select(driver.find_element_by_name('dob-day'))
		daySelect.select_by_value('1')
		monthSelect = Select(driver.find_element_by_name('dob-month'))
		monthSelect.select_by_value('1')
		yearSelect = Select(driver.find_element_by_name('dob-year'))
		yearSelect.select_by_value('1969')
		driver.find_element_by_css_selector('.next-button button').click()
		time.sleep(3)
		

		# Page 3 (Final Username and Password)
		driver.find_element_by_name('username').send_keys(self.username)
		driver.find_element_by_name('password').send_keys(self.password)
		driver.find_element_by_name('confirm_password').send_keys(self.password)
		driver.find_element_by_css_selector('div.checkbox-indicator').click()
		driver.find_element_by_css_selector('.next-button button').click()
		time.sleep(30)
		driver.close()

	def appendUserInfoText(self):
		self.user = {
			'Date Created' : dt.now().strftime('%d/%m/%Y'),
			'Username': self.username,
			'Email': self.email,
			'Password': self.password,
			'ign': self.ign
		}
		if (os.path.exists('./valo acc.json')):
			with open('./valo acc.json', 'r') as infile:
				data = infile.read()
		else: 
			data = ''
		with open('./valo acc.json','w+') as outfile:
			if data == '':
				writedata = {self.username: self.user}
				json_string = json.dumps(writedata)
				outfile.write(json_string)
				outfile.close()
			else:
				json_obj = json.loads(data)
				json_obj[self.username] = self.user
				json_string = json.dumps(json_obj)
				outfile.write(json_string)
				outfile.close()
	
	def show_user_detail(self):
		window = UserInfo(self, self.user)
		window.grab_set()

	def createUser(self):
		self.randomUserInfoGen()
		self.getUserInput()
		self.webCode()
		self.appendUserInfoText()
		self.show_user_detail()

class ViewAccount(tk.Toplevel):
	def __init__(self, parent):
		super().__init__(parent)

		

		self.title('View Accounts')
		self.data = self.get_data()
		if self.data == '':
			ttk.Label(self, text='No Accounts File Found').pack(expand=True)
		else:
			ttk.Label(self, text='Accounts').pack(expand=True)
			for username in self.data:
				ttk.Button(self, text=self.data[username]['ign'], command=partial(self.show_user_detail, self.data[username])).pack(expand=True, padx=(100, 100))

	def show_user_detail(self, user):
		window = UserInfo(self, user)
		window.grab_set()
	
	def get_data(self):
		if (os.path.exists('./valo acc.json')):
			with open('./valo acc.json', 'r') as infile:
				data = json.loads(infile.read())
				infile.close()
		else: 
			data = ''
		return data

class passwordManager(tk.Toplevel):
	def __init__(self, parent):
		super().__init__(parent)

		self.geometry('500x200')
		self.title('Add Accounts')

		self.usernamestr = StringVar()
		self.passstr = StringVar()
		self.emailstr = StringVar()
		self.ignstr = StringVar()
		ttk.Label(self, text="Account Information").grid(row=0, column=1)
		ttk.Label(self, text="Account Name*").grid(row=1,column=0)
		ttk.Entry(self, textvariable=self.ignstr).grid(row=1, column=2)
		ttk.Label(self, text="Username").grid(row=2,column=0)
		ttk.Entry(self, textvariable=self.usernamestr).grid(row=2, column=2)
		ttk.Label(self, text="Password").grid(row=3,column=0)
		ttk.Entry(self, textvariable=self.passstr).grid(row=3, column=2)
		ttk.Label(self, text="Email").grid(row=4,column=0)
		ttk.Entry(self, textvariable=self.emailstr).grid(row=4, column=2)
		
		ttk.Button(self, text='Add Account', command= self.addUser).grid(row=5,column=1)

	def getUserInput(self):
		self.username = self.usernamestr.get() or ''
		self.usernamestr.set("")
		self.email = self.emailstr.get() or ''
		self.emailstr.set("")
		self.password = self.passstr.get()  or ''
		self.passstr.set("")
		self.ign = self.ignstr.get() or 'Null'
		self.ignstr.set("")

	def appendUserInfoText(self):
		self.user = {
			'Date Created' : dt.now().strftime('%d/%m/%Y'),
			'Username': self.username,
			'Email': self.email,
			'Password': self.password,
			'ign': self.ign
		}
		if (os.path.exists('./valo acc.json')):
			with open('./valo acc.json', 'r') as infile:
				data = infile.read()
		else: 
			data = ''
		with open('./valo acc.json','w+') as outfile:
			if data == '':
				writedata = {self.username: self.user}
				json_string = json.dumps(writedata)
				outfile.write(json_string)
				outfile.close()
			else:
				json_obj = json.loads(data)
				json_obj[self.username] = self.user
				json_string = json.dumps(json_obj)
				outfile.write(json_string)
				outfile.close()
	
	def show_user_detail(self):
		window = UserInfo(self, self.user)
		window.grab_set()

	def addUser(self):
		self.getUserInput()
		self.appendUserInfoText()
		self.show_user_detail()

class App(tk.Tk):
	def __init__(self):
		super().__init__()
		self.geometry('500x200')
		self.title('Valo Accounts')
		ttk.Button(self, text='Create User Account', command=self.createUserAcc).pack(expand=True)
		ttk.Button(self, text='View User Accounts', command=self.viewUserAcc).pack(expand=True)
		ttk.Button(self, text='Add Account', command=self.addUserAcc).pack(expand=True)

	def createUserAcc(self):
		window = CreateAccount(self)
		window.grab_set()
	
	def viewUserAcc(self):
		window = ViewAccount(self)
		window.grab_set()

	def addUserAcc(self):
		window = passwordManager(self)
		window.grab_set()

def main():
	app = App()
	app.mainloop()

if __name__ == '__main__':
	main()