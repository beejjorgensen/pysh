#!/usr/bin/env python3

import sys, os

def internal(args):
    if args[0] == "cd":
        if len(args) != 2:
            print(f"usage: cd directory", file=sys.stderr)
        else:
            try:
                os.chdir(args[1])
            except Exception as e:
                print(f"cd: {e.strerror}", file=sys.stderr)
        return True

    elif args[0] == "exit":
        if len(args) > 2:
            print(f"usage: exit [status]", file=sys.stderr)
        else:
            if len(args) > 1:
                try:
                    sys.exit(int(args[1]))
                except ValueError:
                    print("exit: non-integer status", file=sys.stderr)
            else:
                sys.exit(0)
        return True

    return False

done = False

while not done:
    try:
        line = input("pysh$ ").strip()
    except EOFError:
        print()
        done = True
        continue

    if line == "":
        continue

    args = line.split()

    if internal(args):
        continue

    try:
        cid = os.fork()
    except OSError as e:
        print(f"fork: {e.strerror}", file=sys.stderr)
        continue

    if cid == 0:
        try:
            # child process
            os.execvp(args[0], args)
        except OSError as e:
            print(f"{args[0]}: {e.strerror}", file=sys.stderr)
            sys.exit()

    os.wait()

