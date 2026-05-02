import psycopg2
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD


def get_connection():
    """Открывает соединение с базой данных."""
    return psycopg2.connect(
        host="localhost",
        port=5432,
        dbname="snake_db",
        user="postgres",
        password="12345678"
    )


def init_db():
    """
    Создаёт таблицы players и game_sessions,
    если они ещё не существуют.
    Вызывай один раз при старте игры.
    """
    sql_players = """
        CREATE TABLE IF NOT EXISTS players (
            id       SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL
        );
    """
    sql_sessions = """
        CREATE TABLE IF NOT EXISTS game_sessions (
            id            SERIAL PRIMARY KEY,
            player_id     INTEGER REFERENCES players(id),
            score         INTEGER   NOT NULL,
            level_reached INTEGER   NOT NULL,
            played_at     TIMESTAMP DEFAULT NOW()
        );
    """
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(sql_players)
        cur.execute(sql_sessions)
        conn.commit()
        cur.close()
        conn.close()
        print("[DB] Таблицы созданы (или уже существуют).")
    except Exception as e:
        print(f"[DB] Ошибка при создании таблиц: {e}")


def get_or_create_player(username: str) -> int:
    """
    Возвращает id игрока по имени.
    Если игрока нет — создаёт и возвращает новый id.
    """
    try:
        conn = get_connection()
        cur = conn.cursor()

        
        cur.execute("SELECT id FROM players WHERE username = %s", (username,))
        row = cur.fetchone()

        if row:
            player_id = row[0]
        else:
            cur.execute(
                "INSERT INTO players (username) VALUES (%s) RETURNING id",
                (username,)
            )
            player_id = cur.fetchone()[0]
            conn.commit()

        cur.close()
        conn.close()
        return player_id
    except Exception as e:
        print(f"[DB] Ошибка get_or_create_player: {e}")
        return -1


def save_session(player_id: int, score: int, level_reached: int):
    """Сохраняет результат игровой сессии в базу."""
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO game_sessions (player_id, score, level_reached)
            VALUES (%s, %s, %s)
            """,
            (player_id, score, level_reached)
        )
        conn.commit()
        cur.close()
        conn.close()
        print(f"[DB] Сессия сохранена: score={score}, level={level_reached}")
    except Exception as e:
        print(f"[DB] Ошибка save_session: {e}")


def get_top10() -> list:
    """
    Возвращает топ-10 результатов.
    Каждая запись: (rank, username, score, level_reached, played_at)
    """
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT p.username, gs.score, gs.level_reached,
                   gs.played_at::date AS date
            FROM game_sessions gs
            JOIN players p ON p.id = gs.player_id
            ORDER BY gs.score DESC
            LIMIT 10
            """
        )
        rows = cur.fetchall()
        cur.close()
        conn.close()
       
        return [(i + 1, *row) for i, row in enumerate(rows)]
    except Exception as e:
        print(f"[DB] Ошибка get_top10: {e}")
        return []


def get_personal_best(player_id: int) -> int:
    """Возвращает лучший счёт конкретного игрока."""
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT COALESCE(MAX(score), 0)
            FROM game_sessions
            WHERE player_id = %s
            """,
            (player_id,)
        )
        best = cur.fetchone()[0]
        cur.close()
        conn.close()
        return best
    except Exception as e:
        print(f"[DB] Ошибка get_personal_best: {e}")
        return 0