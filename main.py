import json
import uuid
from modules.generator import generator
from modules.sql_querys import *


def update_achievements(conn, user_id, data):
    with conn.cursor() as cursor:
        if data == 0:
            cursor.execute(sql_update_achievements.format("light", user_id))
        elif data == 2:
            cursor.execute(sql_update_achievements.format("hard", user_id))
    conn.commit()


def count_up(conn, data, user_id, sql_string):
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql_string.format(data, user_id))
        conn.commit()
        return 200, {"answer": "counted"}
    except:
        return 403, {"answer": "somthing wrong"}


def main(conn, event, user_id):
    command = event["command"]
    data = event["data"]

    if command == "new_user":
        with conn.cursor() as cursor:
            cursor.execute(sql_find_user.format(data["name"], data["email"]))
            result = cursor.fetchall()
            if not result:
                data["token"] = str(uuid.uuid4())
                columns = ", ".join(data.keys())
                placeholders = ", ".join(["%s"] * len(data))
                cursor.execute(
                    sql_new_math_user.format(columns, placeholders),
                    tuple(data.values()),
                )
                user_id = cursor.lastrowid
                cursor.execute(sql_new_math_stat, (user_id,))
                cursor.execute(sql_new_math_achievements_stat, (user_id,))
                conn.commit()
                return 200, {"answer": {"token": data["token"]}}
            else:
                return 403, {"answer": "user exists"}

    elif command == "authorization":
        with conn.cursor() as cursor:
            cursor.execute(sql_auth.format(data["name"], data["password"]))
            result = cursor.fetchone()
            if result:
                return 200, {"answer": {"token": result["token"]}}
            else:
                return 403, {"answer": "user not exists"}

    elif command == "get_all_tasks":
        with conn.cursor() as cursor:
            cursor.execute(sql_get_all_tasks)
            rows = cursor.fetchall()
        formatted_data = {"answer": [list(row.values()) for row in rows]}
        return 200, formatted_data

    elif command == "get_task":
        if isinstance(data["hard"], (int, float)):
            with conn.cursor() as cursor:
                cursor.execute(sql_get_task.format(data["hard"]))
                task = cursor.fetchone()
            return 200, {"answer": list(task.values())}
        elif data["hard"] == "custom":
            flag = False
            while not flag:
                try:
                    task = generator(
                        data["numofoperands"],
                        data["numofoperands"],
                        data["brackets"],
                        data["min"],
                        data["max"],
                    )
                    solution = eval(task)
                    flag = True
                except ZeroDivisionError:
                    continue
            return 200, {"answer": [task.replace("/", ":"), round(solution, 2)]}

    elif command == "counter":
        return count_up(conn, data, user_id, sql_incr_total)

    elif command == "correct_solution":
        update_achievements(conn, user_id, data)
        return count_up(conn, data, user_id, sql_incr_right)

    elif command == "wrong_solution":
        return count_up(conn, data, user_id, sql_incr_wrong)

    elif command == "get_leaderboards":
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql_get_leaderboards)
                result = cursor.fetchone()
            return 200, {"answer": json.loads(result["answer"])}
        except:
            return 403, {"answer": "somthing wrong"}

    elif command == "get_achievements":
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql_achievements_names)
                result = cursor.fetchall()
                names = [res["name"] for res in result]
                answer = {}
                for achievement_name in names:
                    cursor.execute(
                        sql_get_achievements.format(achievement_name),
                        (achievement_name, achievement_name, user_id),
                    )
                    result = cursor.fetchone()
                    answer.update(json.loads(result["result"]))
            return 200, {"answer": answer}
        except:
            return 403, {"answer": "somthing wrong"}

    else:
        return 404, {"answer": "undefined command"}