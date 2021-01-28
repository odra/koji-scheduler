import os
import sys
from enum import Enum
import time
import logging
import argparse

from typing import Any, Optional, Dict
import koji #type: ignore
from koji.util import to_list #type: ignore

from koji_builder_kube import config, session, errors, host, utils


class Modes(Enum):
  TEST = 1
  DAEMON = 2

mode = Modes[os.environ.get('MODE', 'DAEMON')]


logger = logging.getLogger('koji.builder')
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def session_setup(opts: Dict[Any, Any]) -> Any: #TODO
  """
  Build the correct session object and login to a koji-hub server.

  Raises an `errors.BaseError` (subclasses) in case of unexpected problems.
  """
  stype = ''
  if 'serverca' in opts and 'cert' in opts:
    stype = 'ssl'
  s = session.get(stype, **opts)
  if s is None:
    raise errors.KojiError('Unable to idenify authentication type.')
  s.login()
  if not s.is_ok():
    raise errors.AuthError('Unable to validate session')
  return s


def run(*args: Any, **kwargs: Any) -> None:
  """
  Glue all CLI functions together.

  `Modes.TEST` will stop the loop on its first iteraction,
  it should be used for testing purposes (such as unit testing).
  """
  # ArgumentParser setup
  parser = argparse.ArgumentParser()
  parser.add_argument("-c", "--config",
  help="kojid configuration file path",
  default="/etc/kojid/kojid.conf")

  # koji-builder options setup
  ns = parser.parse_args(*args, **kwargs)
  c = config.Config.from_path(ns.config)
  opts = c.section('kojid')
  
  # koji-builder session setup
  logger.info('Authenticating...')
  s = session_setup(opts)
  s.session.exclusiveSession(force=True)
  logger.info('Authenticated.')

  # runner setup (kube, mock, etc)
  # scheduler setup (uses runner)
  # task handler setup (used by runners)
  # log each setup step

  h = host.Host(s.session, 'mbbox.default', capacity=3.0)
  h.sync()

  host_id = s.session.host.getID()
  logger.info(f'Using koji-builder host id: "{host_id}".')

  st_expired = koji.BR_STATES['EXPIRED']
  states = [koji.BR_STATES[k] for k in koji.BR_STATES]
  tasks: Dict[Any, Any] = {}
  loop_interval = int(os.environ.get('KOJI_BUILDER_INTERVAL', '5'))

  while True:
    #build roots
    build_roots = s.session.listBuildroots(hostID=host_id, state=tuple(states))
    logger.info(f'Total Build Roots found: {len(build_roots)}')
    build_roots = dict([(row['id'], row) for row in build_roots])
    for k, v in build_roots.items():
      task_id = v['task_id']
      uid = v['id']
      tag_name = v['tag_name']
      arch = v['arch']
      if task_id is None:
        # not associated with a task
        # this makes no sense now, but may in the future
        logger.warning(f'Expiring taskless buildroot: {uid}/{tag_name}/{arch}')
        s.session.host.setBuildRootState(id, st_expired)
      elif task_id not in tasks:
        logger.info('Expiring buildroot: {uid}/{tag_name}/{arch}')
        logger.debug(f'Buildroot task: {task_id}, Current tasks: {to_list(tasks.keys())}')
        s.session.host.setBuildRootState(uid, st_expired)
        continue
    #tasks
    tasks = h.get_tasks()
    if len(tasks) == 0:
      logger.info('0 tasks found, sleeping for 5 seconds.')
      utils.wait(loop_interval)
      continue
    print(tasks)

    # scheduler checks for new tasks (see flow)
    # identify the type of task handler to use
    # scheduler provision a task to run (pod running with some command?)
    # task status check + update (most likely includes FS updates and koji-hub api calls)
    # may need to store logs someplace else
    # errors should have a status of failure and store logs
    if mode == Modes.TEST:
      break
    elif mode == Modes.DAEMON:
      utils.wait(loop_interval)


def main() -> None:
  """
  Function to be used by a script
  as the main CLI entrypoint.
  """
  try:
    run()
  except errors.BaseError as e:
    sys.stderr.write(f'{str(e)}\n')
    sys.exit(e.code)
