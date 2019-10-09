from exceptions import *
from expression import Expression
import helpers


def print_last():
    # global history
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
        print('>>> ', end='')
        cmd = prepare_cmd(input())
        if is_empty(cmd):
            continue
        try:
            new_expr = Expression(cmd)
            helpers.history.append(new_expr)
            print_last()
        except InvalidTypeException:
            print('err: invalid type in expression')
        except InvalidExpressionException:
            print('err: invalid expression')
        except InvalidHistoryCallException:
            print('err: invalid history call')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit(0)
    except EOFError:
        exit(0)
    except SystemError:
        exit(0)
