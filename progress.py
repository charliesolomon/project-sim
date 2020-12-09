import project_sim as sim


project = sim.Project("test project", speed=0.005)

project.staff(
    [
        sim.Person("charlie", ["coder", "sa", "leader"]),
        sim.Person("louis", []),
        sim.Person("wing", ["coder", "sa"]),
    ]
)

project.define(
    [
        sim.Task("t1 is a long task name yep", 10, ["sa"]),
        sim.Task("t2", 20, ["coder"]),
        sim.Task("t3", 5, ["leader"]),
    ]
)

project.simulate()
