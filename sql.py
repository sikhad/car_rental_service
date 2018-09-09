# SQL for car rental service

## Login Page ##

LOGIN_CHECK = "SELECT *"
LOGIN_CHECK += " FROM USER WHERE Username = %s"
LOGIN_CHECK += " AND Password = %s"
## If this returns a row, then successful login

## Else, check username: 
USERNAME_CHECK = "SELECT *"
USERNAME_CHECK += " FROM USER WHERE Username = %s"

    ## If this returns a row, then password incorrect
    ## Else, username incorrect


## New User Registration ##
    
## Create Account Dropdown
ACCOUNT_TYPES = "SELECT DISTINCT User_Type"
ACCOUNT_TYPES += " FROM USER WHERE User_Type <> 'Administrator'"

REGISTER_USER = "INSERT INTO USER (Username, Password, User_Type) VALUES (%s, %s, %s)"


## Student_Faculty Homepage ## 

## If Rent a Car is selected
PERSONALINFO_CHECK = "SELECT 1"
PERSONALINFO_CHECK += "FROM STUDENT_FACULTY"
PERSONALINFO_CHECK += "WHERE Username = $Username"
    ## If returns “1”, then proceed
    ## Else, show error to enter personal information first

## Populate pre-existing information
GET_PERSONALINFO = "SELECT * FROM STUDENT_FACULTY AS a INNER JOIN CREDIT_CARD AS b ON (a.Credit_Card_No = b.Credit_Card_No) WHERE Username = $Username"


## Enter Personal Information (Including Credit Card Info) ##

## Insert Credit Card Information
INSERT_CCINFO = "INSERT INTO CREDIT_CARD (Credit_Card_No, Name_On_Card, CVV, Expiry_Date, Billing_Address) VALUES ($Credit_Card_No, $Name_On_Card, $CVV, $Expiry_Date, $Billing_Address)"

## Then, Insert Student_Faculty Information
INSERT_PERSONALINFO = "INSERT INTO STUDENT_FACULTY (Username, Credit_Card_No, Plan_Type, First_Name, Middle_Init, Last_name, Address, Email, Phone_Number) VALUES ($Username, $Credit_Card_No, $Plan_Type, $First_Name, $Middle_Init, $Last_name, $Address, $Email, $Phone_Number)"


## View Driving Plan ##
GET_DRIVINGPLANINFO = "SELECT Plan_Type, Discount, Annual_Fees, Monthly_Payment"
GET_DRIVINGPLANINFO += "FROM DRIVING_PLAN"


## Update Credit_Card ##
UPDATE_CCINFO = "UPDATE CREDIT_CARD SET Credit_Card_No = $ Credit_Card_No, Name_On_Card = $Name_On_Card, CVV, Expiry_Date = $Expiry_Date, Billing_Address = $ Billing_Address"


## Update Student_Faculty ##
UPDATE_PERSONALINFO = "UPDATE STUDENT_FACULTY SET, Plan_Type = $Plan_Type, First_Name = $ First_Name, Middle_Init = $Middle_Init, Last_Name = $Last_Name, Address = $Address, Email = $Email, Phone_Number = $Phone_Number WHERE Username = $Username"


## Rent a Car ##
GET_LOCATIONS = "SELECT DISTINCT Location_Name"
GET_LOCATIONS += " FROM LOCATION"

# Car type dropdown menu
GET_TYPES = "SELECT DISTINCT Type"
GET_TYPES += " FROM CAR AS c"
GET_TYPES += " INNER JOIN LOCATION AS l"
GET_TYPES += " ON (c.Location_Name = l.Location_Name)"
GET_TYPES += " WHERE l.Location_Name = $Location_Name"

# Car model dropdown menu
GET_MODELS = "SELECT DISTINCT Model FROM CAR AS c INNER JOIN LOCATION AS l ON (c.Location_Name = l.Location_Name) WHERE l.Location_Name = $Location_Name"


## Car Availability ##
CREATE_USERPLAN_VIEW = "CREATE OR REPLACE VIEW USER_PLAN AS SELECT a.Username, a.Plan_Type, IFNULL(b.Discount, 0) AS DISCOUNT FROM STUDENT_FACULTY AS a INNER JOIN DRIVING_PLAN AS b ON (a.Plan_Type = b.Plan_Type)"
CREATE_EARLIEST_CAR_AVAILABILITY_VIEW = "CREATE OR REPLACE VIEW EARLIEST_CAR_AVAILABILITY AS SELECT Vehicle_Sno, MIN(TIMESTAMP(Pickup_Date, Pickup_Time)) AS AVAILABLE_FROM FROM RESERVATION WHERE Return_Status=0 GROUP BY Vehicle_Sno"

# Store as $Daily_Driving_Discount
DAILY_DRIVING_PLAN = "SELECT Discount"
DAILY_DRIVING_PLAN += " FROM DRIVING_PLAN"
DAILY_DRIVING_PLAN += " WHERE Plan_Type = 'Daily Driving'"

# Store as $Frequent_Driving_Discount
FREQUENT_DRIVING_DISCOUNT = "SELECT Discount"
FREQUENT_DRIVING_DISCOUNT += " FROM DRIVING_PLAN"
FREQUENT_DRIVING_DISCOUNT += " WHERE Plan_Type = 'Frequent Driving'"

# Case 1: Only Pickup Time, Return Time, and Location chosen
CASE_1 = " SELECT C.Vehicle_Sno, Model, Type, Location_Name, Color, Hourly_Rate,"
CASE_1 += " Hourly_rate*(1-$Frequent_Driving_Discount) AS Hourly_Rate_Frequent_Driving, Hourly_rate*(1-$Daily_Driving_Discount) AS Hourly_Rate_Daily_Driving,"
CASE_1 += " Daily_Rate, Seating_Capacity, Transmission_Type, Bluetooth, Auxiliary_Cable,"
CASE_1 += " CASE WHEN TIMESTAMPDIFF(hour,TIMESTAMP($Selected_Return_Date, $Selected_Return_Time), AVAILABLE_FROM) BETWEEN 0 AND 12"
CASE_1 += " THEN AVAILABLE_FROM END AS AVAILABLE_TILL,"
CASE_1 += " CASE WHEN TIMESTAMPDIFF(hour, TIMESTAMP($Selected_PickUp_Date, $Selected_PickUp_Time), TIMESTAMP($Selected_Return_Date, $Selected_Return_Time)) < 24" 
CASE_1 += " THEN TIMESTAMPDIFF(hour, TIMESTAMP($Selected_PickUp_Date, $Selected_PickUp_Time), TIMESTAMP($Selected_Return_Date, $Selected_Return_Time)) * Hourly_Rate * (1-D.Discount)"
CASE_1 += " WHEN TIMESTAMPDIFF(hour, TIMESTAMP($Selected_PickUp_Date, $Selected_PickUp_Time), TIMESTAMP($Selected_Return_Date, $Selected_Return_Time)) = 24" 
CASE_1 += " THEN Daily_Rate"
CASE_1 += " ELSE 2*Daily_Rate"
CASE_1 += " END AS Estimated_Cost"
CASE_1 += " FROM CAR AS C"
CASE_1 += " LEFT OUTER JOIN EARLIEST_CAR_AVAILABILITY AS E"
CASE_1 += " ON (C.Vehicle_Sno=E.Vehicle_Sno),"
CASE_1 += " USER_PLAN AS D"
CASE_1 += " WHERE C.Vehicle_Sno" 
CASE_1 += " NOT IN (SELECT Vehicle_Sno" 
CASE_1 += " FROM RESERVATION"
CASE_1 += " WHERE"
CASE_1 += " (TIMESTAMP($Selected_PickUp_Date, $Selected_PickUp_Time)"
CASE_1 += " BETWEEN TIMESTAMP(Pickup_Date, Pickup_Time)" 
CASE_1 += " AND TIMESTAMP(Return_Date, Return_Time)" 
CASE_1 += " OR"
CASE_1 += " TIMESTAMP($Selected_Return_Date, $Selected_Return_Time)"
CASE_1 += " BETWEEN TIMESTAMP(Pickup_Date, Pickup_Time)" 
CASE_1 += " AND TIMESTAMP(Return_Date, Return_Time)))"
CASE_1 += " AND Location_Name = $Location_Name" 
CASE_1 += " AND Under_Maintenance = 0"
CASE_1 += " AND Username = $Username"
CASE_1 += " UNION"
CASE_1 += " SELECT C.Vehicle_Sno, Model, Type, Location_Name, Color, Hourly_Rate," 
CASE_1 += " Hourly_rate*(1-$Frequent_Driving_Discount) AS Hourly_Rate_Frequent_Driving, Hourly_rate*(1-$Daily_Driving_Discount) AS Hourly_Rate_Daily_Driving,"
CASE_1 += " Daily_Rate, Seating_Capacity, Transmission_Type, Bluetooth, Auxiliary_Cable,"
CASE_1 += " CASE WHEN TIMESTAMPDIFF(hour,TIMESTAMP($Selected_Return_Date, $Selected_Return_Time), AVAILABLE_FROM) BETWEEN 0 AND 12" 
CASE_1 += " THEN AVAILABLE_FROM END AS AVAILABLE_TILL,"
CASE_1 += " CASE WHEN TIMESTAMPDIFF(hour, TIMESTAMP($Selected_PickUp_Date, $Selected_PickUp_Time), TIMESTAMP($Selected_Return_Date, $Selected_Return_Time)) < 24"
CASE_1 += " THEN TIMESTAMPDIFF(hour, TIMESTAMP($Selected_PickUp_Date, $Selected_PickUp_Time), TIMESTAMP($Selected_Return_Date, $Selected_Return_Time)) * Hourly_Rate * (1-D.Discount)"
CASE_1 += " WHEN TIMESTAMPDIFF(hour, TIMESTAMP($Selected_PickUp_Date, $Selected_PickUp_Time), TIMESTAMP($Selected_Return_Date, $Selected_Return_Time)) = 24"
CASE_1 += " THEN Daily_Rate"
CASE_1 += " ELSE 2*Daily_Rate"
CASE_1 += " END AS Estimated_Cost"
CASE_1 += " FROM CAR AS C"
CASE_1 += " LEFT OUTER JOIN EARLIEST_CAR_AVAILABILITY AS E"
CASE_1 += " ON (C.Vehicle_Sno=E.Vehicle_Sno)," 
CASE_1 += " USER_PLAN AS D"
CASE_1 += " WHERE C.Vehicle_Sno" 
CASE_1 += " NOT IN (SELECT Vehicle_Sno" 
CASE_1 += " FROM RESERVATION"
CASE_1 += " WHERE"
CASE_1 += " (TIMESTAMP($Selected_PickUp_Date, $Selected_PickUp_Time)"
CASE_1 += " BETWEEN TIMESTAMP(PickUp_Date, PickUp_Time)" 
CASE_1 += " AND TIMESTAMP(Return_Date, Return_Time)"
CASE_1 += " OR"
CASE_1 += " TIMESTAMP($Selected_Return_Date, $Selected_Return_Time)"
CASE_1 += " BETWEEN TIMESTAMP(Pickup_Date, Pickup_Time)" 
CASE_1 += " AND TIMESTAMP(Return_Date, Return_Time)))" 
CASE_1 += " AND Under_Maintenance = 0"
CASE_1 += " AND Username = $Username"

# Case 2: By Model 
CASE_2 = "SELECT C.Vehicle_Sno, Model, Type, Location_Name, Color, Hourly_Rate," 
CASE_2 += " Hourly_rate*(1-$Frequent_Driving_Discount) AS Hourly_Rate_Frequent_Driving, Hourly_rate*(1-$Daily_Driving_Discount) AS Hourly_Rate_Daily_Driving,"
CASE_2 += " Daily_Rate, Seating_Capacity, Transmission_Type, Bluetooth, Auxiliary_Cable,"
CASE_2 += " CASE WHEN TIMESTAMPDIFF(hour,TIMESTAMP($Selected_Return_Date, $Selected_Return_Time), AVAILABLE_FROM) BETWEEN 0 AND 12" 
CASE_2 += " THEN AVAILABLE_FROM END AS AVAILABLE_TILL,"
CASE_2 += " CASE WHEN TIMESTAMPDIFF(hour, TIMESTAMP($Selected_PickUp_Date, $Selected_PickUp_Time), TIMESTAMP($Selected_Return_Date, $Selected_Return_Time)) < 24" 
CASE_2 += " THEN TIMESTAMPDIFF(hour, TIMESTAMP($Selected_PickUp_Date, $Selected_PickUp_Time), TIMESTAMP($Selected_Return_Date, $Selected_Return_Time)) * Hourly_Rate * (1-D.Discount)"
CASE_2 += " WHEN TIMESTAMPDIFF(hour, TIMESTAMP($Selected_PickUp_Date, $Selected_PickUp_Time), TIMESTAMP($Selected_Return_Date, $Selected_Return_Time)) = 24" 
CASE_2 += " THEN Daily_Rate"
CASE_2 += " ELSE 2*Daily_Rate"
CASE_2 += " END AS Estimated_Cost"
CASE_2 += " FROM CAR AS C" 
CASE_2 += " LEFT OUTER JOIN EARLIEST_CAR_AVAILABILITY AS E" 
CASE_2 += " ON (C.Vehicle_Sno=E.Vehicle_Sno)," 
CASE_2 += " USER_PLAN AS D"
CASE_2 += " WHERE C.Vehicle_Sno" 
CASE_2 += " NOT IN (SELECT Vehicle_Sno" 
CASE_2 += " FROM RESERVATION"
CASE_2 += " WHERE"
CASE_2 += " (TIMESTAMP($Selected_PickUp_Date, $Selected_PickUp_Time)"
CASE_2 += " BETWEEN TIMESTAMP(Pickup_Date, Pickup_Time)" 
CASE_2 += " AND TIMESTAMP(Return_Date, Return_Time)"
CASE_2 += " OR"
CASE_2 += " TIMESTAMP($Selected_Return_Date, $Selected_Return_Time)"
CASE_2 += " BETWEEN TIMESTAMP(Pickup_Date, Pickup_Time)" 
CASE_2 += " AND TIMESTAMP(Return_Date, Return_Time)))" 
CASE_2 += " AND Location_Name = $Location_Name AND Model = $Model"
CASE_2 += " AND Under_Maintenance = 0"
CASE_2 += " AND Username = $Username"
CASE_2 += " UNION"
CASE_2 += " SELECT C.Vehicle_Sno, Model, Type, Location_Name, Color, Hourly_Rate," 
CASE_2 += " Hourly_rate*(1-$Frequent_Driving_Discount) AS Hourly_Rate_Frequent_Driving, Hourly_rate*(1-$Daily_Driving_Discount) AS Hourly_Rate_Daily_Driving,"
CASE_2 += " Daily_Rate, Seating_Capacity, Transmission_Type, Bluetooth, Auxiliary_Cable,"
CASE_2 += " CASE WHEN TIMESTAMPDIFF(hour,TIMESTAMP($Selected_Return_Date, $Selected_Return_Time), AVAILABLE_FROM) BETWEEN 0 AND 12" 
CASE_2 += " THEN AVAILABLE_FROM END AS AVAILABLE_TILL,"
CASE_2 += " CASE WHEN TIMESTAMPDIFF(hour, TIMESTAMP($Selected_PickUp_Date, $Selected_PickUp_Time), TIMESTAMP($Selected_Return_Date, $Selected_Return_Time)) < 24"
CASE_2 += " THEN TIMESTAMPDIFF(hour, TIMESTAMP($Selected_PickUp_Date, $Selected_PickUp_Time), TIMESTAMP($Selected_Return_Date, $Selected_Return_Time)) * Hourly_Rate * (1-D.Discount)"
CASE_2 += " WHEN TIMESTAMPDIFF(hour, TIMESTAMP($Selected_PickUp_Date, $Selected_PickUp_Time), TIMESTAMP($Selected_Return_Date, $Selected_Return_Time)) = 24" 
CASE_2 += " THEN Daily_Rate"
CASE_2 += " ELSE 2*Daily_Rate"
CASE_2 += " END AS Estimated_Cost"
CASE_2 += " FROM CAR AS C" 
CASE_2 += " LEFT OUTER JOIN EARLIEST_CAR_AVAILABILITY AS E" 
CASE_2 += " ON (C.Vehicle_Sno=E.Vehicle_Sno)," 
CASE_2 += " USER_PLAN AS D"
CASE_2 += " WHERE C.Vehicle_Sno" 
CASE_2 += " NOT IN (SELECT Vehicle_Sno" 
CASE_2 += " FROM RESERVATION"
CASE_2 += " WHERE"
CASE_2 += " (TIMESTAMP($Selected_PickUp_Date, $Selected_PickUp_Time)"
CASE_2 += " BETWEEN TIMESTAMP(PickUp_Date, PickUp_Time)" 
CASE_2 += " AND TIMESTAMP(Return_Date, Return_Time)" 
CASE_2 += " OR"
CASE_2 += " TIMESTAMP($Selected_Return_Date, $Selected_Return_Time)"
CASE_2 += " BETWEEN TIMESTAMP(Pickup_Date, Pickup_Time)" 
CASE_2 += " AND TIMESTAMP(Return_Date, Return_Time)))" 
CASE_2 += " AND Under_Maintenance = 0"
CASE_2 += " AND Username = $Username"

# Case 3: By Type
CASE_3 = "SELECT C.Vehicle_Sno, Model, Type, Location_Name, Color, Hourly_Rate," 
CASE_3 += " Hourly_rate*(1-$Frequent_Driving_Discount) AS Hourly_Rate_Frequent_Driving, Hourly_rate*(1-$Daily_Driving_Discount) AS Hourly_Rate_Daily_Driving,"
CASE_3 += " Daily_Rate, Seating_Capacity, Transmission_Type, Bluetooth, Auxiliary_Cable,"
CASE_3 += " CASE WHEN TIMESTAMPDIFF(hour,TIMESTAMP($Selected_Return_Date, $Selected_Return_Time), AVAILABLE_FROM) BETWEEN 0 AND 12" 
CASE_3 += " THEN AVAILABLE_FROM END AS AVAILABLE_TILL,"
CASE_3 += " CASE WHEN TIMESTAMPDIFF(hour, TIMESTAMP($Selected_PickUp_Date, $Selected_PickUp_Time), TIMESTAMP($Selected_Return_Date, $Selected_Return_Time)) < 24" 
CASE_3 += " THEN TIMESTAMPDIFF(hour, TIMESTAMP($Selected_PickUp_Date, $Selected_PickUp_Time), TIMESTAMP($Selected_Return_Date, $Selected_Return_Time)) * Hourly_Rate * (1-D.Discount)"
CASE_3 += " WHEN TIMESTAMPDIFF(hour, TIMESTAMP($Selected_PickUp_Date, $Selected_PickUp_Time), TIMESTAMP($Selected_Return_Date, $Selected_Return_Time)) = 24" 
CASE_3 += " THEN Daily_Rate"
CASE_3 += " ELSE 2*Daily_Rate"
CASE_3 += " END AS Estimated_Cost"
CASE_3 += " FROM CAR AS C" 
CASE_3 += " LEFT OUTER JOIN EARLIEST_CAR_AVAILABILITY AS E" 
CASE_3 += " ON (C.Vehicle_Sno=E.Vehicle_Sno)," 
CASE_3 += " USER_PLAN AS D"
CASE_3 += " WHERE C.Vehicle_Sno" 
CASE_3 += " NOT IN (SELECT Vehicle_Sno" 
CASE_3 += " FROM RESERVATION"
CASE_3 += " WHERE"
CASE_3 += " (TIMESTAMP($Selected_PickUp_Date, $Selected_PickUp_Time)"
CASE_3 += " BETWEEN TIMESTAMP(Pickup_Date, Pickup_Time)" 
CASE_3 += " AND TIMESTAMP(Return_Date, Return_Time)"
CASE_3 += " OR"
CASE_3 += " TIMESTAMP($Selected_Return_Date, $Selected_Return_Time)"
CASE_3 += " BETWEEN TIMESTAMP(Pickup_Date, Pickup_Time)" 
CASE_3 += " AND TIMESTAMP(Return_Date, Return_Time)))" 
CASE_3 += " AND Location_Name = $Location_Name AND Type = $Type"
CASE_3 += " AND Under_Maintenance = 0"
CASE_3 += " AND Username = $Username"
CASE_3 += " UNION"
CASE_3 += " SELECT C.Vehicle_Sno, Model, Type, Location_Name, Color, Hourly_Rate," 
CASE_3 += " Hourly_rate*(1-$Frequent_Driving_Discount) AS Hourly_Rate_Frequent_Driving, Hourly_rate*(1-$Daily_Driving_Discount) AS Hourly_Rate_Daily_Driving,"
CASE_3 += " Daily_Rate, Seating_Capacity, Transmission_Type, Bluetooth, Auxiliary_Cable,"
CASE_3 += " CASE WHEN TIMESTAMPDIFF(hour,TIMESTAMP($Selected_Return_Date, $Selected_Return_Time), AVAILABLE_FROM) BETWEEN 0 AND 12" 
CASE_3 += " THEN AVAILABLE_FROM END AS AVAILABLE_TILL,"
CASE_3 += " CASE WHEN TIMESTAMPDIFF(hour, TIMESTAMP($Selected_PickUp_Date, $Selected_PickUp_Time), TIMESTAMP($Selected_Return_Date, $Selected_Return_Time)) < 24"
CASE_3 += " THEN TIMESTAMPDIFF(hour, TIMESTAMP($Selected_PickUp_Date, $Selected_PickUp_Time), TIMESTAMP($Selected_Return_Date, $Selected_Return_Time)) * Hourly_Rate * (1-D.Discount)"
CASE_3 += " WHEN TIMESTAMPDIFF(hour, TIMESTAMP($Selected_PickUp_Date, $Selected_PickUp_Time), TIMESTAMP($Selected_Return_Date, $Selected_Return_Time)) = 24" 
CASE_3 += " THEN Daily_Rate"
CASE_3 += " ELSE 2*Daily_Rate"
CASE_3 += " END AS Estimated_Cost"
CASE_3 += " FROM CAR AS C" 
CASE_3 += " LEFT OUTER JOIN EARLIEST_CAR_AVAILABILITY AS E" 
CASE_3 += " ON (C.Vehicle_Sno=E.Vehicle_Sno)," 
CASE_3 += " USER_PLAN AS D"
CASE_3 += " WHERE C.Vehicle_Sno" 
CASE_3 += " NOT IN (SELECT Vehicle_Sno" 
CASE_3 += " FROM RESERVATION"
CASE_3 += " WHERE"
CASE_3 += " (TIMESTAMP($Selected_PickUp_Date, $Selected_PickUp_Time)"
CASE_3 += " BETWEEN TIMESTAMP(PickUp_Date, PickUp_Time)" 
CASE_3 += " AND TIMESTAMP(Return_Date, Return_Time)" 
CASE_3 += " OR"
CASE_3 += " TIMESTAMP($Selected_Return_Date, $Selected_Return_Time)"
CASE_3 += " BETWEEN TIMESTAMP(Pickup_Date, Pickup_Time)" 
CASE_3 += " AND TIMESTAMP(Return_Date, Return_Time)))" 
CASE_3 += " AND Under_Maintenance = 0"
CASE_3 += " AND Username = $Username"

# When “Reservation” button is pressed, execute this
RESERVATION_BUTTON = "INSERT INTO RESERVATION (Username, PickUp_Date, PickUp_Time, Return_Date, Return_Time, Vehicle_Sno, Location_Name, Return_Status, Estimated_Cost)" 
RESERVATION_BUTTON += " VALUES ($Username, $PickUp_Date, $PickUp_Time, $Return_Date, $Return_Time, $Vehicle_Sno, $Location_Name, 0, $Estimated_Cost)"


## View Rental Information ##
# Show Current Reservation
SHOW_CURRENT_RESERVATION = "SELECT c.Vehicle_Sno, r.PickUp_Time, r.PickUp_Date, r.Return_Time, r.Return_Date, c.Model, c.Location_Name, r.Estimated_Cost"
SHOW_CURRENT_RESERVATION += " FROM RESERVATION AS r" 
SHOW_CURRENT_RESERVATION += " INNER JOIN CAR AS c" 
SHOW_CURRENT_RESERVATION += " ON r.Vehicle_Sno = c.Vehicle_Sno"
SHOW_CURRENT_RESERVATION += " INNER JOIN STUDENT_FACULTY AS u" 
SHOW_CURRENT_RESERVATION += " ON r.Username = u.Username"
SHOW_CURRENT_RESERVATION += " WHERE U.Username = $Username" 
SHOW_CURRENT_RESERVATION += " AND Return_Status = 0"
SHOW_CURRENT_RESERVATION += " AND Current_Timestamp" 
SHOW_CURRENT_RESERVATION += " BETWEEN TIMESTAMP(r.Pickup_Date, r.Pickup_Time)"
SHOW_CURRENT_RESERVATION += " AND TIMESTAMP(r.Return_Date, r.Return_Time)"

# Extend Reservation
# If user chooses to extend, get $Vehicle_Sno from previous SQL to check if the same vehicle has been booked
# by some other user during extend period
# If the query returns true then user should not be allowed to extend
EXTEND_RESERVATION_CHECK = "SELECT *"
EXTEND_RESERVATION_CHECK += " FROM RESERVATION"
EXTEND_RESERVATION_CHECK += " WHERE Vehicle_Sno = $Vehicle_Sno AND TIMESTAMP($Extend_Date, $Extend_Time)"
EXTEND_RESERVATION_CHECK += " BETWEEN TIMESTAMP(Pickup_Date, Pickup_Time)"
EXTEND_RESERVATION_CHECK += " AND TIMESTAMP(Return_Date, Return_Time)"
EXTEND_RESERVATION_CHECK += " AND Username  <> $Username"

# If the previous query returns 0 rows, then extend the reservation
EXTEND_RESERVATION = "INSERT INTO RESERVATION_EXTENDED_TIME (PickUp_Date, PickUp_Time, Return_Date, Return_Time, Extended_Time, Username)"
EXTEND_RESERVATION += " VALUES ($PickUp_Date, $PickUp_Time, $Return_Date, $Return_Time, $Extended_Time, $Username)"

# Calculate New Estimated Amount
CALCULATE_NEW_ESTIMATED_AMOUNT = "SELECT CASE WHEN TIMESTAMPDIFF(hour, TIMESTAMP(PickUp_Date, PickUp_Time),TIMESTAMP($New_Return_Date, $New_Return_Time)) < 24"
CALCULATE_NEW_ESTIMATED_AMOUNT += " THEN TIMESTAMPDIFF(hour, TIMESTAMP(PickUp_Date, PickUp_Time),TIMESTAMP($New_Return_Date, $New_Return_Time))*(1-Discount) * HOURLY_RATE"
CALCULATE_NEW_ESTIMATED_AMOUNT += " WHEN TIMESTAMPDIFF(hour, TIMESTAMP(PickUp_Date, PickUp_Time),TIMESTAMP($New_Return_Date, $New_Return_Time)) = 24"
CALCULATE_NEW_ESTIMATED_AMOUNT += " THEN Daily_Rate"
CALCULATE_NEW_ESTIMATED_AMOUNT += " WHEN TIMESTAMPDIFF(hour, TIMESTAMP(PickUp_Date, PickUp_Time),TIMESTAMP($New_Return_Date, $New_Return_Time)) > 24"
CALCULATE_NEW_ESTIMATED_AMOUNT += " THEN 2* DAILY_RATE"
CALCULATE_NEW_ESTIMATED_AMOUNT += " END AS ESTIMATED_COST"
CALCULATE_NEW_ESTIMATED_AMOUNT += " FROM RESERVATION AS R"
CALCULATE_NEW_ESTIMATED_AMOUNT += " INNER JOIN USER_PLAN AS U"
CALCULATE_NEW_ESTIMATED_AMOUNT += " ON (R.Username = U.Username)"
CALCULATE_NEW_ESTIMATED_AMOUNT += " INNER JOIN CAR AS C"
CALCULATE_NEW_ESTIMATED_AMOUNT += " ON (R.Vehicle_Sno=C.Vehicle_Sno)"
CALCULATE_NEW_ESTIMATED_AMOUNT += " WHERE R.Username = $Username"
CALCULATE_NEW_ESTIMATED_AMOUNT += " AND Pickup_Date = $Pickup_Date"
CALCULATE_NEW_ESTIMATED_AMOUNT += " AND Pickup_Time = $Pickup_Time"
CALCULATE_NEW_ESTIMATED_AMOUNT += " AND Return_Date = $Return_Date"
CALCULATE_NEW_ESTIMATED_AMOUNT += " AND Return_Time = $Return_Time"

# View Previous Reservations
VIEW_PREVIOUS_RESERVATIONS = "SELECT r.PickUp_Date,r.PickUp_Time, r.Return_Date, r.Return_Time, c.Model, c.Location_Name, r.Estimated_Cost, Late_By"
VIEW_PREVIOUS_RESERVATIONS += " FROM RESERVATION AS r" 
VIEW_PREVIOUS_RESERVATIONS += " INNER JOIN CAR AS c" 
VIEW_PREVIOUS_RESERVATIONS += " ON r.Vehicle_Sno = c.Vehicle_Sno"
VIEW_PREVIOUS_RESERVATIONS += " INNER JOIN STUDENT_FACULTY AS u" 
VIEW_PREVIOUS_RESERVATIONS += " ON r.Username = u.Username"
VIEW_PREVIOUS_RESERVATIONS += " WHERE u.Username = $Username" 
VIEW_PREVIOUS_RESERVATIONS += " AND Return_Status = 1"
VIEW_PREVIOUS_RESERVATIONS += " ORDER BY Pickup_Date"


## Manage Cars ##

# Add car
ADD_CAR = "INSERT INTO CAR (Vehicle_Sno, Location_Name, Model, Type, Color, Seating_Capacity, Transmission_Type, Under_Maintenance, Bluetooth, Hourly_Rate, Daily_Rate)"
ADD_CAR += " VALUES ($Vehicle_Sno, $Location_Name, $Model, $Type, $Color, $Seating_Capacity, $Transmission_Type, $Under_Maintenance, $Bluetooth, $Hourly_Rate, $Daily_Rate)"

# Location dropdown ###What is the difference between this and prev location?
LOCATION_DROPDOWN = "SELECT Location_Name"
LOCATION_DROPDOWN += " FROM LOCATION"

# Car dropdown by model
CAR_DROPDOWN_BY_MODEL = "SELECT Model, Vehicle_Sno"
CAR_DROPDOWN_BY_MODEL += " FROM CAR"
CAR_DROPDOWN_BY_MODEL += " WHERE Location_Name = $Location_Name"

# Auto-populate “Brief Description”
BRIEF_DESCRIPTION = "SELECT Type, Color, Seating_Capacity, Transmission_Type"
BRIEF_DESCRIPTION += " FROM CAR"
BRIEF_DESCRIPTION += " WHERE Model = $Model AND Vehicle_Sno = $Vehicle_Sno"

# Update car location
UPDATE_CAR_LOCATION = "UPDATE CAR"
UPDATE_CAR_LOCATION += " SET Location_Name = $Location_Name"
UPDATE_CAR_LOCATION += " WHERE Model = $Model AND Vehicle_Sno = $Vehicle_Sno"


## Maintenance Request ##

# Location dropdown
LOCATION_DROPDOWN = "SELECT Location_Name"
LOCATION_DROPDOWN += " FROM LOCATION"

# Car dropdown by model
CAR_DROPDOWN_BY_MODEL = "SELECT Model, Vehicle_Sno"
CAR_DROPDOWN_BY_MODEL += " FROM CAR"
CAR_DROPDOWN_BY_MODEL += " WHERE Location_Name = $Location_Name"

# Put car under maintenance
PUT_UNDER_MAINTENANCE = "UPDATE CAR"
PUT_UNDER_MAINTENANCE += " SET Under_Maintenance = 1"
PUT_UNDER_MAINTENANCE += " WHERE Model = $Model AND Vehicle_Sno = $Vehicle_Sno"

# For each problem; Employee $Username
INSERT_MAINTENANCE_REQUEST = "INSERT INTO MAINTENANCE_REQUEST (Vehicle_Sno, Request_Date_Time, Username)"
INSERT_MAINTENANCE_REQUEST += " VALUES ($Vehicle_Sno, Current_Date, $Username)"

# For each problem
INSERT_MAINTENANCE_PROBLEM = "INSERT INTO MAINTENANCE_PROBLEMS (Vehicle_Sno, Request_Date_Time, Username, Problems)"
INSERT_MAINTENANCE_PROBLEM += " VALUES ($Vehicle_Sno, Current_Date, $Username, $Problems)"


## Rental Request Change ##

# Show current reservation of late user
LATE_USER_CURRENT_RESERVATION = "SELECT r.PickUp_Time, r.PickUp_Date, r.Return_Time, r.Return_Date, c.Model, c.Location_Name, c.Vehicle_Sno"
LATE_USER_CURRENT_RESERVATION += " FROM RESERVATION AS r"
LATE_USER_CURRENT_RESERVATION += " INNER JOIN CAR AS c"
LATE_USER_CURRENT_RESERVATION += " ON r.Vehicle_Sno = c.Vehicle_Sno"
LATE_USER_CURRENT_RESERVATION += " INNER JOIN STUDENT_FACULTY AS u" 
LATE_USER_CURRENT_RESERVATION += " ON r.Username = u.Username"
LATE_USER_CURRENT_RESERVATION += " WHERE u.Username = $Username" 
LATE_USER_CURRENT_RESERVATION += " AND Return_Status = 0"
LATE_USER_CURRENT_RESERVATION += " AND CURRENT_TIMESTAMP BETWEEN TIMESTAMP(PickUp_Date,PickUp_Time) AND TIMESTAMP(Return_Date,Return_Time)"

# If this query produces any rows, then a user is affected; $Username of the late user
AFFECTED_USER_CHECK = "SELECT r.Username, r.PickUp_Time, r.PickUp_Date, r.Return_Time, r.Return_Date, s.Email, s.Phone_Number"
AFFECTED_USER_CHECK += " FROM RESERVATION AS r"
AFFECTED_USER_CHECK += " INNER JOIN STUDENT_FACULTY AS s" 
AFFECTED_USER_CHECK += " ON r.Username = s.Username" 
AFFECTED_USER_CHECK += " WHERE r.Vehicle_Sno = $Vehicle_Sno" 
AFFECTED_USER_CHECK += " AND r.Username <> $Username"
AFFECTED_USER_CHECK += " AND TIMESTAMP(r.PickUp_Date, r.PickUp_Time) < TIMESTAMP($New_Arrival_Date, $New_Arrival _Time)"
AFFECTED_USER_CHECK += " AND Return_Status = 0"

# If no user is affected, then no late fee is charged; $Username of the late user
EXTEND_NO_AFFECTED_USER = "INSERT INTO RESERVATION_EXTENDED_TIME (PickUp_Date, PickUp_Time, Return_Date, Return_Time, Extended_Time, Username)"
EXTEND_NO_AFFECTED_USER += " VALUES ($PickUp_Date, $PickUp_Time, $Return_Date, $Return_Time,"
EXTEND_NO_AFFECTED_USER += " $Extended_Time, $Username)"

# If there is an affected user; $Username of the late user
AFFECTED_USER_LATE_FEES = "UPDATE RESERVATION"
AFFECTED_USER_LATE_FEES += " SET Late_Fees = 50 * TIMESTAMPDIFF(hour, TIMESTAMP($Return_Date, $Return_Time), TIMESTAMP($New_Arrival_Date, $New_Arrival _Time)), Late_By = TIMESTAMP($New_Arrival_Date, $New_Arrival _Time))"
AFFECTED_USER_LATE_FEES += " WHERE Vehicle_Sno = $Vehicle_Sno" 
AFFECTED_USER_LATE_FEES += " AND Username = $Username" 
AFFECTED_USER_LATE_FEES += " AND Return_Status = 0"
AFFECTED_USER_LATE_FEES += " AND Pickup_Date=$Pickup_Date" 
AFFECTED_USER_LATE_FEES += " AND Pickup_Time = $Pickup_Time" 
AFFECTED_USER_LATE_FEES += " AND Return_Date = $Return_Date" 
AFFECTED_USER_LATE_FEES += " AND Return_Time = $Return_Time"

# Give option to affected user to pick new reservation – Re-run the “Car Availability” queries from above

# If the user choses to cancel
CANCEL_RESERVATION = "DELETE FROM RESERVATION"
CANCEL_RESERVATION += " WHERE Username = $Username" 
CANCEL_RESERVATION += " AND Return_Date = $Return_Date" 
CANCEL_RESERVATION += " AND Return_Time = $Return_Time" 
CANCEL_RESERVATION += " AND PickUp_Time = $PickUp_Time" 
CANCEL_RESERVATION += " AND PickUp_Date = $PickUp_Date"
CANCEL_RESERVATION += " AND Return_Status = 0"


## Revenue Generated Report ##
REVENUE_GENERATED_REPORT = "SELECT r.Vehicle_Sno, c.Type, c.Model, SUM(r.Estimated_Cost) AS Reservation_Revenue, SUM(r.Late_Fees) AS Late_Fees_Revenue"
REVENUE_GENERATED_REPORT += " FROM RESERVATION AS r" 
REVENUE_GENERATED_REPORT += " INNER JOIN CAR AS c" 
REVENUE_GENERATED_REPORT += " ON r.Vehicle_Sno = c.Vehicle_Sno"
REVENUE_GENERATED_REPORT += " WHERE PERIOD_DIFF(EXTRACT(YEAR_MONTH FROM Current_Date), EXTRACT(YEAR_MONTH FROM r.PickUp_Date)) <= 3"
REVENUE_GENERATED_REPORT += " GROUP BY r.Vehicle_Sno"


## Maintenance History Report ##
MAINTENANCE_HISTORY_REPORT = "SELECT bb.Model AS Car, DATE_FORMAT(bb.Request_Date_Time,'%m/%d/%Y %h:%i %p') AS Date_Time, bb.Username AS EMPLOYEE, bb.Problems AS Problem"
MAINTENANCE_HISTORY_REPORT += " FROM"
MAINTENANCE_HISTORY_REPORT += " (SELECT b.Model, a.Request_Date_Time, a.Problems, COUNT(a.Problems) AS numOfProblems"
MAINTENANCE_HISTORY_REPORT += " FROM MAINTENANCE_PROBLEMS AS a"
MAINTENANCE_HISTORY_REPORT += " INNER JOIN CAR AS b" 
MAINTENANCE_HISTORY_REPORT += " ON a.Vehicle_Sno = b.Vehicle_Sno" 
MAINTENANCE_HISTORY_REPORT += " GROUP BY b.Model) AS aa" 
MAINTENANCE_HISTORY_REPORT += " INNER JOIN" 
MAINTENANCE_HISTORY_REPORT += " (SELECT b.Model, a.Request_Date_Time, a.Problems, a.Username" 
MAINTENANCE_HISTORY_REPORT += " FROM MAINTENANCE_PROBLEMS AS a" 
MAINTENANCE_HISTORY_REPORT += " INNER JOIN CAR AS b" 
MAINTENANCE_HISTORY_REPORT += " ON a.Vehicle_Sno = b.Vehicle_Sno) AS bb"
MAINTENANCE_HISTORY_REPORT += " ON bb.Model = aa.Model"
MAINTENANCE_HISTORY_REPORT += " ORDER BY aa.numOfProblems DESC"


## Location Preference Report ##
LOCATION_PREFERENCE_REPORT = "SELECT MONTHNAME(PickUp_Date) AS Month, r.Location_Name, COUNT(r.Location_Name) AS No_of_Reservations," 
LOCATION_PREFERENCE_REPORT += " SUM((TIMESTAMPDIFF(hour, TIMESTAMP(r.Pickup_Date, r.Pickup_Time), TIMESTAMP(r.Return_Date, r.Return_Time))))"
LOCATION_PREFERENCE_REPORT += " AS Total_No_of_Hours"
LOCATION_PREFERENCE_REPORT += " FROM RESERVATION AS r" 
LOCATION_PREFERENCE_REPORT += " INNER JOIN LOCATION AS l"
LOCATION_PREFERENCE_REPORT += " ON (l.Location_Name = r.Location_Name)"	
LOCATION_PREFERENCE_REPORT += " WHERE PERIOD_DIFF(EXTRACT(YEAR_MONTH FROM Current_Date), EXTRACT(YEAR_MONTH FROM r.PickUp_Date)) BETWEEN 0 AND 3"
LOCATION_PREFERENCE_REPORT += " GROUP BY r.Location_Name, MONTHNAME(PickUp_Date)"
LOCATION_PREFERENCE_REPORT += " ORDER BY EXTRACT(YEAR_MONTH FROM r.PickUp_Date) DESC"


## Frequent Users Report ##
FREQUENT_USERS_REPORT = "SELECT r.Username, s.Plan_Type, FLOOR(COUNT(r.Username)/3)"
FREQUENT_USERS_REPORT += " AS No_of_Reservations_Per_Month"
FREQUENT_USERS_REPORT += " FROM STUDENT_FACULTY AS s"
FREQUENT_USERS_REPORT += " INNER JOIN RESERVATION AS r"
FREQUENT_USERS_REPORT += " ON r.Username = s.Username"
FREQUENT_USERS_REPORT += " WHERE PERIOD_DIFF(EXTRACT(YEAR_MONTH FROM Current_Date), EXTRACT(YEAR_MONTH FROM r.PickUp_Date)) <= 3"
FREQUENT_USERS_REPORT += " GROUP BY r.Username" 
FREQUENT_USERS_REPORT += " ORDER BY No_of_Reservations_Per_Month DESC LIMIT 5"
