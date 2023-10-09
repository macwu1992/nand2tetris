# Introductions

## Keynotes

## Unit1.1 - Unit1.3
Basic logic gates:
NOT
AND
OR

All calculations can be composed by basic logic gates.

NAND is constructed from basic logic gates.

NAND(x, y) = NOT(And(x, y))

Proof:
1. NOT
NOT(x) = NAND(x,x)
Since NAND is NOT(AND()), then the equation becomes:
NOT(x) = NOT(AND(x,x))
       = NOT(x)

2. AND
AND(x, y) = NOT(NAND(x,y))
          = NOT(NOT(AND(x,y)))
          = AND(x,y)

3. OR
OR(x,y) = NOT(AND(NOT(x),NOT(y)))
        = OR(NOT(NOT(x)), NOT(NOT(y)))
        = OR(x, y)

All basic logic gates can be transformed to NAND. And all calculations can be composed by basic logic gates. Thus, using only NAND can represent all calculations.

## Unit 1.4

HDL = Hardware Description Language

HDL Example: XOR(x,y) = OR(AND(x, NOT(y)), AND(NOT(x), y))
```
/** Xor gate: out = ((a And Not(b)) Or (Not(a) And b)) */
CHIP Xor {
    IN a, b;
    OUT out;

    PARTS:
    Not(in=a, out=nota);
    Not(in=b, out=notb);
    And(a=a, b=notb, out=aAndNotb);
    And(a=b, b=nota, out=bAndNota);
    Or(a=aAndNotb, b=bAndNota, out=out);
}

```