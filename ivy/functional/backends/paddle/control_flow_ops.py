# def if_exp(cond, if_true, if_false):
#   return if_true() if cond else if_false()


def if_else(cond, body_fn, orelse_fn, vars):
    return body_fn(*vars) if (cond := cond(*vars)) else orelse_fn(*vars)


def while_loop(test_fn, body_fn, vars):
    result = vars
    while test_fn(*result):
        result = body_fn(*result)
    return result
