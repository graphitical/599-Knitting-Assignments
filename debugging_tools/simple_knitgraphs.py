"""A set of functions that generate simple knit-graph structures useful for debugging"""
from knit_graphs.Knit_Graph import Knit_Graph, Pull_Direction
from knit_graphs.Yarn import Yarn


def stockinette(width: int = 4, height: int = 4) -> Knit_Graph:
    """
    :param width: the number of stitches of the swatch
    :param height:  the number of courses of the swatch
    :return: a knitgraph of stockinette on one yarn of width stitches by height courses
    """
    knit_graph = Knit_Graph()
    yarn = Yarn("yarn", knit_graph)
    knit_graph.add_yarn(yarn)

    # make the first set of loops on the bottom (0th) course
    first_course = []
    for _ in range(0, width):
        loop_id, loop = yarn.add_loop_to_end()
        first_course.append(loop_id)
        knit_graph.add_loop(loop)

    # make new course of loops and connect them to the last course
    prior_course = first_course
    for _ in range(1, height):
        next_course = []
        for parent_id in reversed(prior_course):
            child_id, child = yarn.add_loop_to_end()
            next_course.append(child_id)
            knit_graph.add_loop(child)
            knit_graph.connect_loops(parent_id, child_id)
        prior_course = next_course

    return knit_graph


def rib(width: int = 4, height: int = 4, rib_width: int = 1) -> Knit_Graph:
    """
    :param rib_width: determines how many columns of knits and purls are in a single rib.
    (i.e.) the first course of width=4 and rib_width=2 will be kkpp. Always start with knit columns
    :param width: a number greater than 0 to set the number of stitches in the swatch
    :param height: A number greater than 0 to set teh number of courses in the swatch
    :return: A knit graph with a repeating columns of knits (back to front) then purls (front to back).
    """
    assert width > 0
    assert height > 0
    assert rib_width <= width

    knit_graph = Knit_Graph()
    yarn = Yarn("Purple", knit_graph)
    knit_graph.add_yarn(yarn)

    # cast on
    first_course = []
    for _ in range(0, width):
        loop_id, loop = yarn.add_loop_to_end()
        first_course.append(loop_id)
        knit_graph.add_loop(loop)

    # make new courses of loops and connect them to the last course
    prior_course = first_course
    for _ in range(1, height):
        next_course = []
        pull_direction = Pull_Direction.FtB
        for idx, parent_id in enumerate(reversed(prior_course), start=1):
            # flip stitch type for ribbing effect
            if (idx % rib_width == 0):
                pull_direction = pull_direction.opposite()
            
            child_id, child = yarn.add_loop_to_end()
            next_course.append(child_id)
            knit_graph.add_loop(child)
            knit_graph.connect_loops(parent_id, child_id, pull_direction)
        prior_course = next_course

    return knit_graph


def seed(width: int = 4, height=4) -> Knit_Graph:
    """
    :param width: a number greater than 0 to set the number of stitches in the swatch
    :param height: A number greater than 0 to set teh number of courses in the swatch
    :return: A knit graph with a checkered pattern of knit and purl stitches of width and height size.
    The first stitch should be a knit
    """
    assert width > 0
    assert height > 0

    knit_graph = Knit_Graph()
    yarn = Yarn("White", knit_graph)
    knit_graph.add_yarn(yarn)

    # cast on
    first_course = []
    for _ in range(0, width):
        loop_id, loop = yarn.add_loop_to_end()
        first_course.append(loop_id)
        knit_graph.add_loop(loop)

    # make new courses of loops and connect them to the last course
    prior_course = first_course
    for _ in range(1, height):
        next_course = []
        pull_direction = Pull_Direction.FtB
        for parent_id in reversed(prior_course):
            pull_direction = pull_direction.opposite()
            child_id, child = yarn.add_loop_to_end()
            next_course.append(child_id)
            knit_graph.add_loop(child)
            knit_graph.connect_loops(parent_id, child_id, pull_direction)
        prior_course = next_course

    return knit_graph


def twisted_stripes(width: int = 4, height=5, left_twists: bool = True) -> Knit_Graph:
    """
    :param left_twists: if True, make the left leaning stitches in front, otherwise right leaning stitches in front
    :param width: the number of stitches of the swatch
    :param height:  the number of courses of the swatch
    :return: A knitgraph with repeating pattern of twisted stitches surrounded by knit wales
    """
    knitGraph = Knit_Graph()
    yarn = Yarn("yarn", knitGraph)
    knitGraph.add_yarn(yarn)

    # Add the first course of loops
    first_course = []
    for _ in range(0, width):
        loop_id, loop = yarn.add_loop_to_end()
        first_course.append(loop_id)
        knitGraph.add_loop(loop)

    def add_loop_and_knit(p_id, depth=0, parent_offset: int = 0):
        """
        adds a loop by knitting to the knitgraph
        :param parent_offset: Set the offset of the parent loop in the cable. offset = parent_index - child_index
        :param p_id: the parent loop's id
        :param depth: the crossing- depth to knit at
        """
        child_id, child = yarn.add_loop_to_end()
        next_course.append(child_id)
        knitGraph.add_loop(child)
        knitGraph.connect_loops(p_id, child_id, depth=depth, parent_offset=parent_offset)

    if left_twists:  # set the depth for the first loop in the twist (1 means it will cross in front of other stitches)
        twist_depth = 1
    else:
        twist_depth = -2

    # add new courses
    prior_course = first_course
    for course in range(1, height):
        next_course = []
        reversed_prior_course = [*reversed(prior_course)]
        for col, parent_id in enumerate(reversed_prior_course):
            if course % 2 == 0 or col % 4 == 0 or col % 4 == 3:  # knit on even rows and before and after twists
                add_loop_and_knit(parent_id)
            elif col % 4 == 1:
                next_parent_id = reversed_prior_course[col + 1]
                add_loop_and_knit(next_parent_id, twist_depth, -1)
                twist_depth = -1 * twist_depth  # switch depth for neighbor
            elif col % 4 == 2:
                next_parent_id = reversed_prior_course[col - 1]
                add_loop_and_knit(next_parent_id, twist_depth, 1)
                twist_depth = -1 * twist_depth  # switch depth for next twist
        prior_course = next_course

    return knitGraph


def lace(width: int = 4, height: int = 4):
    """
    :param width: the number of stitches of the swatch
    :param height:  the number of courses of the swatch
    :return: a knitgraph with k2togs and yarn-overs surrounded by knit wales
    """
    knitGraph = Knit_Graph()
    yarn = Yarn("yarn", knitGraph)
    knitGraph.add_yarn(yarn)
    first_row = []
    for _ in range(0, width):
        loop_id, loop = yarn.add_loop_to_end()
        first_row.append(loop_id)
        knitGraph.add_loop(loop)

    def add_loop_and_knit(p_id):
        """
        Knits a loop into the graph
        :param p_id: the id of the parent loop being knit through
        :return: the id of the child loop created
        """
        c_id, c = yarn.add_loop_to_end()
        next_row.append(c_id)
        knitGraph.add_loop(c)
        knitGraph.connect_loops(p_id, c_id)
        return c_id

    prior_row = first_row
    for row in range(1, height):
        next_row = []
        prior_parent_id = -1
        reversed_prior_row = [*reversed(prior_row)]
        for col, parent_id in enumerate(reversed_prior_row):
            if row % 2 == 0 or col % 4 == 0 or col % 4 == 3:  # knit on even rows and before and after twists
                add_loop_and_knit(parent_id)
            elif col % 4 == 1:
                child_id, child = yarn.add_loop_to_end()
                knitGraph.add_loop(child)
                next_row.append(child_id)  # yarn over
                prior_parent_id = parent_id
            elif col % 4 == 2:
                child_id = add_loop_and_knit(parent_id)
                knitGraph.connect_loops(prior_parent_id, child_id)
        prior_row = next_row

    return knitGraph


def both_twists(height=20) -> Knit_Graph:
    """
    :param height:  the number of courses of the swatch
    :return: A knitgraph with repeating pattern of twisted stitches surrounded by knit wales
    """
    width = 10
    knitGraph = Knit_Graph()
    yarn = Yarn("yarn", knitGraph)
    knitGraph.add_yarn(yarn)

    # Add the first course of loops
    first_course = []
    for _ in range(0, width):
        loop_id, loop = yarn.add_loop_to_end()
        first_course.append(loop_id)
        knitGraph.add_loop(loop)

    def add_loop_and_knit(p_id, depth=0, parent_offset: int = 0):
        """
        adds a loop by knitting to the knitgraph
        :param parent_offset: Set the offset of the parent loop in the cable. offset = parent_index - child_index
        :param p_id: the parent loop's id
        :param depth: the crossing- depth to knit at
        """
        child_id, child = yarn.add_loop_to_end()
        next_course.append(child_id)
        knitGraph.add_loop(child)
        knitGraph.connect_loops(p_id, child_id, depth=depth, parent_offset=parent_offset)

    # add new courses
    prior_course = first_course
    for course in range(1, height):
        next_course = []
        reversed_prior_course = [*reversed(prior_course)]
        for col, parent_id in enumerate(reversed_prior_course):
            if course % 2 == 1 or col in {0, 1, 4, 5, 8, 9}:  # knit on odd rows and borders or middle
                add_loop_and_knit(parent_id)
            elif col == 2:
                parent_id = reversed_prior_course[3]
                add_loop_and_knit(parent_id, depth=-1, parent_offset=-1)
            elif col == 3:
                parent_id = reversed_prior_course[2]
                add_loop_and_knit(parent_id, depth=1, parent_offset=1)
            elif col == 6:
                parent_id = reversed_prior_course[7]
                add_loop_and_knit(parent_id, depth=1, parent_offset=-1)
            elif col == 7:
                parent_id = reversed_prior_course[6]
                add_loop_and_knit(parent_id, depth=-1, parent_offset=1)
        prior_course = next_course

    return knitGraph
