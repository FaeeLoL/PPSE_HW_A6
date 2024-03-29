from exceptions import *
from expression import Expression
import helpers


def print_last():
    n = str(len(helpers.history) - 1)
    print(f'{n}:{(" " * (2 - len(n)))}', helpers.history[-1])


def prepare_cmd(cmd):
    for i in range(len(cmd)):
        if cmd[i] != ' ':
            cmd = cmd[i:]
            break
    for i in reversed(range(len(cmd))):
        if cmd[i] != ' ':
            cmd = cmd[:i + 1]
            break
    return cmd


def is_empty(cmd):
    if len(cmd) == 0:
        return True
    for i in cmd:
        if i != ' ':
            return False
    return True


def main():
    helpers.init_history()
    while True:
        try:
            print('>>> ', end='')
            cmd = prepare_cmd(input())
            if is_empty(cmd):
                continue
            new_expr = Expression(cmd)
            helpers.history.append(new_expr)
            print_last()
        except InvalidTypeException:
            print('err: invalid expression')
        except InvalidExpressionException:
            print('err: invalid expression')
        except InvalidHistoryCallException:
            print('err: invalid history call')
        except UnicodeDecodeError:
            print('err: some wrong non UTF-8 symbol came to input')
        except ZeroDivisionError:
            print('err: zero division error')
        except YaDaunException:
            print('err: invalid expression')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit(0)
    except EOFError:
        exit(0)
    except SystemError:
        exit(0)
