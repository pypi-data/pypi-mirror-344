from .tokens import Token, TokenType
from .exceptions import ExitREPL
import importlib, datetime, itertools


class Interpreter:
    def __init__(self):
        self.symbols = {}     # 符号表
        self.loop_stack = []  # 跟踪循环层级
        self.libraries = {}   # 存储已导入的库
        self.functions = {}   # 存储函数定义

    def visit_FUNC_DEF(self, node):
        self.functions[node['name']] = {
            'params': node['params'],
            'body': node['body']
        }
        return None

    def visit_FUNC_CALL(self, node):
        # 获取函数定义
        func = self.functions.get(node['name'])
        if not func:
            raise Exception(f"Function {node['name']} not defined")

        # 绑定参数
        params = func['params']
        args = node['args']
        if len(params) != len(args):
            raise Exception(f"Args are not match: need {len(params)}，got {len(args)}")

        # 创建新作用域
        old_symbols = self.symbols.copy()
        local_symbols = {param: self.visit(arg) for param, arg in zip(params, args)}

        # 执行函数体
        result = None
        for stmt in func['body']:
            # 使用局部符号表
            self.symbols.update(local_symbols)
            result = self.visit(stmt)
            if stmt['type'] == 'RETURN':
                break

        # 恢复作用域
        self.symbols = old_symbols
        return result

    def visit_RETURN(self, node):
        return self.visit(node['value'])

    def visit_VERSION_CALL(self, node):
        current_year = datetime.datetime.now().year
        return f"jxlang 0.2.6 2025-{current_year}"

    def visit_CITE(self, node):
        library_name = node['name']
        try:
            # 直接导入 Python 模块
            lib_module = importlib.import_module(library_name)
            self.libraries[library_name] = lib_module
            self.symbols[library_name] = lib_module
        except ModuleNotFoundError:
            raise Exception(f"Python library '{library_name}' not found")

    def visit_MEMBER_ACCESS(self, node):
        obj_wrapper = self.visit(node['object'])
        member_name = node['member']
        if isinstance(obj_wrapper, dict) and obj_wrapper.get('type') == 'JX_LIST':
            if member_name == 'outlist':
                return obj_wrapper['outlist'] # 直接返回 outlist
            else:
                raise Exception(f"JX_LIST does not have member '{member_name}'")
        # 保留对导入库成员的访问
        elif hasattr(obj_wrapper, member_name):
            return getattr(obj_wrapper, member_name)
        else:
            raise Exception(f"Member '{member_name}' not found")

    def visit_CALL(self, node):
        # 解析函数对象
        func = self.visit(node['func'])
        # 解析参数
        args = [self.visit(arg) for arg in node['args']]
        # 调用 Python 函数并返回结果
        return func(*args)

    def visit_BIN_OP(self, node):
        left = self.visit(node['left'])
        right = self.visit(node['right'])
        op = node['op']

        if op == TokenType.PLUS:
            return left + right
        elif op == TokenType.MINUS:
            return left - right
        elif op == TokenType.MUL:
            return left * right
        elif op == TokenType.DIV:
            return left / right  # 注意除零错误
        elif op == TokenType.MOD:
            return left % right
        else:
            raise Exception("Unknown operator")

    # 处理列表求值
    def visit_LIST(self, node):
        # 这个方法处理 table(...) 和 [...] 语法解析出的列表节点
        # 假设解析器生成的节点类型是 'LIST'，包含 'value' 或 'elements'
        elements = node.get('value', node.get('elements', []))
        evaluated_elements = [self.visit(elem) for elem in elements]
        return {'type': 'JX_LIST', 'data': evaluated_elements, 'outlist': []}

    def visit_INDEX_ACCESS(self, node):
        obj_wrapper = self.visit(node['object'])
        index = self.visit(node['index'])
        if isinstance(obj_wrapper, dict) and obj_wrapper.get('type') == 'JX_LIST':
            # 访问包装器内部的 data 列表
            data_list = obj_wrapper['data']
            if not isinstance(index, int):
                raise Exception(f"List index must be int，but got {type(index).__name__}")
            if 0 <= index < len(data_list):
                return data_list[index]
            else:
                raise Exception(f"Index {index} out of bounds")
        elif isinstance(obj_wrapper, list): # 支持访问普通Python列表（例如嵌套列表的子列表）
             if not isinstance(index, int):
                 raise Exception(f"List index must be int，but got {type(index).__name__}")
             if 0 <= index < len(obj_wrapper):
                 return obj_wrapper[index]
             else:
                 raise Exception(f"Index {index} out of bounds")
        else:
            raise Exception("Index access can only be used for lists or JX_LIST wrappers")

    # 处理布尔值
    def visit_BOOL(self, node):
        return node['value']

    # 处理浮点数
    def visit_FLOAT(self, node):
        return node['value']

    # 处理字符串
    def visit_STRING(self, node):
        return node['value']

    def visit(self, node):
        method_name = f'visit_{node["type"]}'
        method = getattr(self, method_name, self.generic_visit)
        return method(node)

    def generic_visit(self, node):
        raise Exception(f"No visit_{node['type']} method")

    def visit_LET(self, node):
        for var_name, value_node in node['vars']:
            value = self.visit(value_node)

            # 检查var_name是否是索引访问
            target_obj = None
            target_index = None
            is_index_assignment = isinstance(var_name, dict) and var_name.get('type') == 'INDEX_ACCESS'

            if is_index_assignment:
                # 获取列表包装器和索引
                # !!! 注意: 这里假设 var_name['object'] 是变量名字符串
                # 如果 parser 返回的是 {'type': 'VAR', 'value': 'a'} 节点，需要调整
                if isinstance(var_name['object'], dict) and var_name['object'].get('type') == 'VAR':
                     list_var_name = var_name['object']['value']
                elif isinstance(var_name['object'], str):
                     list_var_name = var_name['object']
                else:
                     raise Exception("Invalid target for indexed assignment")

                if list_var_name not in self.symbols:
                     raise Exception(f"Undefined variable {list_var_name}")
                target_obj_wrapper = self.symbols[list_var_name]
                if not (isinstance(target_obj_wrapper, dict) and target_obj_wrapper.get('type') == 'JX_LIST'):
                    raise Exception(f"Variable {list_var_name} is not an assignable list.")
                target_obj = target_obj_wrapper['data'] # 操作内部的 data 列表
                target_index = self.visit(var_name['index'])
                if not isinstance(target_index, int):
                     raise Exception("List index must be an integer")
                # 赋值给内部列表的特定索引
                if 0 <= target_index < len(target_obj):
                    target_obj[target_index] = value
                else:
                     raise Exception(f"Index {target_index} out of bounds for list {list_var_name}")

            else: # 普通变量赋值 (var_name 应该是字符串)
                 if not isinstance(var_name, str):
                     # 如果解析器将 'a' 解析为 {'type':'VAR', 'value':'a'}，这里需要提取 'a'
                     if isinstance(var_name, dict) and var_name.get('type') == 'VAR':
                         var_name = var_name['value']
                     else:
                         raise Exception("Invalid variable name structure in LET")

                 # 如果值是列表字面量创建的JX_LIST包装器，直接存储
                 if isinstance(value, dict) and value.get('type') == 'JX_LIST':
                     self.symbols[var_name] = value
                 else:
                     # 对于其他类型的值，直接存储
                     self.symbols[var_name] = value
        return None

    def visit_FOR_LOOP(self, node):
        variables = node['vars']
        start = self.visit(node['start'])
        end = self.visit(node['end'])
        body = node['body']

        # 生成循环范围
        ranges = [range(start, end + 1)] * len(variables)

        # 遍历所有变量组合
        for values in itertools.product(*ranges):
            # 新建作用域
            self.loop_stack.append(self.symbols.copy())

            # 绑定变量到当前作用域
            for var, val in zip(variables, values):
                self.symbols[var] = val

            # 执行循环体
            self.visit(body)

            # 恢复上一层作用域
            self.symbols = self.loop_stack.pop()

        return None

    def visit_TABLE(self, node):
        # 这个方法处理 table(...) 语法解析出的嵌套列表节点
        evaluated_sublists = [self.visit(sublist) for sublist in node['value']]
        # 对于嵌套列表，我们目前只返回嵌套的Python列表，暂不支持嵌套的outlist
        # 如果需要支持，这里的结构需要更复杂
        return [sublist['data'] for sublist in evaluated_sublists if isinstance(sublist, dict) and sublist.get('type') == 'JX_LIST']

    def visit_INT(self, node):
        return node['value']

    def visit_VAR(self, node):
        var_name = node['value']
        if var_name in self.symbols:
            # 如果是列表包装器，返回包装器本身，否则返回值
            return self.symbols[var_name]
        else:
            raise Exception(f"Undefined variable {var_name}")

    # 处理 enter()
    def visit_ENTER_CALL(self, node):
        user_input = input()
        try:
            return int(user_input)  # 尝试转为整数
        except ValueError:
            try:
                return float(user_input)  # 尝试转为浮点数
            except ValueError:
                return user_input  # 保留为字符串

    # 处理 say(expr)
    def visit_SAY(self, node):
        value = self.visit(node['expr'])
        print(value)
        return None

    # 处理 endend()
    def visit_ENDEND(self, node):
        arg = node.get('arg')
        if arg is not None:
            if not (0 <= arg <= 9):  # 检查参数范围
                raise Exception("endend() argument must be between 0 and 9")
            raise ExitREPL(arg)
        else:
            raise ExitREPL(0)  # 默认退出码为 0

    def visit_SHAPE(self, node):
        value = self.visit(node['expr'])
        if isinstance(value, dict) and value.get('type') == 'JX_LIST':
             if all(isinstance(item, list) for item in value['data']): # 检查是否是嵌套列表
                 return "table"
             else:
                 return "list"
        elif isinstance(value, int):
            return "int"
        elif isinstance(value, float):
            return "float"
        elif isinstance(value, str):
            return "string"
        elif isinstance(value, bool):
            return "bool"
        elif isinstance(value, list): # 处理普通Python列表（可能来自库或嵌套表）
             if all(isinstance(item, list) for item in value):
                 return "table"
             else:
                 return "list"
        elif value is None:
            return "none"
        else:
            # 对于其他Python对象（如导入的库模块）
            return str(type(value).__name__)

    def visit_PUSH(self, node):
        element = self.visit(node['element'])
        target_node = node['list']

        if isinstance(target_node, dict) and target_node.get('type') == 'INDEX_ACCESS':
            # 处理索引插入: push 5 -> a[1]
            list_var_node = target_node['object']
            index_node = target_node['index']

            # 假设 list_var_node 是 {'type': 'VAR', 'value': 'a'}
            if not (isinstance(list_var_node, dict) and list_var_node.get('type') == 'VAR'):
                 raise Exception("Target object for indexed push must be a variable")
            list_var_name = list_var_node['value']
            if list_var_name not in self.symbols:
                 raise Exception(f"Undefined variable {list_var_name}")

            list_wrapper = self.symbols[list_var_name]
            if not (isinstance(list_wrapper, dict) and list_wrapper.get('type') == 'JX_LIST'):
                raise Exception("Target for push is not a JX_LIST")

            index = self.visit(index_node)
            if not isinstance(index, int):
                raise Exception("Index for push must be an integer")

            list_wrapper['data'].insert(index, element)

        else:
            # 处理列表末尾添加: push 5 -> a
            list_wrapper = self.visit(target_node) # target_node 应该是 VAR 节点
            if not (isinstance(list_wrapper, dict) and list_wrapper.get('type') == 'JX_LIST'):
                raise Exception("Target for push is not a JX_LIST")
            list_wrapper['data'].append(element)
        return None # push 操作不返回值

    def visit_OUT(self, node):
        element_to_remove = self.visit(node['element'])
        target_node = node['list'] # 这应该是 VAR 节点，如 'a'
        list_wrapper = self.visit(target_node)

        if not (isinstance(list_wrapper, dict) and list_wrapper.get('type') == 'JX_LIST'):
            raise Exception("Target for out is not a JX_LIST")

        if element_to_remove in list_wrapper['data']:
            list_wrapper['data'].remove(element_to_remove)
            list_wrapper['outlist'].append(element_to_remove)
        else:
            raise Exception("Element not found in list for out operation")
        return None # out 操作不返回值

    def visit_THROW(self, node):
        element_to_remove = self.visit(node['element'])
        target_node = node['list']
        list_wrapper = self.visit(target_node)

        if not (isinstance(list_wrapper, dict) and list_wrapper.get('type') == 'JX_LIST'):
            raise Exception("Target for throw is not a JX_LIST")

        if element_to_remove in list_wrapper['data']:
            list_wrapper['data'].remove(element_to_remove)
            # 不添加到 outlist
        else:
            raise Exception("Element not found in list for throw operation")
        return None # throw 操作不返回值