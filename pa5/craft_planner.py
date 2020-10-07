import json
from collections import namedtuple, defaultdict, OrderedDict
from timeit import default_timer as time
from heapq import heappop, heappush

Recipe = namedtuple('Recipe', ['name', 'check', 'effect', 'cost'])


class State(OrderedDict):
    """ This class is a thin wrapper around an OrderedDict, which is simply a dictionary which keeps the order in
        which elements are added (for consistent key-value pair comparisons). Here, we have provided functionality
        for hashing, should you need to use a state as a key in another dictionary, e.g. distance[state] = 5. By
        default, dictionaries are not hashable. Additionally, when the state is converted to a string, it removes
        all items with quantity 0.

        Use of this state representation is optional, should you prefer another.
    """

    def __key(self):
        return tuple(self.items())

    def __hash__(self):
        return hash(self.__key())

    def __lt__(self, other):
        return self.__key() < other.__key()

    def copy(self):
        new_state = State()
        new_state.update(self)
        return new_state

    def __str__(self):
        return str(dict(item for item in self.items() if item[1] > 0))


def make_checker(rule):
    # Implement a function that returns a function to determine whether a state meets a
    # rule's requirements. This code runs once, when the rules are constructed before
    # the search is attempted.

    # Grab Requires ====
    if 'Requires' in rule:
        require = rule['Requires']
    else:
        require = None
    # Grab Consumes ====
    if 'Consumes' in rule:
        consume = rule['Consumes']
    else:
        consume = None

    # print("required:", require) # debug
    # print("consumed:", consume) # debug

    def check(state):
        # This code is called by graph(state) and runs millions of times.
        # Tip: Do something with rule['Consumes'] and rule['Requires'].
        if require:
            for key,value in require.items():
                if state[key] == 0:
                    return False
        if consume:
            for key,value in consume.items():
                if state[key] < value:
                    return False
        return True

    return check

def make_effector(rule):
    # Implement a function that returns a function which transitions from state to
    # new_state given the rule. This code runs once, when the rules are constructed
    # before the search is attempted.

    # Grab Produces ====
    if 'Produces' in rule:
        produce = rule['Produces']
    else:
        produce = None

    # Grab Consumes ====
    if 'Consumes' in rule:
        consume = rule['Consumes']
    else:
        consume = None

    def effect(state):
        # This code is called by graph(state) and runs millions of times
        # Tip: Do something with rule['Produces'] and rule['Consumes'].
        next_state = State.copy(state)
        if consume:
            for key,value in consume.items():
                next_state[key] -= value
        if produce:
            for key,value in produce.items():
                next_state[key] += value
        return next_state

    return effect


def make_goal_checker(goal):
    # Implement a function that returns a function which checks if the state has
    # met the goal criteria. This code runs once, before the search is attempted.

    def is_goal(state):
        # This code is used in the search process and may be called millions of times.
        for key,value in goal.items():
            if state[key] < value:
                return False
        return True

    return is_goal


def graph(state):
    # Iterates through all recipes/rules, checking which are valid in the given state.
    # If a rule is valid, it returns the rule's name, the resulting state after application
    # to the given state, and the cost for the rule.
    for r in all_recipes:
        if r.check(state):
            yield (r.name, r.effect(state), r.cost)

def heuristic(state, next_state, action, need):
    # Implement your heuristic here!
    estimate = 0
    if state["iron_axe"] > 0:
        if action == "stone_axe for wood" or action == "punch for wood" or action == "wooden_axe for wood" or action == "craft iron_axe at bench":
            return 99999999
    elif state["stone_axe"] > 0:
        if action == "punch for wood" or action == "wooden_axe for wood" or action == "craft stone_axe at bench":
            return 99999999
    elif state["wooden_axe"] > 0:
        if action == "punch for wood" or action == "craft wooden_axe at bench":
            return 99999999
    if state["iron_pickaxe"] > 0:
        if action == "stone_pickaxe for cobble" or action == "wooden_pickaxe for cobble" or action == "stone_pickaxe for ore" or action == "wooden pickaxe for ore" or action == "craft iron_pickaxe at bench":
            return 99999999
    elif state["stone_pickaxe"]> 0:
        if action == "wooden_pickaxe for cobble" or action == "wooden pickaxe for ore" or action == "craft stone_pickaxe at bench":
            return 99999999
    if state["bench"] > 0:
        if action == "craft bench":
            return 99999999
    if state["furnace"] > 0:
        if action == "craft furnace at bench":
            return 99999999
    for required in need:
        if next_state[required] > need[required]:
            return 99999999
    for required in need:
        estimate += next_state[required]

    return estimate

def search(graph, state, is_goal, limit, heuristic):

    start_time = time()

    # Implement your search here! Use your heuristic here!
    # When you find a path to the goal return a list of tuples [(state, action)]
    # representing the path. Each element (tuple) of the list represents a state
    # in the path and the action that took you to this state

    # Priority queue
    queue = [(0, state)]

    # Dictionary that will return the cost
    cost = {}
    cost[state] = 0

    # Dictionary that will store the backpointers
    backpointers = {}
    backpointers[state] = None

    # List to track all visited for no repeats
    visited = set()
    visited.add(state)

    # Dictionary that will store the actions
    action = {}
    action[state] = None


    # Check what we need to obtain
    need = find_required(Crafting['Goal'])

    while time() - start_time < limit:
        curr_cost, curr_node = heappop(queue)

        if is_goal(curr_node):
            path = []
            while curr_node is not None and action[curr_node] is not None:
                path.append((curr_node, action[curr_node]))
                curr_node = backpointers[curr_node]
            path.reverse()
            print(time() - start_time, 'seconds.')
            return visited, path

        for next_action, new_state, next_cost in graph(curr_node):
            next_state = State.copy(new_state)
            new_cost = cost[curr_node] + next_cost + heuristic(curr_node, next_state, next_action, need)
            if (next_state not in cost or new_cost < cost[next_state]) and next_state not in visited:
                cost[next_state] = new_cost
                action[next_state] = next_action
                visited.add(next_state)
                backpointers[next_state] = curr_node
                heappush(queue, (new_cost, next_state))


    # Failed to find a path
    print(time() - start_time, 'seconds.')
    print("Failed to find a path from", state, 'within time limit.')
    return None

# Helper Function to check if what we need to obtain
def find_required(state):
    # A function to determine what a state requires. This code runs once,
    # when the rules are constructed before the search is attempted.
    goal = []
    for item in state:
        goal.append((item, state[item]))

    # Set all items to be 0
    required = {}
    for item in Crafting['Items']:
        required[item] = 0

    while goal:
        item, amount = heappop(goal)
        # Add what we need, tool is only 1
        if item == "bench" or item == "furnace":
            required[item] = 1
        elif item == "iron_pickaxe" or item == "iron_axe":
            required[item] = 1
        elif item == "stone_pickaxe" or item == "stone_axe":
            required[item] = 1
        elif item == "wooden_pickaxe" or item == "wooden_axe":
            required[item] = 1
        else:
            required[item] += amount

        for craft in Crafting['Recipes']:
            section = Crafting['Recipes'][craft]
            # Check what makes the item through Produces
            if item in section['Produces']:
                # Add the Consumes of that Produce
                if 'Consumes' in section:
                    for new_items in section['Consumes']:
                        heappush(goal,(new_items, section['Consumes'][new_items]))

                # Add the Requires of that Produce
                if 'Requires' in section:
                    for new_items in section['Requires']:
                        # Check if tool already marked, if not add
                        if required[new_items] == 0:
                            if (new_items, 1) not in goal:
                                heappush(goal,(new_items, 1))
    return required

# Helper Function to count cost
def total_cost(path):
    cost = 0
    for state, action in resulting_plan:
        cost += Crafting["Recipes"][action]["Time"]
    return cost

if __name__ == '__main__':
    with open('Crafting.json') as f:
        Crafting = json.load(f)

    # # List of items that can be in your inventory:
    # print('All items:', Crafting['Items'])
    #
    # # List of items in your initial inventory with amounts:
    # print('Initial inventory:', Crafting['Initial'])
    #
    # # List of items needed to be in your inventory at the end of the plan:
    # print('Goal:',Crafting['Goal'])
    #
    # # Dict of crafting recipes (each is a dict):
    # print('Example recipe:','craft stone_pickaxe at bench ->',Crafting['Recipes']['craft stone_pickaxe at bench'])

    # Build rules
    all_recipes = []
    for name, rule in Crafting['Recipes'].items():
        checker = make_checker(rule)
        effector = make_effector(rule)
        recipe = Recipe(name, checker, effector, rule['Time'])
        all_recipes.append(recipe)

    # Create a function which checks for the goal
    is_goal = make_goal_checker(Crafting['Goal'])


    # Initialize first state from initial inventory
    state = State({key: 0 for key in Crafting['Items']})
    state.update(Crafting['Initial'])

    # Search for a solution
    visited, resulting_plan = search(graph, state, is_goal, 30, heuristic)

    if resulting_plan:
        print("[cost =", total_cost(resulting_plan),'len =',len(resulting_plan),"]")
        print("Number of states visited = ", len(visited))
        # Print resulting plan
        for state, action in resulting_plan:
            print('\t',state)
            print(action)
