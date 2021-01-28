from typing import Any, Dict, List, Optional


class Host:

  uid: int = -1
  name: str = ''
  capacity: float = 1.0
  task_load = 0.0
  __session: Any
  tasks: Dict[Any, Any] = {}
  archs: List[str] = []

  def __init__(self, session: Any, name: str,
    capacity: float = 1.0, archs: List[str] = ['noarch', 'x86_64']):
    """
    Create a new Host instance.
    """
    self.name = name
    self.capacity = capacity
    self.archs = archs
    self.__session = session

  def sync(self, capacity: bool = True, task_load: bool = True, remote: bool = False) -> None:
    """
    Syncs local host data from koji-hub.
    """
    self.uid = self.session.host.getID()
    data = self.__session.host.getLoadData()
    hosts = [h for h in data[1] if h['name'] == self.name]
    if len(hosts) == 0:
      return
    host = hosts[0]
    if capacity:
      self.capacity = host['capacity']
    if task_load:
      self.task_load = host['task_load']
    if remote:
      self.__session.host.updateHost(self.capacity, self.has_capacity())

  def has_capacity(self, weight: Optional[float] = None) -> bool:
    """
    Checks if host has capacity of running a task.
    """
    if weight is None:
      return self.task_load > self.capacity
    return (self.task_load + weight) > self.capacity
    

  def update_capacity(self, weight: float) -> None:
    """
    Updates host task capacity (both locally and in koji-hub).
    """
    has_capacity = self.has_capacity(weight)
    self.__session.host.updateHost(self.capacity - weight, has_capacity)

  def get_tasks(self) -> List[Dict[Any, Any]]:
    """
    Retrieves available tasks for the host.
    """
    '''
    [
      {
        'arch': 'noarch',
        'channel_id': 2,
        'create_time':'2021-01-26 09:51:25.691821+00:00',
        'host_id': None,
        'id': 1,
        'method': 'newRepo',
        'priority': 15,
        'state': 0
      },
      {
        'arch': 'noarch',
        'channel_id': 1,
        'create_time': '2021-01-26 12:14:08.202635+00:00',
        'host_id': None,
        'id': 3, 'method': 'build',
        'priority': 20,
        'state': 0
      }
    ] 
    '''
    data = self.__session.host.getLoadData()
    tasks: List[Dict[Any, Any]] = [t for t in data[1] if t['arch'] in self.archs]

    return tasks
