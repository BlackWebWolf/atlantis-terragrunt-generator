#!/usr/bin/env python

#from collections import OrderedDict
import argparse
import os
import os.path
from yaml import dump

"""A script that can be used to generate an atlantis.yaml from the provided path."""

def find_terragrunt_projects(path):
  """Return a list of terragrunt project paths."""
  projects = []

  # list of directories to exclude from the config
  exclude = set(['.terragrunt-cache'])

  # return a list of all project paths
  for root, dirs, files in os.walk(path, topdown=True):
    dirs[:] = [d for d in dirs if d not in exclude]
    for file in [f for f in files if f.endswith("terragrunt.hcl")]:
      projects.append(os.path.relpath(root, './'))
  # remove top directory from list of projects
  # as it does not contain a deployable config
  projects.remove(path)

  return set(projects)

def generate_config(args):
  """Generate an atlantis.yaml config file."""
  # get list of projects
  projects = find_terragrunt_projects(args.path)

  # generate dict with empty project list
  # OrderedDict is useless as yaml.dump() sorts the dict.
  # see https://github.com/yaml/pyyaml/issues/110
  config = {
    'version': 3,
    'projects': [],
  }

  # add projects to the config dict
  for project in projects:
    project = {
      'dir': project
    }
    config['projects'].append(project)

  # create a YAML structure
  result = dump(config, default_flow_style=False)

  # write to output file if provided
  # otherwise write to stdout
  if args.output:
    with open(args.output, 'w') as new_config:
      new_config.write(result)
      exit(0)

  print("\nReplace the content of atlantis.yaml by this output:\n\n\n" + result + "\n")

def main():
  """Manage the script arguments."""
  parser = argparse.ArgumentParser(description='Generate an atlantis.yaml config from a terragrunt repository.')
  parser.add_argument('path', metavar='PATH',
                    help='path to the terragrunt repository')
  parser.add_argument('--output', '-o', metavar='FILE',
                    help='name of the created file. If no --output flag is used, the script will output to stdout')
  parser.set_defaults(func=generate_config)
  args = parser.parse_args()
  args.func(args)

if __name__=="__main__":
	main()
