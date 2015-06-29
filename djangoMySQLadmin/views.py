from django.shortcuts import render
from django.conf import settings
import MySQLdb as ms
from django.http import HttpResponseRedirect, HttpResponse

global datatypes, labels, values, count
datatypes, labels, values, count = [], [], [], 0

class Row (object):
	def __init__ (self, name, datatype):
		self.name = name
		self.datatype = datatype

class Entry (object):
	def __init__ (self, label, value):
		self.label, self.value = label, value

def connect ():
	host = settings.DATABASES['default']['HOST']
	user = settings.DATABASES['default']['USER']
	password = settings.DATABASES['default']['PASSWORD']
	database = settings.DATABASES['default']['NAME']
	return ms.connect (host, user, password, database)

def home (request):
	c = {'database':settings.DATABASES['default']['NAME'], 'username':settings.DATABASES['default']['USER']}
	return render (request, "djangomysqladmin_home.html", c)

def database (request):
	conn = connect ()
	cur = conn.cursor ()
	cur.execute ("show tables")
	tables = []
	for row in cur.fetchall ():
		tables.append (row[0])

	conn.close ()
	c = {'tables':tables}
	return render (request, "djangomysqladmin_database.html", c)

def view_table (request):
	conn = connect ()
	cur = conn.cursor ()

	cur.execute ("desc %s" % request.GET['table'])
	schema = []
	for row in cur.fetchall ():
		schema.append (Row (row[0], row[1]))

	cur.execute ("select * from %s" % request.GET['table'])
	entries = []
	for row in cur.fetchall ():
		entries.append (row)

	conn.close ()
	c = {'table':request.GET['table'], 'schema':schema, 'entries':entries}
	return render (request, "djangomysqladmin_view_table.html", c)

def insert_entry (request):
	global datatypes, labels
	conn = connect ()
	cur = conn.cursor ()
	cur.execute ("desc %s" % request.GET['table'])
	for row in cur.fetchall ():
		labels.append (row[0])
		datatypes.append (row[1])
	conn.close ()
	return render (request, "djangomysqladmin_insert_entry.html", {'labels':labels, 'table':request.GET['table']})

def entry_inserted (request):
	global datatypes, labels
	conn = connect ()
	cur = conn.cursor ()

	query = "insert into %s values (" % request.GET['table']
	l = len (datatypes)
	for i in range (l):
		tr = datatypes[i].split ("(")[0]
		if tr == "int" or tr == "double" or tr == "float":
			query += "%s" % request.GET[labels[i]]
		else:
			query += "'%s'" % request.GET[labels[i]]
		if i != l-1:
			query += ","
		else:
			query += ")"
	cur.execute (query)

	conn.commit ()
	conn.close ()
	datatypes, labels = [], []
	return HttpResponseRedirect ("/djangomysqladmin/view-table/?table=%s" % request.GET['table'])

def delete_entry (request):
	global labels, datatypes
	conn = connect ()
	cur = conn.cursor ()

	cur.execute ("desc %s" % request.GET['table'])
	for row in cur.fetchall ():
		labels.append (row[0])
		datatypes.append (row[1])

	cur.execute ("select * from %s" % request.GET['table'])
	entries = []
	for row in cur.fetchall ():
		temp = []
		for i in range (len (row)):
			temp.append (Entry (labels[i], row[i]))
		entries.append (temp)

	conn.close ()
	c = {'table':request.GET['table'], 'entries':entries}
	return render (request, "djangomysqladmin_delete_entry.html", c)


def entry_deleted (request):
	global labels, datatypes
	conn = connect ()
	cur = conn.cursor ()

	query = "delete from %s where " % request.GET['table']
	l = len (labels)
	for i in range (l):
		if datatypes[i] in ["int", "float", "double"]:
			query += "%s=%s" % (labels[i], request.GET[labels[i]])
		else:
			query += "%s='%s'" % (labels[i], request.GET[labels[i]])
		if i != l-1:
			query += " and "
	cur.execute (query)

	conn.commit ()
	conn.close ()
	labels, datatypes = [], []
	return HttpResponseRedirect ("/djangomysqladmin/view-table/?table=%s" % request.GET['table'])



def update_entry (request):
	global labels, datatypes, values
	conn = connect ()
	cur = conn.cursor ()

	cur.execute ("desc %s" % request.GET['table'])
	for row in cur.fetchall ():
		labels.append (row[0])
		datatypes.append (row[1])

	cur.execute ("select * from %s" % request.GET['table'])
	entries = []
	for row in cur.fetchall ():
		temp = []
		for i in range (len (row)):
			temp.append (Entry (labels[i], row[i]))
			values.append (row[i])
		entries.append (temp)

	conn.close ()
	c = {'table':request.GET['table'], 'entries':entries}
	return render (request, "djangomysqladmin_update_entry.html", c)


def entry_updated (request):
	global labels, datatypes, values
	conn = connect ()
	cur = conn.cursor ()

	query = "update %s set " % request.GET['table']
	l = len (labels)

	for i in range (l):
		if datatypes[i] in ["int", "float", "double"]:
			query += "%s=%s" % (labels[i], request.GET[labels[i]])
		else:
			query += "%s='%s'" % (labels[i], request.GET[labels[i]])
		if i != l-1:
			query += ", "

	query += " where "
	for i in range (l):
		if datatypes[i] in ["int", "float", "double"]:
			query += "%s=%s" % (labels[i], values[i])
		else:
			query += "%s='%s'" % (labels[i], values[i])
		if i != l-1:
			query += " and "

	cur.execute (query)

	conn.commit ()
	conn.close ()
	labels, datatypes, values = [], [], []
	return HttpResponseRedirect ("/djangomysqladmin/view-table/?table=%s" % request.GET['table'])


def create_table (request):
	global count
	try:
		count = int (request.POST['count'])
	except KeyError:
		pass
	return render (request, "djangomysqladmin_create_table.html", {'count':count, 'counts':range(count)})

def table_created (request):
	global count
	conn = connect ()
	cur = conn.cursor ()
	query = "create table %s (" % request.POST['table']

	for i in range (count):
		temp = str (i)
		if request.POST['datatype'+temp] == "varchar":
			query += "%s %s(%s)" % (request.POST['name'+temp], request.POST['datatype'+temp], request.POST['length'+temp])
		else:
			query += "%s %s" % (request.POST['name'+temp], request.POST['datatype'+temp])
		if i != count-1:
			query += ", "
	query += ")"
	cur.execute (query)

	count = 0
	conn.commit ()
	conn.close ()
	return HttpResponseRedirect ("/djangomysqladmin/database/")
