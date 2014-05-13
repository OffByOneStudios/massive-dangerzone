import queue
import threading
import abc
import functools

class Worker(threading.Thread):
    """Thread executing tasks from a given tasks queue"""
    def __init__(self, task_pool):
        super().__init__()
        self._task_pool = task_pool
        self.daemon = True
        self.start()
    
    def run(self):
        q = self._task_pool._priority
        while not self._task_pool._done:
            task = q.get()
            func, args, kargs = task.task_do()
            try:
                task.task_set_result(func(*args, **kargs), False)
            except Exception as e:
                self._task_pool._error(task, e)
                task.task_set_result(e, True)
            q.task_done()

class TaskPool(object):
    def __init__(self, num_threads, _error=lambda t, e: None):
        self._priority = queue.PriorityQueue()
        self._done = False
        self._error = _error
        
        self._threads = [Worker(self) for _ in range(num_threads)]

    def add_task(self, task):
        if not isinstance(task, ITask):
            raise Exception("Can only add tasks.")
        self._priority.put(task)
        return task

    def add_tasks(self, tasks):
        for task in tasks:
            self.add_task(task)
        return tasks

    def wait_completion(self):
        self._priority.join()

    def shut_down(self):
        self._done = True
        for thread in self._threads:
            thread.join()

@functools.total_ordering
class ITask(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def task_priority(self):
        pass
    @abc.abstractmethod
    def task_dependencies(self):
        pass
    @abc.abstractmethod
    def task_do(self):
        pass
    @abc.abstractmethod
    def task_set_result(self, value, is_exception):
        pass

    def _task_computed_priority(self, _set=None):
        if _set == None:
            _set = set()
        _set.add(self)
        pri = self.task_priority()
        
        for sub_task in self.task_dependencies():
            if sub_task in _set:
                continue
            sub_pri = sub_task._task_computed_priority(_set)
            if sub_pri < pri:
                pri = sub_pri
        return pri

    # Purposefully reversed
    def __gt__(self, other):
        return other > self._task_computed_priority()
    def __lt__(self, other):
        return other < self._task_computed_priority()

    

class Task(ITask):
    def __init__(self, _priority, _dependencies, _func, *args, **kwargs):
        super().__init__()
        self._priority = _priority
        self._dependencies = _dependencies
        self._do = (_func, args, kwargs)
    def task_priority(self):
        return self._priority
    def task_dependencies(self):
        return self._dependencies
    def task_do(self):
        return self._do
    def task_set_result(self, value, is_exception):
        self._is_exception = is_exception
        self._result = value
    def task_get_result(self, do_except=True):
        if self._is_exception and do_except:
            raise self._result
        return self._result
