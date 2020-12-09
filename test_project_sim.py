import project_sim as sim


def test_simple_test():
    project = sim.Project("Simple Project")

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
    project = sim.Project("Project with multi-dependency task")

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
def test_no_capabilities_for_task():
    project = sim.Project("Project we don't have a capability to complete")

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
            sim.Task("t2", 20, ["underwater basket weaving"]),
            sim.Task("t3", 5, ["leader"]),
        ]
    )

    project.simulate()
    assert project.get_task("t2").completed_by == None


# task dependencies
def test_task_dependencies():
    project = sim.Project("Project with task dependencies")

    project.staff(
        [
            sim.Person("charlie", ["coder", "leader"]),
            sim.Person("louis", ["sa", "leader"]),
            sim.Person("wing", ["leader", "coder", "sa"]),
        ]
    )

    project.define(
        [
            sim.Task("t1", 5, ["leader"], blocked_by="t3"),
            sim.Task("t2", 10, ["sa", "leader"]),
            sim.Task("t3", 20, ["coder"]),
        ]
    )

    project.simulate()
    assert project.get_task("t3").completed_by.name == "charlie"


# staff gains capability after project start

# multiple possible assignments

# sub-optimal solution
