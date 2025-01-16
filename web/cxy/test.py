input_sql_file = "C:\\python_food-master\\python_ROS\\python_food.sql"

output_sql_file = "C:\\python_food-master\\python_ROS\\web\\cxy\\insert.sql"

with open(input_sql_file, "r", encoding="utf-8") as file:
    sql_statements = file.read()

    # 分割SQL语句
    statements = sql_statements.split(";")
    # 提取INSERT语句
    insert_statements = [
        stmt for stmt in statements if stmt.strip().upper().startswith("INSERT")
    ]

with open(output_sql_file, "w", encoding="utf-8") as f:
    for statement in insert_statements:
        f.write(statement.strip() + ";\n")
