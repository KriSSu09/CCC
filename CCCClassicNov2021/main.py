def stop_func_exec_with_error():
    global exe_stack, nr_unfinished_if, sym_table, output_list, outfile, nr_true_if, nr_expected_end
    temp = exe_stack.pop(0)
    while temp != 'start' and len(exe_stack):
        temp = exe_stack.pop(0)
    outfile.write('ERROR\n')
    sym_table = {}
    output_list = []
    nr_unfinished_if = 0
    nr_true_if = 0
    nr_expected_end = 0


def stop_func_exec_without_error():
    global exe_stack, nr_unfinished_if, sym_table, output_list, outfile, nr_expected_end, nr_true_if
    temp = exe_stack.pop(0)
    while temp != 'start' and len(exe_stack):
        temp = exe_stack.pop(0)
    to_write = ""
    for item in output_list:
        to_write += str(item)
    if to_write != "":
        to_write += '\n'
    outfile.write(to_write)
    sym_table = {}
    output_list = []
    nr_unfinished_if = 0
    nr_true_if = 0
    nr_expected_end = 0


def skip_to_else():
    global exe_stack, nr_expected_end
    nr_expected_end -= 1
    temp = exe_stack.pop(0)
    while temp != 'else':
        temp = exe_stack.pop(0)


def skip_to_if_end():
    global exe_stack, nr_expected_end
    nr_expected_end -= 1
    temp = exe_stack.pop(0)
    while temp != 'end':
        temp = exe_stack.pop(0)


for i in range(5):
    with open("level3_" + str(i + 1) + ".in", 'r') as f:
        outfile = open("level3_" + str(i + 1) + ".out", 'w')
        N = int(f.readline())
        sym_table = {}
        exe_stack = []
        output_list = []
        nr_unfinished_if = 0
        nr_true_if = 0
        nr_expected_end = 0
        program = f.readlines()
        for line in program:
            exe_stack.append(line.split())
        exe_stack = [item for sublist in exe_stack for item in sublist]
        while len(exe_stack):
            cmd = exe_stack.pop(0)
            if cmd == 'start':
                continue
            elif cmd == 'print':
                to_print = exe_stack.pop(0)
                if to_print in sym_table:
                    output_list.append(sym_table[to_print])
                else:
                    output_list.append(to_print)
            elif cmd == 'var':
                to_declare = exe_stack.pop(0)
                if to_declare in sym_table:
                    stop_func_exec_with_error()
                else:
                    to_declare_value = exe_stack.pop(0)
                    if to_declare_value in sym_table:
                        sym_table[to_declare] = sym_table[to_declare_value]
                    else:
                        sym_table[to_declare] = to_declare_value
            elif cmd == 'set':
                to_set = exe_stack.pop(0)
                if to_set not in sym_table:
                    stop_func_exec_with_error()
                    continue
                to_set_value = exe_stack.pop(0)
                if to_set_value in sym_table:
                    sym_table[to_set] = sym_table[to_set_value]
                else:
                    sym_table[to_set] = to_set_value
            elif cmd == 'if':
                nr_unfinished_if += 1
                nr_expected_end += 2
                if_cond = exe_stack.pop(0)
                if if_cond in sym_table:
                    if sym_table[if_cond] == 'true':
                        nr_true_if += 1
                        continue
                    elif sym_table[if_cond] == 'false':
                        skip_to_else()
                        continue
                    else:
                        stop_func_exec_with_error()
                        continue
                else:
                    if if_cond == 'true':
                        nr_true_if += 1
                        continue
                    elif if_cond == 'false':
                        skip_to_else()
                        continue
                    else:
                        stop_func_exec_with_error()
                        continue
            elif cmd == 'else':
                if nr_unfinished_if == nr_true_if:
                    nr_unfinished_if -= 1
                else:
                    skip_to_if_end()
                    nr_unfinished_if -= 1
            elif cmd == 'end':
                if nr_unfinished_if != 0:
                    nr_expected_end -= 1
                    nr_true_if -= 1
                else:
                    sym_table = {}
                    nr_unfinished_if = 0
                    nr_true_if = 0
                    nr_expected_end = 0
                    to_write = ""
                    for item in output_list:
                        to_write += str(item)
                    if to_write != "":
                        to_write += '\n'
                    outfile.write(to_write)
                    output_list = []
            elif cmd == 'return':
                stop_func_exec_without_error()
        outfile.close()
