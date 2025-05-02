from .interpreter import Interpreter
from .exceptions import ExitREPL
from .lexer import Lexer
from .parser import Parser


def repl():
    print("JxLang MI (输入 endend() 退出，输入 version() 查看版本)")
    interpreter = Interpreter()
    while True:
        text_lines = []
        prompt = "jxlang> "  # 每次新语句开始时重置提示符
        while True:
            try:
                line = input(prompt).strip().replace('\r', '')
                if not line:
                    continue
                text_lines.append(line)
                full_text = "\n".join(text_lines)
                lexer = Lexer(full_text)
                parser = Parser(lexer)
                tree = parser.parse()
                break
            except EOFError:
                prompt = "    ... "  # 多行输入时显示缩进提示符
            except Exception as e:
                print(f"Syntax Error: {e}")
                text_lines = []
                break
        if not text_lines:
            continue

        try:
            result = interpreter.visit(tree)
            if result is not None:
                # 检查结果是否为内部列表表示
                if isinstance(result, dict) and result.get('type') == 'JX_LIST':
                    print(result['data'])  # 只打印列表数据
                else:
                    print(result)  # 正常打印其他结果
        except ExitREPL as e:
            print(f"Exiting with code {e.code}")
            break
        except Exception as e:
            print(f"Runtime Error: {e}")