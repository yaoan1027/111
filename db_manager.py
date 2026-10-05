import os
import pymysql
import pandas as pd

def get_db_connection():
    return pymysql.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', ''),
        database=os.getenv('DB_NAME', 'sales_db'),
        port=int(os.getenv('DB_PORT', 3306)),
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

def import_csv_to_mysql(csv_path, mode='insert'):
    """
    mode='insert': 匯入原始 300 筆 (TRUNCATE + INSERT)
    mode='update': 根據 sale_id 批次更新 (ON DUPLICATE KEY UPDATE)，維持 300 筆，異動 240 筆
    """
    df = pd.read_csv(csv_path, encoding='utf-8-sig')
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            if mode == 'insert':
                cursor.execute("TRUNCATE TABLE sales_records;")
                sql = """
                INSERT INTO sales_records 
                (sale_id, sale_date, product_id, product_name, category, channel, unit_price, quantity, returned_quantity)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                data = [tuple(x) for x in df.to_numpy()]
                cursor.executemany(sql, data)
                conn.commit()
                print(f"成功匯入 {len(data)} 筆初始資料！")
            elif mode == 'update':
                sql = """
                INSERT INTO sales_records 
                (sale_id, sale_date, product_id, product_name, category, channel, unit_price, quantity, returned_quantity)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    quantity = VALUES(quantity),
                    returned_quantity = VALUES(returned_quantity);
                """
                data = [tuple(x) for x in df.to_numpy()]
                cursor.executemany(sql, data)
                conn.commit()
                print(f"成功批次更新 {len(data)} 筆快照至資料庫！")
    finally:
        conn.close()

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'update':
        import_csv_to_mysql('data/sales_updated_300.csv', mode='update')
    else:
        import_csv_to_mysql('data/sales_original_300.csv', mode='insert')
