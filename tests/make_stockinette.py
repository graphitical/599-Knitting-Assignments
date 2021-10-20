"""Tests that generate simple knit graph visualizations"""
from typing import Dict, List, Tuple, Optional
from debugging_tools.knit_graph_viz import visualize_knitGraph
from debugging_tools.simple_knitgraphs import *
from knit_graphs.Knit_Graph import Knit_Graph, Pull_Direction
from knitting_machine.Machine_State import Machine_State, Needle, Pass_Direction
from knitting_machine.machine_operations import outhook
from knitting_machine.operation_sets import Carriage_Pass, Instruction_Type
import argparse


def preamble():
    '''
    Just the header for the file
    '''
    output = f""";!knitout-2
;;Machine: SWG091N2
;;Gauge: 5
;;Width: 250
;;Carriers: 1 2 3 4 5 6 7 8 9 10
;;Position: Center
"""
    return output



def cast_on(direction: Pass_Direction, carrier_id: int):
    '''
    Casting on is different than just running down a row so this interleaves the needles
    '''
    commands = list()
    
    instruction = Instruction_Type.Tuck
    # Casting on is different
    for needle in [*reversed(needles)][0::2]:
        commands.append(command(instruction, direction, needle, carrier_id))

    direction = direction.opposite()

    for needle in [*needles][0::2]:
        commands.append(command(instruction, direction, needle, carrier_id))

    commands.append(f"releasehook {carrier_id}\n")

    return ''.join(commands)


def create_row(instruction: Instruction_Type, direction: Pass_Direction, needles: List[int], carrier: int):
    '''
    This knits a whole row either right-to-left or left-to-right in specified needle order
    '''
    commands = list()
    if direction == Pass_Direction.Right_to_Left:
        needles = reversed(needles)
    
    for needle in needles:
        commands.append(command(instruction, direction, needle, carrier))
    
    return ''.join(commands)

def command(instruction: Instruction_Type, direction: Pass_Direction, needle: int, carrier: int):
    '''
    Creates a knitout command to be written
    '''
    return f"{instruction.value} {direction.value} f{needle} {carrier}\n"

if __name__ == '__main__':
    # parse arguments for number of rows and columns
    parser = argparse.ArgumentParser(description='Create an MxN stocknette KnitOut .k file')
    parser.add_argument('rows', default=16, metavar='M', type=int, help='number of rows in the stockinette, default: 16')
    parser.add_argument('cols', default=16, metavar='N', type=int, help='number of columns in the stocknette, default: 16')
    parser.add_argument('-f', '--output_file', default='test.k', help="output file name, default: test.k")
    args = parser.parse_args()
    # make a graph, ws going t o
    # graph = stockinette(args.rows, args.cols)
    # visualize_knitGraph(graph)

    instruction = Instruction_Type.Tuck
    direction = Pass_Direction.Right_to_Left
    needle = None # set on first pass
    carrier_id = 3
    needles = list(range(1, args.cols + 1))

    with open(args.output_file, 'w') as kfile:
        # write preamble
        kfile.write(preamble())
    
        # cast on
        kfile.write(cast_on(direction, carrier_id))

        # knit rows
        for row in range(1,args.rows):
            kfile.write(create_row(Instruction_Type.Knit, direction, needles, carrier_id))
            direction = direction.opposite()

        # finish file
        kfile.write(f"outhook {carrier_id}")