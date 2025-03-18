"""Set of functions that generate specific swatch samples as Knit Graphs"""
from knit_graphs.Knit_Graph import Knit_Graph
from knit_graphs.Pull_Direction import Pull_Direction
from knit_graphs.Yarn import Yarn


def cast_on(width: int = 10) -> tuple[Knit_Graph, Yarn, list[int]]:
    knit_graph = Knit_Graph()
    yarn = Yarn("yarn")
    knit_graph.add_yarn(yarn)

    for _ in range(0, width):
        yarn.add_loop_to_end(knit_graph=knit_graph)
    return knit_graph, yarn, [*yarn]


def jersey_knit(width: int = 10, height: int = 10) -> Knit_Graph:
    """
    :param width: number of stitches.
    :param height: number of courses.
    :return: A knit graph structure of width loop and height course with all knit stitches.
    """

    knit_graph, yarn, last_course = cast_on(width)
    for r in range(1, height):
        new_course: list[int] = []
        for parent_loop_id in reversed(last_course):
            loop_id, loop = yarn.add_loop_to_end(knit_graph=knit_graph)
            new_course.append(loop_id)
            knit_graph.connect_loops(parent_loop_id=parent_loop_id, child_loop_id=loop_id, pull_direction=Pull_Direction.BtF)
        last_course = new_course
    return knit_graph


def seed_stitch(width: int = 10, height: int = 10) -> Knit_Graph:
    """
    :param width: number of stitches.
    :param height: number of courses.
    :return: A knit graph structure of width loop and height course with alternating knit and purl stitches in a checkered pattern.
    """
    knit_graph, yarn, last_course = cast_on(width)
    # TODO Implement this method sixth for 1 pt
    #raise NotImplementedError

    # Ensure valid input dimensions
    assert width > 0
    assert height > 1

    # Create a new Knit_Graph instance
    knitGraph = Knit_Graph()
    yarn = Yarn("yarn")
    knitGraph.add_yarn(yarn)

    # Create the first row of loops
    first_row = []
    
    for _ in range(0, width):
        loop_id, loop = yarn.add_loop_to_end(knit_graph=knitGraph)
        first_row.append(loop_id)
        knitGraph.add_loop(loop)
    
     # Create subsequent rows with alternating knit and purl stitches
    prior_row = first_row
    next_row = []
    for column, parent_id in enumerate(reversed(prior_row)):
        child_id, child = yarn.add_loop_to_end(knit_graph=knitGraph)
        next_row.append(child_id)
        knitGraph.add_loop(child)

        # Alternate the pull direction for seed stitch
        pull_direction = Pull_Direction.BtF if column % 2 == 0 else Pull_Direction.FtB
        knitGraph.connect_loops(parent_id, child_id, pull_direction=pull_direction)

    # Create additional rows by mirroring the previous row's stitch pattern
    for _ in range(2, height):
        prior_row = next_row
        next_row = []
        for parent_id in reversed(prior_row):
            child_id, child = yarn.add_loop_to_end(knit_graph=knitGraph)
            next_row.append(child_id)
            knitGraph.add_loop(child)
            
            # Use the opposite pull direction from the parent
            grand_parent = [*knitGraph.graph.predecessors(parent_id)][0]
            parent_pull_direction = knitGraph.graph[grand_parent][parent_id]["pull_direction"]
            knitGraph.connect_loops(parent_id, child_id, pull_direction=parent_pull_direction.opposite())

    return knitGraph


def kp_rib(width: int = 10, height: int = 10) -> Knit_Graph:
    """
    :param width: number of stitches.
    :param height: number of courses.
    :return: A knit graph structure of width loop and height course with alternating columns of knits and purls.
    """
    knit_graph, yarn, last_course = cast_on(width)
    # TODO Implement this method seventh for 1 pt
    #raise NotImplementedError

    # Ensure valid input parameters
    assert width > 0
    assert height > 1
    rib_width = 1
    assert rib_width <= width
    
    # Create a new Knit_Graph instance
    knitGraph = Knit_Graph()

    # Add a yarn to the knit graph
    yarn = Yarn("yarn")
    knitGraph.add_yarn(yarn)

    # Initialize the first row of loops
    first_row = []
    for _ in range(0, width):
        loop_id, loop = yarn.add_loop_to_end(knit_graph=knitGraph)
        first_row.append(loop_id)
        knitGraph.add_loop(loop)

    prior_row = first_row
    next_row = []

    # Create alternating columns of knits and purls
    for column, parent_id in reversed([*enumerate(prior_row)]):
        child_id, child = yarn.add_loop_to_end(knit_graph=knitGraph)
        next_row.append(child_id)
        knitGraph.add_loop(child)
        rib_id = int(int(column) / int(rib_width))
        if rib_id % 2 == 0:  # even ribs:
            pull_direction = Pull_Direction.BtF
        else:
            pull_direction = Pull_Direction.FtB
        knitGraph.connect_loops(parent_id, child_id, pull_direction=pull_direction)

    # Continue creating the pattern for the specified height
    for _ in range(2, height):
        prior_row = next_row
        next_row = []
        for parent_id in reversed(prior_row):
            child_id, child = yarn.add_loop_to_end(knit_graph=knitGraph)
            next_row.append(child_id)
            knitGraph.add_loop(child)
            grand_parent = [*knitGraph.graph.predecessors(parent_id)][0]
            parent_pull_direction = knitGraph.graph[grand_parent][parent_id]["pull_direction"]
            knitGraph.connect_loops(parent_id, child_id, pull_direction=parent_pull_direction)

    return knitGraph


def lace(width: int = 12, height: int = 10) -> Knit_Graph:
    """
    :param width: Number of stitches. Must be increments of 6
    :param height: Number of courses.
    :return: A knit graph structure of width loop and height course with a | |\ o o /| | structure on odd rows.
    """
    assert width % 6 == 0, "Lace must be a repeat of 6 stitches"
    knit_graph, yarn, last_course = cast_on(width)
    for r in range(1, height):
        new_course: list[int] = []
        reversed_course = [*reversed(last_course)]
        for i, parent_loop_id in enumerate(reversed_course):
            loop_id, loop = yarn.add_loop_to_end(knit_graph=knit_graph)
            new_course.append(loop_id)
            if r % 2 == 0:  # even rows knit across
                knit_graph.connect_loops(parent_loop_id=parent_loop_id, child_loop_id=loop_id, pull_direction=Pull_Direction.BtF)
            else:
                if i % 6 in [0, 5]:  # knits
                    knit_graph.connect_loops(parent_loop_id=parent_loop_id, child_loop_id=loop_id, pull_direction=Pull_Direction.BtF)
                elif i % 6 == 1:
                    knit_graph.connect_loops(parent_loop_id=parent_loop_id, child_loop_id=loop_id, pull_direction=Pull_Direction.BtF, stack_position=1)
                    knit_graph.connect_loops(parent_loop_id=reversed_course[i + 1], child_loop_id=loop_id, pull_direction=Pull_Direction.BtF, stack_position=0, parent_offset=1)
                elif i % 6 == 4:
                    knit_graph.connect_loops(parent_loop_id=reversed_course[i - 1], child_loop_id=loop_id, pull_direction=Pull_Direction.BtF, stack_position=0, parent_offset=-1)
                    knit_graph.connect_loops(parent_loop_id=parent_loop_id, child_loop_id=loop_id, pull_direction=Pull_Direction.BtF, stack_position=1)
        last_course = new_course
    return knit_graph


def cable(width: int = 10, height: int = 10) -> Knit_Graph:
    """
    :param width: Number of stitches. Must be increments of 5
    :param height: Number of courses.
    :return: A knit graph structure of width loop and height course with a 2-to-left cable surrounded by knits on odd rows.
    """
    assert width % 5 == 0, "Cable must be a repeat of 5 stitches"
    knit_graph, yarn, last_course = cast_on(width)
    for r in range(1, height):
        new_course: list[int] = []
        cable_course: list[int] = []
        reserved_course = [*reversed(last_course)]
        for l, parent_loop_id in enumerate(reserved_course):
            loop_id, loop = yarn.add_loop_to_end(knit_graph=knit_graph)
            new_course.append(loop_id)
            if r % 2 == 0:  # even rows knit across
                knit_graph.connect_loops(parent_loop_id=parent_loop_id, child_loop_id=loop_id, pull_direction=Pull_Direction.BtF)
            else:
                if l % 5 in [0, 4]:
                    knit_graph.connect_loops(parent_loop_id=parent_loop_id, child_loop_id=loop_id, pull_direction=Pull_Direction.BtF)
                    cable_course.append(loop_id)
                elif l % 5 in [3, 2]:
                    cable_course.insert(-1, loop_id)
                    knit_graph.connect_loops(parent_loop_id=parent_loop_id, child_loop_id=loop_id, pull_direction=Pull_Direction.BtF, depth=-1, parent_offset=1)
                elif l % 5 == 1:
                    cable_course.append(loop_id)
                    knit_graph.connect_loops(parent_loop_id=parent_loop_id, child_loop_id=loop_id, pull_direction=Pull_Direction.BtF, depth=1, parent_offset=-2)
        if len(cable_course) > 0:
            new_course = cable_course
        last_course = new_course
    return knit_graph
