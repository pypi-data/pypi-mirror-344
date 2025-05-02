# https://gist.github.com/dannguyen/b7d7ce593fe748157f34 참고

# !pip install future
import inspect
import ast
import sys
#from past.builtins import basestring

def cprint(*args, **kwargs):
    result = ''
    fp = kwargs.pop("file", sys.stdout)
    
    def write(data):
        #if not isinstance(data, basestring): data = str(data)
        if not isinstance(data, str): data = str(data)
        fp.write(data)

    sep   = kwargs.pop("sep"  , None)
    end   = kwargs.pop("end"  , None)
    equal = kwargs.pop("equal", None)
    back  = kwargs.pop("back" , None)
    ptype = kwargs.pop("ptype", None)
    pid   = kwargs.pop("pid"  , None)
    cmd   = kwargs.pop("cmd"  , None)

    if kwargs: raise TypeError("invalid keyword arguments to print()")
        
    if sep is None: sep = "\n"
    if end is None: end = "\n"
    if end == 'nl': end = '\n\n'
    if equal is None: equal = ' = '
    if back is None: back = False   
    if cmd  is None: cmd  = True

    index = 0
    for i, arg in enumerate(args):
        #print(args)
        if i: write(sep)
            
        caller_frame = inspect.currentframe().f_back
        code_context = inspect.getframeinfo(caller_frame).code_context
        line         = code_context[0].strip()
        tree         = ast.parse(line, mode='exec')
        thin_fn_nm   = inspect.currentframe().f_code.co_name
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == thin_fn_nm:
                if node.args:
                    arg_node = node.args[index]
                    arg_expr = ast.unparse(arg_node).strip()
                    index += 1
                    if cmd == False:
                        arg_expr = ''
                        equal = ''
                        
                    if ptype == True: ptype_txt = ' --> ' + str(type(arg)) 
                    else:             ptype_txt = ''
                    if pid   == True: pid_txt   = ' id:' + str(hex(id(arg)))
                    else:             pid_txt   = ''
                    #if back  == True: result    = f'{repr(arg)} {equal} {arg_expr}{ptype_txt}{pid_txt}'
                    #else:             result    = f'{arg_expr} {equal} {repr(arg)}{ptype_txt}{pid_txt}'
                    if back  == True: result    = f'{arg}{equal}{arg_expr}{ptype_txt}{pid_txt}'
                    else:             result    = f'{arg_expr}{equal}{arg}{ptype_txt}{pid_txt}'                        
        write(result)
    write(end)