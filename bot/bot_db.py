import MySQLdb

class DBHelper:


    def __init__(self, dbname = "jekabm$chatbotdb"):
        self.dbname = dbname
        self.conn = MySQLdb.connect(host="jekabm.mysql.pythonanywhere-services.com",
                           user = "jekabm",
                           passwd = "aaabbbMYSQL",
                           db = dbname,
                           charset = "utf8",
                           use_unicode = True)
        self.c = self.conn.cursor()

    def setup(self):
        stmt = "CREATE TABLE IF NOT EXISTS items (description text)"
        self.c.execute(stmt)
        self.conn.commit()

    def add_item(self, item_text, user, date):
        stmt = "INSERT INTO items (description, user, date) VALUES (%s, %s, %s)"
        args = (item_text, user, date, )
        self.c.execute(stmt, args)
        self.conn.commit()

    def add_user(self, user):
        stmt = "INSERT INTO users (id, first_name, last_name) VALUES (%s, %s, %s)"
        args = (user["id"], user["first_name"], user["last_name"], )
        self.c.execute("SELECT * from users where id = " + str(user["id"]) + ";")
        if not self.c.rowcount:
            self.c.execute(stmt, args)
        self.conn.commit()

    def add_update(self, id):
        stmt = "INSERT INTO updates (update_id) VALUES (%s)"
        args = (id, )
        self.c.execute(stmt, args)
        self.conn.commit()

    def delete_item(self, item_text):
        stmt = "DELETE FROM items WHERE description = (?)"
        args = (item_text, )
        self.c.execute(stmt, args)
        self.conn.commit()

    def add_conversation(self, chat, name):
        stmt = "INSERT INTO CONVERSATION (chat_id, name) VALUES (%s, %s)"
        args = (chat, name)
        self.c.execute(stmt, args)
        self.conn.commit()

    def get_items(self):
        stmt = "SELECT description FROM items"
        return [x[0] for x in self.c.execute(stmt)]
