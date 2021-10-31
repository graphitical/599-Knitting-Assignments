from debugging_tools.knit_graph_viz import visualize_knitGraph
from debugging_tools.simple_knitgraphs import *
from knitting_machine.knitgraph_to_knitout import Knitout_Generator


def test_stst():
    knitGraph = stockinette(4, 4)
    generator = Knitout_Generator(knitGraph)
    generator.write_instructions("my_test_stst.k")


def test_rib():
    knitGraph = rib(4, 4, 2)
    generator = Knitout_Generator(knitGraph)
    generator.write_instructions("my_test_rib2.k")


def test_seed():
    knitGraph = seed(4, 4)
    generator = Knitout_Generator(knitGraph)
    generator.write_instructions("my_test_seed.k")


def test_lace():
    knitGraph = lace(4, 4)
    generator = Knitout_Generator(knitGraph)
    generator.write_instructions("my_test_lace_k.k")


def test_both_twists():
    knitGraph = both_twists(height=4)
    generator = Knitout_Generator(knitGraph)
    generator.write_instructions("my_test_twists.k")

if __name__ == '__main__':
    test_stst()
    test_rib()
    test_seed()
    test_lace()
    test_both_twists()
