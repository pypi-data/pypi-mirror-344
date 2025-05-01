import argparse
import os
import subprocess
import sys
import re

green = '\033[92m'
default = '\033[0m'

PARSER = argparse.ArgumentParser(description='Run a command with a subset of the environment.', epilog=f"{green}@readwithai{default} 📖⚡️🖋️ machine-aided reading 📖⚡️🖋️ {green}https://readwithai.substack.com/{default}")


PARSER.add_argument("command", type=str, nargs="+", help="command to run. Add -- before flags. E.g. `env-subset LANG -- python -m pdb`")
PARSER.add_argument("-e", "--variable", type=str, help="Add variable from surround scope. Use -e VAR=value to set a value", action="append")
PARSER.add_argument("-r", "--regexp", type=str, help="Add variables whose values match a regular expression", action="append")
PARSER.add_argument('-x', '--exclude', action='store_true', default=False, help="Exclude the given expressions but include everything else")
PARSER.add_argument('-f', '--file', help="Read expression from a file. File can be generated with printenv, but also supports variables names")







def main():
    args = PARSER.parse_args()

    new_env = {}
    existing_env = {}

    if args.file:
        with open(args.file) as f:
            for line in f.readlines():
                v = line.strip()
                if "=" in v:
                    if args.exclude:
                        raise Exception('Expressions are not supported when excluding')

                    v, _, value = v.partition("=")
                    new_env[v] = value
                elif v.startswith("/") and v.endswith("/"):
                    existing_env.update({k:value for k, value in os.environ.items() if re.search(v[1:-1], k)})
                else:
                    new_env[v] = os.environ[v]


    variables = args.variable or ()
    for v in variables:
        if "=" in v:
            if args.exclude:
                raise Exception('Expressions are not supported when excluding')

            v, _, value = v.partition("=")
            new_env[v] = value
        elif v.startswith("/") and v.endswith("/"):
            existing_env.update({k:value for k, value in os.environ.items() if re.search(v[1:-1], k)})
        else:
            new_env[v] = os.environ[v]



    regexps = args.regexp or ()
    for r in regexps:
        if r.startswith("/") and r.endswith("/"):
            r = r[1:-1]
        existing_env.update({k:value for k, value in os.environ.items() if re.search(r, k)})

    env = dict(**existing_env, **new_env)

    if args.exclude:
        env = {k: v for k,v in os.environ.items() if k not in env}

    sys.exit(subprocess.call(args.command, env=env))
