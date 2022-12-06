# PARHL

## To start conda:

```
$ conda env create -f environment.yml
$ conda activate parhl
```

## To test

```
$ pytest
```

# PARHL USER MANUAL
**In this section we reference the file ./user_manual.parhl file.**

## CPU Variable Declaration:
Code:
```
let x : int := 5
let y : float := 2.91
let z : bool
z := True
let q : string := "parhl string!"
```

## GPU Variable Declaration:
Code:
```
let g_x : gpu_int := 8
let g_y : gpu_float := 3.14, g_z : gpu_bool := False
```

## Tensor Declatation (GPU and CPU):
Code:
```
let tens_x[2][3] : int := [[1, 2, 3], [4, 5, 6]]
let tens_g_y[2][2] : gpu_float := [[1.5, 2.1], [3.14, 2.91]]
let tens_g_z[2] : gpu_bool := [True, False]
let tens_q[1][2] : string := [["parhl", "tensor"]]
```

## Operations With Primitives:
Code:
```
x := 10

let x1 : int := x + 3 * 5 ^ 2 / 2.5 + y + (x%2)
let g_x2 : gpu_float := x + 3 * 5 ^ 2 / 2.5 + g_y + (x%2)
let x3 : bool := (not (z and False) or True) = False and True
let g_x4 : gpu_bool := x1 >= g_x2 and x3 or (x1 < g_x2 and g_x <> x)
let x5 : string := q + " concatenated";

print(x, "\n")
print(x1, "\n")
print(g_x2, "\n")
print(x3, "\n")
print(g_x4, "\n")
print(x5, "\n")
```
Stdout:
```
10
42
GPU(43.14)
False
GPU(True)
parhl string! concatenated
```

## Operations With Tensors:

Here we would like to note some of the interesting features of the compiler as we allow special operations with tensors:
- We can do matrix multiplication of 2 tensors using the ** operator.
- We can do elementwise multiplication of 2 tensors using the * operator.
- We can raise matrices to a given integer scalar by using the ^ operator
- In general we can do all elementwise operations among tensors such as +, -, /, %, *, as long as the dimensions of this tensors allow it.

Code:
```
tens_g_y[0][0] := 3
let tens_g_y1[2][2] : gpu_float := tens_g_y ^ 3
let tens_g_y2[2][3] : gpu_float := tens_g_y1 ** [[1.0, 2.3, 3.2], [-5.1, 2.8, 3.9]]
let tens_y3[2][1] : int := tens_x ** [[1],[2],[3]] + [[1000], [2000]]

print(g_y, "\n")
print(tens_g_y1, "\n")
print(tens_g_y2, "\n")
print(tens_y3, "\n")
```
Stdout:
```
GPU(3.14)
GPU([[85.75254000000001, 68.86341000000002], [102.967194, 82.80125100000001]])
GPU([[-265.45085100000006, 390.04839000000004, 542.9754270000001], [-319.3191861, 468.668049, 652.4198997000001]])
[[1014], [2032]]
```

### Broadcasting:

Broadcasting allows us to do interesting stuff with tensors of different dimensions:
- In general the rules for broadcasting that we follow, given our Pytorch backend are: https://pytorch.org/docs/stable/notes/broadcasting.html
- Exmaples are listed below

Code:
```
let tens_y4[2][2] : int := [1000, 2000] + [[1, 2], [3, 4]]
let tens_y5[2][2] : bool := tens_y4 <= 100000
let tens_y6[2][2]: gpu_bool := tens_g_z or [[True, False], [False, True]]

print(tens_y4, "\n")
print(tens_y5, "\n")
print(tens_y6, "\n")
```
Stdout:
```
[[1001, 2002], [1003, 2004]]
[[True, True], [False, False]]
GPU([[True, False], [True, True]])
```


## Conditionals:
Code:
```
if(True){
    print("We got True", "\n")
}
else {
    print("We got False", "\n")
}

if(tens_y6[0][0]){
    print("tens_y6[0][0] is True", "\n")
}
else if((not tens_y6[0][0] and False) or True){
    print("not tens_y6[0][0] and False) or True \t evaluated to: True", "\n")
}
```
Stdout:
```
We got True
tens_y6[0][0] is True
```

## Loops:
Code:
```
let i : int := 0
while(i < 5){
    # do whatever you want here
    print("i is worth: ", i, "\n")
    i := i+1
}

for(let i[2][2] : gpu_int := [[0, 1], [2, 3]]; i <= 50; i := i ** i){
    # do whatever you want here
    print("i is worth:", i, "\n")
}

for(let i : int := 0; i < 2; i := i+1){
    for(let j : int := 0; j < 2; j := j+1){
        print("tens_g_y1[", i, "]","[", j, "] =", tens_g_y1[i][j], "\n")
    }
}
```
Stdout:
```
i is worth: 0
i is worth: 1
i is worth: 2
i is worth: 3
i is worth: 4

i is worth:GPU([[0, 1], [2, 3]])
i is worth:GPU([[2, 3], [6, 11]])

tens_g_y1[0][0] =GPU(85.75254000000001)
tens_g_y1[0][1] =GPU(68.86341000000002)
tens_g_y1[1][0] =GPU(102.967194)
tens_g_y1[1][1] =GPU(82.80125100000001)
```


## Functions:
Code:
```
let gpu_fibo (n : int) : void {
    let nested_func(n : int) : gpu_float {
        print("inner scope n =", n, "\n")
        return 3.14
    }
    print(nested_func(123), "\n")
    let fib_init[1][2] : gpu_int := [[1, 0]]
    let fib_matr[2][2] : gpu_int := [[1, 1], [1, 0]] 
    let res[1][2] : gpu_int := fib_init ** (fib_matr ^ n)
    print("fibo(", n, ") = ", res[0][1], "\n")
}
gpu_fibo(10)

let plain_old_rec_fibo (n : int) : int {
    if(n <= 1){
        return 1
    }
    return plain_old_rec_fibo(n-1) + plain_old_rec_fibo(n-2)
}
let fibo_10 : int := plain_old_rec_fibo(10)
print("plain_old_rec_fibo(", 10, ")=", fibo_10, "\n")
```
Stdout:
```
inner scope n =123
GPU(3.14)
fibo(10) = GPU(55)
plain_old_rec_fibo(10)=89
```

## Special IO Functinos

Code:
```
print("doing a print", "\n")
```
Stdout:
```
print("doing a print", "\n")
```

</br>

Code:
```
let tens_readline[2][2] : float := read_line(float[2][2])
print(tens_readline, "\n")
```
Stdin:
```
[[1.1, 1.2],[1.3,1.4]]
```
Stdout:
```
[[1.100000023841858, 1.2000000476837158], [1.2999999523162842, 1.399999976158142]]
```

</br>

Code:
```
let prim_readline : int := read_line(int)
print(prim_readline, "\n")
```
Stdin:
```
3
```
Stdout:
```
3
```


</br>

Code:
```
write_file("my_output_file", tens_readline)
```
my_output_file:
```
[[1.100000023841858, 1.2000000476837158], [1.2999999523162842, 1.399999976158142]]
```


</br>

Code:
```
let tens_readfile[3][3] : gpu_bool := read_file(bool[3][3], "my_input_file")
print(tens_readfile, "\n")
```
my_input_file:
```
[[True, False, True], [False, True, False], [True, True, True]]
```
Stdout:
```
GPU([[True, False, True], [False, True, False], [True, True, True]])
```
