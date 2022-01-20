from mindsync.cli import main
from mindsync.exc import MindsyncCliError

import sys


if __name__ == '__main__':
    try:
        main()
    except SystemExit:
        raise
    except MindsyncCliError as e:
        print(e.args[0], file=sys.stderr)
        e.args[1].print_help()
