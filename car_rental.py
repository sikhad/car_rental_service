# Car rental service GUI project 

from tkinter import *
from tkinter import ttk
from datetime import date, datetime, time, timedelta
import pymysql
import sql
import time as timex

DATE_FORMAT = "%m/%d/%Y"
TIME_FORMAT = "%I:%M %p"
EXPIRY_DATE = "%m/%Y"

# To bold text
to_bold = ("Lucida Grande", 12, "bold")

def Connect():
    ## Try to connect to db
    try:
        db = pymysql.connect(host="", user="", passwd="", db="") # removed, private
        return db
    except:
        messagebox.showerror("Unable to Connect to Database", "Check your Internet connection!")

def wm_handler(win, parent):
    win.destroy()
    parent.deiconify()
    
class LoginPage:

    def __init__(self, root):
        """Draws the login screen in the root window."""
        
        self.username = StringVar()
        root.title("Login Page")
        self.frame = ttk.Frame(root, padding=(3,3,12,12)) # use ttk Frame to keep styling consistent
        self.frame.grid(sticky=N+W+E+S)
        self.root = root # reference to root window

        ##-----------STYLES------------##
        s = ttk.Style(root)
        s.configure("Header.TLabel", font=to_bold,
                padding=(3,1), anchor=CENTER)
        s.configure("Grid.TLabel", relief='solid', background='white')
        s.configure("GridTitle.TLabel", relief='solid', padding=2)
        s.configure("Green.Grid.TLabel", background='SpringGreen2')
        ##-----------------------------##
        
        ## Make Entry boxes and Buttons
        self.user_box = ttk.Entry(self.frame, width=30, textvariable=self.username)
        self.password_box = ttk.Entry(self.frame, width=30, show='*')
        login_button = ttk.Button(self.frame, text="Login", command=self.login)
        register_button = ttk.Button(self.frame, text="Register", command=self.register_page)

        ## Grid widgets
        ttk.Label(self.frame, text="Username:").grid(row=0, column=0, sticky=S+E, pady=3)
        ttk.Label(self.frame, text="Password:").grid(row=1, column=0, sticky=N+E, pady=3)
        self.user_box.grid(row=0, column=1, columnspan=2, sticky=S+W, padx=5, pady=3)
        self.password_box.grid(row=1, column=1, columnspan=2, sticky=N+W, padx=5, pady=3)
        login_button.grid(row=2, column=1, sticky=N+E+W, padx=5)
        register_button.grid(row=2, column=2, sticky=N+E+W, padx=5)

##        ## Auto-resize if user resizes window
##        root.columnconfigure(0, weight=1)
##        root.rowconfigure(0, weight=1)
##        self.frame.columnconfigure(0, weight=1)
##        self.frame.rowconfigure(0, weight=1)
##        self.frame.rowconfigure(2, weight=1)

        root.bind("<Return>", self.login) # Pressing Enter key does login

   
    def login(self, event=None):
        """Determines if user is valid, and directs him to correct homepage."""

        curs = db.cursor()
        #try:
        if curs.execute(sql.LOGIN_CHECK,(self.username.get(),self.password_box.get())) == 1:
            row = curs.fetchone()
            if row[2] == "Member":
                home_page = MemberHomepage(self.root, row[0])
            elif row[2] == "Employee":
                home_page = EmployeeHomepage(self.root, row[0])
            else:
                home_Page = AdminHomepage(self.root)
        elif curs.execute(sql.USERNAME_CHECK,(self.user_box.get())) == 1:
            messagebox.showerror("Incorrect Password!", "Check your password and try again!")        
        else:
            messagebox.showerror("Incorrect Username!", "This username does not exist. Please try again or go to the register page to create a new account.")
            self.username.set(''), self.password_box.delete(0,END)
        #except:
            #messagebox.showerror("Unexpected Error!")

        #finally:
            #curs.close()
           
    def register_page(self):
        """Takes user to Registration page."""
        register_page = RegisterPage(self.root)
        
## Optional: forgotten password mechanism
class RegisterPage:
    """Class representing a Registration Page."""
    
    def __init__(self, parent):
        """Draws the Register page in a TopLevel window."""

        self.parent = parent # keep reference to parent window

        ## Hide parent and make new registration window
        parent.withdraw()
        self.registration_window = Toplevel(parent)
        self.registration_window.title("Registration")
        mainframe = ttk.Frame(self.registration_window, padding=(3, 3, 12, 12))
        mainframe.grid(sticky=N+E+W+S)
        
        ## Make Entry boxes and Button
        self.new_user = ttk.Entry(mainframe)
        self.new_password = ttk.Entry(mainframe)
        self.confirm_password = ttk.Entry(mainframe)
        register_button = ttk.Button(mainframe, text="Register", command=self.register)

        ## Dropdown/Combobox Values
        themes = []
        self.value = StringVar()

        try:
            curs = db.cursor()
            curs.execute(sql.ACCOUNT_TYPES)

            for item in curs:
                themes.append(item[0])
                
        except:
            pass
        finally:
            curs.close()
         
        ##Grid everything
        ttk.Label(mainframe, text="Username:").grid(row=0, column=0, sticky=E)
        ttk.Label(mainframe, text="Password:").grid(row=1, column=0, sticky=E)
        ttk.Label(mainframe, text="Confirm Password:").grid(row=2, column=0, sticky=E)
        ttk.Label(mainframe, text="Type of User").grid(row=3, column=0, sticky=E)
        ttk.Combobox(mainframe, values=themes, textvariable=self.value, state='readonly').grid(row=3, column=1, sticky=E)
        self.new_user.grid(row=0, column=1, columnspan=2, sticky=E+W)
        self.new_password.grid(row=1, column=1, columnspan=2, sticky=E+W)
        self.confirm_password.grid(row=2, column=1, columnspan=2, sticky=E+W)
        register_button.grid(row=4, column=2, sticky=E+W)

        self.registration_window.bind("<Return>", self.register)

    def register(self, event=None):
        """Tries to register new user into database."""
        curs = db.cursor()

        try:
            if self.confirm_password.get() != self.new_password.get():
                messagebox.showerror("Password Problem","Your passwords don't match!")
            elif curs.execute((sql.USERNAME_CHECK),(self.new_user.get())) == 1:
                messagebox.showerror("Registration Problem","This user is already in the database!")
            elif self.value.get() != "Employee" and self.value.get() != "Member":
                messagebox.showerror("Incomplete Form!", "You must select a user type!")
            else:
                curs.execute(sql.REGISTER_USER,(self.new_user.get(),self.new_password.get(),self.value.get()))
        except:
            messagebox.showerror("Unexpected Error!")
        finally:
            curs.close()

        self.registration_window.destroy()
        self.parent.deiconify()
        

class MemberHomepage:
    """The homepage for Members"""

    def __init__(self, parent, username):
        """Draw the Member homepage"""

        self.parent = parent
        self.username = username

        parent.withdraw()
        self.home_window = Toplevel(parent)
        self.home_window.title("Member Homepage")
        self.home_window.protocol("WM_DELETE_WINDOW", lambda: wm_handler(self.home_window, self.parent))
        mainframe = ttk.Frame(self.home_window, padding=(3, 3, 12, 12))
        mainframe.grid(sticky=N+E+W+S)
        self.notebook = ttk.Notebook(mainframe)
        self.notebook.grid(sticky=N+E+W+S)

        ##-------------- Personal Information tab ---------------##
        personalinfo_tab = ttk.Frame(self.notebook)
        self.personalinfo_tab = personalinfo_tab
        self.notebook.add(personalinfo_tab, text="Personal Information")

        ## Make Panes for Personal Information tab
        general_pane = ttk.Frame(personalinfo_tab, relief="sunken", padding=(3,3,3,3))
        ttk.Label(personalinfo_tab, text="General Information").grid(column=0, row=0, sticky=E)
        general_pane.grid(column=0, row=1, sticky=N+E+W+S)
        
        drivingplan_pane = ttk.Frame(personalinfo_tab, relief="sunken", padding=(3,3,3,3))
        ttk.Label(personalinfo_tab, text="Driving Plan").grid(column=0, row=2, sticky=E)
        drivingplan_button = ttk.Button(drivingplan_pane, text="View Plan Details", command=self.driving_plan_info)
        drivingplan_button.grid(column=1, row=0, rowspan=3, sticky=N+E+W+S)
        drivingplan_pane.grid(column=0, row=3, sticky=N+E+W+S)

        creditcard_pane = ttk.Frame(personalinfo_tab, relief="sunken", padding=(3,3,3,3))    
        ttk.Label(personalinfo_tab, text="Credit Card Information").grid(column=0, row=4, sticky=E)
        creditcard_pane.grid(column=0, row=5, sticky=N+E+W+S)       

        ## StringVars and widgets.
        self.firstname = StringVar()
        self.middleinitial = StringVar()
        self.lastname = StringVar()
        self.email = StringVar()
        self.phonenum = StringVar()
        self.address = StringVar()
        self.name_on_card = StringVar()
        self.card_number = StringVar()
        self.cvv = StringVar()
        self.expiry_date = StringVar()
        self.billing_address = StringVar()
        self.drivingplan = StringVar() # For use with Radiobutton.
        
        firstname_box = ttk.Entry(general_pane, textvariable=self.firstname)
        middleinitial_box = ttk.Entry(general_pane, textvariable=self.middleinitial)
        lastname_box = ttk.Entry(general_pane, textvariable=self.lastname)
        email_box = ttk.Entry(general_pane, textvariable=self.email)
        phonenum_box = ttk.Entry(general_pane, textvariable=self.phonenum)
        address_box = ttk.Entry(general_pane, textvariable=self.address)
        name_on_card_box = ttk.Entry(creditcard_pane, textvariable=self.name_on_card)
        card_number_box = ttk.Entry(creditcard_pane, textvariable=self.card_number)
        cvv_box = ttk.Entry(creditcard_pane, textvariable=self.cvv)
        expiry_date_box = ttk.Entry(creditcard_pane, textvariable=self.expiry_date) # should be spinboxes
        billing_address_box = ttk.Entry(creditcard_pane, textvariable=self.billing_address)
        
        for box in personalinfo_tab.winfo_children():
            box.configure(width=30)

        # These radio buttons could be replaced with a combobox if we wanted to
        # populate info using SQL
        occasional_rbutton = ttk.Radiobutton(drivingplan_pane, text="Occasional Driving Plan",
                                             variable=self.drivingplan, value="Occasional Driving")
        frequent_rbutton = ttk.Radiobutton(drivingplan_pane, text="Frequent Driving Plan",
                                           variable=self.drivingplan, value="Frequent Driving")
        daily_rbutton = ttk.Radiobutton(drivingplan_pane, text="Daily Driving Plan",
                                        variable=self.drivingplan, value="Daily Driving")

        ## Grid general info.
        general_info = [(firstname_box, "First name:"), (middleinitial_box, "Middle initial:"),
                        (lastname_box, "Last name:"), (email_box, "Email:"),
                        (phonenum_box, "Phone number:"), (address_box, "Address:")]

        for i in range(len(general_info)):
            ttk.Label(general_pane, text=general_info[i][1]).grid(column=0, row=i+1,
                                                                  sticky=E, padx=3)
            general_info[i][0].grid(column=1, row=i+1, sticky=E+W, padx=3, pady=3)

        
        ## Grid driving plan.
        occasional_rbutton.grid(column=0, row=0, sticky=W)
        frequent_rbutton.grid(column=0, row=1, sticky=W)
        daily_rbutton.grid(column=0, row=2, sticky=W)
                         
        ## Grid credit card info.
        creditcard_info = [(name_on_card_box, "Name on card:"), (card_number_box, "Credit Card #:"),
                           (cvv_box, "CVV"), (expiry_date_box, "Expiry date:"),
                           (billing_address_box, "Billing address:")]

        for i in range(len(creditcard_info)):
            ttk.Label(creditcard_pane, text=creditcard_info[i][1]).grid(column=0, row=i+1,
                                                                        sticky=E, padx=3)
            creditcard_info[i][0].grid(column=1, row=i+1, sticky=E+W, padx=3, pady=3)

        ## Make and grid submit button for Personal Information
        submit_button = ttk.Button(personalinfo_tab, text="Submit",
                                   command=self.personal_submit)
        submit_button.grid(column=0, row=6)

        ##-------------- Rent a Car tab -----------------##
        rentcar_tab = ttk.Frame(self.notebook)
        self.notebook.add(rentcar_tab, text="Rent a Car")

        ttk.Label(rentcar_tab, text="Pick Up Time:").grid(column=0, row=0, sticky=E)
        ttk.Label(rentcar_tab, text="Return Time:").grid(column=0, row=1, sticky=E)
        ttk.Label(rentcar_tab, text="Location:").grid(column=0, row=2, sticky=E)
        ttk.Label(rentcar_tab, text="Cars:").grid(column=0, row=3, sticky=E)

        ## HANDLE RETURN TIMES AND STUFF -Michael

        self.pickupday_text = StringVar()
        self.pickupday_combo = ttk.Combobox(rentcar_tab, values = [], state='readonly',
                                            postcommand=self.pickupday_post, width=12,
                                            textvariable=self.pickupday_text)
        self.pickupday_combo.grid(row=0, column=1)
        self.pickupday_combo.bind("<<ComboboxSelected>>", self.pickupday_selected)


        self.pickuptime_text = StringVar()
        self.pickuptime_combo = ttk.Combobox(rentcar_tab, values = [], state='readonly',
                                             postcommand=self.pickuptime_post, width=13,
                                             textvariable=self.pickuptime_text)
        self.pickuptime_combo.grid(row=0, column=2)


        self.returnday_text = StringVar()
        self.returnday_combo = ttk.Combobox(rentcar_tab, values = [], state='disabled',
                                            width=13, textvariable=self.returnday_text)
        self.returnday_combo.grid(row=1, column=1)
        self.returnday_combo.bind("<<ComboboxSelected>>", self.returnday_selected)

        self.returntime_text = StringVar()
        self.returntime_combo = ttk.Combobox(rentcar_tab, values = [], state='disabled',
                                             postcommand=self.returntime_post,
                                             width=13, textvariable=self.returntime_text)
        self.returntime_combo.grid(row=1, column=2)


        self.location_text = StringVar()
        self.location_combo = ttk.Combobox(rentcar_tab, values = [], state='readonly',
                                           postcommand=self.location_post, width=13,
                                           textvariable=self.location_text)
        self.location_combo.grid(row=2, column=1, columnspan=2, sticky=E+W)


        self.choice_text = StringVar()
        self.choice_combo = ttk.Combobox(rentcar_tab, values = ["Choose by Type", "Choose by Model"],
                                         state='readonly', postcommand=self.pickupday_post, width=13,
                                         textvariable=self.choice_text)
        self.choice_combo.grid(row=3, column=1)


        self.typeormodel_text = StringVar()
        self.typeormodel_combo = ttk.Combobox(rentcar_tab, values = [], state='readonly',
                                              postcommand=self.typeormodel_post, width=13,
                                              textvariable=self.typeormodel_text)
        self.typeormodel_combo.grid(row=3, column=2)
        
        ttk.Button(rentcar_tab, text="Search", command=self.rent_car).grid(row=4, column=2, sticky=S+E)


        ##------------- Rental Information tab -------------##
        self.rentalinfo_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.rentalinfo_tab, text="Rental Information")

        
        ##---------Default to Rent a Car if possible--------##
        curs = db.cursor()
        if curs.execute(sql.PERSONALINFO_CHECK, (self.username,)): # if user has personal info, default to rentcar_tab
            self.notebook.select(rentcar_tab)
        curs.close()
        
        self.notebook.bind("<<NotebookTabChanged>>", self.tabChange)
        
    def rent_car(self):

        if self.choice_text.get() == "Choose by Type":
            Car_Availability(self.home_window, self.username, self.returnday_text.get(),
                             self.returntime_text.get(), self.pickupday_text.get(),
                             self.pickuptime_text.get(), self.location_text.get(),
                             _type=self.typeormodel_text.get())
        elif self.choice_text.get() == "Choose by Model":
            Car_Availability(self.home_window, self.username, self.returnday_text.get(),
                             self.returntime_text.get(), self.pickupday_text.get(),
                             self.pickuptime_text.get(), self.location_text.get(),
                             model=self.typeormodel_text.get())
        else:
            Car_Availability(self.home_window, self.username, self.returnday_text.get(),
                             self.returntime_text.get(), self.pickupday_text.get(),
                             self.pickuptime_text.get(), self.location_text.get())

    ## Index 0: Personal info tab; Index 1: Rent a Car tab; Index 2: Rental Info tab
    def tabChange(self, event):
        """Handles changing of tabs"""
        current_index = self.notebook.index("current")

        if current_index == 0: # Personal info
            
            self.populate_personal_info()

        if current_index == 1:
            
             self.rent_car_check()
        
        if current_index == 2:
        
            self.populate_rental_info()
                
    def populate_personal_info(self):
        """Populate Personal Info"""
        
        curs = db.cursor()
        if curs.execute(sql.PERSONALINFO_CHECK, (self.username,)):
            curs.execute(sql.GET_PERSONALINFO, (self.username,))
            personal_info = curs.fetchone()

            personal_vars = [self.firstname, self.middleinitial, self.lastname,
                             self.email, self.phonenum, self.address, self.drivingplan,
                             self.name_on_card, self.card_number, self.cvv,
                             self.expiry_date, self.billing_address]

            for i in range(len(personal_vars)):
                personal_vars[i].set(personal_info[i])
        curs.close()

    def rent_car_check(self):
        """Check that user has inserted personal info"""

        curs=db.cursor()
        if not curs.execute(sql.PERSONALINFO_CHECK, (self.username,)):
            messagebox.showerror("", "You must enter CC info and select a driving plan before searching for a car!")
            self.notebook.select(self.personalinfo_tab)
        curs.close()

    def populate_rental_info(self):
        """Populate Rental information"""

        curs = db.cursor()
        if curs.execute(sql.PERSONALINFO_CHECK, (self.username,)):
            self.prev_frame = ttk.LabelFrame(self.rentalinfo_tab, text="Previous Reservations")
            labels = ['Pick-up Date', 'Pick-up Time', 'Return Date', 'Return Time',
                      'Car', 'Location Name', 'Amount', 'Return Status']
            for i in range(len(labels)):
                ttk.Label(self.prev_frame, text=labels[i], style="GridTitle.TLabel").grid(row=0, column=i, sticky=N+E+W+S)
            self.prev_frame.grid(row=2, column=0, sticky=E+W+S)
            
            curs.execute(sql.VIEW_PREVIOUS_RESERVATIONS, (self.username,))
            count = 1
            tups = list(curs.fetchall())
            for i in range(len(tups)):
                for j in range(len(tups[i])):
                    if j==0 or j==2:
                        _text = tups[i][j].strftime(DATE_FORMAT)
                    elif j==1 or j==3:
                        _text = (tups[i][j]+datetime.combine(date(2013,4,30), time())).strftime(TIME_FORMAT)
                    elif j==7:
                        if tups[i][j] == None:
                            _text = "On time"
                        else:
                            _text = "Late - " + str(tups[i][j])
                    else:
                        _text = tups[i][j]
                    ttk.Label(self.prev_frame, text=_text, style="Grid.TLabel").grid(row=1+i, column=j, sticky=N+E+W+S)

            self.current_frame = ttk.LabelFrame(self.rentalinfo_tab, text="Current Reservations")
            
            self.info_frame = ttk.Frame(self.current_frame)
            currentlabels = ['Pick-up Date', 'Pick-up Time', 'Return Date', 'Return Time',
                             'Car', 'Location Name', 'Amount']
            for i in range(len(currentlabels)):
                ttk.Label(self.info_frame, text=currentlabels[i], style="GridTitle.TLabel").grid(row=0, column=i, sticky=N+E+W+S)

            exist = curs.execute(sql.SHOW_CURRENT_RESERVATION, (self.username))
            tup = curs.fetchone()
            if tup != None:
                self.current_vsno = tup[0]
                self.current_pickuptime = tup[2]
                self.current_pickupday = tup[1]
                self.current_returntime = tup[4]
                self.current_returnday = tup[3]
                for i in range(1,len(tup)):
                    if i==1 or i==3:
                        _text = tup[i].strftime(DATE_FORMAT)
                    elif i==2 or i==4:
                        _text = (tup[i]+datetime.combine(date(2013,4,30), time())).strftime(TIME_FORMAT)
                    else:
                        _text = tup[i]
                    ttk.Label(self.info_frame, text=_text, style='Grid.TLabel').grid(row=1, column=i-1, sticky=N+E+W+S)
                
                self.info_frame.grid(sticky=N+E+S+W)

                self.button_frame = ttk.Frame(self.current_frame)
                if exist != 0:
                    ttk.Label(self.button_frame, text="Would you like to extend this reservation?").grid(row=0, column=0, columnspan=2, sticky=W)
                    ttk.Button(self.button_frame, text="Extend", command=self.extend_reservation).grid(row=0, rowspan=2, column=2, sticky=W)
                    self.extendday_combo = ttk.Combobox(self.button_frame, postcommand=self.extendday_post, state='readonly')
                    self.extendday_combo.grid(row=1, column=0, sticky=N+E+W+S)
                    self.extendtime_combo = ttk.Combobox(self.button_frame, postcommand=self.extendtime_post, state='readonly')
                    self.extendtime_combo.grid(row=1, column=1, sticky=N+E+W+S)
                self.button_frame.grid(row=1)
                
                self.current_frame.grid(row=0, column=0, sticky=N+E+W)
        curs.close()
        
    def extendday_post(self):
        day_list = []
        for i in range(3):
            _date = (self.current_returnday+timedelta(days=i)).strftime(DATE_FORMAT)
            day_list.append(_date)
        self.extendday_combo.configure(values=day_list)
        #returnday = datetime.strptime(self.current_return

    def extendtime_post(self):
        time_list = []
        for i in range(48):
            total_minutes = 30*i
            hours = total_minutes//60
            minutes = total_minutes%60
            _time = time(hour=hours, minute=minutes)
            time_list.append(_time.strftime(TIME_FORMAT))
        self.extendtime_combo.configure(values=time_list)
    
    def extend_reservation(self):
        current_datetime = datetime.combine(self.current_returnday, datetime.time((datetime.combine(date(2013,4,30), time())+self.current_returntime)))
        extend_datetime = datetime.combine(datetime.date(datetime.strptime(self.extendday_combo.get(), DATE_FORMAT)),
                                           datetime.time(datetime.strptime(self.extendtime_combo.get(), TIME_FORMAT)))
        if current_datetime >= extend_datetime:
            messagebox.showerror("Error", "Can only extend reservation")
        else:
            curs = db.cursor()
            invalid = curs.execute(sql.EXTEND_RESERVATION_CHECK, (self.current_vsno, datetime.date(extend_datetime),
                                                                     datetime.time(extend_datetime), self.username))
            if invalid:
                messagebox.showerror("Error!", "Sorry, there is a conflict with this reservation time.")
            else:
                curs.execute(sql.EXTEND_RESERVATION, (self.current_pickupday, datetime.time(datetime.combine(date(2013,4,30), time())+self.current_pickuptime),
                                                      self.current_returnday, datetime.time(datetime.combine(date(2013,4,30), time())+self.current_returntime),
                                                      (extend_datetime-current_datetime).seconds/3600, self.username))
                db.commit()
                messagebox.showinfo("Success!", "You extended your reservation to " + self.extendday_combo.get() + " " +
                                    self.extendtime_combo.get() + ".")
                                                                                        
            curs.close()
##        curs = db.cursor()
##        can_extend = curs.execute(sql.CHECK_EXTEND_RESERVATION, (Vehicle Sno, timestampdate, timestamptime, username))
##        if can_extend !=0:
##            messagebox.showerror("Error!", "Sorry, there is a conflict with this reservation time.")
##        else:
##            curs.execute(sql.EXTEND_RESERVATION, (PickUp_Date, PickUp_Time, Return_Date, Return_Time, Extended_Time, Username))
    
                
                
    def personal_submit(self):
        """Submit personal info into database if possible."""
##        try:
        curs = db.cursor()
        
        has_personal_info = False
        if curs.execute(sql.PERSONALINFO_CHECK,(self.username,)): # if statement returns a tuple
            has_personal_info = True

        # Make sure driving plan selected and CC info filled out.
        # This is going to more complicated than anticipated...
        # Cannot update Credit_Card table. Nothing to update on. We can only insert new entries into it.
        # Question. They way this works now, if a member changes credit cards, his previous one just stays in the database.
        # Why did we not make Credit_Card table have a foreign key to Student_Faculty so that each member could
        # have more than one credit card attributed to his account?
        if not((self.drivingplan.get() != 0) and self.name_on_card.get() != '' and self.card_number.get() != '' and self.cvv.get() != '' and self.expiry_date.get() != '' and self.billing_address.get() != ''):
            messagebox.showerror("Incomplete Form!", "You must complete the CC info and select a driving plan!")

        else:
            
            if has_personal_info:
                
                cc_number_exists = False
                if curs.execute(sql.CC_NUMBER_CHECK, (self.card_number.get(),)):
                    cc_number_exists = True
                
                if cc_number_exists: 
                    
                    curs.execute(sql.UPDATE_CCINFO, (self.name_on_card.get(), self.cvv.get(),
                                                     self.expiry_date.get(), self.billing_address.get(),
                                                     self.card_number.get()))
                else:

                    curs.execute(sql.INSERT_CCINFO, (self.card_number.get(), self.name_on_card.get(),
                                                     self.cvv.get(), self.expiry_date.get(),
                                                     self.billing_address.get()))

                
                curs.execute(sql.UPDATE_PERSONALINFO,(self.card_number.get(), self.drivingplan.get(),
                                                      self.firstname.get(), self.middleinitial.get(),
                                                      self.lastname.get(), self.address.get(),
                                                      self.email.get(), self.phonenum.get(), self.username)) 
                
            else:

                curs.execute(sql.INSERT_CCINFO,(self.card_number.get(), self.name_on_card.get(),
                                                self.cvv.get(),
                                                datetime.strptime(self.expiry_date.get(), EXPIRY_DATE),
                                                self.billing_address.get()))
                
                curs.execute(sql.INSERT_PERSONALINFO,(self.username, self.card_number.get(),
                                                      self.drivingplan.get(),  self.firstname.get(),
                                                      self.middleinitial.get(), self.lastname.get(),
                                                      self.address.get(), self.email.get(),
                                                      self.phonenum.get())) 

            db.commit()
            messagebox.showinfo("Success!", "Personal Information updated.")
            
##        except:
##            pass
##        finally:
##            curs.close()
            
    def pickupday_post(self):
        """Populate Pick-up day combobox with 30 days starting from today."""
        date_list = []
        for i in range(30):
            _date = date.today() + timedelta(days=i)
            date_list.append(_date.strftime(DATE_FORMAT))
        self.pickupday_combo.configure(values = date_list)

    def pickupday_selected(self, event):
        """Populate Return day combobox with valid dates."""
        date_list = []
        for i in range(3):
            _datetime = datetime.strptime(self.pickupday_text.get(), DATE_FORMAT) + timedelta(days=i)
            date_list.append(_datetime.strftime(DATE_FORMAT))
        self.returnday_combo.configure(values=date_list)

        if (str(self.returnday_combo['state']) == 'disabled'): #make return day box usable
            self.returnday_combo.configure(state='readonly')
        if (self.returnday_text.get() not in self.returnday_combo['values']):
            self.returnday_text.set("")
            
        self.pickuptime_post()
        if (self.pickuptime_text.get() not in self.pickuptime_combo['values']):
            self.pickuptime_text.set("")
            
    def pickuptime_post(self): #NOT REALLY NEEDED FOR WHAT IT DOES RIGHT NOW
        """Postcommand for pickup time combobox"""
        time_list = []
        current_time = time(0)
        if self.pickupday_text.get() != "" and datetime.date(datetime.strptime(self.pickupday_text.get(), DATE_FORMAT)) == date.today():
            current_time = datetime.time(datetime.now())
        for i in range(48):
            total_minutes = 30*i
            hours = total_minutes//60
            minutes = total_minutes%60
            _time = time(hour=hours, minute=minutes)
            if current_time < _time:
                time_list.append(_time.strftime(TIME_FORMAT))
        self.pickuptime_combo.configure(values=time_list)

        self.returntime_post()
        if (self.returntime_text.get() not in self.returntime_combo['values']):
            self.returntime_text.set("")

    def returntime_post(self):
        time_list = []
        
        if self.pickupday_text.get() != "" and self.pickuptime_text.get() != "" and self.returnday_text.get() != "":
            self.returntime_combo['state']='readonly'
            pu_day = datetime.date(datetime.strptime(self.pickupday_text.get(), DATE_FORMAT))
            pu_time = datetime.time(datetime.strptime(self.pickuptime_text.get(), TIME_FORMAT))
            pu_datetime = datetime.combine(pu_day, pu_time)

            r_day = datetime.date(datetime.strptime(self.returnday_text.get(), DATE_FORMAT))

            for i in range(48):
                total_minutes = 30*i
                hours = total_minutes//60
                minutes = total_minutes%60
                _time = time(hour=hours, minute=minutes)
                _timedelta = datetime.combine(r_day, _time) - pu_datetime
                if _timedelta <= timedelta(days=2) and _timedelta > timedelta(hours=0) :
                    time_list.append(_time.strftime(TIME_FORMAT))
            self.returntime_combo.configure(values=time_list)
            
        else:
            self.returntime_combo['state']='disabled'
            self.returntime_text.set("")

    def returnday_selected(self, event):
        """Event handler for returnday selected"""
        if (str(self.returntime_combo['state']) == 'disabled'):
            self.returntime_combo.configure(state='readonly')
        
        self.returntime_post()
        if self.returntime_text.get() not in self.returntime_combo['values']:
            self.returntime_text.set("")
            

    def location_post(self):
        """Postcommand for location combobox"""
        loc_list = []
        try:
            curs = db.cursor()
            curs.execute(sql.GET_LOCATIONS)
            for item in curs:
                loc_list.append(item[0])
            self.location_combo.configure(values=loc_list)
        except:
            pass
        finally:
            curs.close()

    def typeormodel_post(self):
        type_list = []
        model_list = []

        try:
            curs = db.cursor()
            if self.choice_text.get() == "Choose by Type":
                curs.execute(sql.GET_TYPES, (self.location_text.get(),))

                for item in curs:
                    type_list.append(item[0])

                self.typeormodel_combo.configure(values=type_list)
                
            elif self.choice_text.get() == "Choose by Model":
                curs.execute(sql.GET_MODELS, (self.location_text.get(),))

                for item in curs:
                    model_list.append(item[0])

                self.typeormodel_combo.configure(values=model_list)
        except:
                pass
        finally:
            curs.close()

    def driving_plan_info(self):
        dp_win = Toplevel(self.parent)
        dp_win.title("Driving Plan Info")
        frame = ttk.Frame(dp_win, padding=(3, 3, 12, 12))
        frame.pack()
        labels = ['Driving Plan', 'Monthly Payment', 'Discount',
                  'Annual Fees']
        for i in range(len(labels)):
            ttk.Label(frame, text=labels[i], style="GridTitle.TLabel").grid(row=0, column=i, sticky=N+E+W+S)
        curs = db.cursor()
        curs.execute(sql.GET_DRIVINGPLANINFO)
        tups = curs.fetchall()

        for i in range(len(tups)):
            for j in range(len(tups[i])):
                if (tups[i][j] == None):
                    _text = "N/A"
                else:
                    _text = tups[i][j]
                ttk.Label(frame, text=_text, style="Grid.TLabel").grid(row=1+i, column=j, sticky=N+E+W+S)

        curs.close()

        ttk.Button(dp_win, text="Back", command=lambda:dp_win.destroy()).pack(side=BOTTOM, anchor=E)
        

#--------------------Employee Homepage--------------------#
class EmployeeHomepage:
    """The homepage for Employees"""

    def __init__(self, parent, username):
        """Draw the Employee Homepage"""

        self.parent = parent
        self.username = username

        parent.withdraw()
        self.home_window = Toplevel(parent)
        self.home_window.title("Employee Homepage")
        self.home_window.protocol("WM_DELETE_WINDOW", lambda:wm_handler(self.home_window, parent))
        mainframe = ttk.Frame(self.home_window, padding=(3,3,12,12))
        mainframe.grid(sticky=N+E+W+S)
        self.notebook = ttk.Notebook(mainframe)
        self.notebook.grid(sticky=N+E+W+S)

        ###Manage Cars Tab
        managecars_tab = ttk.Frame(self.notebook)
        self.notebook.add(managecars_tab, text="Manage Cars")

        ##Panes
        addcar_pane = ttk.Frame(managecars_tab, relief="sunken", padding=(3,3,3,3))
        ttk.Label(addcar_pane, text="ADD CAR", font=to_bold).grid(column=0, row=0, columnspan=2)
        addcar_pane.grid(column=0, row=0, sticky=N+E+W+S)

        changecar_pane = ttk.Frame(managecars_tab, relief="sunken", padding=(10,3,10,3))
        ttk.Label(changecar_pane, text="CHANGE CAR LOCATION", font=to_bold).grid(column=0, row=0, columnspan=2)
        changecar_pane.grid(column=1, row=0, sticky=N+E+W+S)

        
        #Add Car
        self.vehicle_sno = StringVar()
        self.carmodel2 = StringVar()
        self.cartype = StringVar()
        self.location = StringVar()
        self.color = StringVar()
        self.hourly_rate = StringVar()
        self.daily_rate = StringVar()
        self.seating_capacity = StringVar()
        self.transmission_type = StringVar()
        self.bluetooth = StringVar()
        self.aux = StringVar()


        vehicle_sno_box = ttk.Entry(addcar_pane, textvariable=self.vehicle_sno)
        carmodel_box = ttk.Entry(addcar_pane, textvariable=self.carmodel2)
        color_box = ttk.Entry(addcar_pane, textvariable=self.color)
        hourly_rate_box = ttk.Entry(addcar_pane, textvariable=self.hourly_rate)
        daily_rate_box = ttk.Entry(addcar_pane, textvariable=self.daily_rate)
        seating_capacity_box = ttk.Entry(addcar_pane, textvariable=self.seating_capacity)

        # Get Location List
        loc_list = []
        try:
            curs = db.cursor()
            curs.execute(sql.LOCATION_DROPDOWN)
            for item in curs:
                loc_list.append(item[0])
            self.location_combo.configure(values=loc_list)
        except:
            pass
        finally:
            curs.close()

        # Get Car Type List
           
        self.cartype_combo = ttk.Combobox(addcar_pane, values = ["VAN", "SUV", "PICKUP", "SPORTS CAR", "SEDAN", "CONVERTIBLE", "COUPE", "WAGON"], state="readonly",
                                          width=13, textvariable=self.cartype)
        self.location_combo = ttk.Combobox(addcar_pane, values = loc_list, state="readonly",
                                          width=13, textvariable=self.location)
        self.transmission_type_combo = ttk.Combobox(addcar_pane, values = ["Manual", "Automatic"], state="readonly",
                                          width=13, textvariable=self.transmission_type)
        self.bluetooth_combo = ttk.Combobox(addcar_pane, values = ["Yes", "No"], state="readonly",
                                          width=13, textvariable=self.bluetooth)
        self.aux_combo = ttk.Combobox(addcar_pane, values = ["Yes", "No"], state="readonly",
                                          width=13, textvariable=self.aux)

        


        #Grid Add Car
        addcar = [(vehicle_sno_box, "Vehicle SNO:"), (carmodel_box, "Car Model:"),
                  (self.cartype_combo, "Car Type:"), (self.location_combo, "Location:"),
                  (color_box, "Color:"), (hourly_rate_box, "Hourly Rate:"),
                  (daily_rate_box, "Daily Rate:"), (seating_capacity_box, "Seating Capacity:"),
                  (self.transmission_type_combo, "Transmission Type:"), (self.bluetooth_combo, "Bluetooth Connectivity:"),
                  (self.aux_combo, "Auxiliary Cable:")]

        for i in range(len(addcar)):
            ttk.Label(addcar_pane, text=addcar[i][1]).grid(column=0, row=i+1, sticky=W, padx=3)
            addcar[i][0].grid(column=1, row=i+1, sticky = E+W, padx=3, pady=3)

        
        add_button = ttk.Button(addcar_pane, text="Add", command=self.add_car_submit).grid(column=1, row=12, sticky=E, pady=10)


        #Change Car Location
        
        brief_pane = ttk.Frame(changecar_pane, relief="ridge", padding=(30,3,30,15))
        ttk.Label(brief_pane, text="Brief Description", font=to_bold).grid(column=0, row=0, columnspan=2)
        brief_pane.grid(column=0, row=4, sticky=E+W, columnspan=2)
        
        self.choosecurrent = StringVar()
        self.choosecar = StringVar()
        self.choosenew = StringVar()
        
        self.cartype2 = StringVar()
        self.color2 = StringVar()
        self.seating_capacity2 = StringVar()
        self.transmission_type2 = StringVar()

        # Location Dropdown Values 
        try:
            curs = db.cursor()

            loc_list = []
            
            curs.execute(sql.LOCATION_DROPDOWN)
            for item in curs:
                loc_list.append(item[0])
        except:
            pass
        finally:
            curs.close()

        self.choosecurrent_combo = ttk.Combobox(changecar_pane, values = loc_list, state="readonly",
                                          width=13, textvariable=self.choosecurrent)


        self.choosecar_combo = ttk.Combobox(changecar_pane, values = [], state="readonly",
                                          width=13, textvariable=self.choosecar, postcommand=self.model_in_loc)

            
        self.choosenew_combo = ttk.Combobox(changecar_pane, values = loc_list, state="readonly",
                                          width=13, textvariable=self.choosenew)
        
        cartype_box = ttk.Entry(brief_pane, textvariable=self.cartype2, state="readonly")
        color_box = ttk.Entry(brief_pane, textvariable=self.color2, state="readonly")
        seating_capacity_box = ttk.Entry(brief_pane, textvariable=self.seating_capacity2, state="readonly")
        transmission_type_box = ttk.Entry(brief_pane, textvariable=self.transmission_type2, state="readonly")

        self.choosecar_combo.bind("<<ComboboxSelected>>", self.autopop_description)

        #Grid Change Car Location
        changecar = [(self.choosecurrent_combo, "Choose Current Location:"), (self.choosecar_combo, "Choose Car:")]

        briefdescription = [(cartype_box, "Car Type:"), (color_box, "Color:"), (seating_capacity_box, "Seating Capacity:"),
                            (transmission_type_box, "Transmission Type:")]

        for i in range(len(changecar)):
            ttk.Label(changecar_pane, text=changecar[i][1]).grid(column=0, row=i+1, sticky=W, padx=3)
            changecar[i][0].grid(column=1, row=i+1, sticky=E+W, padx=3, pady=3)
       
        # Extra padding
        ttk.Label(changecar_pane).grid(column=0, row=3)
        ttk.Label(changecar_pane).grid(column=1, row=3)

        for i in range(len(briefdescription)):
            ttk.Label(brief_pane, text=briefdescription[i][1]).grid(column=0, row=i+1, sticky=W, padx=3)
            briefdescription[i][0].grid(column=1, row=i+1, sticky=E+W, padx=3, pady=3)

        ttk.Label(changecar_pane, text="Choose New Location:").grid(column=0, row=6, sticky=W, padx=3, pady=20)
        self.choosenew_combo.grid(column=1, row=6, sticky=E+W, padx=3, pady=20)

        submit_changes_button = ttk.Button(changecar_pane, text="Submit Changes", command=self.new_loc_submit).grid(column=1, row=7, sticky=E)

        ###Maintenance Requests Tab
        mreq_tab = ttk.Frame(self.notebook)
        self.notebook.add(mreq_tab, text="Maintenance Requests")

        self.chooseloc_maint = StringVar()
        self.choosecar_maint = StringVar()
        self.briefproblem = StringVar()

        self.chooseloc_maint_combo = ttk.Combobox(mreq_tab, values = loc_list, state="readonly",
                                            width=13, textvariable=self.chooseloc_maint)
        self.choosecar_maint_combo = ttk.Combobox(mreq_tab, values = [], state="readonly",
                                            width=13, textvariable=self.choosecar_maint, postcommand=self.model_in_loc_maint)

        placeholder1 = ttk.Frame()
        placeholder2 = ttk.Frame()

        #Grid Maintenance Requests
        mreq = [(placeholder1,""), (placeholder2,""), (self.chooseloc_maint_combo, "Choose Location:"), (self.choosecar_maint_combo, "Choose Car:"),]

        for i in range(len(mreq)):
            ttk.Label(mreq_tab, text=mreq[i][1]).grid(column=0, row=i+1, sticky=E, padx=3)
            mreq[i][0].grid(column=1, row=i+1, sticky=E+W, padx=3, pady=3)

        #Problems Box
        self.briefproblem_text = Text(mreq_tab, font=("Lucida Grande", 12), height=10, width=40, wrap='none')
        self.briefproblem_xbox = Scrollbar(mreq_tab, command=self.briefproblem_text.xview, orient=HORIZONTAL)
        self.briefproblem_ybox = Scrollbar(mreq_tab, command=self.briefproblem_text.yview, orient=VERTICAL)
        self.briefproblem_text.config(yscrollcommand=self.briefproblem_ybox.set, xscrollcommand=self.briefproblem_xbox.set)
    
        ttk.Label(mreq_tab, text="Brief Description of Problem:").grid(column=0, row=5, sticky=E, padx=10, pady=10)

        self.briefproblem_text.grid(column=1, row=5, padx=3, pady=10)
        self.briefproblem_ybox.grid(column=2, row=5, sticky=N+S, padx=3, pady=10)
        self.briefproblem_xbox.grid(column=1, row=6, sticky=E+W, padx=3)


        #Date
        date_time = datetime.now().strftime(DATE_FORMAT + "   " + TIME_FORMAT)
        date_label = ttk.Label(mreq_tab, text=date_time)
            
        datelabel = ttk.Label(mreq_tab, text="Date:").grid(column=3, row=0)
        date_label.grid(column=4, row=0)

        submit_req_button = ttk.Button(mreq_tab, text="Submit Request", command=self.maint_submit).grid(column=1, row=12, sticky=E, pady=10)


       ###Rental Change Request Tab
        rcreq_tab = ttk.Frame(self.notebook)
        self.notebook.add(rcreq_tab, text="Rental Change Requests")

        def find_offending_user():
            curs = db.cursor()
            curs.execute(sql.LATE_USER_CURRENT_RESERVATION, (self.offending_username.get()))
            for row in curs:
                self.offending_user_original_pickup_time = row[5]
                self.offending_user_original_pickup_date = row[6]
                self.sno_for_later = row[4]
                self.carmodel.set(row[0])
                self.location2.set(row[1])
                self.originalreturntime.set((datetime(year=2000, month=1, day=1, hour=0)+row[2]).strftime(TIME_FORMAT))
                self.originalreturndate.set(row[3].strftime(DATE_FORMAT))

        def cancel_reservation():
            curs = db.cursor()
            delete = curs.execute(sql.CANCEL_RESERVATION, (self.affected_username.get(),
                                                  datetime.date(datetime.strptime(self.original_return_date.get(), DATE_FORMAT)), datetime.time(datetime.strptime(self.original_return_time.get(), TIME_FORMAT)),
                                                  datetime.time(datetime.strptime(self.original_pickup_time.get(), TIME_FORMAT)), datetime.date(datetime.strptime(self.original_pickup_date.get(), DATE_FORMAT))))
            if delete != 0:
                messagebox.showinfo("Cancellation!", "%s's reservation has been cancelled." % self.affected_username.get())
                
        def show_car_availability():
            Car_Availability(self.home_window, self.affected_username.get(), self.original_return_date.get(),
                             self.original_return_time.get(), self.original_pickup_date.get(),
                             self.original_pickup_time.get(), self.original_location)
            
            

        ##Panes
        self.offending_username = StringVar()
        username_pane = ttk.Frame(rcreq_tab, relief="sunken", padding=(3,3,3,3))
        ttk.Label(username_pane, text="Enter Username:").grid(sticky=E+W)
        ttk.Entry(username_pane, textvariable=self.offending_username).grid(sticky=E+W)
        ttk.Button(username_pane, text="Enter", command=find_offending_user).grid(sticky=E+W)
        username_pane.grid(column=0, row=0, sticky=N+E+W+S)
                                  
        rentinfo_pane = ttk.Frame(rcreq_tab, relief="sunken", padding=(3,3,3,3))
        ttk.Label(rentinfo_pane, text="Rental Information").grid(column=0, row=0, sticky=E+W)
        rentinfo_pane.grid(column=0, row=1, sticky=N+E+W+S)

        user_pane = ttk.Frame(rcreq_tab, relief="sunken", padding=(10,10,10,10))
        ttk.Label(user_pane, text="User Affected:", style="GridTitle.TLabel").grid(column=1, row=0, sticky=E, padx=3)
        ttk.Label(user_pane, text="Username:").grid(column=0, row=1, sticky=E, padx=3)
        ttk.Label(user_pane, text="Original Pick-up Time:").grid(column=0, row=2, sticky=E, padx=3)
        ttk.Label(user_pane, text="Original Return Time:").grid(column=0, row=3, sticky=E, padx=3)
        ttk.Label(user_pane, text="Email Address:").grid(column=0, row=4, sticky=E, padx=3)
        ttk.Label(user_pane, text="Phone Number:").grid(column=0, row=5, sticky=E, padx=3)
        ttk.Button(user_pane, text="Cancel Reservation", command=cancel_reservation).grid(column=1, row=6)
        ttk.Button(user_pane, text="Show Car Availability", command=show_car_availability).grid(column=2, row=6)
        user_pane.grid(column=1, row=0, rowspan=2, sticky=N+E+W+S)

        #Rental Information

        self.carmodel = StringVar()
        self.location2 = StringVar()
        self.originalreturndate = StringVar()
        self.originalreturntime = StringVar()
        self.newarrivaldate = StringVar()
        self.newarrivaltime = StringVar()
        self.affected_username = StringVar()
        self.original_pickup_date = StringVar()
        self.original_pickup_time = StringVar()
        self.original_return_date = StringVar()
        self.original_return_time = StringVar()
        self.affected_email_address = StringVar()
        self.affected_phone_number = StringVar()

        ttk.Entry(user_pane, textvariable=self.affected_username).grid(column=1, row=1, columnspan=2, sticky=E+W, pady=4)
        ttk.Entry(user_pane, textvariable=self.original_pickup_date).grid(column=1, row=2, pady=4, sticky=E+W)
        ttk.Entry(user_pane, textvariable=self.original_pickup_time).grid(column=2, row=2, pady=4, sticky=E+W)
        ttk.Entry(user_pane, textvariable=self.original_return_date).grid(column=1, row=3, pady=4, sticky=E+W)
        ttk.Entry(user_pane, textvariable=self.original_return_time).grid(column=2, row=3, pady=4, sticky=E+W)
        ttk.Entry(user_pane, textvariable=self.affected_email_address).grid(column=1, row=4, columnspan=2, sticky=E+W, pady=4)
        ttk.Entry(user_pane, textvariable=self.affected_phone_number).grid(column=1, row=5, columnspan=2, sticky=E+W, pady=4)

        carmodel_box = ttk.Entry(rentinfo_pane, textvariable=self.carmodel)
        location2_box = ttk.Entry(rentinfo_pane, textvariable=self.location2)

        def populate_day_box():
            date_list = []
            for i in range(3):
                _datetime = datetime.now() + timedelta(days=i)
                date_list.append(_datetime.strftime(DATE_FORMAT))
            self.newarrivaldate_combo.configure(values=date_list)
            
        def populate_time_box():
            time_list = []
            for i in range(48):
                total_minutes = 30*i
                hours = total_minutes//60
                minutes = total_minutes%60
                _time = time(hour=hours, minute=minutes)
                time_list.append(_time.strftime(TIME_FORMAT))
            self.newarrivaltime_combo.configure(values=time_list)
            
        self.originalreturndate_combo = ttk.Combobox(rentinfo_pane, values = [], state="readonly",
                                            width=6, textvariable=self.originalreturndate)
        self.originalreturntime_combo = ttk.Combobox(rentinfo_pane, values = [], state="readonly",
                                            width=6, textvariable=self.originalreturntime)
        self.newarrivaldate_combo = ttk.Combobox(rentinfo_pane, values = [], state="readonly",
                                            width=6, textvariable=self.newarrivaldate, postcommand=populate_day_box)
        self.newarrivaltime_combo = ttk.Combobox(rentinfo_pane, values = [], state="readonly",
                                            width=6, textvariable=self.newarrivaltime, postcommand=populate_time_box)

        

        #Grid Rental Information
        rentinfo = [(carmodel_box, "Car Model:"), (location2_box, "Location:"),
                    (self.originalreturndate_combo, "Original Return Time:"), (self.originalreturntime_combo, ""),
                    (self.newarrivaldate_combo, "New Arrival Time:"), (self.newarrivaltime_combo, "")]
            
        for i in range(len(rentinfo)):
            ttk.Label(rentinfo_pane, text=rentinfo[i][1]).grid(column=0, row=i+1, sticky=W, padx=3)
            rentinfo[i][0].grid(column=1, row=i+1, sticky=E+W, padx=3, pady=3)
        

        def check_for_conflicts():
            curs = db.cursor()
            affected_users = curs.execute(sql.AFFECTED_USER_CHECK, (self.sno_for_later, self.offending_username.get(), datetime.strptime(self.newarrivaldate.get(), DATE_FORMAT), datetime.time(datetime.strptime(self.newarrivaltime.get(), TIME_FORMAT))))
            if affected_users == 0:
                orig_return = datetime.strptime(self.originalreturndate.get(), DATE_FORMAT)
                new_return = datetime.strptime(self.newarrivaldate.get(), DATE_FORMAT)
                orig_time = datetime.strptime(self.originalreturntime.get(), TIME_FORMAT)
                new_time = datetime.strptime(self.newarrivaltime.get(), TIME_FORMAT)
                if orig_return == new_return:
                    self.extend = (new_time - orig_time).seconds
                    self.extension = self.extend/3600
                else:
                    days = (new_return - orig_return).days
                    self.extend = ((new_time - orig_time) + timedelta(hours=24*days)).seconds
                    self.extension = self.extend/3600

                try:
                    curs.execute(sql.EXTEND_NO_AFFECTED_USER, (datetime.strptime(self.originalreturndate.get(), DATE_FORMAT), self.originalreturntime.get(), datetime.strptime(self.newarrivaldate.get(), DATE_FORMAT), self.newarrivaltime.get(), self.extension, self.offending_username.get()))
                    ttk.Label(rentinfo_pane, text="Successfully updated!").grid(column=1, row=13)
                    db.commit()
                except:
                    messagebox.showerror("Unexpected error!", "Could not be inserted into database")
                    
            else:
                row = curs.fetchone()
                self.affected_username.set(row[0])
                _time=datetime.time(row[1] + datetime.combine(row[2], time()))
                timetime=datetime.time(row[3] + datetime.combine(row[4], time()))
                self.original_pickup_time.set(_time.strftime(TIME_FORMAT))
                self.original_pickup_date.set(row[2].strftime(DATE_FORMAT))
                self.original_return_date.set(row[4].strftime(DATE_FORMAT))
                self.original_return_time.set(timetime.strftime(TIME_FORMAT))
                self.affected_email_address.set(row[5])
                self.affected_phone_number.set(row[6])
                self.original_location = row[7]
                try:
                    curs.execute(sql.AFFECTED_USER_LATE_FEES, (datetime.date(datetime.strptime(self.original_pickup_date.get(), DATE_FORMAT)), datetime.time(datetime.strptime(self.original_pickup_time.get(), TIME_FORMAT)),
                                                               datetime.date(datetime.strptime(self.newarrivaldate.get(), DATE_FORMAT)), datetime.time(datetime.strptime(self.newarrivaltime.get(), TIME_FORMAT)),
                                                               datetime.date(datetime.strptime(self.originalreturndate.get(), DATE_FORMAT)), datetime.time(datetime.strptime(self.originalreturntime.get(), TIME_FORMAT)),
                                                               datetime.date(datetime.strptime(self.newarrivaldate.get(), DATE_FORMAT)), datetime.time(datetime.strptime(self.newarrivaltime.get(), TIME_FORMAT)),
                                                               self.sno_for_later, self.offending_username.get(),
                                                               self.offending_user_original_pickup_date, self.offending_user_original_pickup_time,
                                                               datetime.date(datetime.strptime(self.originalreturndate.get(), DATE_FORMAT)), datetime.time(datetime.strptime(self.originalreturntime.get(), TIME_FORMAT))))
                                                           
                    curs.execute(sql.EXTEND_NO_AFFECTED_USER, (datetime.strptime(self.originalreturndate.get(), DATE_FORMAT), self.originalreturntime.get(), datetime.strptime(self.newarrivaldate.get(), DATE_FORMAT), self.newarrivaltime.get(), self.extension, self.offending_username.get()))
                    db.commit()
                    messagebox.showinfo("Late Fees!", "The late user has been charged a late fee.")
                except:
                    messagebox.showerror("Unexpected error!", "Could not be inserted into database")
                
        update_button = ttk.Button(rentinfo_pane, text="Update", command=check_for_conflicts).grid(column=1, row=12, sticky=E)
        

        ###View Reports Tab
        viewreports_tab = ttk.Frame(self.notebook)
        self.notebook.add(viewreports_tab, text="View Reports")

        def location():
            self.location_report = ttk.Frame(viewreports_pane)
            self.location_report.grid(row=0, column=1, rowspan=4)
            ttk.Label(self.location_report, text="Month", style="GridTitle.TLabel").grid(row=0, column=0, sticky=N+E+W+S)
            ttk.Label(self.location_report, text="Location", style="GridTitle.TLabel").grid(row=0, column=1, sticky=N+E+W+S)
            ttk.Label(self.location_report, text="No. of Reservations", style="GridTitle.TLabel").grid(row=0, column=2, sticky=N+E+W+S)
            ttk.Label(self.location_report, text="Total No. of Hours", style="GridTitle.TLabel").grid(row=0, column=3, sticky=N+E+W+S)
            curs = db.cursor()
            curs.execute(sql.LOCATION_PREFERENCE_REPORT)
            count = 1
            for row in curs:
                ttk.Label(self.location_report, text="%s" % row[0], style='Grid.TLabel').grid(row=count, column=0, sticky=N+E+W+S)
                ttk.Label(self.location_report, text="%s" % row[1], style='Grid.TLabel').grid(row=count, column=1, sticky=N+E+W+S)
                ttk.Label(self.location_report, text="%s" % row[2], style='Grid.TLabel').grid(row=count, column=2, sticky=N+E+W+S)
                ttk.Label(self.location_report, text="%s" % row[3], style='Grid.TLabel').grid(row=count, column=3, sticky=N+E+W+S)
                count = count + 1
            self.previous = report.get()
            


        def frequent():
            self.frequent_report = ttk.Frame(viewreports_pane)
            self.frequent_report.grid(row=0, column=1, rowspan=4)
            ttk.Label(self.frequent_report, text="Username", style="GridTitle.TLabel").grid(row=0, column=0, sticky=N+E+W+S)
            ttk.Label(self.frequent_report, text="Driving Plan", style="GridTitle.TLabel").grid(row=0, column=1, sticky=N+E+W+S)
            ttk.Label(self.frequent_report, text="No. of Reservations per month", style="GridTitle.TLabel").grid(row=0, column=2, sticky=N+E+W+S)
            curs = db.cursor()
            curs.execute(sql.FREQUENT_USERS_REPORT)
            count = 1
            for row in curs:
                ttk.Label(self.frequent_report, text="%s" % row[0], style='Grid.TLabel').grid(row=count, column=0, sticky=N+E+W+S)
                ttk.Label(self.frequent_report, text="%s" % row[1], style='Grid.TLabel').grid(row=count, column=1, sticky=N+E+W+S)
                ttk.Label(self.frequent_report, text="%s" % row[2], style='Grid.TLabel').grid(row=count, column=2, sticky=N+E+W+S)
                count = count + 1
            self.previous = report.get()
                

        def maintenance():
            self.maintenance_report = ttk.Frame(viewreports_pane)
            self.maintenance_report.grid(row=0, column=1, rowspan=4)
            ttk.Label(self.maintenance_report, text="Car", style="GridTitle.TLabel").grid(row=0, column=0, sticky=N+E+W+S)
            ttk.Label(self.maintenance_report, text="Date-time", style="GridTitle.TLabel" ).grid(row=0, column=1, sticky=N+E+W+S)
            ttk.Label(self.maintenance_report, text="Employee", style="GridTitle.TLabel").grid(row=0, column=2, sticky=N+E+W+S)
            ttk.Label(self.maintenance_report, text="Problem", style="GridTitle.TLabel").grid(row=0, column=3, sticky=N+E+W+S)
            curs = db.cursor()
            curs.execute(sql.MAINTENANCE_HISTORY_REPORT)
            count = 1
            for row in curs:
                ttk.Label(self.maintenance_report, text="%s" % row[0], style='Grid.TLabel').grid(row=count, column=0, sticky=N+E+W+S)
                ttk.Label(self.maintenance_report, text="%s" % row[1], style='Grid.TLabel').grid(row=count, column=1, sticky=N+E+W+S)
                ttk.Label(self.maintenance_report, text="%s" % row[2], style='Grid.TLabel').grid(row=count, column=2, sticky=N+E+W+S)
                ttk.Label(self.maintenance_report, text="%s" % row[3], style='Grid.TLabel').grid(row=count, column=3, sticky=N+E+W+S)
                count = count + 1
            self.previous = report.get()

        def select_report(event):
            if self.previous != None:
                if self.previous == "Location Preference Report":
                    self.location_report.grid_forget()
                elif self.previous == "Frequent Users Report":
                    self.frequent_report.grid_forget()
                elif self.previous == "Maintenance History Report":
                    self.maintenance_report.grid_forget()
            if report.get() == "Location Preference Report":
                location()
            elif report.get() == "Frequent Users Report":
                frequent()
            elif report.get() == "Maintenance History Report":
                maintenance()
                
        self.previous = None
        viewreports_pane = ttk.Frame(viewreports_tab, relief="sunken", padding=(3,3,3,3))
        reportcombo_pane = ttk.Frame(viewreports_tab, relief="sunken", padding=(3,3,3,3))
        ttk.Label(reportcombo_pane, text="Which report would you like to view?").grid(column=0, row=0, sticky=E+W)
        report = StringVar()
        report_combo = ttk.Combobox(reportcombo_pane, values = ["Location Preference Report", "Frequent Users Report", "Maintenance History Report"], state="readonly",
                                            width=30, textvariable=report)
        report_combo.grid(column=0, row=1)
        viewreports_pane.grid(column=1, row=0, sticky=N+E+W+S)
        reportcombo_pane.grid(column=0, row=0, sticky=N+E+W+S)
        report_combo.bind("<<ComboboxSelected>>", select_report)


    def add_car_submit(self):
    # Add new car into database.
        try:
            curs = db.cursor()
            vehicle_sno_list = []
            capacity_list = []
            model_list = []


            # Make sure the fields aren't blank
            if self.vehicle_sno.get() == "" or self.location.get() == "" or self.carmodel2.get() == "" or self.cartype.get() == "" or self.seating_capacity.get() == "" or self.transmission_type.get() == "" or self.hourly_rate.get() == "" or self.daily_rate.get() == "" or self.bluetooth.get() == "" or self.aux.get() == "" or self.color.get() == "":
                messagebox.showerror("Error!", "One or more fields are left blank. Please try again.")
                return
                
            # Make sure not trying to add an existing vehicle 
            curs.execute(sql.VEHICLE_SNO_ERROR)
            for item in curs:
                vehicle_sno_list.append(item)

            for item in vehicle_sno_list:
                if self.vehicle_sno.get() == item[0]:
                    messagebox.showerror("Error!", "This car already exists!")
                    return

            # Make sure only one of each model at a location
            curs.execute(sql.MODEL_ERROR, self.location.get())
            for item in curs:
                model_list.append(item[0])

            for item in model_list:
                if self.carmodel2.get() == item:
                    messagebox.showerror("Error!", "A car of this model already exists at the selected location!")
                    return

            # Make sure adding the car doesn't exceed the location capacity
            curs.execute(sql.CAPACITY_ERROR)
            for item in curs:
                capacity_list.append(item)

            # Make sure adding the car doesn't exceed the location capacity
            curs.execute(sql.CAPACITY_ERROR)
            for item in curs:
                capacity_list.append(item)

            if len(capacity_list) > 0:
                if self.location.get() == capacity_list[0][0]:
                    messagebox.showerror("Error!", "The selected location is already at capacity!")
                    return
                
            sql_values = []

            curs.execute(sql.ADD_CAR, (self.vehicle_sno.get(), self.location.get(), self.carmodel2.get(),
                      self.cartype.get(), self.color.get(), self.seating_capacity.get(),
                      self.transmission_type.get(), self.aux.get(), "0", self.bluetooth.get(),
                      self.hourly_rate.get(), self.daily_rate.get()))
            db.commit()
            messagebox.showinfo("Success!", "New Car Added!")

        except:
            pass
        finally:
            curs.close()


    def model_in_loc(self):
    # Choose Car Dropdown Values
        try:
            curs = db.cursor()

            car_model_list = []
            
            curs.execute(sql.CAR_DROPDOWN_BY_MODEL, (self.choosecurrent.get()))
            
            for item in curs:
                car_model_list.append(item[0])

            self.choosecar_combo.configure(values=car_model_list)
            self.autopop_description()

        except:
            pass
        finally:
            curs.close()

    def model_in_loc_maint(self):
    # For Maintenance
        try:
            curs = db.cursor()

            car_model_list = []
            
            curs.execute(sql.CAR_DROPDOWN_BY_MODEL, (self.chooseloc_maint.get()))
            
            for item in curs:
                car_model_list.append(item[0])

            self.choosecar_maint_combo.configure(values=car_model_list)
        
        except:
            pass
        finally:
            curs.close()

    def autopop_description(self, event):
        try:
            curs = db.cursor()

            curs.execute(sql.BRIEF_DESCRIPTION, (self.choosecar_combo.get()))

            for item in curs:
                self.cartype2.set(item[0])
                self.color2.set(item[1])
                self.seating_capacity2.set(item[2])
                self.transmission_type2.set(item[3])
        except:
            pass
        finally:
            curs.close()

 
    def new_loc_submit(self):
        try:
        
            # Make sure adding the car doesn't exceed the location capacity

            curs = db.cursor()

            capacity_list = []

            model_list = []
            
            # Make sure only one of each model at a location
            curs.execute(sql.MODEL_ERROR, self.choosenew.get())
            for item in curs:
                model_list.append(item[0])

            for item in model_list:
                if self.choosecar.get() == item:
                    messagebox.showerror("Error!", "A car of this model already exists at the selected location!")
                    return

            if self.choosenew.get()== "" or self.choosecar.get() == "" or self.choosecurrent.get() == "":
                messagebox.showerror("Error!", "One or more fields are left blank. Please try again.")
                return
            
            # Make sure adding the car doesn't exceed the location capacity
            curs.execute(sql.CAPACITY_ERROR)
            for item in curs:
                capacity_list.append(item)
            
            if len(capacity_list) > 0:
                if self.choosenew.get() == capacity_list[0][0]:
                    messagebox.showerror("Error!", "The selected location is already at capacity!")
                    return

            curs.execute(sql.UPDATE_CAR_LOCATION, (self.choosenew.get(), self.choosecar.get()))
            db.commit()
            messagebox.showinfo("Success!", "Location updated.")
                
        except:
            pass
        finally:
            curs.close()


    def maint_submit(self):
        problem_list = ()
        data = self.briefproblem_text.get(1.0, END)
        len_problemlist = int(self.briefproblem_text.index('end').split('.')[0])-1
        vehicle_sno = ""

        for i in range(len_problemlist):
            problem_list = data.split("\n")

        del problem_list[len(problem_list)-1]

        problem_list_tup = tuple(problem_list)

        # Put car under maintenance
        try:
            curs = db.cursor()

            if self.choosecar_maint.get() == "" or self.chooseloc_maint.get() == "" or problem_list_tup[0] == "":
                messagebox.showerror("Error!", "One or more fields are left blank. Please try again.")
                return

            curs.execute(sql.PUT_UNDER_MAINTENANCE, (self.choosecar_maint.get(), self.chooseloc_maint.get()))

            # Get Vehicle SNO 

            curs.execute(sql.GET_VEHICLE_SNO, (self.choosecar_maint.get(), self.chooseloc_maint.get()))

            for item in curs:
                vehicle_sno = item[0]

            curs.execute(sql.INSERT_MAINTENANCE_REQUEST, (vehicle_sno, self.username))

            # For each problem
            for item in problem_list_tup:
                curs.execute(sql.INSERT_MAINTENANCE_PROBLEM, (vehicle_sno, self.username, item))

            db.commit()

            messagebox.showinfo("Success!", "Problem(s) Submitted!")
            
        except:
            pass
        finally:
            curs.close()
        

class AdminHomepage:
    def __init__(self, parent):
        """Draw the Admin Homepage"""

        self.parent = parent
        parent.withdraw()
        self.home_window = Toplevel(parent)
        self.home_window.title("Admin Homepage")
        self.home_window.protocol("WM_DELETE_WINDOW", lambda:wm_handler(self.home_window, parent))
        mainframe = ttk.Frame(self.home_window, padding=(3,3,12,12))
        mainframe.grid(sticky=N+E+W+S)

        revenue_report = ttk.LabelFrame(mainframe, text="Revenue Generated")
        ttk.Label(revenue_report, text="Vehicle Sno").grid(row=0, column=0)
        ttk.Label(revenue_report, text="Type").grid(row=0, column=1)
        ttk.Label(revenue_report, text="Car Model").grid(row=0, column=2)
        ttk.Label(revenue_report, text="Reservation Revenue").grid(row=0, column=3)
        ttk.Label(revenue_report, text="Late Fees Revenue").grid(row=0, column=4)


        curs = db.cursor()
        curs.execute(sql.REVENUE_GENERATED_REPORT)
        count = 1
        for row in curs:
            ttk.Label(revenue_report, text="%s" % row[0]).grid(row=count, column=0)
            ttk.Label(revenue_report, text="%s" % row[1]).grid(row=count, column=1)
            ttk.Label(revenue_report, text="%s" % row[2]).grid(row=count, column=2)
            ttk.Label(revenue_report, text="%s" % row[3]).grid(row=count, column=3)
            ttk.Label(revenue_report, text="%s" % row[4]).grid(row=count, column=4)
            count = count + 1
        revenue_report.grid()


class Car_Availability:

    def __init__(self, parent, username, return_date, return_time,
                 pickup_date, pickup_time, location,
                 _type=None, model=None):
        """Initiate Car Availability window. Keyword arg _type or model necessary"""

        self.parent = parent
        self.username = username
        self.return_date = return_date
        self.return_time = return_time
        self.pickup_date = pickup_date
        self.pickup_time = pickup_time
        self.location = location

        if return_date=="" or return_time=="" or pickup_date=="" or pickup_time=="" or location=="":
            messagebox.showerror("Error!", "Please fill out necessary fields")
            return
            
        
        parent.withdraw()
        car_avail_window = Toplevel(parent)
        car_avail_window.title("Car Availability")

        time_label = ttk.Label(car_avail_window, text="Reservation Time: ")
        
        if pickup_date == return_date:
            time_label['text'] += pickup_time + " - " + return_time
        else:
            time_label['text'] += pickup_date + " " + pickup_time + " - " + return_date + " " + return_time

        time_label.grid(sticky=N+W)
        
        labels = ["Car Model", "Car Type", "Location", "Color", "Hourly Rate",
                  "Discounted\nRate (Frequent\nDriving plan)", "Discounted\nRate (Daily\nDriving plan)",
                  "Daily Rate", "Seating\nCapacity", "Transmission\nType", "Bluetooth\nConnectivity",
                  "Auxiliary\ncable", "Available\ntill", "Estimated Cost"]

        frame = ttk.Frame(car_avail_window, padding=5)
        for i in range(len(labels)):
            ttk.Label(frame, text=labels[i], style="GridTitle.TLabel").grid(row=0, column=i, sticky=N+E+W+S)
        ttk.Label(frame).grid(row=0, column=len(labels))

        curs = db.cursor()
        curs.execute(sql.CREATE_USERPLAN_VIEW)
        curs.execute(sql.CREATE_EARLIEST_CAR_AVAILABILITY_VIEW)
        curs.execute(sql.DAILY_DRIVING_DISCOUNT)
        daily_driving_discount = curs.fetchone()[0]
        curs.execute(sql.FREQUENT_DRIVING_DISCOUNT)
        frequent_driving_discount = curs.fetchone()[0]

        values = sql.CAR_AVAILABILITY_DICTIONARY
        values["freq_discount"] = frequent_driving_discount
        values["daily_discount"] = daily_driving_discount
        values["return_date"] = datetime.date(datetime.strptime(return_date, DATE_FORMAT))
        values["return_time"] = datetime.time(datetime.strptime(return_time, TIME_FORMAT))
        values["pickup_date"] = datetime.date(datetime.strptime(pickup_date, DATE_FORMAT))
        values["pickup_time"] = datetime.time(datetime.strptime(pickup_time, TIME_FORMAT))
        values["location"] = location
        values["username"] = username
        values["type"] = _type
        values["model"] = model
        
        if _type != None:
            curs.execute(sql.CASE_3, values)
        elif model != None:
            curs.execute(sql.CASE_2, values)
        else:
            curs.execute(sql.CASE_1, values)

        tups = curs.fetchall()
        curs.close()
        self.selection = IntVar()
        self.selection.set(-1)

        for i in range(len(tups)):
            for j in range(1,len(tups[i])): #FIRST ELEMENT IS VEHICLE SNO. GET IT LATER
                label = ttk.Label(frame, text=tups[i][j])
                if tups[i][3] == location:
                    label.configure(style="Green.Grid.TLabel")
                else:
                    label.configure(style="Grid.TLabel")
                label.grid(row=1+i, column=j-1, sticky=N+E+W+S)
            ttk.Radiobutton(frame, value=i, variable=self.selection).grid(row=1+i, column=len(tups[i])-1, sticky=N+E+W+S)

        frame.grid()

        ttk.Button(car_avail_window, text="Reserve",
                   command=lambda:self.reserve(tups, car_avail_window)).grid(row=2, sticky=E)
        ttk.Button(car_avail_window, text="Back",
                   command=lambda:self.back(car_avail_window)).grid(row=2,sticky=W)

    def back(self, win):
        win.destroy()
        self.parent.deiconify()
    
    def reserve(self, tups, win):

        if self.selection.get() == -1:
            messagebox.showerror("No Reservation Selected", "Please select a" +
                    " Reservation")
        else:
            #(Username, PickUp_Date, PickUp_Time, Return_Date, Return_Time, Vehicle_Sno, Location_Name, Return_Status, Estimated_Cost)
            for i in range(len(tups)):
                if self.selection.get() == i:
                    _input = (self.username, datetime.date(datetime.strptime(self.pickup_date, DATE_FORMAT)),
                              datetime.time(datetime.strptime(self.pickup_time, TIME_FORMAT)),
                              datetime.date(datetime.strptime(self.return_date, DATE_FORMAT)),
                              datetime.time(datetime.strptime(self.return_time, TIME_FORMAT)), tups[i][0],
                              self.location, tups[i][14])
                    
            curs = db.cursor()
            curs.execute(sql.RESERVATION_BUTTON, _input)
            curs.close()
            db.commit()
            messagebox.showinfo("Reservation made", "You made a reservation"
                    + " on " + _input[5] + " for " +
                    _input[1].strftime(DATE_FORMAT) + " " +
                    _input[2].strftime(TIME_FORMAT) + ".")
            win.destroy()
            self.parent.deiconify()

root = Tk()
login = LoginPage(root)
db = Connect()
root.mainloop()
db.close()
