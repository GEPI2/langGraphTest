import sqlite3

def inspect_db():
    db_path = 'checkpoints.sqlite'
    
    try:
        # 읽기 전용으로 열기 (혹시 모를 락 방지)
        conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
        cursor = conn.cursor()
        
        print(f"--- Inspecting {db_path} ---")

        # 1. 테이블 목록 조회
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"Tables: {[t[0] for t in tables]}")
        
        # 2. checkpoints 테이블 데이터 조회
        if ('checkpoints',) in tables:
            # 컬럼 정보 확인
            cursor.execute("PRAGMA table_info(checkpoints)")
            columns = [info[1] for info in cursor.fetchall()]
            print(f"Columns: {columns}")

            print("\n--- Recent Checkpoints (Top 5) ---")
            cursor.execute("SELECT * FROM checkpoints LIMIT 5")
            rows = cursor.fetchall()
            
            if not rows:
                print("No checkpoints found.")
            
            for row in rows:
                print(row)

        conn.close()

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    inspect_db()
