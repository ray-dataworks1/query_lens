from querylens.syntaxer import parse_sql

def test_basic_query():
    sql = "SELECT id, name FROM users WHERE age > 18"
    ast = parse_sql(sql)

    assert ast["type"] == "Query"
    assert ast["select"]["columns"] == ["id", "name"]
    assert ast["from_clause"]["table"] == "users"
    assert ast["where_clause"]["operator"] == ">"
