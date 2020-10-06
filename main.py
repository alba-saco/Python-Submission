# IMPORT LIBRARIES
import pickle
import pandas as pd
import datetime

#LOAD PICKLED FILES
unpickle_users = open("users.pickle", 'rb')
users = pickle.load(unpickle_users)
unpickle_patients = open("patient_info.pickle", 'rb')
patient_info = pickle.load(unpickle_patients)
unpickle_availability = open("gp_availability.pickle", 'rb')
gp_availability = pickle.load(unpickle_availability)
unpickle_bookings = open("bookings.pickle", 'rb')
bookings = pickle.load(unpickle_bookings)
unpickle_activity = open("gp_active.pickle", 'rb')
gp_active = pickle.load(unpickle_activity)
unpickle_prescriptions = open("prescriptions.pickle", 'rb')
prescriptions = pickle.load(unpickle_prescriptions)
unpickle_inquiries = open("inquiries.pickle", 'rb')
inquiries = pickle.load(unpickle_inquiries)
unpickle_responses = open("responses.pickle", 'rb')
responses = pickle.load(unpickle_responses)
unpickle_booked = open("booked.pickle", 'rb')
booked_patients = pickle.load(unpickle_booked)

# begin with cleared credentials
username = ''
pw = ''
def login():
	logged_in = False
	# loop until credentials are correct
	while logged_in == False:
		global username
		global pw
		username = input('Enter username: ')
		username = username.upper()
		pw = input('Enter password: ')
		try:
			# if username exists
			if users[username]:
				# if password in database matches entered password
				if users[username]['password'] == pw:
					print('Login successful')
					logged_in = True
					return logged_in, username, pw
				else:
					print('Password incorrect')
		# exception handling for no username matching entered username
		except KeyError:
			cont = input('No such username exists\nPress 1 to reenter\nPress any other key to cancel\n')
			if cont == '1':
				pass
			else:
				logged_in = True

# Add GP function
def add_GP():
	username_valid = False
	fname_GP = input('Enter GP\'s first name: ')
	lname_GP = input('Enter GP\'s last name: ')
	lname_GP = lname_GP.upper()
	# loop until chosen username can be used
	while username_valid == False:
		username_GP = input('Choose a username for GP: ')
		username_GP = username_GP.upper()
		try:
			# if username exists
			if users[username_GP]:
				confirm = input('Username already exists\nPress 1 to choose another username\nPress any other key to cancel\n')
				if confirm == '1':
					pass
				else:
					username_valid = True
		# if no username exists, continue creating account
		except KeyError:
			username_valid = True
			password_confirm = False
			# loop until 'password' and 'confirm password' inputs match
			while password_confirm == False:
				password_GP = input('Provide a password for this account: ')
				password_GP_confirm = input('Confirm password: ')
				# if password and confirm password match
				if password_GP == password_GP_confirm:
					password_confirm = True
				# if password and confirm password inputs don't match
				else:
					print('Passwords do not match')
			confirm = input('Create account for Dr. %s?\nPress 1 to confirm\nPress any other key to cancel\n' % lname_GP)
			# if account creation is confirmed, submit details
			if confirm == '1':
				users[username_GP] = {'fname' : fname_GP, 'lname' : lname_GP, 'password' : password_GP, 'role' : 'GP'}
				gp_active[lname_GP] = 'yes'
				print('Account created successfully')
				pickling_user = open('users.pickle', 'wb')
				pickle.dump(users, pickling_user)
				pickling_user.close()
				pickling_activity = open('gp_active.pickle', 'wb')
				pickle.dump(gp_active, pickling_activity)
				pickling_activity.close()

# Sign up function
def signup():
	username_valid = False
	name_patient = input('Enter your full name: ')
	name_patient = name_patient.upper()
	# loop until chosen username can be used
	while username_valid == False:
		global username
		username = input('Choose a username: ')
		username = username.upper()
		try:
			# if username alreay exists
			if users[username]:
				print('Username already exists')
		# if username doesn't exist, continue sign up process
		except KeyError:
			username_valid = True
			password_confirm = False
			# loop until 'password' and 'confirm password' inputs match
			while password_confirm == False:
				password_patient = input('Provide a password for this account: ')
				password_patient_confirm = input('Confirm password: ')
				# if password and confirm inputs match
				if password_patient == password_patient_confirm:
					password_confirm = True
				# if password and confirm inputs don't match
				else:
					print('Passwords do not match')
			dob = input('Enter your date of birth: ')
			sex = input('Enter your sex: ')
			blood_group = input('Enter your blood group: ')
			problem = input('Describe your problem: ')
			address = input('Enter your address in one line: ')
			phone_no = input('Enter your phone number: ')
			history = input('Enter any pre-existing medical conditions or any important medical history: ')
			valid_gp = False
			repeat = True
			cancel = False
			# loop until entered GP name exists in hospital database
			while valid_gp == False:
				gp = input('Enter your GP\'s surname: ')
				gp = gp.upper()
				# loop to find inputted GP name in GP database
				for lname, active in gp_active.items():
					# if inputted name matches name in database
					if lname == gp:
						# if GP has not been deactivated
						if active == 'yes':
							valid_gp = True
							repeat = False
							break
				# if repeat is true, then for loop finished without finding a match
				if repeat == True:
					action = input('GP last name entered not valid\nPress 1 to reenter\nPress 2 to view GP list\nPress any other key to cancel\n')
					# go back to start of while loop
					if action == '1':
						pass
					# view gp list
					elif action == '2':
						gp_list = []
						# loop through GPs in database
						for lname, active in gp_active.items():
							# add to list if GP not deactivated
							if active == 'yes':
								gp_list.append(lname.upper())
						pd_gps = pd.Series(gp_list)
						print(pd_gps)
					# else, cancel and exit loop
					else:
						valid_gp = True
						cancel = True
			# if action not cancelled, submit details
			if cancel == False:
				users[username] = {'name' : name_patient, 'password' : password_patient, 'role' : 'patient'}
				patient_info[username] = {'name' : name_patient, 'dob' : dob, 'sex' : sex, 'blood_group' : blood_group, 'problem' : problem, 'address' : address, 'phone_no' : phone_no, 'gp' : gp, 'history' : history}
				print('Patient successfully added to system')
				pickling_patient = open('patient_info.pickle', 'wb')
				pickle.dump(patient_info, pickling_patient)
				pickling_patient.close()
				pickling_user = open('users.pickle', 'wb')
				pickle.dump(users, pickling_user)
				pickling_user.close()

# Delete GP function
def delete_GP():
	deleted = False
	cancel = False
	# loop until GP name entered exists
	while deleted == False:
		GP_delete = input('Enter the username of the GP you\'d like to remove from system: ')
		GP_delete = GP_delete.upper()
		try:
			# if gp username exists, exit loop
			if users[GP_delete]:
				deleted = True
		# if inputted username doesnt exist
		except KeyError:
			wrong_user = input('No user exists under this username\nPress 1 to reenter\nPress any other key to cancel\n')
			# go to next loop iteration
			if wrong_user == '1':
				pass
			# else, cancel and exit loop
			else:
				deleted = True
				cancel = True
	last_name = users[GP_delete]['lname']
	delete_confirm = input('Are you sure you want to delete Dr. %s\'s profile?\nPress 1 for yes\nPress any other key for cancel\n' % last_name.upper())
	# if action confirmed, continue
	if delete_confirm == '1':
		del users[GP_delete]
		del gp_active[last_name]
		try:
			del gp_availability[last_name]
		# if there was no availability created for GP, pass
		except KeyError:
			pass
		print('GP deleted successfully')
		pickling_user = open('users.pickle', 'wb')
		pickle.dump(users, pickling_user)
		pickling_user.close()

# Add availability function
def add_availability():

	# function to add availability for range of dates
	def date_range(first_date, last_date, time_start, time_end, lname):
		date = first_date
		while date <= last_date:
			time_range(time_start, time_end, date, lname)
			date += datetime.timedelta(days = 1)

	# function to add availability for range of times
	def time_range(time_start, time_end, date, lname):
		time = time_start
		try:
			times = gp_availability[lname][date]
		# if there is no GP availability under given date
		except KeyError:
			try:
				gp_availability[lname][date] = []
				times = gp_availability[lname][date]
			# if there is no GP availability under inputted GP name
			except KeyError:
				gp_availability[lname] = {date : []}
				times = gp_availability[lname][date]
		try:
			booking_times = bookings[lname][date].keys()
		# if there are no bookings for inputted date
		except KeyError:
			booking_times = []
		# loop until time reaches end time in inputted range
		while time <= time_end:
			# if time already set of available times, go to next iteration
			if time in times:
				time += datetime.timedelta(hours = 1)
			# if there is a booking at this time, go to next iteration
			elif time in booking_times:
				time += datetime.timedelta(hours = 1)
			# else, check if time can be added
			else:
				dont_add = False
				# loop through pre-existing availabilities
				for slot in times:
					# if the difference between pre-existing availability and current time in loop is under an hour, don't add
					if abs(time - slot) < datetime.timedelta(hours = 1):
						dont_add = True
						break
				# if loop iterates through all existing available times and there are no clashes, add time to set of availabilities
				if dont_add == False:
					times.append(time)
				time += datetime.timedelta(hours = 1)
		gp_availability[lname][date] = times

	def add_by_day(lname):
		valid_date = False
		# loop until date entered can be used
		while valid_date == False:
			date_str = input('Enter the date you want to enter your availability for (dd/mm/yyyy): ')
			try:
				date = datetime.datetime.strptime(date_str, '%d/%m/%Y')
				# if date is after current date
				if date >= datetime.datetime.today():
					valid_date = True
				# else, next loop iteration
				else:
					print('Dates from before current date not permitted')
			# next loop iteration if date no entered in specified format
			except ValueError:
				print('Please enter date in specified format')
		time_or_range = input('Press 1 to enter a time\nPress 2 to enter a range of times\nPress any other key to cancel\n')
		# enter availability for specific time
		if time_or_range == '1':
			cancel = False
			valid_time = False
			# loop until entered time can be used
			while valid_time == False:
				add_time_str = input('Enter the time you want to enter your availability for (military time): ')
				try:
					add_time = datetime.datetime.strptime(add_time_str, '%H:%M')
				# next loop iteration if time not in specified format
				except ValueError:
					print('Please enter time in specified format (hh:00)')
				try:
					# if there is a booking for inputted time
					if bookings[lname][date][add_time]:
						booked = input('You are already booked for this time\nPress 1 to enter another time\nPress any other key to cancel\n')
						# next loop iteration
						if booked == '1':
							continue
						# else, cancel and exit loop
						else:
							valid_time = True
							cancel = True
				# if no booking at given time, continue
				except KeyError:
					pass
				try:
					# if other availabilities exist on given date
					if gp_availability[lname][date]:
						reenter = False
						# loop through available times on date
						for time in gp_availability[lname][date]:
							# if inputted time already exists in set of available times
							if time == add_time:
								action = input('Already have availability at this time\nPress 1 to enter another time\nPress any other key to cancel\n')
								# go to next loop iteration
								if action == '1':
									reenter = True
								# else, cancel and exit loop
								else:
									cancel = True
							# if there is a difference of less than an hour between inputted time and an existing availability
							elif abs(time - add_time) < datetime.timedelta(hours = 1):
								action = input('You must allow 1 hour between availability slots\nPress 1 to reenter time\nPress 2 to view availability on this day\nPress any other key to cancel\n')
								# next loop iteration
								if action == '1':
									reenter = True
								# view availabilities for given date
								elif action == '2':
									view_availability(lname, date)
									action = input('Press 1 to reenter time\nPress any other key to cancel\n')
									# next loop iteration
									if action != '1':
										cancel = True
									# else, cancel and exit loop
									else:
										reenter = True
								# else, cancel and exit loop
								else:
									cancel = True
								break
						# if entered time passes all constraints, exit loop
						if reenter == False:
							valid_time = True
				# if no other availabilites exist on given date, exit loop (no concern for clashes)
				except KeyError:
					valid_time = True
			# if action not cancelled
			if cancel == False:
				confirm = input('Add availability for Dr. %s on %s at %s?\nPress 1 to confirm\nPress any other key to cancel\n' % (lname, date_str, add_time_str))
				# if action confirmed
				if confirm == '1':
					try:
						# if there are already availabilities on given date
						if gp_availability[lname][date]:
							time = gp_availability[lname][date]
							time.append(add_time)
							gp_availability[lname][date] = time
						# if date key exists but set of availabilities is empty
						elif gp_availability[lname][date] == [] or gp_availability[lname][date] == None:
							gp_availability[lname][date] = [add_time]
					# if there are no availabilities existing on date
					except KeyError:
						try:
							# if there is a key for GP already created
							if gp_availability[lname] or gp_availability[lname] == {}:
								gp_availability[lname][date] = [add_time]
						# if there is no key for GP already created, create it
						except KeyError:
							gp_availability[lname] = {date : [add_time]}
					print('Availability added successfully')

		# enter range of times chosen
		elif time_or_range == '2':
			print('NOTE: Times are added in intervals of one hour from start time. If there is a slot which clashes with this the slot will be kept and only availabilities that do not clash will be added from the start count')
			time_input = False
			cancel = False
			# loop until time input can be submitted
			while time_input == False:
				time_start_str = input('Enter the first time in the range: ')
				try:
					time_start = datetime.datetime.strptime(time_start_str, '%H:%M')
					try:
						# if there are already availabilities on given date
						if gp_availability[lname][date]:
							reenter = False
							# loop through existing availability times
							for time in gp_availability[lname][date]:
								# if there is a difference of less than an hour between inputted range start time and an existing availability slot, start time is invalid
								if abs(time - time_start) < datetime.timedelta(hours = 1):
									action = input('You must allow 1 hour between availability slots\nPress 1 to reenter time\nPress 2 to view availability on this day\nPress any other key to cancel\n')
									# next loop iteration
									if action == '1':
										reenter = True
									# view availabilities for given date
									elif action == '2':
										view_availability(lname, date)
										action = input('Press 1 to reenter time\nPress any other key to cancel\n')
										# next loop iteration
										if action != '1':
											cancel = True
										# else, cancel and exit loop
										else:
											time_input = True
											reenter = True
									# else, cancel and exit loop
									else:
										time_input = True
										cancel = True
									break
							# if start time failed to meet criteria, next loop iteration
							if reenter == True:
								continue
					# if no existing availabilities on given date, continue
					except KeyError:
						pass
					time_end_str = input('Enter the last time in the range: ')
					time_end = datetime.datetime.strptime(time_end_str, '%H:%M')
					# if start time is after end time
					if time_start > time_end:
						print('Start time must be before end time')
					# if difference between start time and end time is less than an hour
					elif time_end - time_start < datetime.timedelta(hours = 1):
						print('You must allow 1 hour between availability slots')
					# if all criteria met, exit loop
					else:
						time_input = True
				# exception handling for time entered in incorrect format
				except ValueError:
					wrong_time = input('Please enter time in specified format (hh:00)\nPress 1 to reenter\nPress any other key to cancel\n')
					# next loop iteration
					if wrong_time == '1':
						continue
					# else, cancel and exit loop
					else:
						time_input = True
						cancel = True
			# if action not cancelled
			if cancel == False:
				confirm = input('Add availability for Dr. %s on %s from %s to %s?\nPress 1 to confirm\nPress any other key to cancel\n' % (lname, date_str, time_start_str, time_end_str))
				# if action confirmed, continue
				if confirm == '1':
					pass
				# else, cancel and exit loop
				else:
					cancel = True
				# if action not cancelled, perform function to add availability for range of times
				if cancel == False:
					time_range(time_start, time_end, date, lname)
					print('Availability added successfully')

	def add_by_date_range(lname):
		date_input = False
		cancel = False
		# loop until date inputs are valid
		while date_input == False:
			first = input('Enter the first day in range (dd/mm/yyyy): ')
			last = input('Enter the last day in range (dd/mm/yyyy): ')
			try:
				first_date = datetime.datetime.strptime(first, '%d/%m/%Y')
				last_date = datetime.datetime.strptime(last, '%d/%m/%Y')
				# if date in start of range is after current date, continue
				if first_date >= datetime.datetime.today():
					pass
				# else, next loop iteration
				else:
					print('Dates from before current date not permitted')
					continue
			# exception handling for date entered in incorrect format
			except ValueError:
				wrong_date = input('Please enter date in specified format\nPress 1 to reenter\nPress any other key to cancel\n')
				# next loop iteration
				if wrong_date == '1':
					continue
				# else, cancel and exit loop
				else:
					date_input = True
					cancel = True
			# if start date is before end date, all criteria is met, exit loop
			if first_date < last_date:
				date_input = True
			# else, next loop iteration
			else:
				print('Start date must be before end date')
		# if action not cancelled
		if cancel == False:
			time_range_choice = input('Press 1 to add availability from 9-5\nPress 2 to enter custom time range\nPress any other key to cancel\n')
			# add 9-5 availability
			if time_range_choice == '1':
				time_start = datetime.datetime.strptime('9:00', '%H:%M')
				time_end = datetime.datetime.strptime('16:00', '%H:%M')
				confirm = input('Add availability for Dr. %s on days %s to %s for first bookings at 9:00 and last bookings at 16:00?\nPress 1 to confirm\nPress any other key to cancel\n' % (lname, first, last))
				# if action confirmed
				if confirm == '1':
					date_range(first_date, last_date, time_start, time_end, lname)
					print('Availability added successfully')
			# custom time range
			elif time_range_choice == '2':
				print('NOTE: Times are added in intervals of one hour from start time. If there is a slot which clashes with this the slot will be kept and only availabilities that do not clash will be added from the start count')
				time_input = False
				cancel = False
				# loop until valid time input is entered
				while time_input == False:
					time_start_str = input('Enter the first time in the range: ')
					time_end_str = input('Enter the last time in the range: ')
					try:
						time_start = datetime.datetime.strptime(time_start_str, '%H:%M')
						time_end = datetime.datetime.strptime(time_end_str, '%H:%M')
					# exception handling for time entered in incorrect format
					except ValueError:
						wrong_time = input('Please enter time in specified format (hh:00)\nPress 1 to reenter\nPress any other key to cancel\n')
						# next loop iteration
						if wrong_time == '1':
							continue
						# else, cancel and exit loop
						else:
							time_input = True
							cancel = True
					# if range start time is before range end time, all conditions met, exit loop
					if time_start < time_end:
						time_input = True
					# else, next loop iteration
					else:
						print('Start time must be before end time')
				# if action not cancelled
				if cancel == False:
					confirm = input('Add availability for %s on days %s to %s for first bookings at %s and last bookings at %s?\nPress 1 to confirm\nPress any other key to cancel\n' % (lname.upper(), first, last, time_start_str, time_end_str))
					# if action confirmed
					if confirm == '1':
						date_range(first_date, last_date, time_start, time_end, lname)
						print('Availability added successfully')
	
	# main add availability function
	lname = users[username]['lname']
	print('NOTE: Appointment durations are 1 hour.')
	date_or_range = input('Press 1 to enter a date\nPress 2 to enter a range of dates\nPress any other key to cancel\n')
	# Enter availability for one specific day
	if date_or_range == '1':
		add_by_day(lname)

	# choice to add availability for range of dates
	elif date_or_range == '2':
		add_by_date_range(lname)

	#save data
	pickling_availability = open('gp_availability.pickle', 'wb')
	pickle.dump(gp_availability, pickling_availability)
	pickling_availability.close()

# Add booking function
def add_booking():
	gp = patient_info[username]['gp']
	rebook = '1'
	try:
		# if patient already has booking
		if booked_patients[username]:
				booked_date = booked_patients[username]['date']
				booked_time = booked_patients[username]['time']
		# if booking date hasn't passed yet
		if booked_date > datetime.datetime.today():
			day = booked_date.strftime('%d')
			month = booked_date.strftime('%m')
			year = booked_date.strftime('%Y')
			hour = booked_time.strftime('%H')
			rebook = input('You already have a booking on %s/%s/%s at %s:00\nPress 1 to rebook\nPress any other key to cancel\n' % (day, month, year, hour))
			# if rebook chosen, delete current booking
			if rebook == '1':
				delete_booking_single(gp, booked_date, booked_time, username)
		# if booking date already passed, continue
		else:
			pass
	# if patient has no booking, continue
	except KeyError:
		pass
	# if action not cancelled
	if rebook == '1':
		date_choice = False
		cancel = False
		available_dates = []
		# loop through dates GP has availability for
		for key in gp_availability[gp]:
			formatted_date = key.strftime('%d/%m/%Y')
			if key > datetime.datetime.today():
				available_dates.append(formatted_date)
		pd_dates = pd.Series(available_dates)
		print('Available dates:')
		print(pd_dates)
		# loop until valid date is chosen
		while date_choice == False:	
			date_str = input('Choose a date for your booking (dd/mm/yyyy): ')
			try:	
				date = datetime.datetime.strptime(date_str, '%d/%m/%Y')
				availability_time = gp_availability[gp][date]
				date_choice = True
			# if there is no availability on inputted date
			except KeyError:
				cont_choose = input('GP has no availability on this day\nPress 1 to enter another day\nPress any other key to cancel\n')
				# next loop iteration
				if cont_choose == '1':
					pass
				# cancel and exit loop
				else:
					cancel = True
					date_choice = True
			# exception handling for incorrect date format
			except ValueError:
				cont_choose = input('Please enter date in specified format\nPress 1 to reenter\nPress any other key to cancel\n')
				# next loop iteration
				if cont_choose == '1':
					pass
				# cancel and exit loop
				else:
					cancel = True
					date_choice = True
		# if action not cancelled
		if cancel == False:
			valid_time = False
			cancel_2 = False
			print('Available times:')
			view_availability(gp, date)
			# loop until time choice is valid
			while valid_time == False:
				time_str = input('Choose a time for your booking (military time): ')
				time = datetime.datetime.strptime(time_str, '%H:%M')
				try:
					availability_time.remove(time)
					valid_time = True
				# if inputted time is not in set of GP availability times
				except ValueError:
					cont_choose = input('GP has no availability at this time\nPress 1 to enter another time\nPress any other key to cancel\n')
					# next loop iteration
					if cont_choose == '1':
						pass
					# cancel and exit loop
					else:
						valid_time = True
						cancel_2 = True
			# if action not cancelled
			if cancel_2 == False:
				confirm = input('Add booking on %s at %s?\nPress 1 to confirm\nPress any other key to cancel\n' % (date_str, time_str))
				try:
					bookings[gp][date][time] = username
					booked_patients[username] = {'date' : date, 'time' : time}
				# if date key has not yet been created
				except KeyError:
					try:
						bookings[gp][date] = {time : username}
						booked_patients[username] = {'date' : date, 'time' : time}
					# if GP key has not yet been created
					except KeyError:
						bookings[gp] = {date : {time : username}}
						booked_patients[username] = {'date' : date, 'time' : time}
				# save data
				gp_availability[gp][date] = availability_time
				pickling_bookings = open('bookings.pickle', 'wb')
				pickle.dump(bookings, pickling_bookings)
				pickling_bookings.close()
				pickling_availability = open('gp_availability.pickle', 'wb')
				pickle.dump(gp_availability, pickling_availability)
				pickling_availability.close()
				pickling_booked = open('booked.pickle', 'wb')
				pickle.dump(booked_patients, pickling_booked)
				pickling_booked.close()
				print('Booking created successfully')

# Delete booking function
def delete_booking():
	gp_valid = False
	cancel = False
	gp_patient_choice = False
	# loop until user chooses to delete either by GP or by patient
	while gp_patient_choice == False:
		gp_or_patient = input('Press 1 to search by GP\nPress 2 to search by patient\n')
		# delete by GP
		if gp_or_patient == '1':
			gp_patient_choice = True
			# loop until GP name entered is valid
			while gp_valid == False:
				gp = input('Enter the GP\'s surname who\'s booking you wish to delete: ')
				gp = gp.upper()
				try:
					# if there are bookings under gp name
					if bookings[gp]:
						gp_valid = True
					# if gp key is created but there are no bookings
					elif bookings[gp] == {}:
						no_name = input('No bookings under this name\nPress 1 to reenter\nPress any other key to cancel\n')
						# next loop iteration
						if no_name == '1':
							pass
						# cancel and exit loop
						else:
							gp_valid = True
							cancel = True
				# if there are no bookings under gp name
				except KeyError:
					no_name = input('No bookings under this name\nPress 1 to reenter\nPress any other key to cancel\n')
					# next iteration
					if no_name == '1':
						pass
					# cancel and exit loop
					else:
						gp_valid = True
						cancel = True
			# if action not cancelled
			if cancel == False:
				date_choice = False
				cancel_date = False
				# loop until date chosen is valid
				while date_choice == False:
					try:
						date_str = input('Enter the booking date (dd/mm/yyyy): ')	
						date = datetime.datetime.strptime(date_str, '%d/%m/%Y')
						# if there are bookings under given date, exit loop
						if bookings[gp][date]:
							date_choice = True
						# if date key is created but there are no bookings
						elif bookings[gp][date] == {}:
							cancel_date_choice = input('No bookings for this date\nPress 1 to enter another date\nPress any other key to cancel\n')
							# next iteration
							if cancel_date_choice == '1':
								pass
							# cancel and exit loop
							else:
								date_choice = True
								cancel_date = True
					# if there are no bookings for inputted date
					except KeyError:
						cancel_date_choice = input('No bookings for this date\nPress 1 to enter another date\nPress any other key to cancel\n')
						# next iteration
						if cancel_date_choice == '1':
							pass
						# cancel and exit loop
						else:
							date_choice = True
							cancel_date = True
					# exception handling for incorrect input date formatting
					except ValueError:
						cancel_date_choice = input('Please enter date in the specified format\nPress 1 to reenter\nPress any other key to cancel\n')
						# next iteration
						if cancel_date_choice == '1':
							pass
						# cancel and exit loop
						else:
							date_choice = True
							cancel_date = True
				# if action not cancelled
				if cancel_date == False:
					valid_choice = False
					choose = ''
					# loop until a valid action option is chosen
					while valid_choice == False:
						# if user already chose to view bookings, don't have the option come up to view again
						if choose == '4':
							choose = input('Press 1 to enter a time\nPress 2 to clear whole day\nPress 3 to clear range of times\nPress any other key to cancel\n')
							# if user randomly inputs 4 (view booking), make it a different key to cancel
							if choose == '4':
								choose = '5'
						# if view bookings hadn't been chosen
						else:
							choose = input('Press 1 to enter a time\nPress 2 to clear whole day\nPress 3 to clear range of times\nPress 4 to view booking times on this day\nPress any other key to cancel\n')
						# valid action choice, exit loop
						if choose == '1' or choose == '2' or choose == '3':
							valid_choice = True
						# show booking times and go to next iteration
						elif choose == '4':
							view_bookings(gp, date)
						# cancel, exit loop
						else:
							valid_choice = True
					# enter a time is chosen
					if choose == '1':
						time_choice = False
						cancel_time = False
						# loop until time choice is valid
						while time_choice == False:
							time_str = input('Enter the booking time (military time): ')
							try:
								time = datetime.datetime.strptime(time_str, '%H:%M')
								# if booking exists under inputted time, exit loop
								if bookings[gp][date][time]:
									time_choice = True
							# if there is no booking at inputted time
							except KeyError:
								cancel_time_choice = input('No booking at this time\nPress 1 to enter another time\nPress any other key to cancel\n')
								# next loop iteration
								if cancel_time_choice == '1':
									pass
								# cancel and exit loop
								else:
									cancel_time = True
									time_choice = True
							# exception handling for time entered in incorrect format
							except ValueError:
								cancel_time_choice = input('Please enter time in specified format (hh:00)\nPress 1 to enter another time\nPress any other key to cancel\n')
								# next loop iteration
								if cancel_time_choice == '1':
									pass
								# cancel and exit loop
								else:
									cancel_time = True
									time_choice = True
						# if action not cancelled
						if cancel_time == False:
							patient = bookings[gp][date][time]
							patient_name = patient_info[patient]['name']
							confirm = input('Are you sure you want to delete booking for patient %s with Dr. %s on %s at %s?\nPress 1 for yes\nPress any other key to cancel\n' % (patient_name, gp, date_str, time_str))
							# if action confirmed, delete booking
							if confirm == '1':
								delete_booking_single(gp, date, time, patient)
								print('Booking(s) deleted successfully')
							# no action
							else:
								pass
					# choice to clear whole day
					elif choose == '2':
						confirm = input('Are you sure you want to delete all bookings with Dr. %s on %s?\nPress 1 to continue\nPress any other key to cancel\n' % (gp, date_str))
						# if action confirmed, clear day
						if confirm == '1':
							add_time = gp_availability[gp][date]
							day = bookings[gp][date]
							times = []
							booking_count = 0
							# loop through each booking for the day
							for key, value in day.items():
								add_time.append(key)
								del booked_patients[value]
								booking_count += 1
							del bookings[gp][date]
							gp_availability[gp][date] = add_time
							print('%d booking(s) deleted successfully' % booking_count)
						# no action
						else:
							pass
					# if clear for time range is chosen
					elif choose == '3':
						time_input = False
						cancel = False
						# loop intil valid time input is enterd
						while time_input == False:
							time_start_str = input('Enter the first time in the range: ')
							time_end_str = input('Enter the last time in the range (will delete up to and not including this time): ')
							try:
								time_start = datetime.datetime.strptime(time_start_str, '%H:%M')
								time_end = datetime.datetime.strptime(time_end_str, '%H:%M')
							# exception handling for time entered incorrectly
							except ValueError:
								wrong_time = input('Please enter time in specified format (hh:00)\nPress 1 to reenter\nPress any other key to cancel\n')
								# next loop iteration
								if wrong_time == '1':
									continue
								# cancel and exit loop
								else:
									time_input = True
									cancel = True
							# if range start time is before range end time, all conditions met, exit loop
							if time_start < time_end:
								time_input = True
							# else, next loop iteration
							else:
								print('Start time must be before end time')
						# if action not cancelled
						if cancel == False:
							confirm = input('Are you sure you want to clear all bookings with %s from %s to %s on %s?\nPress 1 for yes\nPress any other key to cancel\n' % (gp, time_start_str, time_end_str, date_str))
							# if action confirmed, clear bookings in range
							if confirm == '1':
								time = time_start
								times = gp_availability[gp][date]
								booking_times = bookings[gp][date]
								booking_count = 0
								# loop until time reached range end time
								while time < time_end:
									try:
										patient = bookings[gp][date][time]
										del bookings[gp][date][time]
										del booked_patients[patient]
										times.append(time)
										time += datetime.timedelta(hours = 1)
										booking_count += 1
									# if no booking at given time, next loop iteration
									except KeyError:
										time += datetime.timedelta(hours = 1)
								gp_availability[gp][date] = times
								print('%d booking(s) deleted successfully' % booking_count)
							# no action
							else:
								pass
		# choice to delete booking by patient
		elif gp_or_patient == '2':
			gp_patient_choice = True
			patient_name = False
			# loop until valid patient name is entered
			while patient_name == False:
				patient = input('Enter the patients\'s username who\'s booking you wish to delete: ')
				patient = patient.upper()
				try:
					# if patient name in system, exit loop
					if patient_info[patient]:
						patient_name = True
				# if patient name not in system
				except KeyError:
					no_name = input('Patient username doesn\'t exist\nPress 1 to reenter\nPress any other key to cancel\n')
					# next loop iteration
					if no_name == '1':
						pass
					# cancel and exit loop
					else:
						patient_name = True
						cancel = True
			# if action not cancelled, delete booking by patient function
			if cancel == False:
				delete_booking_by_patient(patient)
		# else, next loop iteration to choose between search by gp or patient
		else:
			print('Please enter a valid option')
		# save data
		pickling_bookings = open('bookings.pickle', 'wb')
		pickle.dump(bookings, pickling_bookings)
		pickling_bookings.close()
		pickling_availability = open('gp_availability.pickle', 'wb')
		pickle.dump(gp_availability, pickling_availability)
		pickling_availability.close()
		pickling_booked = open('booked.pickle', 'wb')
		pickle.dump(booked_patients, pickling_booked)
		pickling_booked.close()

# Deactivate GP function
def deactivate_GP():
	surname_valid = False
	# loop until entered name is valid
	while surname_valid == False:
		gp = input('Enter the GP\'s surname who\'s profile you wish to deactivate: ')
		gp = gp.upper()
		try:
			# if gp name exists in database
			if gp_active[gp]:
				confirm = input('Are you sure you want to deactivate %s\'s profile?\nPress 1 for yes\nPress any other key for no\n' % gp)
				# if action confirmed
				if confirm == '1':
					gp_active[gp] = 'no'
					pickling_activity = open('gp_active.pickle', 'wb')
					pickle.dump(gp_active, pickling_activity)
					pickling_activity.close()
					print('GP account successfully deactivated')
				surname_valid = True
		# if gp name not in system
		except KeyError:
			print('Surname entered not valid. Please try again: ')

# Delete availability function
def delete_availability(gp):
		date_or_range_choice = False
		# loop until delete by day or range of days option is chosen
		while date_or_range_choice == False:
			day_or_range = input('Press 1 to enter a date\nPress 2 to clear range of dates\n')
			# delete by date
			if day_or_range == '1':
				date_or_range_choice = True
				valid_date = False
				date_cancel = False
				# loop until valid date input is entered
				while valid_date == False:
					try:
						date_str = input('Enter the date (dd/mm/yyyy): ')
						date = datetime.datetime.strptime(date_str, '%d/%m/%Y')
						# if there is availability on that day, exit loop
						if gp_availability[gp][date]:
							valid_date = True
						# if date key has been created but is empty
						elif gp_availability[gp][date] == []:
							no_date = input('No availability on this date\nPress 1 to enter another date\nPress any other key to cancel\n')
							# next loop iteration
							if no_date == '1':
								pass
							# cancel and exit loop
							else:
								valid_date = True
								date_cancel = True
					# if no availability on given day
					except KeyError:
						no_date = input('No availability on this date\nPress 1 to enter another date\nPress any other key to cancel\n')
						# next loop iteration
						if no_date == '1':
							pass
						# cancel and exit loop
						else:
							valid_date = True
							date_cancel = True
					# exception handling for incorrect date format
					except ValueError:
						print('Please enter date in specified format')

				# if action not cancelled
				if date_cancel == False:
					valid_choice = False
					choose = ''
					# loop until action choice is valid
					while valid_choice == False:
						# if user chose to view availabilities, don't have view availability option come up again
						if choose == '4':
							choose = input('Press 1 to enter a time\nPress 2 to clear whole day\nPress 3 to clear range of times\nPress any other key to cancel\n')
							# if user inputs 4 to cancel, change input to 5 so availabilities don't show again
							if choose == '4':
								choose = '5'
						# if no action chosen yet, normal option choice message
						else:
							choose = input('Press 1 to enter a time\nPress 2 to clear whole day\nPress 3 to clear range of times\nPress 4 to view availability on this day\nPress any other key to cancel\n')
						# if user chooses an action
						if choose == '1' or choose == '2' or choose == '3':
							valid_choice = True
						# if user chooses view availability
						elif choose == '4':
							view_availability(gp, date)
						# if user chooses to cancel
						else:
							valid_choice = True
					# enter time choice
					if choose == '1':
						time_input = False
						# loop until a valid time input is chosen
						while time_input == False:
							try:
								time_str = input('Enter the time (military time): ')
								time = datetime.datetime.strptime(time_str, '%H:%M')
							# exception handling for time not entered correctly
							except ValueError:
								print('Please enter time in specified format')
							# if no error, continue
							else:
								# if entered time in set of availabilities for the date
								if time in gp_availability[gp][date]:
									time_input = True
									confirm = input('Are you sure you want to delete %s\'s availability on %s at %s?\nPress 1 to confirm\nPress any other key to cancel\n' % (gp, date_str, time_str))
									# if action confirmed
									if confirm == '1':
										deleted_time = gp_availability[gp][date]
										deleted_time.remove(time)
										gp_availability[gp][date] = deleted_time
										print('Availability deleted successfully')
									# else, no action
									else:
										pass
								# if entered time not in set of available times
								else:
									time_cancel = input('No availability at this time\nPress 1 to reenter\nPress 2 to view availability on this day\nPress any other key to cancel\n')
									# next loop iteration
									if time_cancel == '1':
										pass
									# view availabilities, then next loop iteration
									elif time_cancel == '2':
										view_availability(gp, date)
									# cancel and exit loop
									else:
										time_input = True
					# clear whole day option
					elif choose == '2':
						confirm = input('Are you sure you want to delete all of %s\'s availability on %s?\nPress 1 to continue\nPress any other key to cancel\n' % (gp, date_str))
						# if action confirmed
						if confirm == '1':
							del gp_availability[gp][date]
							print('Availability deleted successfully')
						# else, no action
						else:
							pass
					# if clear time range option chosen
					elif choose == '3':
						time_input = False
						cancel = False
						# loop until entered times are valid
						while time_input == False:
							time_start_str = input('Enter the first time in the range: ')
							time_end_str = input('Enter the last time in the range (will delete up to and not including this time): ')
							try:
								time_start = datetime.datetime.strptime(time_start_str, '%H:%M')
								time_end = datetime.datetime.strptime(time_end_str, '%H:%M')
							# exception handling for times entered incorrectly
							except ValueError:
								wrong_time = input('Please enter time in correct format (hh:00)\nPress 1 to reenter\nPress any other key to cancel\n')
								# next loop iteration
								if wrong_time == '1':
									continue
								# cancel and exit loop
								else:
									time_input = True
									cancel = True
							# if range start time is before range end time, all criteria met, exit loop
							if time_start < time_end:
								time_input = True
							# else, next loop iteration
							else:
								print('Start time must be before end time')
						# if action not cancelled
						if cancel == False:
							confirm = input('Are you sure you want to clear %s\'s availability from %s to %s on %s?\nPress 1 for yes\nPress any other key to cancel\n' % (gp, time_start_str, time_end_str, date_str))
							# if action confirmed
							if confirm == '1':
								time = time_start
								times = gp_availability[gp][date]
								# loop until time reaches range end time
								while time < time_end:
										try:
											times.remove(time)
											time += datetime.timedelta(hours = 1)
										# if current time not in set of available times, next loop iteration
										except ValueError:
											time += datetime.timedelta(hours = 1)
								gp_availability[gp][date] = times
								print('Availability deleted successfully')
							# if action not confirmed, no action
							else:
								pass
			# range of dates choice
			elif day_or_range == '2':
				date_or_range_choice = True
				date_input = False
				cancel = False
				# loop until entered date is valid
				while date_input == False:
					try:
						first = input('Enter the first day in range (dd/mm/yyyy): ')
						last = input('Enter the last day in range (dd/mm/yyyy): ')
						first_date = datetime.datetime.strptime(first, '%d/%m/%Y')
						last_date = datetime.datetime.strptime(last, '%d/%m/%Y')
					# exception handling for date entered incorrectly
					except ValueError:
						wrong_date = input('Please enter date in correct format\nPress 1 to reenter\nPress any other key to cancel\n')
						# next loop iteration
						if wrong_date == '1':
							continue
						# cancel and exit loop
						else:
							date_input = True
							cancel = True
					# if range start date is before range end date, criteria met, exit loop
					if first_date < last_date:
						date_input = True
					# else, next loop iteration
					else:
						print('Start date must be before last date')
				# if action not cancelled
				if cancel == False:
					confirm = input('Are you sure you want to clear %s\'s availability from %s to %s?\nPress 1 to confirm\nPress any other key to cancel\n' % (gp, first, last))
					# if action confirmed
					if confirm == '1':
						date = first_date
						# loop until date reaches range end date
						while date <= last_date:
							try:
								del gp_availability[gp][date]
								date += datetime.timedelta(days = 1)
							# if no availability on current date, next loop iteration
							except KeyError:
								date += datetime.timedelta(days = 1)
						print('Availability deleted successfully')
					# if action not confirmed, no action
					else:
						pass
			# next loop iteration if neither date nor range of dates options are chosen
			else:
				print('Please choose a valid option')
		# save data
		pickling_availability = open('gp_availability.pickle', 'wb')
		pickle.dump(gp_availability, pickling_availability)
		pickling_availability.close()

# view list of GPs function
def view_GPs():
	gp_list = []
	# loop through users list
	for value in users.values():
		# if user role is gp
		if value['role'] == 'GP':
			try:
				gp_list.append(value['lname'])
			# exception handling for some mistake in system
			except KeyError:
				pass
	pd_gps = pd.Series(gp_list)
	print(pd_gps)

# view gp availability on given date
def view_availability(GP, date):
	times = gp_availability[GP][date]
	formatted_times = []
	# loop through available times on given date
	for time in times:
		try:
			hour = time.strftime('%H:%M')
			formatted_times.append(hour)
		# exception handling for error in system
		except AttributeError:
			pass
	pd_availability = pd.Series(formatted_times)
	print(pd_availability.sort_values())

# view booking for a gp on given date
def view_bookings(GP, date):
	day_bookings = bookings[GP][date].items()
	formatted_bookings = {}
	for time, patient in day_bookings:
		hour = time.strftime('%H:%M')
		formatted_bookings[hour] = patient_info[patient]['name']
	pd_bookings = pd.Series(formatted_bookings)
	print(pd_bookings.sort_index())

# input prescriptions for patient function
def input_prescription():
	valid_patient = False
	repeat = True
	cancel = False
	another_prescription = True
	gp = users[username]['lname']
	# loop until patient name entered is valid
	while valid_patient == False:
		patient = input('Input patient full name: ')
		patient = patient.upper()
		# loop through users in system
		for patient_username, user in users.items():
			try:
				# if user is a patient and their name matches input
				if user['name'] == patient and user['role'] == 'patient':
					# if patient's registered gp is the gp currently logged in
					if patient_info[patient_username]['gp'] == gp:
						valid_patient = True
						repeat = False
						break
			# exception handling to complete loop if any error in system
			except KeyError:
				pass
		# if loop completed with no match found
		if repeat == True:
			action = input('No patient registered under this name for Dr. %s\nPress 1 to reenter\nPress 2 to view patient list\nPress any other key to cancel\n' % users[username]['lname'].upper())
			# next while loop iteration
			if action == '1':
				pass
			# view patient list for current gp logged in
			elif action == '2':
				view_patients(gp)
			# cancel and exit loop
			else:
				valid_patient = True
				cancel = True
	# if action not cancelled
	if cancel == False:
		# loop so gp can easily input multiple prescriptions in a row
		while another_prescription == True:
			med = input('Input the product name: ')
			try:
				# if patient has already been prescribed medication
				if prescriptions[patient][med]:
					action = input('Patient already prescribed this medicine\nPress 1 to update prescription instructions\nPress 2 to view prescription instructions for this product\nPress any other key to cancel\n')
					# update medication instructions (continue)
					if action == '1':
						pass
					# view current medication instructions
					elif action == '2':
						print(prescriptions[patient][med])
						action = input('Press 1 to update prescription instructions\nPress any other key to cancel\n')
						# update medation instructions (continue)
						if action == '1':
							pass
						# cancel and exit loop
						else:
							cancel = True
							another_prescription = False
					# cancel and exit loop
					else:
						cancel = True
						another_prescription = False
			# if patient has not already been prescribed medication, continue
			except KeyError:
				pass
			# if action not cancelled
			if cancel == False:
				instr = input('Input the usage instructions: ')
				confirm = input('Confirm prescription for %s: %s, %s\nPress 1 to confirm\nPress any other key to cancel\n' % (patient, med, instr))
				# if action confirmed
				if confirm == '1':
					try:
						prescriptions[patient][med] = instr
					# if no key for patient does not exist yet
					except KeyError:
						prescriptions[patient] = {med : instr}
					another = input('Prescription added successfully\nPress 1 to add another prescription for this patient\nPress any other key to finish\n')
					# if gp is done inputting prescriptions
					if another != '1':
						another_prescription = False
				# if action not confirmed, no action and exit loop
				else:
					another_prescription = False
	# save data
	pickling_prescriptions = open('prescriptions.pickle', 'wb')
	pickle.dump(prescriptions, pickling_prescriptions)
	pickling_prescriptions.close()

# view patients for current gp logged in
def view_patients(gp):
	patient_list = []
	# loop through patient list
	for patient in patient_info.values():
		try:
			# if patient's registered gp is current logged in gp
			if patient['gp'] == users[username]['lname']:
				patient_list.append(patient['name'])
		# exception handling for error in system
		except KeyError:
			pass
	pd_patients = pd.Series(patient_list)
	print(pd_patients)

def make_inquiry():
	patient = patient_info[username]['name']
	gp = patient_info[username]['gp']
	cancel = False
	try:
		# if patient has already submitted an inquiry
		if inquiries[gp][patient]:
			action = input('You\'ve already submitted an inquiry with the message: \'%s\', only one inquiry is permitted at a time, would you like to overwrite this?\nPress 1 to overwrite\nPress any other key to cancel\n' % inquiries[gp][patient])
			# update inquiry (continue)
			if action == '1':
				pass
			# cancel
			else:
				cancel = True
	# if patient has not yet submitted inquiry, continue
	except KeyError:
		pass
	# if action not cancelled
	if cancel == False:
		inquiry = input('Type your inquiry here: ')
		confirm = input('Submit inquiry with message: \'%s\' to GP?\nPress 1 to confirm\nPress any other key to cancel\n' % inquiry)
		# if action confirmed
		if confirm == '1':
			try:
				inquiries[gp][patient] = inquiry
			# if no patient key exists yet
			except KeyError:
				inquiries[gp] = {patient : inquiry}
			print('Inquiry submitted successfully')
			# save data
			pickling_inquiries = open('inquiries.pickle', 'wb')
			pickle.dump(inquiries, pickling_inquiries)
			pickling_inquiries.close()

# respond to inquiries function
def respond_inquiries():
	try:
		# loop until gp has no inquiries left to respond to
		while inquiries[gp] != {}:
			pd_inquiries = pd.Series(inquiries[gp])
			print(pd_inquiries)
			action = input('Press 1 to respond\nPress any other key to exit\n')
			# if gp chooses to respond to inquiries
			if action == '1':
				patient_valid = False
				# loop until entered patient name is valid
				while patient_valid == False:
					patient = input('Type the name of the patient who\'s inquiry you\'d like to respond to: ')
					patient = patient.upper()
					try:
						# if patient has an inquiry
						if inquiries[gp][patient]:
							patient_valid = True
							response = input('Type your response: ')
							confirm = input('Submit reponse?\nPress 1 to confirm\nPress any other key to cancel\n')
							# if action confirmed
							if confirm == '1':
								responses[patient] = {inquiries[gp][patient] : response}
								del inquiries[gp][patient]
								print('Response submitted successfully')
					# if no inquiry registered under inputted name
					except KeyError:
						action = input('Please type the patient name correctly\nPress 1 to reenter\nPress any other key to cancel\n')
						# next loop iteration
						if action == '1':
							pass
						# cancel and exit loop
						else:
							patient_valid = True
	# if gp has no inquiries
	except KeyError:
		print('No inquiries to respond to')
	# save data
	pickling_inquiries = open('inquiries.pickle', 'wb')
	pickle.dump(inquiries, pickling_inquiries)
	pickling_inquiries.close()
	pickling_responses = open('responses.pickle', 'wb')
	pickle.dump(responses, pickling_responses)
	pickling_responses.close()

def delete_booking_single(gp, date, time, patient):
	add_time = gp_availability[gp][date]
	# if booking being deleted is not in current set of available times for date
	if time not in add_time:
		add_time.append(time)
	try:
		del bookings[gp][date][time]
		gp_availability[gp][date] = add_time
	# exception handling for error in system
	except KeyError:
		pass
	del booked_patients[patient]

def delete_booking_by_patient(patient):
	gp = patient_info[patient]['gp']
	name = patient_info[patient]['name']
	gp_bookings = bookings[gp]
	booked_date = booked_patients[patient]['date']
	booked_time = booked_patients[patient]['time']
	day = booked_date.strftime('%d')
	month = booked_date.strftime('%m')
	year = booked_date.strftime('%Y')
	hour = booked_time.strftime('%H')
	confirm = input('Are you sure you want to delete booking for %s with DR.%s on %s/%s/%s at %s:00?\nPress 1 to confirm\nPress any other key to cancel\n' % (name, gp, day, month, year, hour))
	# if action confirmed
	if confirm == '1':
		delete_booking_single(gp, booked_date, booked_time, patient)
		print('Booking deleted successfully')
	# save data
	pickling_bookings = open('bookings.pickle', 'wb')
	pickle.dump(bookings, pickling_bookings)
	pickling_bookings.close()
	pickling_availability = open('gp_availability.pickle', 'wb')
	pickle.dump(gp_availability, pickling_availability)
	pickling_availability.close()
	pickling_booked = open('booked.pickle', 'wb')
	pickle.dump(booked_patients, pickling_booked)
	pickling_booked.close()

# view GP's response to patient inquiry
def view_responses():
	try:
		name = patient_info[username]['name']
		response = responses[name]
		pd_response = pd.Series(response)
		print(pd_response)
	# if no response for patient
	except KeyError:
		print('Not received a reponse to inquiry')

# re-activate gp profile
def reactivate_gp():
	surname_valid = False
	# loop until a valid name is entered
	while surname_valid == False:
		gp = input('Enter the GP\'s surname who\'s profile you wish to re-activate: ')
		gp = gp.upper()
		try:
			# if entered name exist in gp dataset
			if gp_active[gp]:
				surname_valid = True
				# if gp is deactivated
				if gp_active[gp] == 'no':
					confirm = input('Re-activate %s\'s profile?\nPress 1 for yes\nPress any other key for no\n' % gp)
					# confirm action
					if confirm == '1':
						gp_active[gp] = 'yes'
						# save data
						pickling_activity = open('gp_active.pickle', 'wb')
						pickle.dump(gp_active, pickling_activity)
						pickling_activity.close()
						print('GP account successfully re-activated')
				# if gp account is active
				else:
					print('GP account already active')
		# if entered name not in gp database
		except KeyError:
			print('Surname entered not valid. Please try again: ')

# view all patients in database function
def view_all_patients():
	patient_list = {}
	# loop through patients in patient list
	for patient in patient_info.values():
		patient_list[patient['name']] = patient['gp']
	pd_patients = pd.Series(patient_list)
	print(pd_patients)

# view patient's booking date and time
def view_patient_booking(patient):
	booked_date = booked_patients[patient]['date']
	booked_time = booked_patients[patient]['time']
	formatted_date = booked_date.strftime('%d/%m/%Y')
	fomatted_time = booked_time.strftime('%H:%M')
	booking = {formatted_date : fomatted_time}
	pd_booking = pd.Series(booking)
	print(pd_booking)

# view patient's medical details
def patient_details(gp):
	print('Patient list: ')
	view_patients(gp)
	valid_name = False
	reenter = True
	cancel = False
	# loop until valid patient name is entered
	while valid_name == False:
		patient_name = input('Enter patient name you wish to view details for: ')
		patient_name = patient_name.upper()
		# loop though patient list
		for key, patient in patient_info.items():
			# if a name matched inputted patient name and their registered gp is current logged in gp
			if patient['name'] == patient_name and patient['gp'] == gp:
				valid_name = True
				reenter = False
				patient_username = key
				break
		# if loop finishes and no match is found
		if reenter == True:
			action = input('No patient under entered name registered for Dr. %s\nPress 1 to reenter\nPress any other key to cancel\n' % gp)
			# next while loop iteration
			if action == '1':
				pass
			# cancel and exit while loop
			else:
				valid_name = True
				cancel = True
	# if action not cancelled
	if cancel == False:
		dob = patient_info[patient_username]['dob']
		sex = patient_info[patient_username]['sex']
		blood_group = patient_info[patient_username]['blood_group']
		problem = patient_info[patient_username]['problem']
		history = patient_info[patient_username]['history']
		patient_summary = {'D.O.B.' : dob, 'SEX' : sex, 'BLOOD GROUP' : blood_group, 'PROBLEM' : problem, 'HISTORY' : history}
		pd_summary = pd.Series(patient_summary)
		print(pd_summary)

# view prescriptions function
def view_prescriptions():
	patient_name = patient_info[username]['name']
	pd_prescriptions = pd.Series(prescriptions[patient_name])
	print(pd_prescriptions)

# Main
terminate = False
login_needed = True
initial_action = ''
# loop until user chooses to end program
while terminate == False:
	# if no initial action has been chosen yet
	if initial_action == '':
		initial_action = input('What would you like to do?\nPress 1 for: Login\nPress 2 for: Sign up as a new patient\nPress any other key to terminate\n')
	# if login action chosen
	if initial_action == '1':
		if login_needed == True:
			login()
		#Admin capabilities
		try:
			# if logged in user is an admin
			if users[username]['role'] == 'admin':
				login_needed = False
				cancel = False
				# loop until user logs out or ends program
				while cancel == False: 
					action = input("What would you like to do?\nType 1 for: Add new GP\nType 2 for: Delete GP profile\nType 3 for: Delete booking(s)\nType 4 for: Deactivate GP profile\nType 5 for: Delete GP availability\nType 6 for: View list of GPs\nType 7 for: View list of patients\nType 8 for: View GP availability\nType 9 for: View bookings\nType 10 for: Re-activate GP profile\nType 11 to log out\nPress any other key to terminate\n")
					# add gp
					if action == '1':
						add_GP()
					# delete gp
					elif action == '2':
						delete_GP()
					# delete booking
					elif action == '3':
						delete_booking()
					# deactivate gp profile
					elif action == '4':
						deactivate_GP()
					# delete gp availability
					elif action == '5':
						gp_valid = False
						cancel = False
						# loop until entered gp name is valid
						while gp_valid == False:
							gp = input('Enter the surname of the GP who\'s availability you wish to delete: ')
							gp = gp.upper()
							try:
								# if there is availability under entered gp name
								if gp_availability[gp]:
									gp_valid = True
								# if gp key exists in availability but set of availabilities is empty
								elif gp_availability[gp] == {}:
									no_name = input('No bookings under this name\nPress 1 to reenter\nPress any other key to cancel\n')
									# next loop iteration
									if no_name == '1':
										pass
									# cancel and exit loop
									else:
										gp_valid = True
										cancel = True
							# if there is no availabilities under inputted name
							except KeyError:
								no_name = input('No bookings under this name\nPress 1 to reenter\nPress any other key to cancel\n')
								# next loop iteration
								if no_name == '1':
									pass
								# cancel and exit loop
								else:
									gp_valid = True
									cancel = True
						# if action not cancelled
						if cancel == False:
							delete_availability(gp)
					# view list of gps
					elif action == '6':
						view_GPs()
					# view list of patients and their corresponding gp
					elif action == '7':
						view_all_patients()
					# view gp availability
					elif action == '8':
						valid_GP = False
						valid_date = False
						cancel = False
						# loop until a valid gp name is entered
						while valid_GP == False:
							GP = input('Enter the last name of the GP who\'s availability you wish to see: ')
							GP = GP.upper()
							try:
								# if there is availability under name
								if gp_availability[GP]:
									valid_GP = True
							# if there is no availability under name
							except KeyError:
								no_name = input('No availability under this name\nPress 1 to reenter\nPress any other key to cancel\n')
								# next loop iteration
								if no_name == '1':
									pass
								# cancel and exit loop
								else:
									valid_GP = True
									cancel = True
						# loop until valid date is entered
						while valid_date == False:
							date_str = input('Enter the date you wish to see availability for (dd/mm/yyyy): ')
							try:
								date = datetime.datetime.strptime(date_str, '%d/%m/%Y')
								# if there is availability under entered date
								if gp_availability[GP][date]:
									valid_date = True
								# if date key exists but set of times is empty
								elif gp_availability[GP][date] == []:
									no_date = input('No availability on this date\nPress 1 to enter another date\nPress any other key to cancel\n')
									# next loop iteration
									if no_date == '1':
										pass
									# cancel and exit loop
									else:
										valid_date = True
										cancel = True
							# if there is no availability under entered date
							except KeyError:
								no_date = input('No availability on this date\nPress 1 to enter another date\nPress any other key to cancel\n')
								# next loop iteration
								if no_date == '1':
									pass
								# cancel and exit loop
								else:
									valid_date = True
									cancel = True
							# exception handling for incorrect input format
							except ValueError:
								print('Please enter date in specified format\n')
						# if action not cancelled
						if cancel == False:
							view_availability(GP, date)
					# view gp bookings
					elif action == '9':
						valid_GP = False
						valid_date = False
						cancel = False
						# loop until valid gp name is entered
						while valid_GP == False:
							GP = input('Enter the last name of the GP who\'s bookings you wish to see: ')
							GP = GP.upper()
							try:
								# if bookings exist under gp name
								if bookings[GP]:
									valid_GP = True
							# if no bookings exist under gp name
							except KeyError:
								no_name = input('No bookings under this name\nPress 1 to reenter\nPress any other key to cancel\n')
								# next loop iteration
								if no_name == '1':
									pass
								# cancel and exit loop
								else:
									valid_GP = True
									cancel = True
						# if action not cancelled
						if cancel == False:
							# loop until valid date is entered
							while valid_date == False:
								date_str = input('Enter the date you wish to see bookings for (dd/mm/yyyy): ')
								try:
									date = datetime.datetime.strptime(date_str, '%d/%m/%Y')
									# if bookings exist under entered date
									if bookings[GP][date]:
										valid_date = True
									# if date key exists but there are no bookings
									elif bookings[GP][date] == {}:
										no_date = input('No bookings on this date\nPress 1 to enter another date\nPress any other key to cancel\n')
										# next loop iteration
										if no_date == '1':
											pass
										# cancel and exit loop
										else:
											valid_date = True
											cancel = True
								# if there are no bookings under entered date
								except KeyError:
									no_date = input('No bookings on this date\nPress 1 to enter another date\nPress any other key to cancel\n')
									# next loop iteration
									if no_date == '1':
										pass
									# cancel and exit loop
									else:
										valid_date = True
										cancel = True
								# exception handling for incorrect input format
								except ValueError:
									print('Please enter date in specified format\n')
							# if action not cancelled
							if cancel == False:
								view_bookings(GP, date)
					# re-activate gp profile
					elif action == '10':
						reactivate_gp()
					# log out
					elif action == '11':
						cancel = True
						login_needed = True
						initial_action = ''
					# end program
					else:
						cancel = True
						terminate = True

			# if logged in user is a gp
			elif users[username]['role'] == 'GP':
				login_needed = False
				cancel = False
				gp = users[username]['lname']
				active = gp_active[gp]
				# if gp account is active
				if active == 'yes':
					# loop until user logs out or ends program
					while cancel == False:
						action = input('What would you like to do?\nPress 1 for: Add availability\nPress 2 for: Input patient prescriptions\nPress 3 for: View bookings\nPress 4 for: View patient list\nPress 5 for: View availability\nPress 6 for: View and respond to patient inquiries\nPress 7 for: Delete availability\nPress 8 for: Access patient medical details\nPress 9 to log out\nPress any other key to terminate\n')
						# add gp availability
						if action == '1':
							add_availability()
						# input prescription for patient
						elif action == '2':
							input_prescription()
						# view current bookings
						elif action == '3':
							valid_date = False
							cancel = False
							# loop until entered date is valid
							while valid_date == False:
								date_str = input('Enter the date you wish to see bookings for (dd/mm/yyyy): ')
								try:
									date = datetime.datetime.strptime(date_str, '%d/%m/%Y')
									# if bookings exist under date
									if bookings[gp][date]:
										valid_date = True
									# if date key exists but set of bookings is empty
									elif bookings[gp][date] == {}:
										no_date = input('No bookings on this date\nPress 1 to enter another date\nPress any other key to cancel\n')
										# next loop iteration
										if no_date == '1':
											pass
										# cancel and exit loop
										else:
											valid_date = True
											cancel = True
								# if no bookings under entered date
								except KeyError:
									no_date = input('No bookings on this date\nPress 1 to enter another date\nPress any other key to cancel\n')
									# next loop iteration
									if no_date == '1':
										pass
									# cancel and exit loop
									else:
										valid_date = True
										cancel = True
								# if date entered incorrectly
								except ValueError:
									print('Please enter date in specified format\n')
							# if action not cancelled
							if cancel == False:
								view_bookings(gp, date)
						# view names of patients registered under gp
						elif action == '4':
							view_patients(gp)
						# view gp availability
						elif action == '5':
							cancel = False
							valid_date = False
							# loop until entered date is valid
							while valid_date == False:
								date_str = input('Enter the date you wish to see availability for (dd/mm/yyyy): ')
								try:
									date = datetime.datetime.strptime(date_str, '%d/%m/%Y')
									# if availability exists under date
									if gp_availability[gp][date]:
										valid_date = True
									# if date key exists but set of available times is empty
									elif gp_availability[gp][date] == []:
										no_date = input('No availability on this date\nPress 1 to enter another date\nPress any other key to cancel\n')
										# next loop iteration
										if no_date == '1':
											pass
										# cancel and exit loop
										else:
											valid_date = True
											cancel = True
								# if no availability under entered date
								except KeyError:
									no_date = input('No availability on this date\nPress 1 to enter another date\nPress any other key to cancel\n')
									# next loop iteration
									if no_date == '1':
										pass
									# cancel and exit loop
									else:
										valid_date = True
										cancel = True
								# exception handling for incorrect input format
								except ValueError:
									print('Please enter date in specified format\n')
							# if action not cancelled
							if cancel == False:
								view_availability(gp, date)
						# respond to patient inquiries
						elif action == '6':
							respond_inquiries()
						# delete availability
						elif action == '7':
							delete_availability(gp)
						# view patient medical details
						elif action == '8':
							patient_details(gp)
						# log out
						elif action == '9':
							cancel = True
							login_needed = True
							initial_action = ''
						# end program
						else:
							cancel = True
							terminate = True
				# if gp account is deactivated
				else:
					print('GP account is deactivated. Capabilities cannot be accessed.')
					cancel = True
					login_needed = True
					initial_action = ''
			
			# if logged in user is a patient
			elif users[username]['role'] == 'patient':
				login_needed = False
				cancel = False
				# loop until user logs out or ends program
				while cancel == False:
					action = input('What would you like to do?\nPress 1 for: Make a booking\nPress 2 for: Make an inquiry to GP\nPress 3 for: Cancel booking\nPress 4 for: View inquiry responses\nPress 5 for: View booking\nPress 6 for: View prescriptions\nPress 7 to log out\nPress any other key to terminate\n')
					# make a booking
					if action == '1':
						add_booking()
					# make an inquiry to gp
					elif action == '2':
						make_inquiry()
					# delete current booking
					elif action == '3':
						delete_booking_by_patient(username)
					# view gp response to inquiry
					elif action == '4':
						view_responses()
					# view current booking
					elif action == '5':
						view_patient_booking(username)
					# view prescriptions
					elif action == '6':
						view_prescriptions()
					# log out
					elif action == '7':
						cancel = True
						login_needed = True
						initial_action = ''
					# end program
					else:
						terminate = True
						cancel = True
			# if user logs in but has no role associated (system error)
			else:
				initial_action = ''
				continue
		# system error handling
		except KeyError:
			initial_action = ''
			continue
	# sign up option
	elif initial_action =='2':
		signup()
		initial_action = '1'
		login_needed = False
	# end program
	else:
		terminate = True