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
        sim.Task("t1 is a long task name yep", 109, ["sa"]),
        sim.Task("t2", 112, ["coder"]),
        sim.Task("t3", 50, ["leader"]),
    ]
)

project.simulate()
