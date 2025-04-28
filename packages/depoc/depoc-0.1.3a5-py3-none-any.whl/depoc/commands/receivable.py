import depoc
import click
import sys
import time

from typing import Any
from datetime import datetime

from .utils._response import _handle_response
from .utils._format import _format_response, spinner


client = depoc.DepocClient()


fields = (
    'contact',
    'issued_at',
    'updated_at',
    'payment_type',
    'installment_count',
    'due_weekday',
    'due_day_of_month',
    'reference',
    'recurrence',
    'status',
    'notes',
)


@click.group
def receivable() -> None:
    ''' Manage receivables. '''
    pass

@receivable.command
def create() -> None:
    ''' Create receivable. '''

    click.echo(f'\n{'ADD NEW RECEIVABLE':-<50}')

    data: dict[str, Any] = {}
    data.update({'total_amount': input('Total Amount: R$')})
    data.update({'due_at': input('Due At: ')})
    data.update({'issued_at': input('Issued At: ')})
    data.update({'payment_method': input('Payment Method: ')})

    while True:
        click.echo('\n• Once \n• Weekly \n• Monthly \n• Installments')
        recurrence = input('- Recurrence: ').strip().lower()

        if recurrence in ('once', 'monthly', 'weekly', 'installments'):
            data.update({'recurrence': recurrence})
            if recurrence == 'monthly':
                data.update({'due_day_of_month': input('- Due Day of Month: ')})
            elif recurrence == 'weekly':
                data.update({'due_weekday': input('- Due Weekday: ')})
            elif recurrence == 'installments':
                data.update({'installment_count': input('- Installments: ')})
            break

        message = click.style(
            '\nPlease choose a valid recurrence type.',
            fg='red'
        )
        click.echo(message)

    data.update({'category': input('\nCategory ID: ')})
    data.update({'contact': input('Contact ID: ')})
    data.update({'reference': input('Reference Number: ')})
    data.update({'notes': input('Notes: ')})

    click.echo(f'{'':-<50}')

    service = client.receivables.create

    if obj := _handle_response(service, data):
        title = f'\n{obj.contact}'
        header = f'R$ {obj.outstanding_balance}'
        highlight = f'{obj.status.upper()}'
        _format_response(obj, title, header, highlight)

@receivable.command
@click.argument('id')
def get(id: str) -> None:
    ''' Retrieve an specific receivable. '''
    service = client.receivables.get

    if obj := _handle_response(service, resource_id=id):
        title = f'\n{obj.contact}'
        header = f'R$ {obj.outstanding_balance}'
        highlight = f'{obj.status.upper()}'
        _format_response(obj, title, header, highlight)

@receivable.command
@click.option('-l', '--limit', default=50)
@click.option('-p', '--page', default=0)
@click.option('-d', '--detailed', is_flag=True)
@click.option('-u', 'unpaid', is_flag=True)
def all(limit: int, page: int, detailed: bool, unpaid: bool) -> None:
    ''' Retrieve all receivables. '''
    service = client.receivables.all

    total_receivable: float = 0

    if response := _handle_response(service, limit=limit, page=page):
        results = sorted(response.results, key=lambda obj: obj.due_at)

        if unpaid:
            results = [obj for obj in results if obj.status != 'paid']
            click.echo(f'\nResults: {len(results)}')
        elif not unpaid:
            click.echo(f'\nResults: {response.count}')
            if limit < response.count:
                click.echo(
                    f'Showing: {len(response.results)} out of {response.count}'
                ) 
            if response.next:
                click.echo(f'For next page: --page <number>')

        for obj in results:
            total_receivable += float(obj.outstanding_balance)
            title = f'\n{obj.contact}'
            header = f'R$ {obj.outstanding_balance}'
            highlight = f'{obj.status.replace('_', ' ').upper()}'

            remove = [] if detailed else \
            [item for item in obj.to_dict().keys() if item in fields]

            _format_response(obj, title, header, highlight, remove=remove)

        division = click.style(f'\n{'':-<49}', bold=True)
        click.echo(division)
        format_total_receivable = f'R$ {total_receivable:.2f}'
        txt = f'\n{'Total to be received: ' + format_total_receivable:>50}\n'
        click.echo(txt)

@receivable.command
@click.argument('id')
@click.option('-ct', '--contact')
@click.option('-cg', '--category')
@click.option('-ia', '--issued-at')
@click.option('-da', '--due-at')
@click.option('-pa', '--paid-at')
@click.option('-t', '--total-amount')
@click.option('-pm', '--payment-method')
@click.option('-r', '--reference')
@click.option('-n', '--notes')
def update(
    id: str,
    contact: str,
    category: str,
    issued_at: str,
    due_at: str,
    paid_at: str,
    total_amount: float,
    payment_method: str,
    reference: str,
    notes: str,
    ) -> None:
    ''' Update an specific receivable. '''
    data: dict[str, Any] = {}
    data.update({'contact': contact}) if contact else None
    data.update({'category': category}) if category else None
    data.update({'issued_at': issued_at}) if issued_at else None
    data.update({'due_at': due_at}) if due_at else None
    data.update({'paid_at': paid_at}) if paid_at else None
    data.update({'total_amount': total_amount}) if total_amount else None
    data.update({'payment_method': payment_method}) if payment_method else None
    data.update({'reference': reference}) if reference else None
    data.update({'notes': notes}) if notes else None

    service = client.receivables.update

    if obj := _handle_response(service, data, resource_id=id):
        header = f'R$ {obj.outstanding_balance}'
        highlight = f'{obj.status.upper()}'
        _format_response(obj, 'UPDATED', header, highlight, color='green')

@receivable.command
@click.argument('ids', nargs=-1)
def delete(ids: str) -> None:
    ''' Delete an specific receivable. '''
    service = client.receivables.delete

    while True:
        prompt = click.style('Proceed to deletion? [y/n] ', fg='red')
        confirmation = input(prompt)
        if confirmation == 'n':
            sys.exit(0)
        elif confirmation == 'y':
            break

    if len(ids) > 1:
        spinner()

    for id in ids:
        time.sleep(0.5)
        if obj := _handle_response(service, resource_id=id):
            _format_response(obj, 'DELETED', 'Done', color='red')

@receivable.command
@click.argument('id')
@click.option('--amount', required=True)
@click.option('--account', required=True)
def settle(id: str, amount: float, account: str) -> None:
    ''' Settle a receivable '''
    data: dict[str, Any] = {'amount': amount, 'account': account}

    service = client.receivable_settle.create

    if obj := _handle_response(service, data, id):
        header = f'R$ {obj.amount}'
        title = f'{obj.account.name} {obj.type}'
        timestamp = datetime.fromisoformat(obj.timestamp)
        obj.timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S')
        remove = [
            'type',
            'description',
            'amount',
            'payment',
            'linked',
            'account',
            'operator',
        ]

        _format_response(
            obj=obj,
            title=title,
            header=header,
            highlight=obj.description,
            remove=remove
        )

@receivable.command
@click.option('-s', '--search')
@click.option('-d', '--date')
@click.option('-sd', '--start-date')
@click.option('-ed', '--end-date')
@click.option('-l', '--limit', default=50)
@click.option('--detailed', is_flag=True)
@click.pass_context
def filter(
    ctx,
    search: str,
    date: str,
    start_date: str,
    end_date: str,
    limit: int,
    detailed: bool,
    ) -> None:
    ''' Filter receivables. '''
    if not any([search, date, start_date, end_date]):
        click.echo(ctx.get_help())
        sys.exit(0)

    total_receivable: float = 0
    service = client.receivables.filter

    if response := _handle_response(
        service,
        search=search,
        date=date,
        start_date=start_date,
        end_date=end_date,
        limit=limit,
    ):
        click.echo(f'\nResults: {response.count}')
        click.echo(f'\nResults: {response.count}')
        if limit < response.count:
            click.echo(
                f'Showing: {len(response.results)} out of {response.count}'
            ) 
        if response.next:
            click.echo(f'For next page: --page <number>')

        results = sorted(response.results, key=lambda obj: obj.due_at)

        for obj in results:
            total_receivable += float(obj.outstanding_balance)
            title = f'\n{obj.contact}'
            header = f'R$ {obj.outstanding_balance}'
            highlight = f'{obj.status.replace('_', ' ').upper()}'

            remove = [] if detailed else \
            [item for item in obj.to_dict().keys() if item in fields]

            _format_response(obj, title, header, highlight, remove=remove)

        division = click.style(f'\n{'':-<49}', bold=True)
        click.echo(division)
        format_total_receivable = f'R$ {total_receivable:.2f}'
        txt = f'\n{'Total to be received: ' + format_total_receivable:>50}\n'
        click.echo(txt)
