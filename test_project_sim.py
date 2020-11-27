import project_sim as sim


def test_simple_test():
    project = sim.Project("test project")

    project.staff(
        [
            sim.Person("charlie", ["coder", "sa", "leader"]),
            sim.Person("louis", []),
            sim.Person("wing", ["coder", "sa"]),
        ]
    )

    project.define(
        [
            sim.Task("t1", 10, ["sa"]),
            sim.Task("t2", 20, ["coder"]),
            sim.Task("t3", 5, ["leader"]),
        ]
    )

    project.simulate()


# task requiring > 1 capability

# missing capabilities (graceful project failure)

# multiple possible assignments

# sub-optimal solution

# task dependencies
