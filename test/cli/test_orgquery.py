import pytest
from click.testing import CliRunner
from moto import (
    mock_organizations,
    mock_sts,
)
from orgcrawler import orgs, utils
from orgcrawler.cli import orgquery
from ..test_orgs import (
    MASTER_ACCOUNT_ID,
    ORG_ACCESS_ROLE,
    SIMPLE_ORG_SPEC,
    build_mock_org,
)


@mock_sts
@mock_organizations
def test_jsonfmt():
    account = orgs.OrgAccount(
        orgs.Org(MASTER_ACCOUNT_ID, ORG_ACCESS_ROLE),
        name='account01',
        id='112233445566',
        email='account01@example.org',
    )
    output = orgquery.jsonfmt(account)
    assert isinstance(output, str)


@mock_sts
@mock_organizations
@pytest.mark.parametrize('options_list', [
    (['--help']),
    (['--version']),
    (['--role', ORG_ACCESS_ROLE, 'dump']),
    (['--role', ORG_ACCESS_ROLE, '--format', 'yaml', 'dump']),
    (['--role', ORG_ACCESS_ROLE, '--format', 'yaml', 'list_accounts_in_ou', 'root']),
])
def test_orgquery_success(options_list):
    org_id, root_id = build_mock_org(SIMPLE_ORG_SPEC)
    runner = CliRunner()
    result = runner.invoke(
        orgquery.main,
        options_list,
    )
    assert result.exit_code == 0


@mock_sts
@mock_organizations
@pytest.mark.parametrize('options_list', [
    (['--blee']),
    (['--role']),
    (['--role', ORG_ACCESS_ROLE, 'bogus_command']),
    (['--role', ORG_ACCESS_ROLE, '--format', 'blee', 'dump']),
    (['--role', ORG_ACCESS_ROLE, 'dump', 'bogus_arg']),
    (['--role', ORG_ACCESS_ROLE, 'list_accounts_in_ou']),
])
def test_orgquery_failure(options_list):
    org_id, root_id = build_mock_org(SIMPLE_ORG_SPEC)
    runner = CliRunner()
    result = runner.invoke(
        orgquery.main,
        options_list,
    )
    assert result.exit_code != 0
