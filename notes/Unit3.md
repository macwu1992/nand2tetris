# Memory Roadmap

## Combinational Logic VS Sequential Logic

t represent time.

Combinational Logic
out[t] = f[t](input)

Sequential Logic
out[t] = f[t-1](intput)

The benefit of sequential logic:
1. There is latency on the output from the electornic perspectives.
2. The output and input can be stored in one bit, but the bit changes by time. (Q: How?  A: Use flip flop chip, load input, and mux chip.)

## Flip Flop
The "Flip Flop" can be change to either "0" or "1", to store the information at "t" timestamp.
This is the basic where loop can be implemented, like memory or counter.

The output of flip flop is the calculation result of t-1 timestamp.

Difference between flip flop and latch: latch is combinational logic and flip flop is sequential logic.

### reference
1. [Flip flop explain](https://www.electronicsforu.com/technology-trends/learn-electronics/flip-flop-rs-jk-t-d)

## 1-bit register / multi-bit register
How to store bit data using flip flop? The below diagram shows:
                load
                 |
                 |
                \|/
             |------------|       |----------------|
input -----> | Mux        | ----> | Data Flip Flop | ----> output
    |------> |------------|       |----------------|         |
    |                                                        |
    |                                                        |
    ---------------------------------------------------------|

## RAM implementation with register

RAM = Random Access Memory.
Q: How the random feature is implemented? How to find register using address instantly?

                        load
                         |
                         |
                        \|/
              |-----------------------|
              |   ------------        |
              |   | Register |        |
input   ----> |   ------------        |
              |   ------------        |
              |   | Register |        | ----> out
              |   ------------        |
address ----> |   ------------        |
              |   | Register |        |
              |   ------------        |
              |       ...             |
              |   ------------        |
              |   | Register |        |
              |   ------------        |
              |-----------------------|

## Conuter

Property: self-increamental

PC = program counter

3 control operations for counter:
1. Reset
2. Next(Increase)
3. Goto

Counter definition in other way:
Counter is the chip supporting 3 basic control operations.

Q: Where counters come to play?
A: The counters are the index of instruction sequence, like a cooking recipe. Step 1, step2, ... step n. And 1, 2, 3 ..., n are counters.

The diagram of counter:
                      load   inc  reset
                        |     |     |
                        |     |     |
                       \|/   \|/   \|/
                   |----------------------|
input(16bit) ----> | PC = program counter | ----> output(16bit)
                   |----------------------|

3 basic operations respectively
1. reset = reset
2. inc = Next
3. load = Goto

## Question:
1. How to construct Flip-Flop from basic Nand gates?
Use 2 Nand gates, and wire them as loop. (SR flip flop)

S -------------->|-------\
                 | Nand   |----
          |----->|-------/    |
          |                  |
          |                  |----------input_a ----> |-------\
          |                                           | Nand   | ----> output_a
          |                                  ------>  |-------/           |
          |                                  |                            |
          |                                  |                            |
          |                             -----(----------------------------|
CLK ------|                              |   |
          |                              |   |
          |                              |    ---------------------------|
          |                              |                               |
          |                              ----------> |-------\           |
          |                                          | Nand   | ----> output_b
          |                  |---------input_b ----> |-------/
          |                  |
          |----->|-------\     |
                 | Nand   |----
R -------------->|-------/

For D-flipflop, here is the implementation:
The output_a is synced with D only on clock rising edge. Once synced, it will be consistant. The output_b is inverted bit of output_a.
D -------------------->|-------\
    |                  | Nand   |----
    |           |----->|-------/    |
    |           |                   |
    |           |                   |----------input_a ----> |-------\
    |           |                                            | Nand   | ----> output_a
    |           |                                   ------>  |-------/           |
    |           |                                   |                            |
    |           |                                   |                            |
    |           |                              -----(----------------------------|
    |           |                              |    |
    |           |                              |    |
  -----         |                              |    ---------------------------|
   \ /          |                              |                               |
    |           |                              ----------> |-------\           |
    |           |                                          | Nand   | ----> output_b
    |           |                  |---------input_b ----> |-------/
    |           |                  |
    |-----------(----->|-------\   |
                |      | Nand   |---
CLK ------------------>|-------/

2. How to implement Bit.hdl?
In HDL, do not think the lines are code, think them as wires to connect chips instead.
Bit chip's diagram is as below:

1-bit register:
If load[t] == 1 then out[t+1] = in[t]
                else out does not change (out[t+1] = out[t])

                      load
                       |
                       |
                      \|/
                     |----\
                     |     \
        in     ----> |      |              |------------|
                     | Mux  | muxOut ----> |   DFF      | ----|----> out
        dffOut ----> |      |              |------------|     |
         /|\         |     /                                  |
          |          |----/                                   |
          |                                                   |
          ----------------------------------------------------|