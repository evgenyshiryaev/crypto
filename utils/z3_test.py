# https://ericpony.github.io/z3py-tutorial/guide-examples.htm

from z3 import *


def test0():
    # x, y = Int('x'), Int('y')
    # x, y = Ints('x y')
    x, y = BitVec('x', 32), BitVec('y', 32)

    solver = Solver()
    solver.add(x + y == 10)
    solver.add(x - y == 6)
    # solver.add(x + y == 0)
    print("asserted constraints...")
    for c in solver.assertions():
        print(c)

    assert solver.check() == sat
    model = solver.model()
    # print(solver.statistics())

    print(model)
    print(model[x], model[y])


def eight_queens():
    Q = [Int(f'Q_{i + 1}') for i in range(8)]

    # Each queen is in a column {1, ... 8 }
    val_c = [And(1 <= Q[i], Q[i] <= 8) for i in range(8)]
    # At most one queen per column
    col_c = [Distinct(Q)]
    # Diagonal constraint
    diag_c = [Or(i == j, And(Q[i] - Q[j] != i - j, Q[i] - Q[j] != j - i)) for i in range(8) for j in range(i)]

    solve(val_c + col_c + diag_c)


def licence_test(n):
    flag = [BitVec(f'b{i}', 8) for i in range(n)]
    solver = Solver()

    # general key format
    for f in flag:
        solver.add(Or(
                    And(ord('0') <= f, f <= ord('9')),
                    And(ord('A') <= f, f <= ord('Z'))))

    # num -> alp -> num
    for i in range(n - 1):
        solver.add(Implies(And(ord('0') <= flag[i], flag[i] <= ord('9')),
                           And(ord('A') <= flag[i + 1], flag[i + 1] <= ord('Z'))))
        solver.add(Implies(And(ord('A') <= flag[i], flag[i] <= ord('Z')),
                           And(ord('0') <= flag[i + 1], flag[i + 1] <= ord('9'))))

    # predefined symbols
    m = {'F': 5, 'U': 5, '6': 5, '9': 5}
    for c in m.keys():
        solver.add(PbEq([(flag[i] == ord(c), 1) for i in range(20)], m[c]))

    assert solver.check() == sat
    model = solver.model()
    print(''.join([chr(model[f].as_long()) for f in flag]))


set_option(html_mode=False)
# test0()
# eight_queens()
# licence_test(20)
