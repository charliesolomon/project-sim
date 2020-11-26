"""
Project Outcome Simulator

Scenario:
  Project teams consists of agents (people or systems)
  with certain capabilities. Agents can complete tasks if
  they 1) have the capability and 2) are available.
  Outcomes are simulated by defining tasks needed to achieve them
  and by defining agents (with their availability).
  
  Simulations use discrete event simulation library "simpy":
  https://simpy.readthedocs.io/en/latest/
"""
import simpy

    
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
        
    def matches(self, agent):
        for r in self.requirements:
            for c in agent.capabilities:
                if r == c:
                    return True
        return False
        

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
            
    def simulate(self):    
        for t in self.tasks:
            for p in self.people:
                if t.matches(p):
                    self.env.process(self.use_resource(t, p))
        self.env.run()
                    
    def use_resource(self, task, person):
        print(f'{self.env.now}: Adding task {task.name} to {person.name} queue.')
        with person.resource.request() as req:      # generate a resource request (get in queue)
            yield req                               # waiting in queue...
            print(f'{self.env.now}: {person.name} starting task {task.name}.')
            yield self.env.timeout(task.duration)   # this resource is tied up for the task's duration
        print(f'{self.env.now}: {person.name} finished task {task.name}.')
        
        
project = Project('test project')

project.staff([
    Person('charlie', ['coder','sa','leader']),
    Person('louis', []),
    Person('wing', ['coder','sa'])
])

project.define([
    Task('t1', 10, ['sa']),
    Task('t2', 20, ['coder']),
    Task('t3',  5, ['leader'])
])

project.simulate()
