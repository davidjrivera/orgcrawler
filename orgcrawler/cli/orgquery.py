#!/usr/bin/env python
"""
Script for querying AWS Organization resources
"""

import click
from orgcrawler import orgs, utils
from orgcrawler.cli.orgcrawler import print_version


_COMMANDS = [
    'dump',
    'dump_accounts',
    'dump_org_units',
    'list_accounts_by_name',
    'list_accounts_by_id',
    'list_org_units_by_name',
    'list_org_units_by_id',
]
_COMMANDS_WITH_ARG = [
    'get_account',
    'get_account_id_by_name',
    'get_account_name_by_id',
    'get_org_unit_id',
    'list_accounts_in_ou',
    'list_accounts_in_ou_recursive',
    'list_org_units_in_ou',
    'list_org_units_in_ou_recursive',
]
AVAILABLE_COMMANDS = _COMMANDS + _COMMANDS_WITH_ARG
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


def jsonfmt(obj):
    return utils.jsonfmt(obj, orgs.OrgObject.dump)


def validate_command(ctx, param, value):
    if value not in AVAILABLE_COMMANDS:
        raise click.BadParameter('{}\n{}'.format(value, main.__doc__))
    return value


def validate_command_argument(ctx, param, value):
    if ctx.params['command'] in _COMMANDS_WITH_ARG and not value:
        raise click.UsageError('Query command "{}" requires an argument\n{}'.format(
            ctx.params['command'], main.__doc__)
        )
    return value


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument('command', callback=validate_command)
@click.argument('argument', nargs=1, required=False, callback=validate_command_argument)
@click.option('--role', '-r',
    required=True,
    help='IAM role to assume for accessing AWS Organization Master account.')
@click.option('--format', '-f',
    default='json',
    type=click.Choice(['json', 'yaml']),
    help='Output format [default: json]')
@click.option('--version', '-V',
    is_flag=True,
    callback=print_version,
    expose_value=False,
    is_eager=True,
    help='Display version info and exit.')
def main(command, argument, role, format):
    """
Arguments:

    \b
    COMMAND     An organization query command to run
    ARGUMENT    A command argument to supply if needed

Available Query Commands:

    \b
    dump
    dump_accounts
    dump_org_units
    list_accounts_by_name
    list_accounts_by_id
    list_org_units_by_name
    list_org_units_by_id
    get_account ACCOUNT_IDENTIFIER
    get_account_id_by_name ACCOUNT_NAME
    get_account_name_by_id ACCOUNT_ID
    get_org_unit_id OU_IDENTIFIER
    list_accounts_in_ou OU_IDENTIFIER
    list_accounts_in_ou_recursive OU_IDENTIFIER
    list_org_units_in_ou OU_IDENTIFIER
    list_org_units_in_ou_recursive OU_IDENTIFIER

Examples:

    \b
    orgquery -r OrgMasterRole list_accounts_by_name
    orgquery -r OrgMasterRole -f json get_account_id_by_name webapps
    """

    if format == 'json':
        formatter = jsonfmt
    elif format == 'yaml':
        formatter = utils.yamlfmt

    master_account_id = utils.get_master_account_id(role)
    org = orgs.Org(master_account_id, role)
    org.load()
    cmd = eval('org.' + command)
    if argument:
        print(formatter(cmd(argument)))
    else:
        print(formatter(cmd()))


if __name__ == '__main__':
    main()  # pragma no cover
