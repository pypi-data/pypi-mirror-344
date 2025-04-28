import depoc
import click
import time
import sys

from typing import Any

from .utils._response import _handle_response
from .utils._format import _format_response, spinner


client = depoc.DepocClient()


@click.group
def customer() -> None:
    ''' Manage customers. '''

@customer.command
def create() -> None:
    ''' Create customer. '''

    click.echo(f'\n{'ADD NEW CUSTOMER':-<50}')

    data: dict[str, Any] = {}
    data.update({'code': input('Customer Internal Code: ')})
    data.update({'name': input('Name: ')})
    data.update({'alias': input('Customer Alias: ')})
    data.update({'gender': input('Gender: ').lower()})
    data.update({'cpf': input('CPF: ')})
    data.update({'notes': input('Notes: ')})
    data.update({'phone': input('Phone: ')})
    data.update({'email': input('Email: ')})
    data.update({'postcode': input('Postal Code: ')})
    data.update({'city': input('City: ')})
    data.update({'state': input('State: ')})
    data.update({'address': input('Address: ')})

    click.echo(f'{'':-<50}')

    service = client.customers.create

    if obj := _handle_response(service, data):
        title = obj.name
        header = f'{obj.id}\n'
        highlight = obj.alias
        _format_response(obj, title, header, highlight)

@customer.command
@click.argument('id')
def get(id: str) -> None:
    ''' Retrieve an specific customer. '''
    service = client.customers.get

    if obj := _handle_response(service, resource_id=id):
        title = obj.name
        header = f'{obj.id}\n'
        highlight = obj.alias
        _format_response(obj, title, header, highlight)

@customer.command
@click.option('-l', '--limit', default=50)
@click.option('-p', '--page', default=0)
@click.option('-d', '--detailed', is_flag=True)
def all(limit: int, page: int, detailed: bool) -> None:
    ''' Retrieve all customers. '''
    service = client.customers.all

    if response := _handle_response(service, limit=limit, page=page):
        click.echo(f'\nResults: {response.count}')
        if limit < response.count:
            click.echo(
                f'Showing: {len(response.results)} out of {response.count}'
            ) 
        if response.next:
            click.echo(f'For next page: --page <number>')

        for obj in response.results:
            title = obj.name
            header = f'{obj.id}\n'
            highlight = obj.alias

            remove = [] if detailed else \
            [item for item in obj.to_dict().keys() if item != '-']

            _format_response(obj, title, header, highlight, remove=remove)

@customer.command
@click.argument('id')
@click.option('-c', '--code')
@click.option('-n', '--name')
@click.option('-a', '--alias')
@click.option('-g', '--gender')
@click.option('-p', '--phone')
@click.option('-e', '--email')
@click.option('-p', '--postcode')
@click.option('-s', '--state')
@click.option('--cpf')
@click.option('--notes')
@click.option('--city')
@click.option('--address')
def update(
    id: str,
    code: str,
    name: str,
    alias: str,
    gender: str,
    cpf: str,
    notes: str,
    phone: str,
    email: str,
    postcode: str,
    city: str,
    state: str,
    address: str,
    ) -> None:
    ''' Update an specific customer. '''
    data: dict[str, Any] = {}
    data.update({'code': code}) if code else None
    data.update({'name': name}) if name else None
    data.update({'alias': alias}) if alias else None
    data.update({'gender': gender}) if gender else None
    data.update({'cpf': cpf}) if cpf else None
    data.update({'notes': notes}) if notes else None
    data.update({'phone': phone}) if phone else None
    data.update({'email': email}) if email else None
    data.update({'postcode': postcode}) if postcode else None
    data.update({'city': city}) if city else None
    data.update({'state': state}) if state else None
    data.update({'address': address}) if address else None

    service = client.customers.update

    if obj := _handle_response(service, data, resource_id=id):
        header = f'{obj.id}\n'
        highlight = obj.alias
        _format_response(obj, 'UPDATED', header, highlight, color='green')

@customer.command
@click.argument('ids', nargs=-1)
def delete(ids: str) -> None:
    ''' Delete an specific customer. '''
    service = client.customers.delete

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
