import argparse
import sys


def main():
    """
    Main entry point for the database dumper application.

    This function parses command line arguments and executes the appropriate
    actions based on the provided options.
    """
    parser = argparse.ArgumentParser(description='Dump data from production database to local database')
    parser.add_argument(
        '-n',
        '--name',
        help='Name of the table to dump',
        type=str,
        required=True,
    )
    parser.add_argument(
        '-v',
        '--visualize',
        help='Visualize the table chain without dumping data',
        action=argparse.BooleanOptionalAction,
        default=False,
    )
    parser.add_argument(
        '-f',
        '--full-tree',
        help='Only visualize the table chain without dumping data',
        action=argparse.BooleanOptionalAction,
        default=False,
    )
    parser.add_argument(
        '-c',
        '--cut-columns',
        help='Cut columns which don`t presented in target table',
        action=argparse.BooleanOptionalAction,
        default=False,
    )
    parser.add_argument(
        '-d',
        '--delete-data',
        help='Delete data from target table',
        action=argparse.BooleanOptionalAction,
        default=False,
    )

    parser.add_argument(
        '-t',
        '--target',
        help='Target database',
        type=str,
    )
    parser.add_argument(
        '-s',
        '--source',
        help='source database',
        type=str,
    )

    kwargs = vars(parser.parse_known_args()[0])
    if 'name' in kwargs:
        from .config import settings
        from .dump import dump_data
        from .utils import get_all_related_chain, get_table_chain

        settings.set_names(kwargs.get('source'), kwargs.get('target'))
        table_chain = get_all_related_chain(
            *reversed(kwargs['name'].split('.')),
            full_tree=kwargs['full_tree'],
        )

        if kwargs.get('visualize'):
            print('Table Chain Visualization:')
            print(get_table_chain(table_chain))
            return 0
        dump_data(table_chain, kwargs['cut_columns'], kwargs['delete_data'])
        try:
            print('Data dump completed successfully')
            return 0
        except Exception as e:
            print(f'Error during data dump: {str(e)}')
            return 1


if __name__ == '__main__':
    sys.exit(main())
