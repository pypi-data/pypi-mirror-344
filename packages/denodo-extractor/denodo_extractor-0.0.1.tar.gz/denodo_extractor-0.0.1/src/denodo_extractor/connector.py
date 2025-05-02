import psycopg2 as dbdriver

class connector:
    """Connector class instantiates a connection to the Denodo VDP Server using the psycopg2 library.
    """

    def __init__(self, server_name, port, database, user_id, pwd):
        """Instantiates the Connector class and prompts the user to enter the server details.
        """

        # Obtain server port, server database, server user id, server password
        self.denodoserver_name = server_name
        self.denodoserver_odbc_port = port
        self.denodoserver_database = database
        self.denodoserver_uid = user_id
        self.__denodoserver_pwd = pwd
        self.cursor = self.connect()

    def connect(self):
        """Establishes the connection to the Denodo VDP Server using the psycopg2 library.

        Raises:
            Exception: when no user id defined yet by the user.

        Returns:
            Object: cursor object 
        """
        # Establishing a connection
        if hasattr(self, "denodoserver_uid"):
            cnxn_str = "user=%s password=%s host=%s dbname=%s port=%s" %\
                (self.denodoserver_uid, self.__denodoserver_pwd, self.denodoserver_name,
                 self.denodoserver_database, self.denodoserver_odbc_port)

            cnxn = dbdriver.connect(cnxn_str)

            # Define a cursor and execute the results
            cursor = cnxn.cursor()

            return cursor
        else:
            raise Exception("No user id defined")