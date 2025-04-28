import depoc
import click

from .utils._response import _handle_response


client = depoc.DepocClient()


@click.command
@click.option('-d', '--date', default='week')
@click.option('-sd', '--start-date')
@click.option('-ed', '--end-date')
@click.pass_context
def balance(ctx, date: str, start_date: str, end_date: str) -> None:
    ''' Balance for a specific period. '''
    division = f'{'':->50}'

    if start_date and end_date:
        date = ''
        click.echo(f'{start_date +  ' - ' + end_date:>50}')
    else:
        click.echo(f'\n{date.upper():>50}')


    income: float = 0
    expenses: float = 0
    balance: float = 0
    
    service = client.financial_transactions.filter

    if response := _handle_response(
        service,
        date=date,
        start_date=start_date,
        end_date=end_date,
        ):
        for obj in response.results:
            if obj.type == 'credit':
                income += float(obj.amount)
            elif obj.type == 'debit':
                expenses += float(obj.amount)

        click.echo(division)
        format_income = f'R$ {income:.2f}'
        txt = f'INCOME{format_income:>44}'
        click.echo(txt)
        click.echo(division)

        format_expenses = f'R$ {expenses:.2f}'
        txt = f'EXPENSES{format_expenses:>42}'
        click.echo(txt)

        balance = round(income + expenses, 2)
        color = 'red' if balance < 0 else 'green'
        
        format_balance = f'R$ {balance:.2f}'

        click.echo(click.style(division, fg=color, bold=True))
        
        txt = click.style(
            f'BALANCE{format_balance:>43}',
            fg=color,
            bold=True
        )
        click.echo(txt)

        click.echo(click.style(division, fg=color, bold=True))
