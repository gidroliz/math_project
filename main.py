import json
import uuid
from generator import generator

def update_achievements(conn, user_id, data):
    sql = '''UPDATE math_achievements_stat SET {0} = {0}+1 WHERE id={1}'''
    with conn.cursor() as cursor:
        if data==0:
            cursor.execute(sql.format('light', user_id))    
        elif data==2:
            cursor.execute(sql.format('hard', user_id))
            
def main(conn, event, user_id):
    command=event['command']
    data=event['data']
    
    if command=='new_user':
        with conn.cursor() as cursor:
            sql = f"SELECT id FROM math_user WHERE name='{data['name']}' or email='{data['email']}';"
            cursor.execute(sql)
            result=cursor.fetchall()
            if not result:
                data['token'] = str(uuid.uuid4())
                columns = ', '.join(data.keys())
                placeholders = ', '.join(["%s"] * len(data))
                sql = f'''INSERT INTO math_user ({columns}) VALUES ({placeholders})'''
                cursor.execute(sql, tuple(data.values()))
                user_id = cursor.lastrowid
                sql = f'''INSERT INTO math_stat (id) VALUES (%s)'''
                cursor.execute(sql, (user_id,))
                sql = f'''INSERT INTO math_achievements_stat (id) VALUES (%s)'''
                cursor.execute(sql, (user_id,))
                conn.commit()
                return 200, {"answer": {"token":data['token']}}
            else:
                return 403, {"answer": "user exists"}
    
    elif command=='authorization':
        with conn.cursor() as cursor:
            sql = f'''SELECT token FROM math_user WHERE name='{data['name']}' and password='{data['password']}';'''
            cursor.execute(sql)
            result=cursor.fetchone()
            if result:
                return 200, {"answer": {"token":result['token']}}
            else:
                return 403, {"answer": "user not exists"}
    
    elif command=='get_all_tasks':
        with conn.cursor() as cursor:
            sql = '''SELECT task, solution, hard FROM math_tasks'''
            cursor.execute(sql)
            rows = cursor.fetchall()

        formatted_data = {"answer": [list(row.values()) for row in rows]}
        return 200, formatted_data
    
    elif command=='get_task':
        if isinstance(data["hard"], (int, float)):
            with conn.cursor() as cursor:
                sql = f'''SELECT task, solution FROM math_tasks where hard={data['hard']} ORDER BY RAND() limit 1'''
                cursor.execute(sql)
                task = cursor.fetchone()
            return 200, {"answer": list(task.values())}
        elif  data["hard"]=='custom':
            flag=False
            while not flag:
                try:
                    task=generator(data['numofoperands'], 
                                data['numofoperands'],
                                data['brackets'],
                                data['min'],
                                data['max'])
                    solution=eval(task)
                    flag=True
                except ZeroDivisionError:
                    continue
            return 200, {"answer":[task.replace('/',':'), round(solution,2)]}
    
    elif command=='counter':
        try:
            with conn.cursor() as cursor:
                sql = f'''UPDATE math_stat SET {data}_total = {data}_total+1 WHERE id={user_id}'''
                cursor.execute(sql)
            conn.commit()
            return 200, {"answer": "counted"}
        except:
            return 403, {"answer": "somthing wrong"}
        
    elif command=='correct_solution':
        try:
            with conn.cursor() as cursor:
                sql = f'''UPDATE math_stat SET {data}_right = {data}_right+1 WHERE id={user_id}'''
                cursor.execute(sql)
            update_achievements(conn, user_id, data)
            conn.commit()
            return 200, {"answer": "counted"}
        except:
            return 403, {"answer": "something wrong"}
        
    elif command=='wrong_solution':
        try:
            with conn.cursor() as cursor:
                sql = f'''UPDATE math_stat SET {data}_wrong = {data}_wrong+1 WHERE id={user_id}'''
                cursor.execute(sql)
            conn.commit()
            return 200, {"answer": "counted"}
        except:
            return 403, {"answer": "somthing wrong"}
    
    elif command=='get_leaderboards':
        try:
            with conn.cursor() as cursor:
                sql = """
                    SELECT 
                        JSON_OBJECT(
                            '0', (SELECT JSON_ARRAYAGG(JSON_ARRAY(name, 
                                                                COALESCE(ROUND(0_right / NULLIF(0_total, 0) * 100, 2), 0)))
                                FROM math_user
                                JOIN math_stat ON math_user.id = math_stat.id
                                ORDER BY COALESCE(ROUND(0_right / NULLIF(0_total, 0) * 100, 2), 0) DESC),
                            '1', (SELECT JSON_ARRAYAGG(JSON_ARRAY(name, 
                                                                COALESCE(ROUND(1_right / NULLIF(1_total, 0) * 100, 2), 0)))
                                FROM math_user
                                JOIN math_stat ON math_user.id = math_stat.id
                                ORDER BY COALESCE(ROUND(1_right / NULLIF(1_total, 0) * 100, 2), 0) DESC),
                            '2', (SELECT JSON_ARRAYAGG(JSON_ARRAY(name, 
                                                                COALESCE(ROUND(2_right / NULLIF(2_total, 0) * 100, 2), 0)))
                                FROM math_user
                                JOIN math_stat ON math_user.id = math_stat.id
                                ORDER BY COALESCE(ROUND(2_right / NULLIF(2_total, 0) * 100, 2), 0) DESC)
                        ) AS answer;
                    """
                cursor.execute(sql)
                result = cursor.fetchone()
            return 200, {"answer": json.loads(result['answer'])}
        except:
            return 403, {"answer": "somthing wrong"}
    
    elif command=='get_achievements':
        try:
            with conn.cursor() as cursor:
                sql='''SELECT name FROM math_achievements'''
                cursor.execute(sql)
                result=cursor.fetchall()
                names=[res['name'] for res in result]
                answer={}
                for achievement_name in names:
                    sql = f'''
                    SELECT 
                        JSON_OBJECT(
                            ma.name, JSON_OBJECT(
                                'progress', 
                                CASE 
                                    WHEN ma.name = %s THEN mas.{achievement_name} 
                                    ELSE 0 
                                END,
                                'size', ma.size,
                                'description', ma.description
                            )
                        ) AS result
                    FROM 
                        math_achievements_stat mas
                    JOIN 
                        math_user mu ON mu.id = mas.id
                    JOIN 
                        math_achievements ma ON ma.name = %s
                    WHERE 
                        mu.id = %s;
                    '''
                    cursor.execute(sql, (achievement_name, achievement_name, user_id))
                    result = cursor.fetchone()
                    answer.update(json.loads(result['result']))
            return 200, {'answer': answer}
        except:
            return 403, {"answer": "somthing wrong"}
    
    else:
        return 404, {'answer':'undefined command'}


if __name__=='__main__':
    main()