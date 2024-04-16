import mysql.connector

# Função para conectar ao banco de dados
def connect_to_database():
    try:
        return mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="336679",
            database="server"
        )
    except mysql.connector.Error as err:
        print("Erro ao conectar ao banco de dados:", err)
        return None

def authenticate_user(username, password):
    try:
        conn = connect_to_database()
        cursor = conn.cursor()

        cursor.execute("SELECT account_id FROM accounts WHERE account=%s AND password=%s", (username, password))
        account_id = cursor.fetchone()

        if account_id:
            account_id = account_id[0]

        cursor.close()
        conn.close()

        return account_id
    except mysql.connector.Error as err:
        print("Erro ao autenticar usuário:", err)
        return None




def get_player_names(account_id):
    try:
        conn = connect_to_database()
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM players WHERE account_id=%s", (account_id,))
        player_names = cursor.fetchall()

        cursor.close()
        conn.close()
        return player_names
    except mysql.connector.Error as err:
        print("Erro ao obter nomes de jogadores:", err)
        return None

def check_player_status(account_id, character_name):
    try:
        conn = connect_to_database()
        cursor = conn.cursor()

        cursor.execute("SELECT player_online FROM players WHERE account_id=%s AND name=%s", (account_id, character_name))
        status = cursor.fetchone()

        cursor.close()
        conn.close()

        if status:
            return status[0]
        else:
            return None
    except mysql.connector.Error as err:
        print("Erro ao verificar status do jogador:", err)
        return None

def update_player_status(account_id, character_name, status):
    try:
        conn = connect_to_database()
        cursor = conn.cursor()

        cursor.execute("UPDATE players SET player_online = %s WHERE account_id = %s AND name = %s", (status, account_id, character_name))
        conn.commit()

        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print("Erro ao atualizar status do jogador:", err)

def create_account(username, password):
    try:
        conn = connect_to_database()
        cursor = conn.cursor()

        cursor.execute("INSERT INTO accounts (account, password) VALUES (%s, %s)", (username, password))
        conn.commit()

        account_id = cursor.lastrowid  # Obtendo o ID da última linha inserida

        cursor.close()
        conn.close()
        return account_id
    except mysql.connector.Error as err:
        print("Erro ao criar conta:", err)
        return None


def create_character(account_id, character_name):
    try:
        conn = connect_to_database()
        cursor = conn.cursor()

        print("Account ID:", account_id)
        print("Character Name:", character_name)

        cursor.execute("INSERT INTO players (account_id, name, player_online, level) VALUES (%s, %s, %s, %s)", (account_id, character_name, 0, 1))

        conn.commit()

        cursor.close()
        conn.close()
        return True
    except mysql.connector.Error as err:
        print("Erro ao criar personagem:", err)
        return False
