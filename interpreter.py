import ply.yacc as yacc
# import ply.lex as lex
import myparser
# import lexer
import sys
# import importlib

yaplParser = yacc.yacc(module=myparser)


# env = (parent, dictionary)
# ident = IDENTIFIER ---> name of the variable
def env_lookup(env, identifier):
    # return env + val
    if identifier in env[1]:
        return env[1][identifier]
    # if we are in global env and still can't find the value, return None
    elif not env[0]:
        return None
    # Check for the val in parent env
    else:
        return env_lookup(env[0], identifier)

# Will update only if the identifier exists in one of envs
def env_update(env, identifier, new_val):
    # print("updating env: ", identifier)
    try:

        # print("updatin env: ", identifier, new_val)
        # update the LOCAL env dictionary
        if identifier in env[1]:
            # if someone tries to change the defined-structure of a struct
            # this exception will trigger
            if env[1][identifier][0] == 'struct_template':
                raise Exception("Can't change the defined structure of {}".format(identifier))
            # print("found: ", env[1][identifier])
            env[1][identifier] = new_val
        # parent env==None and still can't find the identifier, return None
        elif not env[0]:
            raise Exception("Invalid Identifier")
        # Check for the val in parent env
        else:
            return env_update(env[0], identifier, new_val)
        # print("updated env: ", identifier)
    
    # Normal work flow of env update
    except:
        raise Exception("Some Error Occured while updating env")

# add identifier to the env passed as argument
def add_to_env(env, identifier, val):
    # print("adding to env: ", identifier)
    env[1][identifier] = val
    # print("Added to env: ", env)


# check if the given dtype matches the value, if the match is true, return the value
def type_cast( data_type, val):

    # print("type_cat: ", val)
    if (data_type=='int'  and (str(type(val))=="<class 'int'>" or str(type(val))=="<class 'float'>")):
        return int(val)
    if (data_type=='double'  and (str(type(val))=="<class 'int'>" or str(type(val))=="<class 'float'>")):
        return float(val)
    if (data_type =='string' and str(type(val))=="<class 'str'>"):
        return val
    if(data_type =='char' and str(type(val))=="<class 'str'>" and len(val)<=1):
        return val
    if(data_type =='bool' and str(type(val))=="<class 'bool'>" ):
        return val
    # if(data_type == 'struct'):

    return None

def eval_exp(env, tree):
    # print(tree)
    node_type = tree[0]
    if node_type == 'number' or node_type=='string' or node_type=='char' or node_type=='int' or node_type=='double': # ("number" , "5")
        return tree[1]
    if node_type=='binop':      # ("binop" , ... , "+", ... )
        left_val = eval_exp(env, tree[1])
        operator = tree[2]
        right_val = eval_exp(env, tree[3])
        if operator == '+':
            return left_val + right_val
        if operator == '-':
            return left_val - right_val
        if operator == '*':
            return left_val * right_val
        if operator == '/':
            return left_val / right_val
        if operator == '%':
            return left_val % right_val
        if operator == '^':
            return left_val ** right_val
        if operator == '&&':
            return left_val and right_val
        if operator == '||':
            return left_val or right_val
        if operator == '!=':
            return left_val != right_val
        if operator == '==':
            return left_val == right_val
        if operator == '>':
            return left_val > right_val
        if operator == '>=':
            return left_val >= right_val
        if operator == '<':
            return left_val < right_val
        if operator == '<=':
            return left_val <= right_val
    if node_type=='identifier':         # ('identifier', name)
        id_val = env_lookup(env, tree[1])
        if id_val:
            return id_val[1]
        raise NameError("Variable {} not Declared".format(tree[1]))
    if node_type=='bool': # ('bool', true/false)
        return tree[1]
    if node_type=='unary':              # ('unary', ..., operator)
        operator = tree[2]              # ('unary',('identifier', 'b'), operator)
        val = eval_exp(env, tree[1])
        type_val = env_lookup(env, tree[1][1])
        if val == None:
            raise NameError("{} does not exist".format(tree[1][1]))
        # env_update handles the invalid identifier exceptions
        # print("Unary: ", val[1]+1)
        # print("Unary: ",  (val[0], val[1]+1))
        if operator == '++':
            env_update(env, tree[1][1], (type_val, val+1))
            # print("updated env: ", env)
            return val+1
        if operator == '--':
            env_update(env, tree[1][1], (type_val, val-1))
            return val-1
        if operator == '!':
            return not val
        if operator == '-':
            return -val
    if node_type=='new_assign': # ('assign', type, name, ('d_type', val))
        # print(tree)
        if env_lookup(env, tree[2]) != None:
            raise Exception("Can't redeclare '{}'".format(tree[2]))
        val = eval_exp(env, tree[3])
        type_matched_value = type_cast(tree[1], val)
        # if(tree[2] == tree[3][0] or tree[2]=='int' and tree[3]==):
        if type_matched_value != None:
            add_to_env(env, tree[2], (tree[1], type_matched_value))
        else:
            raise TypeError("Can't assign {} to <class '{}'>".format(type(val), tree[1]))
    if node_type=='re_assign': # ('re_assign', "x" , ('number', 2)) --- val can also be an expression
        name = tree[1].split('.')
        prev_val = env_lookup(env, name[0])
        new_val = eval_exp(env, tree[2])
        # should generate an error if the variable is not present in the env.
        if prev_val == None:
            raise Exception("Variable Not Declared {}".format(tree[1]))
        # assigning values to structs is a lil different
        if prev_val[0]=='struct':
            attr = prev_val[1].get(name[1])
            if not attr:
                raise AttributeError("'{}' has not '{}' attribute".format(name[0], name[1]))
            new_val_typed_casted = type_cast(attr[0], new_val) # prev_val -> (dtype, val)
            prev_val[1][name[1]] = (attr[0], new_val_typed_casted)
            new_val_typed_casted = prev_val
                
        else:
            new_val_typed_casted = type_cast(prev_val[0], new_val) # prev_val -> (dtype, val)
        if new_val_typed_casted == None:
            raise TypeError("Can't assign {} to <class '{}'>".format(type(new_val), prev_val[0]))
        # update the change in the envoirnment
        env_update(env, name[0], new_val_typed_casted)
    if node_type=='declare': # ('declare', type, name)
        data_type = tree[1]
        # python_dtype = set_dtype(data_type)
        if env_lookup(env, tree[2]):
            raise Exception("Can't redeclare {}".format(tree[2]))
        if data_type == 'double' or data_type == 'int':
            add_to_env(env, tree[2], (data_type,0))
        if data_type == 'bool':
            add_to_env(env, tree[2], (data_type, True))
        if data_type == 'string' or data_type == 'char':
            add_to_env(env, tree[2], (data_type, ''))
    if node_type=='print': # ('print', [('string', 'Standard Output')])
        args = tree[1] # --> can be a list of expressions
        for arg in args:
            val = eval_exp(env, arg)
            if val == None:
                raise Exception("Undeclared variable: {}".format(arg[1]))
            print(val, end=' ') # other vals separated by a space
        print()
    if node_type=='struct-attribute': # ('struct_attribute', sname, attribute)
        struct = env_lookup(env, tree[1])
        attr = struct[1].get(tree[2])
        if attr:
            return attr[1]
        raise AttributeError("'{}' has not '{}' such attribute!".format(tree[1], tree[2]))
            
    if node_type=='struct-construct': # ('struct-construct', struct-name, identifier)
        # print(tree)
        s_attributes = env_lookup(env, tree[1]) # ---> ('struct-template', attributes)  We just need the attributes
        if s_attributes==None:
            raise Exception("No Struct is defined with such name")
        else:
            add_to_env(env, tree[2], ('struct', s_attributes[1].copy()))

def eval_stmtS(env, stmts):
    for statement in stmts:
        # print("Evaluating: ", statement)
        # print(statement[0])
        eval_stmt(env, statement)
        # print(env)
        
def eval_stmt(env, tree):
    stmt_type = tree[0]
    if stmt_type=='stmt': # ('stmt',  exp)
        # print(tree[1])
        eval_exp(env, tree[1])
        # raise Exception (retval)
    if stmt_type=='if-then-else': # (exp, if_stmtS, else_stmtS)
        conditional_exp = eval_exp(env, tree[0])
        if_stmts = tree[1]
        else_stmts = tree[2]
        if conditional_exp:
            eval_stmtS(env, if_stmts) # it should be given a new env...?
        else:
            eval_stmtS(env, else_stmts) # it should be given a new env...?
    if stmt_type=='call':
        fname = tree[1] # sqrt
        args = tree[2] # [ ('number', '2') ] ---> (maybe it's "x" in our oroginal env)
        fvalue = env_lookup(env, fname)
        if fvalue[0] == 'function': # ('function', params, body, env)
            fparams = fvalue[1] # ["x"]
            fbody = fvalue[2]
            fenv = fvalue[3]
            if len(fparams) != len(args):
                print ("Error in eval_stmt: len_params != len_args")
            else:
                # Make a new env frame
                new_env = (fenv, {})
                for i in range (len(args)): # add each param_val in the new env
                    argval = eval_exp(args[i], env)
                    new_env[0][fparams[i]] = argval
                try:
                    eval_stmtS(fbody, new_env) # excute the function in the new_env
                    return None
                except Exception as return_val:
                    return return_val
        else:
            print("{} is not a function".format(fname))
    if stmt_type=='do-while': # ('do-while', (stmtS, expression))
        dow_stmts = tree[1][0]
        dow_env = (env, {})
        expression = tree[1][1]
        try:
            eval_stmtS(dow_env, dow_stmts) # do
            while eval_exp(dow_env, expression): # while
                dow_env = (env, {})
                eval_stmtS(dow_env, dow_stmts)
        except Exception as Error:
            print("Error in do-while: ", Error)
    if stmt_type=='struct-define': # ('struct', name , [declare/assign stmts])
        sname = tree[1]
        sbody = tree[2]
        # print(sbody)
        senv = (None, {})
        for stmt in sbody:
            if not (stmt[1][0] == 'declare' or stmt[1][0] == 'new_assign'):
                raise Exception("SyntaxError: Can Only declare variables in struct")
            eval_stmt(senv, stmt)
        # The variables will be declared in the env we provided.
        svars = {}
        for val in senv[1]:
            svars[val] = senv[1][val]
        # added the template for struct to the envoirnment
        struct_property = ('struct_template', svars)
        add_to_env(env, sname, struct_property)
        # print(env)

        

# def eval_elt(env, tree):
#     elt_type = tree[0]
#     if elt_type == 'function':
#         fname = tree[1]
#         fparams = tree[2]   # List of params
#         fbody = tree[3]     # List of stmtS
#         fvalue = ('function', fparams, fbody, env)
#         add_to_env(env, fname, fvalue)


if len(sys.argv) != 2:
    raise Exception("\nFormat ---> python3 interpreter.py <name_of_test_case>\n")

global_env = (None, {}) # Need a global env to start the program

path = "./test_cases/"+sys.argv[1]
with open(path, "r") as infile:
    val = infile.read()
    parsed = yaplParser.parse(val)
    # print("parsed: ", parsed)
    print("Welcome to the MyYAPL Interpreter!")
    print("Output:")
    eval_stmtS(global_env, parsed)


