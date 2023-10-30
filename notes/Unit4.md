# Machine language

# Overview
Instructions are set of 10101011101, which is meaningless for human.
The assembly language is used to interpret symbols to instructions.

## Basic elements
- Memory
Need to suply a long address.
Accessing memory is expensive.
Memory hierachy (solution)

- Registers (inside CPU)
1. Data register like R1, R2 to store data
2. Address register, like store R1, @A

- Flow control
unconditional jump:
Like jump, goto, they are the unconditional.

conditional jump:
JGP R1, 0, cont -> jump to cont when R1>0

## Hack computer (16-bit computer)

### Basic elements
The 16-bit computer consists of
RAM: A sequence of 16-bit registers, RAM[0], RAM[1], RAM[2]
ROM(Instruction Memory): A sequence of 16-bit registers, ROM[0], ROM[1], ROM[2]
CPU: Performs 16-bit instructions.
Buses: Instruction bus, data bus, address bus.

A registers - Holds address either data
D registers - Holds data
M registers - holds memory represents the register selected by A

### Instructions
1. A-instruction
2. C-instruction

### Control
1. Reset button is used once a program is performed

### A-instruction (Addressing)
Example: @21
Sets A register to 21.
The binary value of the symbol is 0 000000000010101
The value is contained in last 15-bit, while the 16th bit is the op code, which mean it is A-instruction or C-instruction.

//Set RAM[100] to -1
@100 // A=100
M=-1

### C-instruction (Control)
dest = comp ; jump

"dest = ": destination
"comp": compute
"jump": jump to some address of memory

1          1 1          a(select mode) c1 c2 c3 c4 c5 c6     d1 d2 d3        j1 j2 j3
|           |                                   |                 |               |
op code    not used                         comp bits          dest bits      jump bits

### Input / Output

- Screen
Screen memory map. The display is refreshed from the memory map, which maps memory to its pixels. So, by manipulating the memory map, the content is changed accordingly.
Example of 256x512 screen is mapped to 8192 16-bit values, where each value is a "word".

- Keyboard
Key board memory map, which requires only 16-bit register.

### How to terminate a program properly?
Make an infinite loop.
Example:
@6
0;JMP

### How exactly a device is connected to CPU and how it works?
Typically, each device has a controller which connects to buses and connects to CPU(coprocessor).

The buses will be like PCI, USB, I2C, GPIO.

Initially, when device is connect to buses, CPU and the device controller will communicate with each other and configurate the bus.

The CPU will then write/read bytes to device controller and the controller will read/write data received from bus to its own registers.

How the bus work? There are usually a CLK, DAT line connected to the device, physically. CPU can pull/drop the voltage of the line to negotiate the communication protocol, and transmit data using the protocol.

How does CPU control the device?
1. Port-mapped
Port-mapped method maps devices registers into a separate memory space apart from the main memory. CPU will send perform instructions on this separate memory to change register values on the devices.
2. Memory-mapped
Memory-mapped method uses same address space just inside main memory, so CPU can use universal instructions to manipulate the device registers mapped in main memory.

Some perspectives:

DO NOT get confused by the course, CPU are not connected to monitors/keyboards directly. Device like controllers inside CPU get memory mapped. CPU and its controllers are connected with external peripherals by buses.

|----------------------|
|    CPU               |
|                      |
|   Memory             |
|                      |
|    /|\               |
|     |(Memory-mapped) |          <----->  | BUS, like I2C, PCI, GPIO, etc| <-----> devices
|     |                |
|   controllers(IP)    |
|----------------------|

How device registers are mapped to CPU?

Memory mapped IO usually refers to peripherals INSIDE the mcu that are all connected on the parallel bus. Ie the I2C hardware peripherals registers are memory mapped but the device connected externally through I2C is not.

Typically, device registers are mapped to its own on board RAM. And its MCU will perform instructions to retrieve/manipulate the registers by accessing its own RAM.
And if CPU wants to communicate with device through a bus, CPU will just manipulate its usb controller internally to send bus commands to the device and the bus controller is mapped to main memory so CPU can get wanted data from memory. There is bus between host and devices.

So, inside a computer, host can map devices to memory-map and use instructions to manipulate them directly or use bus.

NOT confusing it with memory-mapped files.

1. Memory-mapped registers
In short words, memory mapped registers are just actual registers in memory.
How to use this register to control I/O? like LED?
https://www.youtube.com/watch?v=aT5XMOrid7Y

The device registers are assigned with memory addresses, in microprocessor's memory space.
        Main memory
        ----------
        Register 0
        Register 1
CPU <-> Register 2
        Register 3
        (Reserved for GPIOA)
        Register 4
        (Reserved for GPIOB)
        Register 5
        (Reserved for I2C controller)
            ...             ...... etc
        reserved
        ----------
        Other regs

By manipulating reg3, it is about to pull high/low on GPIOA.
By manipulating reg4, it is about to pull high/low on GPIOB.
By manipulating reg5, it is about to issuing signal on I2C_CLK I2C_DAT.

And devices behind GPIOA, GPIOB, I2C are receiving signals through those buses.