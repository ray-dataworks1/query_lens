from querylens.lexer import tokenise

def test_basic_select():
    sql = "SELECT id, name FROM users WHERE age > 18"
    tokens = tokenise(sql)
    types = [t.type for t in tokens]
    assert "SELECT" in types and "FROM" in types and "WHERE" in types

