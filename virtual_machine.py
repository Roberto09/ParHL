import json
from os import device_encoding
from sys import argv
import torch

DEVICE = "cpu"

class MemoryManager():
    def __init__(self, func_dir):
        # track memory relevant information
        self.mem_stack = [[] for _ in range(len(func_dir))]
        # dormant_mem_stack holds memory for functions which are inactive
        # i.e. which exist between an ERA and GOSUB state
        self.dormant_mem_stack = [[] for _ in range(len(func_dir))]
        self.func_dir = func_dir

    def dereference(self, initial_mem_dir):
        while(initial_mem_dir[2]):
            fid, idx, _, tid = initial_mem_dir
            initial_mem_dir = tuple(self.mem_stack[fid][-1][tid][idx+i] for i in range(4))
        return initial_mem_dir

    def get_mem(self, mem_dir):
        fid, idx, _, tid = self.dereference(mem_dir)
        return self.mem_stack[fid][-1][tid][idx]

    def set_mem_w_val(self, mem_dir_dst, val):
        fid, idx, _, tid = self.dereference(mem_dir_dst)
        self.mem_stack[fid][-1][tid][idx] = val

    def set_mem_w_mem(self, mem_dir_src, mem_dir_dst):
        val = self.get_mem(mem_dir_src)
        self.set_mem_w_val(mem_dir_dst, val)

    def set_dorm_mem_w_val(self, dorm_mem_dir_dst, val):
        fid, idx, _, tid = self.dereference(dorm_mem_dir_dst)
        self.dormant_mem_stack[fid][-1][tid][idx] = val
    
    def set_dorm_mem_w_mem(self, mem_dir_src, dorm_mem_dir_dst):
        val = self.get_mem(mem_dir_src)
        self.set_dorm_mem_w_val(dorm_mem_dir_dst, val)

    def malloc_dormant(self, func_id):
        cpu_var_counter, gpu_var_counters = self.func_dir[func_id][0], self.func_dir[func_id][2]
        mem = [
            [None] * cpu_var_counter,
            torch.empty(gpu_var_counters["GPU_INT_T"], dtype=torch.int64, device=DEVICE),
            torch.empty(gpu_var_counters["GPU_FLOAT_T"], dtype=torch.float64, device=DEVICE),
            torch.empty(gpu_var_counters["GPU_BOOL_T"], dtype=torch.bool, device=DEVICE),
        ]
        self.dormant_mem_stack[func_id].append(mem)
        return self.dormant_mem_stack[func_id]

    def era_func_stack(self, func_id):
        self.malloc_dormant(func_id)
        const_dicts = self.func_dir[func_id][1]
        for _, consts in const_dicts.items():
            for val, mem_dir in consts:
                self.set_dorm_mem_w_val(mem_dir, val)

    def start_func_stack(self, func_id):
        self.mem_stack[func_id].append(self.dormant_mem_stack[func_id].pop())        

    def end_func_stack(self, func_id):
        self.mem_stack[func_id].pop()

def bin_op(q, mem, op):
    mem.set_mem_w_val(q[3], op(mem.get_mem(q[1]), mem.get_mem(q[2])))

def assig_op(q, mem):
    mem.set_mem_w_mem(q[1], q[3])

def verify_op(q, mem):
    index_val = mem.get_mem(q[3])
    limit = mem.get_mem(q[1]) 
    if  index_val >= limit:
        raise Exception(f"Out of bounds: tensor index with value {index_val} must be lower than {limit}")

def parse_input(input, type_str):
    if type_str in ['INT_T', 'GPU_INT_T']:
        return int(input)
    elif type_str in ['FLOAT_T', 'GPU_FLOAT_T']:
        return float(input)
    elif type_str in ['BOOL_T', 'GPU_BOOL_T']:
        return input == "True"
    else: # string
        return input

def recursive_assign(mem: MemoryManager, mem_dir_dst, data, type,  dims):
    assert len(data) == dims[0]
    for item in data:
        if isinstance(item, list):
            mem_dir_dst = recursive_assign(mem, mem_dir_dst, item, type, dims[1:] )
        else:
            mem.set_mem_w_val(mem_dir_dst, parse_input(item, type))
            mem_dir_dst = (mem_dir_dst[0], mem_dir_dst[1] + 1, mem_dir_dst[2], mem_dir_dst[3])
    return mem_dir_dst

def read(mem: MemoryManager, q, input):
    if len(q[1]) > 1: # has tensor dims
        recursive_assign(mem, q[3], eval(input), q[1][0], q[1][1:])
    else:
        mem.set_mem_w_val(q[3], parse_input(input, q[1][0]))

def create_tensor_from_dims(mem: MemoryManager, mem_dir, dims):
    t = []
    if len(dims) > 1:
        for i in range(0, dims[0]):
            item, mem_dir = create_tensor_from_dims(mem, mem_dir, dims[1:])
            t.append(item)
    else:
        for d in range(0, dims[0]):
            t.append(mem.get_mem(mem_dir))
            mem_dir = (mem_dir[0], mem_dir[1]+1, mem_dir[2], mem_dir[3])
    return t, mem_dir

def write_to_file(mem: MemoryManager, q):
    filename = mem.get_mem(q[3])
    f = open(filename, "w")
    if q[2] != None: # has tensor dimensions
        data, m = create_tensor_from_dims(mem, q[1], q[2])
    else:
        data = mem.get_mem(q[1])
    f.write(str(data))

def print_op(q, mem):
    if len(q[3]) == 2: # tensor dims provided
        data, m = create_tensor_from_dims(mem, q[3][0], q[3][1])
        print(data)
    else:
        val = mem.get_mem(q[3])
        if type(val) == torch.Tensor:
            if val.dim() == 0:
                print(f"GPU({val.item()})")
                return
        print(val)

def run_func(mem : MemoryManager, quads, q_idx):
    basic_op_handler = {
        "ASSIG" : lambda q : assig_op(q, mem),
        "PARAM" : lambda q : mem.set_dorm_mem_w_mem(q[1], q[3]),
        "PLUS" : lambda q : bin_op(q, mem, lambda x,y:x+y) 
                                if q[2] != None else 
                            mem.set_mem_w_val(q[3], 1 * mem.get_mem(q[1])),
        "MINUS" : lambda q : bin_op(q, mem, lambda x,y:x-y)
                                if q[2] != None else
                            mem.set_mem_w_val(q[3], -1 * mem.get_mem(q[1])),
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
        "PRINT" : lambda q : print_op(q, mem),
        "VERIFY": lambda q : verify_op(q, mem),
        "READ_LINE": lambda q : read(mem, q, input())
    }
    try: 
        while(q_idx < len(quads)):
            q = quads[q_idx]
            q_op = q[0]
            nxt_q_idx = q_idx + 1
            # block special quads
            if q_op == "GOTO":
                nxt_q_idx = q[3]
            elif q_op == "GOTOF":
                if(not mem.get_mem(q[1])):
                    nxt_q_idx = q[3]
            elif q_op == "STRTBLK":
                mem.era_func_stack(q[3])
                mem.start_func_stack(q[3])
            elif q_op == "ENDBLK":
                mem.end_func_stack(q[3])
            # function special quads
            elif q_op == "ERA":
                mem.era_func_stack(q[3])
            elif q_op == "GOSUB":
                mem.start_func_stack(q[3])
                run_func(mem, quads, q[1])
                mem.end_func_stack(q[3])
            elif q_op == "RETURN":
                assig_op(q, mem)
                break
            elif q_op == "ENDFUNC":
                break
            elif q_op == "READ_FILE":
                filename = mem.get_mem(q[2])
                f = open(filename, 'r')
                data = f.read()
                read(mem, q, data)
            elif q_op == "WRITE_FILE":
                write_to_file(mem, q)
            else:
                basic_op_handler[q_op](q)
            q_idx = nxt_q_idx
    except Exception as e:
        raise Exception(f"Error executing op: {q_idx} - {quads[q_idx]}") from e

def run_global(func_dir, quads):
    memory_manager = MemoryManager(func_dir)
    memory_manager.era_func_stack(0)
    memory_manager.start_func_stack(0)
    run_func(memory_manager, quads, 0)
    memory_manager.end_func_stack(0)

def setup_device():
    global DEVICE
    if len(argv) > 2:
        DEVICE = argv[2]
        alowed_devs = ["cuda", "cpu"]
        if DEVICE not in alowed_devs:
            raise Exception(f"Error with device: {DEVICE} not in {alowed_devs}")
    if torch.cuda.is_available():
        DEVICE = "cuda"
    else:
        DEVICE = "cpu"
    print("CUDA device not found. Using CPU for GPU operations)." + 
        "\nNote this is still faster due to vectorization.\n")

def main():
    filename = argv[1]
    with open(filename, "r") as ir_file:
        ir = ir_file.read()
        compiler_dict = json.loads(ir)
    func_dir = compiler_dict["func_dir"]
    quads = compiler_dict["quads"]
    setup_device()
    run_global(func_dir, quads)

if __name__ == '__main__':
    main()
