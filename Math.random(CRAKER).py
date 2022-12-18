# In front of you is a program that can predict a consecutive values of Math.random() in any given conditions and in any
# web agent, you choose to invoke this function.
# Be aware to supply program with dependencies as "struct" and "z3-solver"*!*
# Run and Have fun!

import z3
import struct

ComputingVar = z3.Solver()

a0, a1 = z3.BitVecs('A00 A01', 64)

Prompt = input("In order to predict a future value of Math.random(), You are gonna be asked to provide five "
               "consecutive float numbers from this function. For next step please press ENTER")
x0 = float(input("please provide a first float number: "))
x1 = float(input("please provide a second float number: "))
x2 = float(input("please provide a third float number: "))
x3 = float(input("please provide a fourth float number: "))
x4 = float(input("please provide a fifth float number: "))

inputSequence = [
                    x0,
                    x1,
                    x2,
                    x3,
                    x4,
                ][::-1]

for i in range(len(inputSequence)):
    state1 = a0
    state0 = a1
    a0 = state0
    state1 ^= state1 << 23
    state1 ^= z3.LShR(state1, 17)
    state1 ^= state0
    state1 ^= z3.LShR(state0, 26)
    a1 = state1

    FL64 = struct.pack('d', inputSequence[i] + 1)
    ong64 = struct.unpack('<Q', FL64)[0]
    FiniteMantissis = ong64 & ((1 << 52) - 1)
    ComputingVar.add(int(FiniteMantissis) == z3.LShR(a0, 12))

if ComputingVar.check() == z3.sat:
    baseModel = ComputingVar.model()

    positions = {}
    for state in baseModel.decls():
        positions[state.__str__()] = baseModel[state]

    a0 = positions['A00'].as_long()

    ong64 = (a0 >> 12) | 0x3FF0000000000000
    FL64 = struct.pack('<Q', ong64)
    PredictedSequence = struct.unpack('d', FL64)[0]
    PredictedSequence -= 1

    print("The accuracy of a prediction shall be 100% each time. Thanks to Satisfiability modulo theories. Your next "
          "future number for Math.random() is: ", PredictedSequence)
