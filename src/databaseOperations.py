import os
from dotenv import load_dotenv
import psycopg2
from src.utility import *

class NotifierDB():
    # Operazioni di notifica email/telegram col database. Verranno usate 
    # in produzione solo le funzioni di richiesta dati (inserimento dati 
    # verrà fatto da sito).

    # Descrizione account status:
    # A : Novizio - non è stata inviata la mail di benvenuto
    # B : Utente a cui è stata inviata la mail di benvenuto
    # mantenibile


    def __init__(self):
        # Inizializzatore della connessione

        load_dotenv()
        HOSTNAME = os.getenv('HOSTNAME')
        DATABASE = os.getenv('DATABASE')
        USERNAME = os.getenv('USERNAME')
        PASSWORD = os.getenv('PASSWORD')
        PORT_ID = os.getenv('PORT_ID')

        self.Connection = psycopg2.connect(
            host = HOSTNAME,
            dbname = DATABASE,
            user = USERNAME,
            password = PASSWORD,
            port = PORT_ID,
        )

        self.Cursor = self.Connection.cursor()

    def closeConnection(self):
        # Chiude la connessione con il database

        self.Connection.close()
        return


    def getSubscribers(self):
        # Restituisce il database (lista di tuple)

        self.Cursor.execute(f"SELECT * FROM subscribers")
        response = self.Cursor.fetchall()
        self.Connection.commit()

        all_users = []
        for _ in response:
            user = {}
            user["id"] = _[0]
            user["name"] = _[1]
            user["surname"] = _[2]
            user["email"] = _[3]
            user["telegram"] = _[5]
            user["tags"] = _[6]
            user["n_not"] = _[7]
            
            all_users.append(user)

        return all_users

    def getSub(self):
        self.Cursor.execute(f"SELECT * FROM subscribers;")
        response = self.Cursor.fetchall()
        self.Connection.commit()

        all_elements = []
        for _ in response:
            all_elements.append(_)

        return(all_elements)

    def getUserSentId(self, user_id):
        # Query sucks but function works
        self.Cursor.execute("SELECT * FROM sent;")
        response = self.Cursor.fetchall()
        self.Connection.commit()

        all_id = []
        for _ in response:
            all_id.append(_[2])

        return all_id

    def incrementNumNot(self, user_id):
        self.Cursor.execute(f"""
            UPDATE subscribers
                SET notifications = notifications + 1
            WHERE id = {user_id};
        """)
        self.Connection.commit()
        
        return

    def updateTelegramId(self, user_email, telegram_id):
        self.Cursor.execute(f"""
            UPDATE subscribers
                SET telegram = '{telegram_id}'
            WHERE subscribers.email = '{user_email}';
        """)
        self.Connection.commit()
        return

    def storeNotification(self, user_id, event_id):
        pattern = "INSERT INTO sent(sub_id, evt) VALUES (%s, %s)"
        self.Cursor.execute(pattern, (user_id, event_id))
        self.Connection.commit()
        
        return

    def createTable(self):
        # Operazione di configurazione/testing/debugging.
        self.Cursor.execute("""CREATE TABLE subscribers (
            id BIGSERIAL PRIMARY KEY NOT NULL,
            name VARCHAR (50) NOT NULL,
            surname VARCHAR (50) NOT NULL,
            email VARCHAR (50) UNIQUE NOT NULL,
            password VARCHAR (120) NOT NULL,
            telegram VARCHAR (50) UNIQUE,
            tags text ARRAY,
            notifications SMALLINT
        )""")
        self.Connection.commit()

        return

    def createTable2(self):
        # Operazione di configurazione/testing/debugging.
        self.Cursor.execute("""CREATE TABLE sent (
            id BIGSERIAL PRIMARY KEY NOT NULL,
            sub_id SMALLINT NOT NULL,
            evt VARCHAR (60) NOT NULL
        )""")
        self.Connection.commit()

        return

    def dropTable(self, password1: str, password2: str, password3: str):
        # Operazione di configurazione/testing/debugging.
        # Elimina tutta la tabella di database. Funzione di debugging. 
        # Richiede 3 password perche' una sua esecuzione non volontaria
        # causerebbe danni (molti).

        if password1 == "S0n0D4vv£r0'$1cur*" \
            and password2 == "U4cC1=qu3st4=0p3r4zion3=3=ri$chiosa" \
            and password3 == "password":
            self.Cursor.execute("TRUNCATE TABLE subscribers;")
            self.Connection.commit()
            print("Tabella svuotata")
            return
        else:
            return "operazione non concessa"

    def truncateTable(self):
        self.Cursor.execute("TRUNCATE TABLE subscribers;")
        self.Connection.commit()
        return
    
    def __store(self):
        # Carica utenti nel database (debugging & tests)

        pattern = 'INSERT INTO subscribers (username, emailAddress, telegramName, gender, telegramNotifications, emailNotifications, tags, personalStatus) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'

        self.Cursor.execute(pattern, ("Matteo Bini", "mail@matteobini.me", "MatteoBini", "M", "TRUE", "TRUE", "3CIIN, OLIMPIADI DI INFORMATICA, OIS, BINI", "A"))
        self.Connection.commit()

        return

    def debug(self):
        # Funzione per effettuare debugging dal momento che tutte le funzioni di questa classe sono
        # riservate per ragioni di sicurezza.

        # a = NotifierDB()
        #
        # a.dropTable("S0n0D4vv£r0'$1cur*", "U4cC1=qu3st4=0p3r4zion3=3=ri$chiosa", "password")
        # print(a.getTables())
        # a.createTable()
        # print(a.getTables())
        # a.store()
        # print(a.getTables())
        pass

def storeSent(user_id, event_id):
    DB = NotifierDB()
    DB.storeNotification(user_id, event_id)
    DB.closeConnection()

    return

def getUserSentId(user_id):
    DB = NotifierDB()
    k = DB.getUserSentId(user_id)
    DB.closeConnection

    return k

def incrementNumNot(user_id):
    DB = NotifierDB()
    DB.incrementNumNot(user_id)
    DB.closeConnection()
    return

def getSubscribers():
    DB = NotifierDB()
    k = DB.getSubscribers()
    DB.closeConnection()

    return k

def updateTelegramId(user_email, telegram_id):
    DB = NotifierDB()
    DB.updateTelegramId(user_email, telegram_id)
    DB.closeConnection()

def db_notification(user_id, notified_events):
    for _ in notified_events:
        storeSent(user_id, _["id"])
        incrementNumNot(user_id)
    return

# o = NotifierDB()
#
# print("Db originale: ")
# l = o.getSub()
# for _ in l:
#     print(_)
# #
# print("Db eliminato: ")
# o.dropTable("S0n0D4vv£r0'$1cur*","U4cC1=qu3st4=0p3r4zion3=3=ri$chiosa","password")
#
# print("Genero nuovo db:")
# o.createTable2()
#
# print("Nuovo db: ")
# l = o.getUserSentId("25")
# for _ in l:
#     print(_)
#
# o.createTable2()
# o.closeConnection()
