sql_verify_token = """SELECT id FROM math_user WHERE token='{0}' LIMIT 1;"""
sql_update_achievements = (
    """UPDATE math_achievements_stat SET {0} = {0}+1 WHERE id={1}"""
)
sql_find_user = "SELECT id FROM math_user WHERE name='{0}' or email='{1}';"
sql_new_math_user = """INSERT INTO math_user ({0}) VALUES ({1})"""
sql_new_math_stat = """INSERT INTO math_stat (id) VALUES (%s)"""
sql_new_math_achievements_stat = (
    """INSERT INTO math_achievements_stat (id) VALUES (%s)"""
)
sql_auth = """SELECT token FROM math_user WHERE name='{0}' and password='{1}';"""
sql_get_all_tasks = """SELECT task, solution, hard FROM math_tasks"""
sql_get_task = (
    """SELECT task, solution FROM math_tasks where hard={0} ORDER BY RAND() limit 1"""
)
sql_incr_total = """UPDATE math_stat SET {0}_total = {0}_total+1 WHERE id={1}"""
sql_incr_right = """UPDATE math_stat SET {0}_right = {0}_right+1 WHERE id={1}"""
sql_incr_wrong = """UPDATE math_stat SET {0}_wrong = {0}_wrong+1 WHERE id={1}"""
sql_get_leaderboards = """
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
sql_achievements_names = """SELECT name FROM math_achievements"""
sql_get_achievements = """
    SELECT 
        JSON_OBJECT(
            ma.name, JSON_OBJECT(
                'progress', 
                CASE 
                    WHEN ma.name = %s THEN mas.{0} 
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
"""
sql_check_tasks='''SELECT COUNT(*) from math_tasks'''