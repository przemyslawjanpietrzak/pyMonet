from pymonet.task import Task


class TaskSpy:

    def resolved(self, value):
        return value

    def rejected(self, value):
        return value

    def mapper(self, arg):
        return arg + 1

    def side_effect(self, arg):  # remove?
        return arg

    def folder(self, arg):
        return Task(lambda reject, resolve: resolve(arg + 1))

    def fork_rejected(self, reject, _):
        reject(0)

    def fork_resolved(self, _, resolve):
        resolve(42)


def test_task_resolved_fork_should_be_called_only_during_calling_fork(mocker):
    task_spy = TaskSpy()
    mocker.spy(task_spy, 'resolved')
    mocker.spy(task_spy, 'rejected')
    mocker.spy(task_spy, 'fork_rejected')
    mocker.spy(task_spy, 'fork_resolved')

    task = Task(task_spy.fork_resolved)
    assert task_spy.fork_resolved.call_count == 0

    task.fork(task_spy.rejected, task_spy.resolved)
    assert task_spy.fork_resolved.call_count == 1
    assert task_spy.fork_rejected.call_count == 0
    assert task_spy.resolved.call_count == 1
    assert task_spy.rejected.call_count == 0


def test_task_rejected_fork_should_be_called_only_during_calling_fork(mocker):
    task_spy = TaskSpy()
    mocker.spy(task_spy, 'resolved')
    mocker.spy(task_spy, 'rejected')
    mocker.spy(task_spy, 'fork_rejected')
    mocker.spy(task_spy, 'fork_resolved')

    task = Task(task_spy.fork_rejected)
    assert task_spy.fork_resolved.call_count == 0

    task.fork(task_spy.rejected, task_spy.resolved)
    assert task_spy.fork_resolved.call_count == 0
    assert task_spy.fork_rejected.call_count == 1
    assert task_spy.fork_resolved.call_count == 0
    assert task_spy.fork_rejected.call_count == 1


def test_task_resolved_fork_should_return_resolved_value():
    def rejected_spy(_):
        assert False

    def resolved_spy(value):
        assert value == 42

    task_spy = TaskSpy()
    task = Task(task_spy.fork_resolved)
    task.fork(rejected_spy, resolved_spy)


def test_task_rejected_fork_should_return_resolved_value():
    def rejected_spy(value):
        assert value == 0

    def resolved_spy(_):
        assert False

    task_spy = TaskSpy()
    task = Task(task_spy.fork_rejected)
    task.fork(rejected_spy, resolved_spy)


def test_task_maper_should_be_called_during_calling_fork(mocker):
    task_spy = TaskSpy()
    mocker.spy(task_spy, 'mapper')

    task = Task(task_spy.fork_resolved).map(task_spy.mapper)
    assert task_spy.mapper.call_count == 0

    task.fork(task_spy.rejected, task_spy.resolved)
    assert task_spy.mapper.call_count == 1


def test_task_rejected_fork_should_not_applied_map_on_his_result():
    def rejected_spy(value):
        assert value == 0

    def resolved_spy(_):
        assert False

    task_spy = TaskSpy()
    task = Task(task_spy.fork_rejected).map(task_spy.mapper)
    task.fork(rejected_spy, resolved_spy)


def test_task_resolved_fork_should_applied_map_on_his_result():
    def rejected_spy(_):
        assert False

    def resolved_spy(value):
        assert value == 42 + 1

    task_spy = TaskSpy()
    task = Task(task_spy.fork_resolved).map(task_spy.mapper)
    task.fork(rejected_spy, resolved_spy)


def test_task_rejected_fork_should_not_applied_fold_on_his_result():
    def rejected_spy(value):
        assert value == 0

    def resolved_spy(_):
        assert False

    task_spy = TaskSpy()
    task = Task(task_spy.fork_rejected).fold(task_spy.folder)
    task.fork(rejected_spy, resolved_spy)


def test_task_resolved_fork_should_applied_fold_on_his_result():
    def rejected_spy(_):
        assert False

    def resolved_spy(value):
        assert value == 42 + 1

    task_spy = TaskSpy()
    task = Task(task_spy.fork_resolved).fold(task_spy.folder)
    task.fork(rejected_spy, resolved_spy)
