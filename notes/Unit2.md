# Adders

## How to implement Adder?

### Half Adder (1-bit adder)

            -----------------
a ----->    |               |   -----> out
            |   Half Adder  |
b ----->    |               |   -----> carry
            -----------------

It all start will half adder, which is the operation of adding 2 bits. Here is the flow:
a + b = out | carry, where a, and b are both binary numbers.

And here is the trueth table on half adder:
| a | b | out | carry|
| 0 | 0 | 0   | 0    |
| 0 | 1 | 1   | 0    |
| 1 | 0 | 1   | 0    |
| 1 | 1 | 0   | 1    |

It is obvious that the table can be constructed with XOR and AND gates.

### Full Adder

Full adder is more complete than half adder which takes 3 bits as input:
                -----------------
a     ----->    |               |   -----> out
carry ---->     |   Full Adder  |
b     ----->    |               |   -----> carry
                -----------------

With full adder, it can be possible to construct the 16-bit adder in a loop:
Example:
???????? ?????011
???????? ?????010

step 1:
a = 1, b=0 ; carry=0
out=a+b+carry=1+0+0

carry=0, out=1

???????? ?????011
???????? ?????010
->
???????? ???????1

step 2:
a = 1, b=1, carry=0
out=a+b+carry=1+1+0

carry=1, out=0

???????? ?????011
???????? ?????010
->
???????? ??????01

step 3:
a = 0, b=0, carry=1
out=a+b+carry=0+0+1

carry=0, out=1

???????? ?????011
???????? ?????010
->
???????? ?????101

### Negtive numbers - 2's complement
In previous shcool class, negtive numbers are represented with sign bit. It changes the MSB to 1, like:
0000 0001 -> 1
1000 0001 -> -1

But sign bit has some problems:
1. There will be -0, like 1000 0000, which is invalid.
2. Implementation needs to handle different cases.

In real machine, 2's complement is used to represent negtive numbers.
2's complement: negtive number = positive number - 2^n
Take 4-bit as instance, n=4, 2^n=16:
binary  | decimal | negtive

0000    |   0     |
0001    |   1     |
0010    |   2     |
0011    |   3     |
0100    |   4     |
0101    |   5     |
0110    |   6     |
0111    |   7     |
1000    |   8     | 8-16 =  -8
1001    |   9     | 9-16 =  -7
1010    |   10    | 10-16 = -6
1011    |   11    | 11-16 = -5
1100    |   12    | 12-16 = -4
1101    |   13    | 13-16 = -3
1110    |   14    | 14-16 = -2
1111    |   15    | 15-16 = -1

#### Cons on 2's complement

Add (+) function on negtive numbers is "free"
Example: (-4) + (-7)

(-4) is represented as (+12), the binary is 1100
(-3) is represented as (+13), the binary is 1101

1100 + 1101 = 1 1001 the MSB is overflowed. Just drop it, and the result is 1001(9), which is representing (-7). And (-7) is the exact answer for (-4) + (-3)

#### Quick method representing -x in theory
With input x, how to quickly represent -x?
Formula: -x = (2^n - 1) - x + 1

Example: 4-bit, n=4
-7 = 2^4 - 1 - 7 + 1 = 10000 - 1 - 0111 + 0001 = 1111 - 0111 + 0001 = 1001
1001 represent -7 in 2's complement

#### Quick method representing -x in implementation of ALU
(2^N - 1 is all 1's bit array in N dimension, 2^n - 1 = NOT(0))
Here is a hidden theory in 2's complement: x + NOT(x) = 2^n - 1 -> 
Thus, there comes an important transformation: 2^n - 1 - x = NOT(x)

And (2^n - 1) - x + 1 is representing -x in 2's complement

Therefore,
-x = (2^n - 1) - x + 1
   = (2^n - 1) - (x - 1)
   = NOT(x - 1)

So, by getting x - 1 and performing NOT operation on it, the -x can be retrieved.

In ALU's implementation, how to get (x - 1) by "NOT" and "ADD" ?
In 2's complement, it can be done by adding 2^n on it without changing its value:
```2^n + x - 1```

2^n + x - 1
    = x + 2^n - 1
    = 2^n - 1 + x
    = 2^n + x - 1

Since x can never exceed the 2^n, 2^n + x - 1 is actually (2^n + x - 1) mod 2^n:
(2^n + x - 1) mod 2^n
    = 0 + x - 1
    = x - 1
-> x - 1 = 2^n + x - 1

So, in ALU's implementation, -x can be transformed, with (2^n - 1) denoting NOT(0):
-x = (2^n - 1) - x + 1
   = (2^n - 1) - (x - 1)
   = NOT(x - 1)
   = NOT(2^n + x - 1)
   = NOT(2^n - 1 + x)
   -> NOT(NOT(0) ADD x)

Example:

// Compute -x
set zx 0,
set nx 0,
set zy 1,
set ny 1, // get all 1's N array -> 2^n - 1
set f  1, // perform x + 2^n - 1
set no 1, // perform NOT(x + 2^n - 1)

1 - 1 = 0 = 0000
NOT(0) = 1111 = -1

Similarly, x - y can be represented as NOT(NOT(x) + y):
x - y = 2^n - 1 - 2^n + 1 + x - y
      = 2^n - 1 - (2^n - 1 - x + y)
      = NOT(2^n - 1 - x + y)
      = NOT(NOT(x) + y)
      -> NOT(NOT(x) ADD y)

And y - x can be represented as NOT(NOT(y) + x):
y - x = 2^n - 1 - 2^n + 1 + y - x
      = 2^n - 1 - (2^n - 1 - y + x)
      = NOT(2^n - 1 - y + x)
      = NOT(NOT(y) + x)
      -> NOT(NOT(y) ADD x)

There is a quicker way to accomplish +1 in the formula:
???? + 0001 -> ? + 1 : if ? is 1, carry=1, and move to next position; is ? is 0, carry=0, out=1 stop the process.

### ALU - arithmetic logic unit
The ALU chip contains both arithmetic and logic computations.
The diagram of the ALU can be presented as below:

zx: zero operation on x
nx: negate operation on x
zy: zero operation on y
ny: negate operation on y
f: if f=1 do x+y; else if f=0 do x&y
no: negate the out result

            zx nx zy ny f no

            |  |  |  |  |  |

            |\
x ---->     | \
            |   - -
            | ALU  | ----> out
            |   - -
y ---->     | /
            |/
             |    |
            \|/  \|/
            zr    ng

zr: if the out is all-zero value, zr=1, else zr=0
ng: if the out is negtive value(<0), ng=1, else ng=0

### Questions/Perspectives
- What about (-7) + (-8) in 2's complement? Overflow?