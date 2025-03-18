"""The graph structure used to represent knitted objects"""
import networkx

from knit_graphs.Loop import Loop
from knit_graphs.Pull_Direction import Pull_Direction
from knit_graphs.Yarn import Yarn


class Course:
    """
    Course object for organizing loops into knitting rows
    """

    def __init__(self):
        self.loops_by_id_in_order: list[int] = []
        self.loops_by_id: dict[int, Loop] = {}

    def add_loop(self, loop: Loop, index: int or None = None):
        """
        Add the loop at the given index or to the end of the course
        :param loop: loop to add
        :param index: index to insert at or None if adding to end
        """
        for parent_loop in loop.parent_loops:
            assert parent_loop not in self, f"{loop} has parent {parent_loop}, cannot be added to same course"
        self.loops_by_id[loop.loop_id] = loop
        if index is None:
            self.loops_by_id_in_order.append(loop.loop_id)
        else:
            self.loops_by_id_in_order.insert(index, loop.loop_id)

    def __getitem__(self, index: int) -> int:
        return self.loops_by_id_in_order[index]

    def index(self, loop_id: int or Loop) -> int:
        """
        Searches for index of given loop_id
        :param loop_id: loop_id or loop to find
        :return: index of the loop_id
        """
        if isinstance(loop_id, Loop):
            loop_id = loop_id.loop_id
        return self.loops_by_id_in_order.index(loop_id)

    def __contains__(self, loop_id: int or Loop) -> bool:
        if isinstance(loop_id, Loop):
            loop_id = loop_id.loop_id
        return loop_id in self.loops_by_id

    def __iter__(self):
        return self.loops_by_id_in_order.__iter__()

    def __len__(self):
        return len(self.loops_by_id_in_order)

    def __str__(self):
        return str(self.loops_by_id_in_order)

    def __repr__(self):
        return str(self)


class Knit_Graph:
    """
    A representation of knitted structures as connections between loops on yarns
    ...

    Attributes
    ----------
    graph : networkx.DiGraph
        the directed-graph structure of loops pulled through other loops.
    loops: Dict[int, Loop]
        A map of each unique loop id to its loop
    yarns: Dict[str, Yarn]
         A list of Yarns used in the graph
    """

    def __init__(self):
        self.graph: networkx.DiGraph = networkx.DiGraph()
        self.loops: dict[int, Loop] = {}
        self.last_loop_id: int = -1
        self.yarns: dict[str, Yarn] = {}

    def add_loop(self, loop: Loop):
        """
        Adds a loop to the graph
        :param loop: the loop to be added in as a node in the graph
        """
        # TODO Implement this method third for 1 pt
        #raise NotImplementedError
        
        if isinstance(loop, Loop):
            # Add the loop as a node in the graph
            self.graph.add_node(loop.loop_id, loop=loop)
            
            # Ensure the yarn associated with the loop is part of the graph   
            if loop.yarn not in self.yarns:
                self.add_yarn(loop.yarn)
            
            # Ensure the loop is on the specified yarn
            if loop not in self.yarns[loop.yarn.yarn_id]:  # make sure the loop is on the yarn specified
                self.yarns[loop.yarn].add_loop_to_end(loop_id=None, loop=loop, knit_graph=self)
            
            # Update the last loop ID if necessary
            if loop.loop_id > self.last_loop_id:
                self.last_loop_id = loop.loop_id
            
            # Add the loop to the loops dictionary
            self.loops[loop.loop_id] = loop

    def add_yarn(self, yarn: Yarn):
        """
        Adds a yarn to the graph. Assumes that loops do not need to be added
        :param yarn: the yarn to be added to the graph structure
        """
        self.yarns[yarn.yarn_id] = yarn

    def connect_loops(self, parent_loop_id: int, child_loop_id: int,
                      pull_direction: Pull_Direction = Pull_Direction.BtF,
                      stack_position: int or None = None, depth: int = 0, parent_offset: int = 0):
        """
        Creates a stitch-edge by connecting a parent and child loop
        :param parent_offset: The direction and distance, oriented from the front, to the parent_loop
        :param depth: -1, 0, 1: The crossing depth in a cable over other stitches. 0 if Not crossing other stitches
        :param parent_loop_id: the id of the parent loop to connect to this child
        :param child_loop_id:  the id of the child loop to connect to the parent
        :param pull_direction: the direction the child is pulled through the parent
        :param stack_position: The position to insert the parent into, by default add on top of the stack
        """
        assert parent_loop_id in self, f"parent loop {parent_loop_id} is not in this graph"
        assert child_loop_id in self, f"child loop {child_loop_id} is not in this graph"
        # TODO Implement this method fourth for 1 pt
        #raise NotImplementedError
        
        # Add an edge in the graph to represent the connection between parent and child loops
        self.graph.add_edge(parent_loop_id, child_loop_id, pull_direction=pull_direction, depth=depth, parent_offset=parent_offset)
        
        # Get references to the parent and child loops
        child_loop = self[child_loop_id]
        parent_loop = self[parent_loop_id]
        
        # Add the parent loop to the child loop's stack of parent_loops
        child_loop.add_parent_loop(parent_loop, stack_position)

    def get_courses(self) -> list[Course]:
        """
        :return: A dictionary of loop_ids to the course they are on,
        a dictionary or course ids to the loops on that course in the order of creation.
        The first set of loops in the graph is on course 0.
        A course change occurs when a loop has a parent loop that is in the last course.
        """
        # TODO Implement this method fifth for 1 pt
        #raise NotImplementedError
        
        # Dictionary to store loop_ids to the course they are on
        loop_ids_to_course_dict = {}

        # Dictionary to store course ids to the loops on that course in the order of creation
        course_to_loop_dict = {}

        # Set to keep track of loops in the current course
        current_course_set = set()
        
        # List to store loops in the current course in the order of creation
        current_course = []

        # Used to track the current course number
        course = 0

        # Iterate through sorted loop_ids
        for loop_id in sorted([*self.graph.nodes]):
            no_parents_in_course = True
            
            # Check if the loop has no parents in the current course
            for parent_id in self.graph.predecessors(loop_id):
                if parent_id in current_course_set:
                    no_parents_in_course = False
                    break

            # If the loop has no parents in the current course, add it to the current course
            if no_parents_in_course:
                current_course_set.add(loop_id)
                current_course.append(loop_id)
            else:
                # Update course_to_loop_ids and reset current_course for the next course
                course_to_loop_dict[course] = current_course
                current_course = [loop_id]
                current_course_set = {loop_id}
                course += 1

            # Update loop_ids_to_course
            loop_ids_to_course_dict[loop_id] = course

        # Add the loops of the last course to course_to_loop_ids
        course_to_loop_dict[course] = current_course

        # Create Course instances
        courses = [Course() for _ in range(course + 1)]  # Create Course instances

        # Add loops to corresponding Course instances
        for course_id, loop_ids in course_to_loop_dict.items():
            course_instance = courses[course_id]
            for loop_id in loop_ids:
                loop_instance = self.get_loop(loop_id)  # Replace with the actual method
                course_instance.add_loop(loop_instance)

        return courses
        

    def __contains__(self, item):
        """
        Returns true if the item is in the graph
        :param item: the loop being checked for in the graph
        :return: true if the loop_id of item or the loop is in the graph
        """
        if type(item) is int:
            return self.graph.has_node(item)
        elif isinstance(item, Loop):
            return self.graph.has_node(item.loop_id)
        else:
            return False

    def get_loop(self, loop_id: int) -> Loop:
        """
        Gets the loop by an id
        :param loop_id: the loop_id being checked for in the graph
        :return: the Loop in the graph with the matching id
        """
        return self[loop_id]

    def __getitem__(self, loop_id: int) -> Loop:
        """
        Gets the loop by an id
        :param loop_id: the loop_id being checked for in the graph
        :return: the Loop in the graph with the matching id
        """
        if loop_id not in self:
            raise AttributeError
        else:
            return self.graph.nodes[loop_id]["loop"]

    def get_stitch_edge(self, parent: Loop or int, child: Loop or int, stitch_property: str or None = None):
        """
        Shortcut to get stitch-edge data from loops or ids
        :param stitch_property: property of edge to return
        :param parent: parent loop or id of parent loop
        :param child: child loop or id of child loop
        :return: the edge data for this stitch edge
        """
        parent_id = parent
        if isinstance(parent, Loop):
            parent_id = parent.loop_id
        child_id = child
        if isinstance(child, Loop):
            child_id = child.loop_id
        if self.graph.has_edge(parent_id, child_id):
            if stitch_property is not None:
                return self.graph[parent_id][child_id][stitch_property]
            else:
                return self.graph[parent_id][child_id]
        else:
            return None

    def get_child_loop(self, loop_id: Loop or int) -> int or None:
        """
        :param loop_id: loop_id to look for child from.
        :return: child loop_id or None if no child loop
        """
        if isinstance(loop_id, Loop):
            loop_id = loop_id.loop_id
        successors = [*self.graph.successors(loop_id)]
        if len(successors) == 0:
            return None
        return successors[0]
