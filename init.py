import restservice
import os

dbname = 'demodb'

#extConnName = 'pg_local'
primarytablename = 'pt1'
#externaltablename = 'x15_table'

parserSpecPath = '/home/anandi/x15/testdata/splunk_cstxt.xml'
dataFilePath = '/home/anandi/x15/testdata/tutorialdata'
indexconfig = {"version": 0, "indexFields": [{"path": "_ts", "strategies": [{'type': "value-index"}]}, {"path": "clientip", "strategies": [{'type': "value-index"}]}, {"path": "hcode", "strategies": [{'type': "value-index"}]}, {"path": "size", "strategies": [{'type': "value-index"}]}, {"path": "verb", "strategies": [{'type': "value-index"}]}, {"path":"_raw","strategies": [{"type":"text-index","analyzer":{"type":"machine-data-analyzer"}}]}, {"path":"ref","strategies": [{"type":"text-index","analyzer":{"type":"simple-analyzer"}}]}, {"path":"path","strategies": [{"type":"text-index","analyzer":{"type":"simple-analyzer"}}]}]}

# Authenticate by username & password - admin/admin and creates session id 
sessionid = restservice.do_authentication()

# Creates database
restservice.create_database(sessionid, dbname)

# Get database by Name
database = restservice.get_database(sessionid, dbname)

# Extract database UID from database json
dbuid = restservice.get_value_from_json(database, '_id')

# Create External Connection - Arguments - session id, database uid, ext connection name, db type, connection url, driver, username, password
#restservice.create_external_connection(sessionid, dbuid, extConnName, 'postgresql', 'jdbc:postgresql://localhost:5432/x15', 'org.postgresql.Driver', 'nop', None)

# Get External Connection
#connection = restservice.get_connection(sessionid, dbuid, extConnName)

# Extract Connection UID from Connection JSON
#connuid = restservice.get_value_from_json(connection, '_id')

# Create Managed Primary Table
restservice.create_managed_primary_table(sessionid, dbuid, primarytablename, parserSpecPath, indexconfig, 8)

# Get the table by name
table = restservice.get_table(sessionid, dbuid, primarytablename)

# Extract Table uid from table json
mptuid = restservice.get_value_from_json(table, '_id')

# Load data into Primary Table by UID
for dir, directories, filenames in os.walk(dataFilePath):
	for file in filenames:
		restservice.load_primary_table(sessionid, mptuid, dir + "/" + file)

# Create External Table
#restservice.create_external_table(sessionid, dbuid, None, externaltablename, connuid)

# Get the table by name
#table = restservice.get_table(sessionid, dbuid, externaltablename)

# Run a Query
#restservice.query(sessionid, dbuid, 'select * from ' + primarytablename + ' LIMIT 1')
#restservice.query(sessionid, dbuid, 'select * from ' + externaltablename + ' LIMIT 1')

# Runs a Paginated Query
#queryId = restservice.paginated_query_create(sessionid, dbuid, 'select * from ' + primarytablename)
#restservice.paginated_query_fetch(sessionid, dbuid, queryId, 0, 5)
#restservice.paginated_query_delete(sessionid, dbuid, queryId)

# Delete a table by name
#restservice.delete_table(sessionid, dbuid, primarytablename)


# Delete a database by name
#restservice.delete_database(sessionid, dbname)
