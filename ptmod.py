import argparse
import collections
import shlex
from typing import Sequence

import torch


def torch_load(fname):
    obj = torch.load(fname, map_location=torch.device("cpu"))
    if not isinstance(obj, collections.abc.Mapping):
        raise RuntimeError(f"{fname} must be dict, but got {type(obj)}")
    return obj


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
                    raise RuntimeError(f"Must be a form as filepath:key, but got {c}")
                var, key = c.split(":", 1)
                if var not in states:
                    states[var] = torch_load(var)

                state = states[var]
                new_state = {}
                found = False
                for k, v in state.items():
                    if not (k == key or k.startswith(f"{key}.")):
                        new_state[k] = v
                        found = True
                if not found:
                    raise RuntimeError(f"Key '{key}' is not found in {var}")
                states[var] = new_state
                modified.add(var)

        elif commands[0] == "cp":
            if len(commands) != 3:
                raise RuntimeError(f"Must be a form as 'cp src dest', but got {s}")
            src_state = {}
            if ":" not in commands[1]:
                var1 = commands[1]
                if var1 not in states:
                    states[var1] = torch_load(var1)
                src_state = states[var1]
            else:
                var1, key1 = commands[1].split(":", 1)
                if var1 not in states:
                    states[var1] = torch_load(var1)
                for k, v in states[var1].items():
                    if k == key1 or k.startswith(f"{key1}."):
                        src_state[k[len(key1) :]] = v
                if len(src_state) == 0:
                    raise RuntimeError(f"Key '{key1}' is not found in {var1}")

            if ":" not in commands[2]:
                var2 = commands[2]
                key2 = ""
            else:
                var2, key2 = commands[2].split(":", 1)

            if var2 not in states:
                states[var2] = {}
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
            if commands[1] == "-l":
                verbose = True
                commands = commands[1:]
            else:
                verbose = False

            for var in commands[1:]:
                if var not in states:
                    states[var] = torch_load(var)

                for k, v in states[var].items():
                    if verbose:
                        print(k, tuple(v.shape))
                    else:
                        print(k)

        elif commands[0] in ("average", "sum"):
            if len(commands) > 3:
                raise RuntimeError(
                    f"Require 2 or more arguments: '{commands[0]} out-file in-file...'"
                )

            out_states = {}
            for var in commands[2:]:
                if var not in states:
                    states[var] = torch_load(var)
                for k, v in states[var].items():
                    if k not in out_states:
                        out_states[k] = v
                    else:
                        out_states[k] += v

            if commands[0] == "average":
                for k, v in list(out_states.items()):
                    # For integer type, not dividing
                    if not str(out_states[k].dtype).startswith("torch.int"):
                        out_states[k] = v / len(commands[2:])
            states[commands[1]] = out_states
            modified.add(commands[1])

        else:
            raise RuntimeError(
                "Available commands:\n"
                "  ls model.pth\n"
                "  rm model.pth:key\n"
                "  average out.pth in.pth in2.pth...\n"
                "  sum out.pth in.pth in2.pth...\n"
            )

        for var in modified:
            torch.save(states[var], var)


def ptmod_ls():
    parser = argparse.ArgumentParser(
        description="Modify PyTorch model file",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("args", nargs="+")
    args = parser.parse_args()
    modify(["ls " + " ".join(args.args)])


def ptmod_rm():
    parser = argparse.ArgumentParser(
        description="Modify PyTorch model file",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("args", nargs="+")
    args = parser.parse_args()
    modify(["rm" + " ".join(args.args)])


def ptmod_cp():
    parser = argparse.ArgumentParser(
        description="Modify PyTorch model file",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("input")
    parser.add_argument("output")
    args = parser.parse_args()
    modify([f"cp {args.input} {args.output}"])


def ptmod_average():
    parser = argparse.ArgumentParser(
        description="Modify PyTorch model file",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("output")
    parser.add_argument("args", nargs="+")
    args = parser.parse_args()
    modify([f"average {args.output}" + " ".join(args.args)])


def ptmod_sum():
    parser = argparse.ArgumentParser(
        description="Modify PyTorch model file",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("output")
    parser.add_argument("args", nargs="+")
    args = parser.parse_args()
    modify([f"sum {args.output}" + " ".join(args.args)])


def ptmod_main():
    parser = argparse.ArgumentParser(
        description="Modify PyTorch model file",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("operations", nargs="+")
    args = parser.parse_args()
    modify(**vars(args))


if __name__ == "__main__":
    ptmod_main()
