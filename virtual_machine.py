import json
from sys import argv

class MemoryManager():
    def __init__(self, func_dir):
        # track memory relevant information
        self.mem_stack = []
        self.func_mem_idx_stack = [[] for _ in range(len(func_dir))]
        self.func_dir = func_dir

        # track current function
        self.func_id_stack = [None]
        self.curr_func_id = None

    def get_mem(self, mem_dir):
        func_id, mem_dir = mem_dir
        if func_id == self.curr_func_id:
            return self.func_mem_idx_stack[-1][mem_dir]
        return self.mem_stack[self.func_mem_idx_stack[func_id][-1]][mem_dir]

    def set_mem_w_val(self, mem_dir_dst, val):
        func_id, mem_dir_dst = mem_dir_dst
        if func_id == self.curr_func_id:
            self.func_mem_idx_stack[-1][mem_dir_dst] = val
        self.mem_stack[self.func_mem_idx_stack[func_id][-1]][mem_dir_dst] = val

    def set_mem_w_mem(self, mem_dir_src, mem_dir_dst):
        val = self.get_mem(mem_dir_src)
        self.set_mem_w_val(mem_dir_dst, val)
    
    def start_func_stack(self, func_id):
        self.func_id_stack.append(func_id)
        self.curr_func = func_id
        
        func_ttl_vars = self.func_dir[func_id][0]
        self.func_mem_idx_stack[func_id].append(len(self.mem_stack))
        self.mem_stack.append([None] * func_ttl_vars)

    def end_func_stack(self, func_id):
        assert self.curr_func == func_id
        self.func_id_stack.pop()
        self.curr_func = self.func_id_stack[-1]

        self.mem_stack.pop()
        self.func_mem_idx_stack[func_id].pop()

def bin_op(q, mem, op):
    mem.set_mem_w_val(q[3], op(mem.get_mem(q[1]), mem.get_mem(q[2])))

def run_func(mem : MemoryManager, quads, q_idx):
    basic_op_hanlder = {
        "ASSIG" : lambda q : mem.set_mem_w_mem(q[1], q[3]),
        "PARAM" : lambda q : mem.set_mem_w_mem(q[1], q[3]),
        "PLUS" : lambda q : bin_op(q, mem, lambda x,y:x+y),
        "MINUS" : lambda q : bin_op(q, mem, lambda x,y:x-y),
        "DIV" : lambda q : bin_op(q, mem, lambda x,y:x/y),
        "MULT" : lambda q : bin_op(q, mem, lambda x,y:x*y),
        "EXP" : lambda q : bin_op(q, mem, lambda x,y:x**y),
        "MOD" : lambda q : bin_op(q, mem, lambda x,y:x%y),
        "EQ" : lambda q : bin_op(q, mem, lambda x,y:x==y),
        "NOT_EQ" : lambda q : bin_op(q, mem, lambda x,y:x!=y),
        "GEQT" : lambda q : bin_op(q, mem, lambda x,y:x>=y),
        "LEQT" : lambda q : bin_op(q, mem, lambda x,y:x<=y),
        "GT" : lambda q : bin_op(q, mem, lambda x,y:x>y),
        "LT" : lambda q : bin_op(q, mem, lambda x,y:x<y),
        "OR" : lambda q : bin_op(q, mem, lambda x,y:x or y),
        "AND" : lambda q : bin_op(q, mem, lambda x,y:x and y),
        "NOT" : lambda q : mem.set_mem_w_val(q[3], not mem.get_mem(q[1])),
        "PRINT" : lambda q : print(mem.get_mem(q[3])),
        "CONST" : lambda q : mem.set_mem_w_val(q[3], q[1]),
    }

    while(q_idx < len(quads)):
        q = quads[q_idx]
        q_op = q[0]
        nxt_q_idx = q_idx + 1
        if q_op == "GOTO":
           nxt_q_idx = q[3] 
        elif q_op == "GOTOF":
            if(mem.get_mem(q[1])):
                nxt_q_idx = q[3] 
        elif q_op == "ERA":
           func_id = q[3]
           mem.start_func_stack(func_id)
        elif q_op == "GOSUB":
            func_id = q[3]
            run_func(mem, quads, q[1])
            mem.end_func_stack(func_id)
        elif q_op == "RETURN":
            basic_op_hanlder["ASSIG"](q)
        elif q_op == "ENDFUNC":
            break
        else:
            basic_op_hanlder[q_op](q)
        q_idx = nxt_q_idx

def run_global(func_dir, quads):
    memory_manager = MemoryManager(func_dir)
    memory_manager.start_func_stack(0)
    run_func(memory_manager, quads, 0)
    memory_manager.end_func_stack(0)

def main():
    filename = argv[1]
    with open(filename, "r") as ir_file:
        ir = ir_file.read()
        compiler_dict = json.loads(ir)
    func_dir = compiler_dict["func_dir"]
    quads = compiler_dict["quads"]
    run_global(func_dir, quads)

if __name__ == '__main__':
    main()