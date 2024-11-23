from dotenv import load_dotenv
import psycopg2
import os

load_dotenv(verbose=True)
DBNAME = os.environ.get("DBNAME")
DBUSER = os.environ.get("DBUSER")
DBPASSWORD = os.environ.get("DBPASSWORD")
DBHOST = os.environ.get("DBHOST")

DB_CONFIG = {
    "dbname": DBNAME,
    "user": DBUSER,
    "password": DBPASSWORD,
    "host": DBHOST,
    "port": 5432,
}


def add_character(owner_id: int, name: str, avatar_url: str):
    try:
        # データベースに接続
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        owner_id = str(owner_id)

        # owner_idごとの件数を取得
        count_query = """
            SELECT COUNT(*)
            FROM webhook_characters
            WHERE owner_id = %s;
        """
        cursor.execute(count_query, (owner_id,))
        result = cursor.fetchone()

        # 件数が存在しない場合はindexを1とする
        if result[0]:
            new_character_index = result[0] + 1
        else:
            new_character_index = 1

        # INSERTクエリを実行
        insert_query = """
            INSERT INTO webhook_characters (owner_id, name, avatar_url, character_index)
            VALUES (%s, %s, %s, %s)
            RETURNING id, character_index;
        """
        cursor.execute(insert_query, (owner_id, name, avatar_url, new_character_index))

        # 挿入されたレコードのIDとcharacter_indexを取得
        inserted_index = cursor.fetchone()
        conn.commit()

        return inserted_index[1]

    except psycopg2.Error as e:
        print(f"Database error: {e}")
        if conn:
            conn.rollback()
    finally:
        # 接続を閉じる
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def get_character(owner_id: str, character_index: int):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        owner_id = str(owner_id)

        select_query = """
            SELECT id, owner_id, name, avatar_url, character_index
            FROM webhook_characters
            WHERE owner_id = %s AND character_index = %s;
        """
        cursor.execute(select_query, (owner_id, character_index))
        result = cursor.fetchone()
        if result:
            return True, result[2], result[3]
        else:
            return False, False, False
    except psycopg2.Error as e:
        print(f"Database error: {e}")
        if conn:
            conn.rollback()
        return False, False, False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
