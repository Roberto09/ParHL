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

    def get_mem_dir_val(self, mem_dir):
        func_id, mem_dir = mem_dir
        if func_id == self.curr_func_id:
            return self.func_mem_stack[-1][mem_dir]
        return self.mem_stack[self.func_mem_stack[func_id][-1]][mem_dir]

    def set_mem_dir_val(self, mem_dir_dst, mem_dir_tgt):
        func_id, mem_dir_dst = mem_dir_dst
        val = self.get_mem_dir_val(mem_dir_tgt)
        if func_id == self.curr_func_id:
            self.func_mem_stack[-1][mem_dir_dst] = val
        self.mem_stack[self.func_mem_stack[func_id][-1]][mem_dir_dst] = val

    def start_func_stack(self, func_id):
        self.func_id_stack.append(func_id)
        self.curr_func = func_id
        
        func_ttl_vars = self.func_dir[func_id][0]
        self.mem_stack.append([None] * func_ttl_vars)
        self.func_mem_idx_stack[func_id].append(len(self.mem_stack))

    def end_func_stack(self, func_id):
        assert self.curr_func == func_id
        self.func_id_stack.pop()
        self.curr_func = self.curr_func_id[-1]

        self.mem_stack.pop()
        self.func_mem_idx_stack[func_id].pop()

def run_func(memory : MemoryManager, func_id):
    pass

def run_global(func_dir):
    memory_manager = MemoryManager(func_dir)
    memory_manager.start_func_stack(0)
    run_func(memory_manager, 0)
    memory_manager.end_func_stack(0)

def main():
    filename = argv[1]
    with open(filename, "r") as ir_file:
        ir = ir_file.read()
        compiler_dict = json.loads(ir)
    func_dir = compiler_dict["func_dir"]
    quads = compiler_dict["quads"]

if __name__ == '__main__':
    main()