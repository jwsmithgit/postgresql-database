#Jacob Smith
#V00700979

#1/usr/bin/python
import psycopg2
import sys

def start_menu():
	print "1: Select a pre-made database query"
	print "2: Add a campaign"
	print "3: Add a volunteer"
	print "4: Assign volunteer to campaign"
	print "5: View a campaign"
	print "6: View accounting information"
	print "7: View volunteer history"
	print "8: Add annotation to campaign"
	print "9: Add annotation to member record"
	print "10: Change members email address"
	print "0: Exit"
	print
	return

def query_menu():
	print "Please select a query: "
	print 
	print "1: What are the names of members that are also donors?"
	print "2: What are the causes of every campaign that has been put on the website?"
	print "3: What are the names of members that are also in other groups?"
	print "4: Which supporters supported cause has been or is going to be campaigned?"
	print "5: How much money is being sent to rent?"
	print "6: What equipment does GnG only have one of?"
	print "7: What members have participated at the most campaigns?"
	print "8: What are the last names of volunteers who have the first name 'tori' and tier is 1?"
	print "9: What is the cost of the most and least expensive campaign that has ended?"
	print "10: How many of each type of equipment does GnG have?"
	print "11: What funds have the same amount as the fund with id 6?"
	print "12: What is the current balance of GnG?"
	print
	return

def get_input_number_bound ( question, min_input, max_input ):
	need_input = True
	while need_input:
		try: 
			user_input = int( raw_input( "%s" %( question, )))
			need_input = False
		except ValueError:
			print "That is not a valid number"
			need_input = True
			continue
		if min_input <= user_input <= max_input:
			break
		else:
			print "Number entered is not in range"
			need_input = True
	print
	return user_input

def get_input_number ( question ):
	need_input = True
	while need_input:
		try: 
			user_input = int(raw_input( "%s" %( question, )))
			need_input = False
		except ValueError:
			print "That is not a valid number"
			need_input = True
			continue
	print
	return user_input

def get_input_string ( question ):
	need_input = True
	while need_input:
		try: 
			user_input = str(raw_input( "%s" %( question, )))
			need_input = False
		except ValueError:
			print "That is not a valid string"
			need_input = True
			continue
	print
	return user_input

def print_result ( result_cursor ):
	i = 0
	print "Result:"
	for row in result_cursor.fetchall():
		if i == 0:
			j = 0
			print "(",
			for attribute in row:
				if ( j != 0 ):
					print "\b, ",
				print "\b" + result_cursor.description[j].name,
				j += 1
			print "\b)"
		print row
		i += 1
	print
	return

def print_table ( cursor, table_name ):
	print "Result for table %s:" % ( table_name, )
	
	cursor.execute("""
	select * from %s;
	""" %( table_name, ))
	i = 0
	print "(",
	for attribute in cursor.fetchone():
		if ( i != 0 ):
			print "\b, ",
		print "\b" + cursor.description[i].name,
		i += 1
	print "\b)"
	
	
	cursor.execute("""
	select * from %s;
	""" %( table_name, ))
	for row in cursor.fetchall():
		print row
		#for attribute in row:
		#	print "%s" % ( attribute, ),
		#print
	print
	return

def view_queries( cursor ):
	query_menu()
	user_input = get_input_number_bound( "Enter a query number: ", 0, 12 )

	if user_input == 0:
		return
	 
	cursor.execute("""
	select * from "%s";
	""" %( str(user_input), ))

	print_result( cursor )
	return

def add_campaign( cursor ):
	try:
		#Get all the data for new campaign
		cursor.execute(""" select max(campaigns.id) from campaigns; """)
		for row in cursor.fetchall():
			for attribute in row:
				cid = 1 + int(row[0])
	except:
		print "connection error"
		sys.exit()
	location = get_input_string( "Where will the campaign be located? " )
	cause = get_input_string( "What is the cause of the campaign? " )
	start_year = get_input_number_bound( "What year does the campaign start? (2000-3000) ", 2000, 3000 )
	start_month = get_input_number_bound( "What month does the campaign start? (1-12) ", 1, 12 )
	if start_month == 2:
		start_day = get_input_number_bound( "What day does the campaign start? (1-28) ", 1, 28 )
	elif start_month == 4 or start_month == 6 or start_month == 9 or start_month == 11:
		start_day = get_input_number_bound( "What day does the campaign start? (1-30) ", 1, 30 )
	else:
		start_day = get_input_number_bound( "What day does the campaign start? (1-31) ", 1, 31 )
	duration = get_input_number_bound( "How many days will the campaign last? (14-60) ", 14, 60 )
	cost = get_input_number( "what is the cost of the campaign? " )
	phase = get_input_number_bound( "What is the current phase of the campaign? (1-3) ", 1, 3 )
	push_to_web_year = get_input_number_bound( "What year does the campaign get push to the web? (2000-3000) ", 2000, 3000 )
	push_to_web_month = get_input_number_bound( "What month does the campaign get pushed to the web? (1-12) ", 1, 12 )
	if push_to_web_month == 2:
		push_to_web_day = get_input_number_bound( "What day does the campaign get pushed to the web? (1-28) ", 1, 28 )
	elif push_to_web_month == 4 or push_to_web_month == 6 or push_to_web_month == 9 or push_to_web_month == 11:
		push_to_web_day = get_input_number_bound( "What day does the campaign get pushed to the web? (1-30) ", 1, 30 )
	else:
		push_to_web_day = get_input_number_bound( "What day does the campaign get pushed to the web? (1-31)  ", 1, 31 )
	
	cursor.execute("BEGIN")
	try:
		#Insert data into campaign table
		cursor.execute("""
		insert into campaigns( id, location, cause, start_date, duration, cost, phase, push_to_web ) values ( %d, '%s', '%s', to_date('%s', 'YYYY-MM-DD'), %d, '%s', %d, to_date( '%s', 'YYYY-MM-DD'));
		""" %( cid, location, cause, str(start_year)+'-'+str(start_month)+'-'+str(start_day), duration, \
			str(cost), phase, str(push_to_web_year)+'-'+str(push_to_web_month)+'-'+str(push_to_web_day), ))
	except:
		print "connection error"
		sys.exit()
		
	try:
		#Update funds
		cursor.execute(""" select max(funds.id) from funds; """)
		for row in cursor.fetchall():
			for attribute in row:
				fid = 1 + int(row[0])
	except:
		print "connection error"
		sys.exit()
	
	try:
		cursor.execute("""
		insert into funds( id, amount, flow ) values ( %d, '%s', 'out' );
		""" %( fid, str(cost), ) )
	except:
		print "connection error"
		sys.exit()

	try:
		#Update funds to campaign
		cursor.execute("""
		insert into funds_to_campaign( fund_id, campaign_id ) values ( %d, %d );
		""" %( fid, cid, ) )
	except:
		print "connection error"
		sys.exit()
	
	
	print_table ( cursor, "campaigns" )
	print_table ( cursor, "funds" )
	print_table ( cursor, "funds_to_campaign" )
	
	cursor.execute("COMMIT")
			
	return

def add_volunteer( cursor ):
	 #Get volunteer data
	first_name = get_input_string( "What is the volunteers first name? " )
	last_name = get_input_string( "What is the volunteers last name? " )
	email = get_input_string( "What is the volunteers email? " )
	campaign_num = get_input_number_bound( "How many campaigns has the volunteer participated at? (0+) ", 0, 999999999 )
	if campaign_num < 3:
		tier = 1
	else:
		tier = 2
	
	cursor.execute("BEGIN")
	try:
		#Insert into member table
		cursor.execute("""
		insert into members( email, first_name, last_name ) values ( '%s', '%s', '%s' );
		""" %( email, first_name, last_name, ) )
	except psycopg2.IntegrityError:
		print "That email address already exists!"
		print "Returning to main menu..."
		print
		return
	except:
		print "connection error"
		print
		sys.exit()
		
	try:
		#Insert into member table
		cursor.execute("""
		insert into volunteers( email, tier, number_of_campaigns) values ( '%s', %d, %d );
		""" %( email, tier, campaign_num, ) )
	except:
		print "connection error"
		sys.exit()
		
	
	print_table ( cursor, "members" )
	print_table ( cursor, "volunteers" )
	
	cursor.execute("COMMIT")
  
	return

def assign_volunteer( cursor ):
	try:
		#Get data
		cursor.execute(""" select max(campaigns.id) from campaigns; """)
		for row in cursor.fetchall():
			for attribute in row:
				cid_max = int(row[0])
	except:
		print "connection error"
		sys.exit()
	
	cid = get_input_number_bound( "What is the id of the campaign? (1-%d) " %(cid_max,), 1, cid_max )
	member_email = get_input_string( "What is the volunteers's email? " )
	
	try:
		cursor.execute("""
		select * from members,volunteers where members.email = '%s' and volunteers.email = '%s';
		""" %( member_email, member_email, ))
	except:
		print "connection error"
		sys.exit()
		
	i = 0
	for row in cursor.fetchall():
		i += 1
	
	if i == 0:
		print "A volunteer for that email does not exist!"
		print "Returning to main menu..."
		print
		return
	else:
		cursor.execute("BEGIN")
		try:
			#Update volunteering_at_campaign relation
			cursor.execute("""
			insert into volunteering_at_campaign( volunteer_email, campaign_id ) values ( '%s', %d );
			""" %( member_email, cid, ) )
		except psycopg2.IntegrityError:
			print "That volunteer has already been assigned to that campaign!"
			print "Returning to main menu..."
			print
			return
		except:
			print "connection error"
			sys.exit()
		
		try:
			#Insert into volunteer data
			cursor.execute("""
			select number_of_campaigns from volunteers where email = '%s';
			""" %( member_email, ))
		except:
			print "connection error"
			sys.exit()
		
		for row in cursor.fetchone():
			new_number = row + 1
		
		try:
			cursor.execute("""
			update volunteers set number_of_campaigns = %d where email = '%s';
			""" %( new_number, member_email))
		except:
			print "connection error"
			sys.exit()

		if new_number == 3:
			try:
				cursor.execute("""
				update volunteers set tier = 2;
				""")
			except:
				print "connection error"
				sys.exit()
		
		print_table ( cursor, "volunteering_at_campaign" )
		print_table ( cursor, "volunteers" )
		
		cursor.execute("COMMIT")
	
	return
	

def view_campaign( cursor ):
	#Get data
	try:
		cursor.execute(""" select max(campaigns.id) from campaigns; """)
		for row in cursor.fetchall():
			for attribute in row:
				cid_max = int(row[0])
	except:
		print "connection error"
		sys.exit()
			
	cid = get_input_number_bound( "What campaign do you want to view? (1-%d) " %(cid_max,), 1, cid_max )
	
	#Display campaign
	try:
		cursor.execute("""
		select * from campaigns where id = %d;
		""" %( cid, ))
	except:
		print "connection error"
		sys.exit()
		
	print_result(cursor)
	
	return

def view_accounting( cursor ):
	donor_outflow = 0
	campaign_outflow = 0
	total_inflow = 0
	rent_inflow = 0
	campaign_inflow = 0
	total_outflow = 0
	total_flow = 0
	
	# get money flow from funds table
	try:
		cursor.execute(""" select * from funds; """)
		for row in cursor.fetchall():
			money_string = row[1].replace(',','')
			money_string = money_string.replace('$','')
			money_string = money_string[:len(money_string)-3]
			if row[2] == "in":
				total_inflow += int(money_string)
				total_flow += int(money_string)
			else:
				total_outflow += int(money_string)
				total_flow -= int(money_string)
	except:
		print "connection error"
		sys.exit()
	
	# get money flow from donors
	try:
		cursor.execute(""" select amount from funds, donor_donation where funds.id = donor_donation.fund_id; """)
		for row in cursor.fetchall():
			money_string = row[0].replace(',','')
			money_string = money_string.replace('$','')
			money_string = money_string[:len(money_string)-3]
			donor_outflow += int(money_string)
	except:
		print "connection error"
		sys.exit()
	
	# get money flow from campaign
	try:
		cursor.execute(""" select amount from funds, campaign_to_funds where funds.id = campaign_to_funds.fund_id; """)
		for row in cursor.fetchall():
			money_string = row[0].replace(',','')
			money_string = money_string.replace('$','')
			money_string = money_string[:len(money_string)-3]
			campaign_outflow += int(money_string)
	except:
		print "connection error"
		sys.exit()
	
	# get money flow to rent
	try:
		cursor.execute(""" select amount from funds, funds_to_rent where funds.id = funds_to_rent.fund_id; """)
		for row in cursor.fetchall():
			money_string = row[0].replace(',','')
			money_string = money_string.replace('$','')
			money_string = money_string[:len(money_string)-3]
			rent_inflow += int(money_string)
	except:
		print "connection error"
		sys.exit()
		
	# get money flow to campaign
	try:
		cursor.execute(""" select amount from funds, funds_to_campaign where funds.id = funds_to_campaign.fund_id; """)
		for row in cursor.fetchall():
			money_string = row[0].replace(',','')
			money_string = money_string.replace('$','')
			money_string = money_string[:len(money_string)-3]
			campaign_inflow += int(money_string)
	except:
		print "connection error"
		sys.exit()
		
	i = 1000
	print "donor outflow: "
	while i < donor_outflow:
		print "+",
		i += 1000
	print 
	i = 1000
	print "campaign outflow: "
	while i < campaign_outflow:
		print "+",
		i += 1000
	print 
	i = 1000
	print "total inflow: "
	while i < total_inflow:
		print "+",
		i += 1000
	print 
	i = 1000
	print "rent inflow: "
	while i < rent_inflow:
		print "-",
		i += 1000
	print 
	i = 1000
	print "campaign inflow: "
	while i < campaign_inflow:
		print "-",
		i += 1000
	print 
	i = 1000
	print "total outflow: "
	while i < total_outflow:
		print "-",
		i += 1000
	print
	print "total balance: "
	if total_flow >= 0:
		i = 1000
		while i < total_flow:
			print "+",
			i += 1000
	else:
		i = -1000
		while i > total_flow:
			print "-",
			i -= 1000
	print
	print
	print "each symbol represents $1000.00"
	print "+ denotes revenue"
	print "- denotes expense"
	print
	
	return

def view_membership( cursor ):
  
	try:
		cursor.execute("""
		select email from volunteers;
		""" )
	except:
		print "connection error"
		sys.exit()
	print_result( cursor )
	
	#Get data
	member_email = get_input_string( "What is the email of the volunteer? " )
	
	try:
		cursor.execute("""
		select * from members,volunteers where members.email = '%s' and volunteers.email = '%s';
		""" %( member_email, member_email, ))
	except:
		print "connection error"
		sys.exit()
		
	i = 0
	for row in cursor.fetchall():
		i += 1
	
	if i == 0:
		print "A volunteer for that email does not exist!"
		print "Returning to main menu..."
		print
		return
	else:
		try:
			cursor.execute("""
			select members.email, first_name, last_name, tier, number_of_campaigns from members,volunteers where members.email = '%s' and volunteers.email = '%s';
			""" %( member_email, member_email, ))
		except:
			print "connection error"
			sys.exit()
		print_result(cursor)
		
		try:
			cursor.execute("""
			select * from volunteering_at_campaign where volunteer_email = '%s';
			""" %( member_email ))
		except:
			print "connection error"
			sys.exit()
		print_result(cursor)
	
	return

def annotate_campaign( cursor ):
	#Get data
	try:
		cursor.execute(""" select max(campaigns.id) from campaigns; """)
		for row in cursor.fetchall():
			for attribute in row:
				cid_max = int(row[0])
	except:
		print "connection error"
		sys.exit()
			
	cid = get_input_number_bound( "What campaign do you want to annotate? (1-%d) " %(cid_max,), 1, cid_max )
	annotation = get_input_string( "What would you like to annotate? " )
	
	cursor.execute("BEGIN")
	try:
		cursor.execute("""
		update campaigns set notes = '%s' where id = %d;
		""" %( annotation, cid, ))
	except:
		print "connection error"
		sys.exit()
		
	cursor.execute("COMMIT")
	
	print_table ( cursor, "campaigns" )
	
	return

def annotate_member( cursor ):
	try:
		cursor.execute("""
		select email from volunteers;
		""" )
	except:
		print "connection error"
		sys.exit()
	print_result( cursor )
	
	#Get data
	member_email = get_input_string( "What is the volunteer's email you want to annotate? " )
	annotation = get_input_string( "What would you like to annotate? " )
	
	try:
		cursor.execute("""
		select * from members,volunteers where members.email = '%s' and volunteers.email = '%s';
		""" %( member_email, member_email, ))
	except:
		print "connection error"
		sys.exit()
	i = 0
	for row in cursor.fetchall():
		i += 1
	
	if i == 0:
		print "A volunteer for that email does not exist!"
		print "Returning to main menu..."
		print
		return
	else:
		cursor.execute("BEGIN")
		try:
			cursor.execute("""
			update members set notes = '%s' where email = '%s';
			""" %( annotation, member_email, ))
		except:
			print "connection error"
			sys.exit()
		
		
		print_table ( cursor, "members" )
		
		cursor.execute("COMMIT")
	
	return

def mystery_function( cursor ):
	 
	try:
		cursor.execute("""
		select email from members;
		""" )
	except:
		print "connection error"
		sys.exit()
	print_result( cursor )
	
	#Get data
	member_email = get_input_string( "What is the members's email you want to change? " )
	new_email = get_input_string( "What would you like to change it to? " )
	
	try:
		cursor.execute("""
		select * from members where email = '%s';
		""" %( member_email,))
	except:
		print "connection error"
		sys.exit()
	i = 0
	for row in cursor.fetchall():
		i += 1
	
	if i == 0:
		print "A member with that email does not exist!"
		print "Returning to main menu..."
		print
		return
	else:
		  
		cursor.execute("BEGIN")
		#insert into members
		try:
			cursor.execute("""
			select * from members where email = '%s';
			""" %( member_email ))
		except:
			print "connection error"
			sys.exit()
		
		memory = cursor.fetchone()
		fname = memory[1]
		lname = memory[2]
		
		try:
			cursor.execute("""
			insert into members( email, first_name, last_name ) values ( '%s', '%s', '%s' ); 
			""" %( new_email, fname, lname, ))
		except psycopg2.IntegrityError:
			print "A member with that email already exists!"
			print "Returning to main menu..."
			print
			return
		except:
			print "connection error"
			sys.exit()
			
		# update employee and supporters, not depended upon
		try:
			cursor.execute("""
			update employees set email = '%s' where email = '%s';
			""" %( new_email, member_email, ))
		except:
			print "connection error"
			sys.exit()
		try:
			cursor.execute("""
			update supporters set email = '%s' where email = '%s';
			""" %( new_email, member_email, ))
		except:
			print "connection error"
			sys.exit()
		
		# update member_of, not depended
		try:
			cursor.execute("""
			update member_of set member_email = '%s' where member_email = '%s';
			""" %( new_email, member_email, ))
		except:
			print "connection error"
			sys.exit()
			
			
	try:
		cursor.execute("""
		select * from volunteers where email = '%s';
		""" %( member_email,))
	except:
		print "connection error"
		sys.exit()
	i = 0
	for row in cursor.fetchall():
		i += 1
	
	if i > 0:
		#insert into volunteers
		try:
			cursor.execute("""
			select * from volunteers where email = '%s';
			""" %( member_email ))
		except:
			print "connection error"
			sys.exit()
			
		memory = cursor.fetchone()
		tier = memory[1]
		campaign_num = memory[2]
		
		try:
			cursor.execute("""
			insert into volunteers( email, tier, number_of_campaigns) values ( '%s', %d, %d ); 
			""" %( new_email, tier, campaign_num, ))
		except:
			print "connection error"
			sys.exit()
		
		#update volunteer campaign relation
		try:
			cursor.execute("""
			update volunteering_at_campaign set volunteer_email = '%s' where volunteer_email = '%s';
			""" %( new_email, member_email, ))
		except:
			print "connection error"
			sys.exit()
		
		# delete old tuple in volunteers
		try:
			cursor.execute("""
			delete from volunteers where email = '%s';
			""" %( member_email ))
		except:
			print "connection error"
			sys.exit()
		
		
		
	try:
		cursor.execute("""
		select * from donors where email = '%s';
		""" %( member_email,))
	except:
		print "connection error"
		sys.exit()
	i = 0
	for row in cursor.fetchall():
		i += 1
	
	if i > 0:
		#insert into donors
		try:
			cursor.execute("""
			select * from donors where email = '%s';
			""" %( member_email ))
		except:
			print "connection error"
			sys.exit()
		memory = cursor.fetchone()
		fname = memory[1]
		lname = memory[2]
		try:
			cursor.execute("""
			insert into donors( email, first_name, last_name ) values ( '%s', '%s', '%s' );
			""" %( new_email, fname, lname, ))
		except:
			print "connection error"
			sys.exit()
		
		# update donor_donation
		try:
			cursor.execute("""
			update donor_donation set donor_email = '%s' where donor_email = '%s';
			""" %( new_email, member_email, ))
		except:
			print "connection error"
			sys.exit()
			
		# delete old tuple in donors
		try:
			cursor.execute("""
			delete from donors where email = '%s';
			""" %( member_email ))
		except:
			print "connection error"
			sys.exit()
			
		
	# delete old tuple in members
	try:
		cursor.execute("""
		delete from members where email = '%s';
		""" %( member_email ))
	except:
		print "connection error"
		sys.exit()
	
	
	print_table ( cursor, "members" )
	print_table ( cursor, "volunteers" )
	print_table ( cursor, "supporters" )
	print_table ( cursor, "employees" )
	print_table ( cursor, "donors" )
	print_table ( cursor, "donor_donation" )
	print_table ( cursor, "member_of" )
	print_table ( cursor, "volunteering_at_campaign" )
	
	cursor.execute("COMMIT")
  
	return

def main():	
  
	print
	print "Welcome to the Green-not-Greed database!"
	print 
	
	try:
		dbconn = psycopg2.connect( host='studentdb.csc.uvic.ca', user='c370_s50', password='bwQ4ZB58' )
		print "connection successful"
	except:
		print "connection error"
		sys.exit()
	
	cursor = dbconn.cursor()
	print

	user_input = -1

	while ( user_input != 0 ):
		start_menu()	
		user_input = get_input_number_bound( "Enter a command number: ", 0, 10 )

		if user_input == 1:
			view_queries( cursor )		
		elif user_input == 2:
			add_campaign( cursor )
		elif user_input == 3:
			add_volunteer( cursor )
		elif user_input == 4:
			assign_volunteer( cursor )
		elif user_input == 5:
			view_campaign( cursor ) 
		elif user_input == 6:
			view_accounting( cursor )
		elif user_input == 7:
			view_membership( cursor )
		elif user_input == 8:
			annotate_campaign( cursor )
		elif user_input == 9:
			annotate_member( cursor )
		elif user_input == 10:	
			mystery_function( cursor )

	cursor.close()
	dbconn.close()

	sys.exit()

if __name__ == "__main__": main()
