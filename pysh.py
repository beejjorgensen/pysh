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

    else:
        # Not an internal command
        return False

    return True

# Main loop

while True:
    # Get input
    try:
        line = input("pysh>> ").strip()
    except EOFError:
        # Handle ^D
        print()       # Makes things look nice
        sys.exit(0)

    if line == "":
        continue

    args = line.split()

    # Try internal commands, e.g. "cd" or "exit"
    if internal(args):
        continue

    # Must be an external command
    try:
        # Make a new process
        cid = os.fork()
    except OSError as e:
        print(f"fork: {e.strerror}", file=sys.stderr)
        continue

    if cid == 0:
        # We're the child process
        try:
            # Try to run the command
            os.execvp(args[0], args)
        except OSError as e:
            print(f"{args[0]}: {e.strerror}", file=sys.stderr)

            # If the child gets here, the exec must have
            # failed. So let's exit to keep the children
            # from clogging up the main loop.
            sys.exit()

    # Parent wait for child to complete
    os.wait()

