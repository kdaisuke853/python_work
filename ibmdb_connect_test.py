import ibm_db

ibm_db.connect("DATABASE=name;HOSTNAME=host;PORT=60000;PROTOCOL=TCPIP;UID=username;PWD=password;", "", "")

stmt = ibm_db.exec_immediate(conn, "SELECT * from SCHOOLS")

#dictionary = ibm_db.fetch_both(stmt)
#dictionary =ibm_db.fetch_tuple(stmt)
dictionary =ibm_db.fetch_assoc(stmt)
#dictionary =ibm_db.fetch_row(stmt)
