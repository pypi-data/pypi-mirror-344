import depoc
import click
import time
import sys

from typing import Any

from .utils._response import _handle_response
from .utils._format import _format_response, spinner


client = depoc.DepocClient()


@click.group
def supplier() -> None:
    ''' Manage suppliers. '''

@supplier.command
def create() -> None:
    ''' Create supplier. '''
    click.echo(f'\n{'ADD NEW SUPPLIER':-<50}')

    data: dict[str, Any] = {}
    data.update({'code': input('Supplier Internal Code: ')})
    data.update({'legal_name': input('Legal Name: ')})
    data.update({'trade_name': input('Trade Name: ')})
    data.update({'cnpj': input('CNPJ: ')})
    data.update({'ie': input('IE: ')})
    data.update({'im': input('IM: ')})
    data.update({'notes': input('Notes: ')})
    data.update({'phone': input('Phone: ')})
    data.update({'email': input('Email: ')})
    data.update({'postcode': input('Postal Code: ')})
    data.update({'city': input('City: ')})
    data.update({'state': input('State: ')})
    data.update({'address': input('Address: ')})

    click.echo(f'{'':-<50}')

    service = client.suppliers.create

    if obj := _handle_response(service, data):
        title = obj.legal_name
        header = f'{obj.id}\n'
        highlight = obj.trade_name
        _format_response(obj, title, header, highlight)

@supplier.command
@click.argument('id')
def get(id: str) -> None:
    ''' Retrieve an specific supplier. '''
    service = client.suppliers.get

    if obj := _handle_response(service, resource_id=id):
        title = obj.legal_name
        header = f'{obj.id}\n'
        highlight = obj.trade_name
        _format_response(obj, title, header, highlight)

@supplier.command
@click.option('-l', '--limit', default=50)
@click.option('-p', '--page', default=0)
@click.option('-d', '--detailed', is_flag=True)
def all(limit: int, page: int, detailed: bool) -> None:
    ''' Retrieve all customers. '''
    service = client.suppliers.all

    if response := _handle_response(service, limit=limit, page=page):
        click.echo(f'\nResults: {response.count}')
        if limit < response.count:
            click.echo(
                f'Showing: {len(response.results)} out of {response.count}'
            ) 
        if response.next:
            click.echo(f'For next page: --page <number>')

        for obj in response.results:
            title = obj.legal_name
            header = f'{obj.id}'
            highlight = obj.trade_name

            remove = [] if detailed else \
            [item for item in obj.to_dict().keys() if item != '-']

            _format_response(obj, title, header, highlight, remove=remove)

@supplier.command
@click.argument('id')
@click.option('-c', '--code')
@click.option('-ln', '--legal_name')
@click.option('-tn', '--trade_name')
@click.option('-p', '--phone')
@click.option('-e', '--email')
@click.option('-p', '--postcode')
@click.option('-s', '--state')
@click.option('--cnpj')
@click.option('--ie')
@click.option('--im')
@click.option('--notes')
@click.option('--city')
@click.option('--address')
def update(
    id: str,
    code: str,
    legal_name: str,
    trade_name: str,
    notes: str,
    phone: str,
    email: str,
    postcode: str,
    city: str,
    state: str,
    address: str,
    cnpj: str,
    ie: str,
    im: str,
    ) -> None:
    ''' Update an specific supplier. '''
    data: dict[str, Any] = {}
    data.update({'code': code}) if code else None
    data.update({'legal_name': legal_name}) if legal_name else None
    data.update({'trade_name': trade_name}) if trade_name else None
    data.update({'cnpj': cnpj}) if cnpj else None
    data.update({'ie': ie}) if ie else None
    data.update({'im': im}) if im else None
    data.update({'notes': notes}) if notes else None
    data.update({'phone': phone}) if phone else None
    data.update({'email': email}) if email else None
    data.update({'postcode': postcode}) if postcode else None
    data.update({'city': city}) if city else None
    data.update({'state': state}) if state else None
    data.update({'address': address}) if address else None

    service = client.suppliers.update

    if obj := _handle_response(service, data, resource_id=id):
        header = f'{obj.id}\n'
        highlight = obj.trade_name
        _format_response(obj, 'UPDATED', header, highlight, color='green')

@supplier.command
@click.argument('ids', nargs=-1)
def delete(ids: str) -> None:
    ''' Delete an specific supplier. '''
    service = client.suppliers.delete

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
