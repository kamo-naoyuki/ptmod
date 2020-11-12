import argparse
import collections
from pathlib import Path
import shlex
from typing import Union
from typing import Sequence
import warnings

import torch


def modify(
    operations: Sequence[str],
):
    states = {}

    modified = set()
    for s in operations:
        s = s.strip()
        commands = shlex.split(s)
        if commands[0] == "rm":
            for c in commands[1:]:
                if ":" not in c:
                    raise RuntimeError(
                        f"Must be a form as filepath:key, but got {c}"
                    )
                var, key = c.split(":", 1)
                if var not in states:
                    states[var] = torch.load(var, map_location=torch.device('cpu'))

                state = states[var]
                new_state = {}
                found = False
                for k, v in state.items():
                    if not (k == key or k.startswith(f"{key}.")):
                        new_state[k] = v
                        found = True
                if not found:
                    raise RuntimeError(
                        f"Key '{key}' is not found in {var}"
                    )
                states[var] = new_state
                modified.add(var)

        elif commands[0] == "cp":
            if len(commands) != 3:
                raise RuntimeError(
                    f"Must be a form as 'cp src dest', but got {s}"
                )
            for c in commands[1:]:
                if ":" not in c:
                    var = c
                else:
                    var, key = c.split(":", 1)

            src_state = {}
            if ":" not in commands[1]:
                var1 = commands[1]
                if var1 not in states:
                    states[var1] = torch.load(var1, map_location=torch.device('cpu'))
                src_state = states[var1]
            else:
                var1, key1 = commands[1].split(":", 1)
                if var1 not in states:
                    states[var1] = torch.load(var1, map_location=torch.device('cpu'))
                for k, v in states[var1].items():
                    if k == key1 or k.startswith(f"{key1}."):
                        src_state[k[len(key1):]] = v
                if len(src_state) == 0:
                    raise RuntimeError(
                        f"Key '{key1}' is not found in {var1}"
                    )

            if ":" not in commands[2]:
                var2 = commands[2]
                key2 = ""
            else:
                var2, key2 = commands[2].split(":", 1)

            if var2 not in states:
                if not Path(var2).exists():
                    states[var2] = {}
                else:
                    states[var2] = torch.load(var2, map_location=torch.device('cpu'))
            for k, v in src_state.items():
                if key2 == "":
                    if k == "":
                        raise RuntimeError("No key name is specified")
                    if k.startswith("."):
                        states[var2][k[1:]] = v
                    else:
                        states[var2][k] = v
                else:
                    if key2.endswith(".") and k.startswith("."):
                        states[var2][key2 + k[1:]] = v
                    elif not key2.endswith(".") and not k.startswith("."):
                        states[var2][key2 + "." + k] = v
                    else:
                        states[var2][key2 + k] = v

            modified.add(var2)

        elif commands[0] == "ls":
            for var in commands[1:]:
                if var not in states:
                    states[var] = torch.load(var, map_location=torch.device('cpu'))
                for k in states[var]:
                    print(k)
        else:
            raise RuntimeError

        for var in modified:
            torch.save(states[var], var)


def get_parser():
    parser = argparse.ArgumentParser(
        description="Modify PyTorch model file",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("operations", nargs="+")
    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()
    modify(**vars(args))


if __name__ == "__main__":
    main()

