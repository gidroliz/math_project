from modules.generator import generator

hard0 = (2, 2, False, 0, 10)
hard1 = (3, 3, False, -10, 10)
hard2 = (4, 6, True, -10, 10)


def generate_table(connection):
    for hard in range(3):
        i = 0
        values = []
        while i < 200:
            item = generator(*eval(f"hard{hard}"))
            try:
                solution = eval(item)
                task = (item.replace("/", ":"), round(solution, 2), hard)
                if task not in values:
                    values.append(task)
                else:
                    continue
                i += 1
            except ZeroDivisionError:
                continue
        with connection.cursor() as cursor:
            sql = "INSERT INTO math_tasks (task, solution, hard) VALUES (%s, %s, %s)"
            cursor.executemany(sql, values)
    connection.commit()
