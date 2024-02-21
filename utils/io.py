# -*- coding: utf-8 -*-

"""
	Copyright (C) 2023  Soheil Khodayari, CISPA
	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU Affero General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.
	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU Affero General Public License for more details.
	You should have received a copy of the GNU Affero General Public License
	along with this program.  If not, see <http://www.gnu.org/licenses/>.
	
	Description:
	------------
	IO utility functions 

"""
import io
import subprocess
import os
import argparse
import signal
import os
import re
import shutil
import json
import yaml
from threading import Timer


def load_config_yaml(yaml_file):
	"""
	loads a yaml config into json
	"""
	fd = open(yaml_file, "r")
	config = yaml.safe_load(fd)
	fd.close()
	return config

def run_os_command(cmd, print_stdout=True, timeout=30*60, cwd='default', log_command=False, prettify=False):
  
  """
  @description run a bash command
  """

  def kill(process): 
    logger.warning('Killing Process.')
    logger.warning('TimeoutExpired (%s seconds) for cmd: %s'%(str(timeout), cmd))
    # kill the whole process group (i.e., including all subprocesses, not just the process)
    # process.kill()
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    

  
  if log_command:
    logger.debug('Running command: %s'%cmd)
    
  if cwd == 'default':
    p = subprocess.Popen(cmd, start_new_session=True, shell=True, stdout = subprocess.PIPE, stderr= subprocess.PIPE)
  else:
    p = subprocess.Popen(cmd, start_new_session=True, shell=True, stdout = subprocess.PIPE, stderr= subprocess.PIPE, cwd=cwd)
  my_timer = Timer(timeout, kill, [p])

  ret = -1
  try:
    my_timer.start()

    try:
      if print_stdout:
        if not prettify:
          if p.stdout:
            for line in io.TextIOWrapper(p.stdout, encoding="utf-8"):
              if len(line.strip()) > 0:
                logger.info(line.strip())   

          if p.stderr:
            for line in io.TextIOWrapper(p.stderr, encoding="utf-8"):
              if len(line.strip()) > 0:
                logger.info(line.strip()) 
        else:
          if p.stdout:
            lst = []
            for line in io.TextIOWrapper(p.stdout, encoding="utf-8"):
              if len(line.strip()) > 0:
                lst.append(line.strip())
            logger.info(re.sub(' +', ' ', '\n'.join(lst)))

          if p.stderr:
            lst = []
            for line in io.TextIOWrapper(p.stderr, encoding="utf-8"):
              if len(line.strip()) > 0:
                lst.append(line.strip())
            logger.info(re.sub(' +', ' ', '\n'.join(lst)))
    except Exception as e:
      logger.warning('error while reading the stdout')
      logger.error(e)
    p.wait(timeout=timeout)
    # ret = p.returncode
    ret = 1
  except subprocess.TimeoutExpired:
    logger.warning('TimeoutExpired (%s s)for cmd: %s'%(str(timeout), cmd))
    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
    ret = -1
  finally:
    my_timer.cancel()

  return ret

def get_json_file_content(file_path_name):
  """
  return the text content of a given file
  """
  fd = open(file_path_name, 'r')
  content = json.load(fd)
  fd.close()
  return content