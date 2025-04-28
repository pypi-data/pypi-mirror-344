import depoc
import click

from typing import Any

from .utils._response import _handle_response
from .utils._format import _format_response


client = depoc.DepocClient()


@click.group
def owner() -> None:
    ''' Owner - retrieve and update. '''
    pass

@owner.command
def get() -> None:
    ''' Retrive owner. '''
    service = client.owner.get

    if obj := _handle_response(service):
        _format_response(obj, obj.name, obj.email)

@owner.command
@click.option('-n', '--name')
@click.option('-e', '--email')
@click.option('-p', '--phone')
def update(name: str, email: str, phone: str) -> None:
    ''' Update owner. '''
    data: dict[str, Any] = {}
    data.update({'name': name}) if name else None
    data.update({'email': email}) if email else None
    data.update({'phone': phone}) if phone else None
    
    service = client.owner.update

    if obj := _handle_response(service, data):
        _format_response(obj, obj.name, obj.email)
