"""The graph structure used to represent knitted objects"""
from enum import Enum
from typing import Dict, Optional, List, Tuple, Union

import networkx

from knit_graphs.Loop import Loop
from knit_graphs.Yarn import Yarn


class Pull_Direction(Enum):
    """An enumerator of the two pull directions of a loop"""
    BtF = "BtF"
    FtB = "FtB"

    def opposite(self):
        """
        :return: returns the opposite pull direction of self
        """
        if self is Pull_Direction.BtF:
            return Pull_Direction.FtB
        else:
            return Pull_Direction.BtF


class Knit_Graph:
    """
    A class to knitted structures
    ...

    Attributes
    ----------
    graph : networkx.DiGraph
        the directed-graph structure of loops pulled through other loops
    loops: Dict[int, Loop]
        A map of each unique loop id to its loop
    yarns: Dict[str, Yarn]
         Yarn Ids mapped to the corrisponding yarn
    """

    def __init__(self):
        self.graph: networkx.DiGraph = networkx.DiGraph()
        self.loops: Dict[int, Loop] = {}
        self.last_loop_id: int = -1
        self.yarns: Dict[str, Yarn] = {}

    def add_loop(self, loop: Loop):
        """
        :param loop: the loop to be added in as a node in the graph
        """
        # TODO: Implement
        # Add a node with the loop id to the graph with a parameter keyed to it at "loop" to store the loop
        self.graph.add_node(loop.loop_id, loop=loop)

        # If this loop is not on its specified yarn add it to the end of the yarn
        if loop.loop_id not in self.yarns[loop.yarn_id]:
            self.yarns[loop.yarn_id].add_loop_to_end(loop.loop_id, loop, loop.is_twisted)

        # Add the loop to the loops dictionary
        self.loops[loop.loop_id] = loop

    def add_yarn(self, yarn: Yarn):
        """
        :param yarn: the yarn to be added to the graph structure
        """
        self.yarns[yarn.yarn_id] = yarn

    def connect_loops(self, parent_loop_id: int, child_loop_id: int,
                      pull_direction: Pull_Direction = Pull_Direction.BtF,
                      stack_position: Optional[int] = None, depth: int = 0, parent_offset: int = 0):
        """
        Creates a stitch-edge by connecting a parent and child loop
        :param parent_offset: The direction and distance, oriented from the front, to the parent_loop
        :param depth: -1, 0, 1: The crossing depth in a cable over other stitches. 0 if Not crossing other stitches
        :param parent_loop_id: the id of the parent loop to connect to this child
        :param child_loop_id:  the id of the child loop to connect to the parent
        :param pull_direction: the direction the child is pulled through the parent
        :param stack_position: The position to insert the parent into, by default add on top of the stack
        """
        # TODO: Implement
        # Make an edge in the graph from the parent loop to the child loop. The edge should have three parameters:
        # "pull_direction", "depth", and "parent_offset"
        self.graph.add_edge(parent_loop_id, child_loop_id, pull_direction=pull_direction, depth=depth, parent_offset=parent_offset)
        # add the parent loop to the child's parent loop stack
        self.loops[child_loop_id].add_parent_loop(parent_loop_id);

    def get_courses(self) -> Tuple[Dict[int, float], Dict[float, List[int]]]:
        """
        Course information will be used to generate instruction for knitting machines and
         visualizations that structure knitted objects like grids.
         Evaluation of a course structure should be done in O(n*m) time where n is the number of loops in the graph and
         m is the largest number of parent loops pulled through a single loop (rarely more than 3).
        :return: A dictionary of loop_ids to the course they are on,
                 and a dictionary of course ids to the loops on that course in the order of creation
        The first set of loops in the graph is on course 0.
        A course change occurs when a loop has a parent loop that is in the last course.
        """
        # TODO: Implement
        # A course  of a knitted structure is a set of neighboring loops that do not involve loops on the prior course
        # The first course (starting with loop 0) is the 0th course
        # Note that not having a parent loop does not mean a loop is on course 0, consider yarn-overs
        loop2course = dict()
        course2loop = dict()
        # First course is the 0th course
        course_id = 0
        # Check all the loops in the graph
        for child_loop_id, child_loop in self.loops.items():
            # See what the parent loops are for this loop
            for parent_loop_id in child_loop.parent_loops:
                # If this loop has a parent that is already in a course we are now in a new course
                if ((parent_loop_id in loop2course) and loop2course[parent_loop_id] == course_id):
                    course_id += 1    
            # Store the course we are in for the child_loop
            loop2course[child_loop_id] = course_id

        # for k, v in loop2course.items():
        #     print(f'Loop {k}: Course {v}')

        for k, v in loop2course.items():
            course2loop.setdefault(v, []).append(k)

        # for k, v in course2loop.items():
        #     print(f'Course: {k}\nLoops: {v}')

        return loop2course, course2loop

    def __contains__(self, item: Union[int, Loop]) -> bool:
        """
        :param item: the loop being checked for in the graph
        :return: true if the loop_id of item or the loop is in the graph
        """
        if type(item) is int:
            return self.graph.has_node(item)
        elif isinstance(item, Loop):
            return self.graph.has_node(item.loop_id)

    def __getitem__(self, item: int) -> Loop:
        """
        :param item: the loop_id being checked for in the graph
        :return: the Loop in the graph with the matching id
        """
        if item not in self:
            raise AttributeError
        else:
            return self.graph.nodes[item]["loop"]
