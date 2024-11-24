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
            SELECT character_index
            FROM webhook_characters
            WHERE owner_id = %s;
        """
        cursor.execute(count_query, (owner_id,))
        existing_indexes = [row[0] for row in cursor.fetchall()]

        # 欠番を探す
        next_index = 1
        for index in existing_indexes:
            if index == next_index:
                next_index += 1
            else:
                break

        # INSERTクエリを実行
        insert_query = """
            INSERT INTO webhook_characters (owner_id, name, avatar_url, character_index)
            VALUES (%s, %s, %s, %s)
            RETURNING id, character_index;
        """
        cursor.execute(insert_query, (owner_id, name, avatar_url, next_index))

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


def delete_character(owner_id: str, character_index: str) -> bool:
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        owner_id = str(owner_id)

        delete_query = """
            DELETE
            FROM webhook_characters
            WHERE owner_id = %s AND character_index = %s;
        """
        cursor.execute(delete_query, (owner_id, character_index))
        if cursor.rowcount > 0:
            conn.commit()
            return True
        else:
            return False
    except psycopg2.Error as e:
        print(f"Database error: {e}")
        if conn:
            conn.rollback()
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def get_all_character(owner_id: str):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        owner_id = str(owner_id)

        select_query = """
            SELECT name, character_index
            FROM webhook_characters
            WHERE owner_id = %s;
        """
        cursor.execute(select_query, (owner_id,))
        result = cursor.fetchall()
        if len(result) == 0:
            return False
        else:
            return result
    except psycopg2.Error as e:
        print(f"Database error: {e}")
        if conn:
            conn.rollback()
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
