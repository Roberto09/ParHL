from .parhl_exceptions import ParhlException

def _produce_all_same(prod_type, but={}):
    return {t: prod_type for t in ['INT_T', 'FLOAT_T', 'BOOL_T', 'STRING_T', 'GPU_INT_T', 'GPU_FLOAT_T', 'GPU_BOOL_T']
            if t not in but}

class SemanticCube():
    def __init__(self):
        """
        - Combinations producing ERROR are ommited
        """
        basic_bool_ops_bin = {
            'BOOL_T':{
                'BOOL_T':'BOOL_T',
                'GPU_BOOL_T':'GPU_BOOL_T',
            },
            'GPU_BOOL_T':{
                'BOOL_T':'GPU_BOOL_T',
                'GPU_BOOL_T':'GPU_BOOL_T',
            },
        }
        basic_arithmetic_ops_bin = {
           'INT_T': {
                'INT_T':'INT_T',
                'FLOAT_T':'FLOAT_T',
                'GPU_INT_T':'GPU_INT_T',
                'GPU_FLOAT_T':'GPU_FLOAT_T',
            },
            'FLOAT_T': {
                'INT_T':'FLOAT_T',
                'FLOAT_T':'FLOAT_T',
                'GPU_INT_T':'GPU_FLOAT_T',
                'GPU_FLOAT_T':'GPU_FLOAT_T',
            },
            'GPU_INT_T': {
                'INT_T':'GPU_INT_T',
                'FLOAT_T':'GPU_FLOAT_T',
                'GPU_INT_T':'GPU_INT_T',
                'GPU_FLOAT_T':'GPU_FLOAT_T',
            },
            'GPU_FLOAT_T': {
                'INT_T':'FLOAT_T',
                'FLOAT_T':'FLOAT_T',
                'GPU_INT_T':'GPU_FLOAT_T',
                'GPU_FLOAT_T':'GPU_FLOAT_T',
            } 
        }
        basic_arithmetic_ops_un = {
            'INT_T':'INT_T',
            'FLOAT_T':'FLOAT_T',
            'GPU_INT_T':'GPU_INT_T',
            'GPU_FLOAT_T':'GPU_FLOAT_T',
        }
        basic_equality_ops_bin = {
            'INT_T': _produce_all_same('BOOL_T', but={'GPU_BOOL_T', 'GPU_FLOAT_T', 'GPU_INT_T', 'STRING_T'}) | {
                'GPU_INT_T': 'GPU_BOOL_T',
                'GPU_FLOAT_T': 'GPU_BOOL_T',
                'GPU_BOOL_T' : 'GPU_BOOL_T',
            },
            'BOOL_T': _produce_all_same('BOOL_T', but={'GPU_BOOL_T', 'GPU_FLOAT_T', 'GPU_INT_T', 'STRING_T'}) | {
                'GPU_INT_T': 'GPU_BOOL_T',
                'GPU_FLOAT_T': 'GPU_BOOL_T',
                'GPU_BOOL_T' : 'GPU_BOOL_T',
            },
            'FLOAT_T': _produce_all_same('BOOL_T', but={'GPU_BOOL_T', 'GPU_FLOAT_T', 'GPU_INT_T', 'STRING_T'}) | {
                'GPU_INT_T': 'GPU_BOOL_T',
                'GPU_FLOAT_T': 'GPU_BOOL_T',
                'GPU_BOOL_T' : 'GPU_BOOL_T',
            },
            'STRING_T': {
                'STRING_T' : 'BOOL_T',
            },
            'GPU_INT_T':_produce_all_same('GPU_BOOL_T', 'STRING_T'),
            'GPU_FLOAT_T':_produce_all_same('GPU_BOOL_T', 'STRING_T'),
            'GPU_BOOL_T':_produce_all_same('GPU_BOOL_T', 'STRING_T'),
        }
        basic_comp_ops_bin = {
            'INT_T':{
                'INT_T':'BOOL_T',
                'FLOAT_T':'BOOL_T',
                'GPU_INT_T':'GPU_BOOL_T',
                'GPU_FLOAT_T': 'GPU_BOOL_T', 
            },
            'FLOAT_T':{
                'INT_T':'BOOL_T',
                'FLOAT_T':'BOOL_T',
                'GPU_INT_T':'GPU_BOOL_T',
                'GPU_FLOAT_T': 'GPU_BOOL_T', 
            },
            'GPU_INT_T':_produce_all_same('GPU_BOOL_T', but={'BOOL_T', 'GPU_BOOL_T', 'STRING_T'}),
            'GPU_FLOAT_T':_produce_all_same('GPU_BOOL_T', but={'BOOL_T', 'GPU_BOOL_T', 'STRING_T'}),
        }

        self.semantic_cube = {
            "OR_BIN": basic_bool_ops_bin,
            "AND_BIN": basic_bool_ops_bin,
            "NOT_UN": {
                'BOOL_T':'BOOL_T',
                'GPU_BOOL_T':'GPU_BOOL_T'
            },
            'PLUS_BIN': basic_arithmetic_ops_bin | 
                {'STRING_T': {
                    'STRING_T':'STRING_T',
                }},
            'PLUS_UN': basic_arithmetic_ops_un,
            'MINUS_BIN': basic_arithmetic_ops_bin,
            'MINUS_UN': basic_arithmetic_ops_un,
            'DIV_BIN': basic_arithmetic_ops_bin,
            'MMULT_BIN': basic_arithmetic_ops_bin,
            'MULT_BIN': basic_arithmetic_ops_bin,
            'EXP_BIN': basic_arithmetic_ops_bin,
            'MOD_BIN': {
                'INT_T':{
                    'INT_T':'INT_T',
                    'GPU_INT_T':'GPU_INT_T'
                },
                'GPU_INT_T':{
                    'INT_T':'GPU_INT_T',
                    'GPU_INT_T':'GPU_INT_T'
                }
            },
            'EQ_BIN': basic_equality_ops_bin,
            'NOT_EQ_BIN': basic_equality_ops_bin,
            'ASSIG_BIN': {
                'INT_T':_produce_all_same('INT_T', but={'BOOL_T', 'GPU_BOOL_T', 'STRING_T'}),
                'BOOL_T':{
                    'BOOL_T':'BOOL_T',
                    'GPU_BOOL_T':'BOOL_T',
                },
                'FLOAT_T':_produce_all_same('FLOAT_T', but={'BOOL_T', 'GPU_BOOL_T', 'STRING_T'}),
                'STRING_T':{
                    'STRING_T':'STRING_T',
                },
                'GPU_INT_T':_produce_all_same('GPU_INT_T', but={'BOOL_T', 'GPU_BOOL_T', 'STRING_T'}),
                'GPU_FLOAT_T':_produce_all_same('GPU_FLOAT_T', but={'BOOL_T', 'GPU_BOOL_T', 'STRING_T'}),
                'GPU_BOOL_T':{
                    'BOOL_T':'GPU_BOOL_T',
                    'GPU_BOOL_T':'GPU_BOOL_T',
                },
            },
            'GT_BIN': basic_comp_ops_bin,
            'LT_BIN': basic_comp_ops_bin,
            'GEQT_BIN': basic_comp_ops_bin,
            'LEQT_BIN': basic_comp_ops_bin,
        }

    def raise_type_error(t_arg1, operator, t_arg2=None):
        if t_arg2 is not None:
            raise ParhlException(f"Unsupported binary operation {t_arg1} {operator} {t_arg2}")
        raise ParhlException(f"Unsupported unary operation {operator} {t_arg1}")

    def get_type(self, operator, t_arg1, t_arg2=None):
        try:
            if t_arg2 is not None:
                return self.semantic_cube[f"{operator}_BIN"][t_arg1][t_arg2]
            return self.semantic_cube[f"{operator}_UN"][t_arg1]
        except:
            SemanticCube.raise_type_error(t_arg1, operator, t_arg2)
