#!/usr/bin/env python

"""
Script for querying AWS Organization resources

Usage:
    organizer [-h]
    organizer [-f format] [-m master_account_id] -r role COMMAND [ARGUMENT]

Arguments:
    COMMAND     An organizer query command to run
    ARGUMENT    A command argument to supply if needed

Options:
    -h, --help              Print help message
    -f format               Output format:  "json" or "yaml". [Default: json]
    -m master_account_id    The master account id for the organization
    -r role                 The AWS role name to assume when running organizer

Available Query Commands:
    dump
    dump_json
    list_accounts
    list_accounts_by_name
    list_accounts_by_id
    list_org_units
    list_org_units_by_name
    list_org_units_by_id
    list_accounts_in_ou OU_NAME
    list_accounts_in_ou_by_name OU_NAME
    list_accounts_in_ou_by_id OU_NAME
    list_accounts_under_ou OU_NAME
    list_accounts_under_ou_by_name OU_NAME
    list_accounts_under_ou_by_id OU_NAME
    get_account_id_by_name ACCOUNT_NAME
    get_account_name_by_id ACCOUNT_ID
    get_org_unit_id_by_name OU_NAME
"""


import sys
from docopt import docopt
from organizer import orgs, utils
from organizer.utils import get_master_account_id


_COMMANDS = [
    'dump',
    'dump_json',
    'list_accounts',
    'list_accounts_by_name',
    'list_accounts_by_id',
    'list_org_units',
    'list_org_units_by_name',
    'list_org_units_by_id',
]
_COMMANDS_WITH_ARG = [
    'list_accounts_in_ou',
    'list_accounts_in_ou_by_name',
    'list_accounts_in_ou_by_id',
    'list_accounts_under_ou',
    'list_accounts_under_ou_by_name',
    'list_accounts_under_ou_by_id',
    'get_account_id_by_name',
    'get_account_name_by_id',
    'get_org_unit_id_by_name',
]
AVAILABLE_COMMANDS = _COMMANDS + _COMMANDS_WITH_ARG


def main():
    args = docopt(__doc__)
    if len(sys.argv) == 1:
        sys.exit(__doc__)
    if args['COMMAND'] not in AVAILABLE_COMMANDS:
        print('ERROR: "{}" not an available query command'.format(args['COMMAND']))
        sys.exit(__doc__)
    if args['COMMAND'] in _COMMANDS_WITH_ARG and not args['ARGUMENT']:
        print('ERROR: Query command "{}" requires an argument'.format(args['COMMAND']))
        sys.exit(__doc__)
    if args['-f'] == 'json':
        formatter = utils.jsonfmt
    elif args['-f'] == 'yaml':
        formatter = utils.yamlfmt
    else:
        print('ERROR: Print format must be either "json" or "yaml"')
        sys.exit(__doc__)

    if args['-m'] is None:
        master_account_id = get_master_account_id(args['-r'])
    else:
        master_account_id = args['-m']

    org = orgs.Org(master_account_id, args['-r'])
    org.load()
    cmd = eval('org.' + args['COMMAND'])
    if args['ARGUMENT']:
        print(formatter(cmd(args.get('ARGUMENT'))))
    else:
        print(formatter(cmd()))


if __name__ == '__main__':
    main()