"""
Project Outcome Simulator

Scenario:
  Project teams consists of agents (people or systems)
  with certain capabilities. Agents can complete tasks if
  they:
    1) have the capability and 
    2) are available.
  Project outcomes are simulated by assigning agents to
  tasks on a schedule.
  
References:
  Simulations use the discrete event simulation library "simpy":
  https://simpy.readthedocs.io/en/latest/
"""
import simpy
import tqdm


class Person:
    """
    The most valuable agent (resource) on a project team.
    A person can:
    - Acquire capabilities by completing tasks (example: training)
    - Complete tasks (if they have the required capabilities)
    """

    def __init__(self, name, capabilities):
        self.capabilities = capabilities
        self.name = name
        self.resource = []


class Task:
    """
    A task uses team resources (agents: people or systems) and
    requires those agents to have certain capabilities before the
    task can be executed.
    A task takes time to complete.
    """

    def __init__(self, name, duration, requirements):
        self.name = name
        self.duration = duration
        self.requirements = requirements
        self.started = False
        self.completed_by = None

    def matches(self, agent):
        num_requirements = len(self.requirements)
        for r in self.requirements:
            for c in agent.capabilities:
                if r == c:
                    num_requirements = num_requirements - 1
        return num_requirements == 0


class Project:
    """
    A project is made up of agents (people or systems) working to
    complete a set of tasks.
    """

    def __init__(self, name):
        self.env = simpy.Environment()
        self.name = name
        self.people = []
        self.tasks = []

    def staff(self, people):
        for p in people:
            p.resource = simpy.Resource(self.env, capacity=1)
            self.people.append(p)

    def define(self, tasks):
        for t in tasks:
            self.tasks.append(t)

    def get_task(self, name):
        for t in self.tasks:
            if t.name == name:
                return t
        return None

    def simulate(self):
        print(f"Using greedy search to place tasks in agent queues...")
        for t in self.tasks:
            for p in self.people:
                if t.matches(p):
                    # place tasks in queues of matching agents
                    self.env.process(self.use_resource(t, p))
        self.env.run()
        print(f"Finished simulation in {self.env.now} time units!")

    def use_resource(self, task, person):
        # generate a resource request (get in queue)
        with person.resource.request() as req:
            # wait in agent's queue...
            yield req
            # resource became available
            if task.started:
                # get the task out of this person's queue if the task is already started
                person.resource.release(req)
            else:
                task.started = True
                print(f"{self.env.now}: {person.name} starting task {task.name}.")
                # this resource is tied up for the task's duration
                yield self.env.timeout(task.duration)
                task.completed_by = person
                print(f"{self.env.now}: {person.name} finished task {task.name}.")
