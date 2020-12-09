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
from time import sleep
import simpy
from tqdm import trange, tqdm


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

    def __init__(self, name, duration, requirements, blocked_by=""):
        self.name = name
        self.duration = duration
        self.requirements = requirements
        self.blocked_by = blocked_by
        self.started = -1
        self.completed = -1
        self.completed_by = None

    def finished(self):
        return self.completed >= 0

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

    def __init__(self, name, speed=0.000):
        self.env = simpy.Environment()
        self.name = name
        self.people = []
        self.tasks = []
        self.speed = speed

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

    def blocks(self, task):
        b = []
        for t in self.tasks:
            if t.blocked_by == task.name:
                b.append(t)
        return b

    def log(self, message):
        print(message)

    def assign(self, task):
        if task.started < 0 and (
            task.blocked_by == "" or self.get_task(task.blocked_by).finished()
        ):
            for p in self.people:
                if task.matches(p):
                    # place tasks in queues of matching agents
                    self.env.process(self.use_resource(task, p))

    def use_resource(self, task, person):
        # generate a resource request (get in queue)
        with person.resource.request() as req:
            # wait in agent's queue...
            yield req
            # resource became available
            doTask = False
            if task.started >= 0:
                # get the task out of this person's queue (someone else started it already)
                person.resource.release(req)
            else:
                task.started = self.env.now
                # self.log(f"{self.env.now}: {person.name} starting task {task.name}.")
                # this resource is tied up for the task's duration
                yield self.env.timeout(task.duration)
                task.completed_by = person
                task.completed = self.env.now
                # self.log(f"{task.completed}: {person.name} finished task {task.name}.")
                for t in self.blocks(task):
                    self.assign(t)

    def ltrunc(self, str, max):
        if len(str) > max:
            return str[: (max - 3 - len(str))] + "..."
        return str.ljust(max)

    def simulate(self):
        for t in self.tasks:
            self.assign(t)

        self.env.run()
        self.log(f"\n{self.name} - finished in {self.env.now} time units")

        # progress bar gantt
        max_name = 8
        max_desc = 10
        max_time_digits = len(f"{self.env.now}")
        max_suffix = 1 + 2 * max_time_digits
        max_bar = self.env.now
        for t in self.tasks:
            if not t.finished():
                self.log(f'FAIL: Task "{t.name}" could not be completed!')
            else:
                t_desc = self.ltrunc(t.completed_by.name, max_name) + self.ltrunc(
                    " - " + t.name, max_desc
                )
                t_suffix = (
                    f"{t.started}".rjust(max_time_digits)
                    + ","
                    + f"{t.completed}".rjust(max_time_digits)
                )
                with trange(100) as p:
                    max_bar_screen = p.ncols - max_name - max_desc - max_suffix
                    p.set_description(f"{t_desc}", False)
                    t_leader = int((t.started) * max_bar_screen / max_bar)
                    t_trailer = int((max_bar - t.completed) * max_bar_screen / max_bar)
                    bf = (
                        f"{t_desc}"
                        + " " * t_leader
                        + "|{bar}|"
                        + " " * t_trailer
                        + f"{t_suffix}"
                    )
                    p.bar_format = bf
                    for i in p:
                        sleep(self.speed)