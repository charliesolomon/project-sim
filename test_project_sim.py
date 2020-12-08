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
    assert project.get_task("t1").completed_by.name == "charlie"
    assert project.get_task("t2").completed_by.name == "wing"
    assert project.get_task("t3").completed_by.name == "charlie"


# task requiring > 1 capability
def test_multi_dependency_task():
    project = sim.Project("test project")

    project.staff(
        [
            sim.Person("charlie", ["coder", "sa"]),
            sim.Person("louis", ["sa", "leader"]),
            sim.Person("wing", ["coder", "sa"]),
        ]
    )

    project.define(
        [
            sim.Task("t1", 10, ["sa", "leader"]),
            sim.Task("t2", 20, ["coder"]),
            sim.Task("t3", 5, ["leader"]),
        ]
    )

    project.simulate()
    assert project.get_task("t1").completed_by.name == "louis"


# missing capabilities (graceful project failure)

# multiple possible assignments

# sub-optimal solution

# task dependencies
