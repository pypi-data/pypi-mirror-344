import argparse
import sys
from converter import CurrencyConverter
from InquirerPy import inquirer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box

# Initialize Rich console for attractive output
console = Console()

def display_currencies(converter):
    """Display available currencies in a formatted table"""
    currencies = converter.get_available_currencies()

    if not currencies:
        console.print(Panel.fit("❌ Failed to retrieve currency list. Check your internet connection.", 
                           title="Error", border_style="red"))
        return
    
    table = Table(title="Available Currencies", box=box.ROUNDED, show_header=True, header_style="bold cyan")
    table.add_column("Code", style="green")
    table.add_column("Currency Name", style="yellow")
    
    for currency in currencies:
        table.add_row(currency['code'], currency['name'])
    
    console.print(table)


def choose_currency_menu(converter):
    """Interactive menu to select and view a currency's details"""
    currencies = converter.get_available_currencies()

    if not currencies:
        console.print(Panel.fit("❌ Failed to fetch currencies.", title="Error", border_style="red"))
        return
    
    choices = [f"{c['code']} - {c['name']}" for c in currencies]
    
    selected = inquirer.select(
        message="Select a currency",
        choices=choices,
        pointer="→"
    ).execute()
    
    selected_code = selected.split(" - ")[0]

    selected_currency = next(c for c in currencies if c['code'] == selected_code)
    selected_unit = selected_currency['unit']
    result = converter.convert(selected_unit, selected_code)

    if not result:
        console.print(Panel.fit("❌ Could not fetch conversion data.", title="Error", border_style="red"))
        return

    details = [
        f"Currency Code : [green]{selected_code}[/green]",
        f"Buying Rate   : [yellow]{selected_unit} {selected_code} = {result['buying_rate']:.4f} NPR[/yellow]",
        f"Selling Rate  : [cyan]{selected_unit} {selected_code} = {result['selling_rate']:.4f} NPR[/cyan]",
    ]
    
    console.print(Panel.fit("\n".join(details), title="💱 Currency Details", border_style="blue"))


def convert_currency(converter, amount, target):
    """Convert and display currency conversion in an attractive format"""
    result = converter.convert(amount, target)

    if not result:
        console.print(Panel(f"Failed to convert {amount} NPR to {target}.\n"
                           "Please check your internet connection or try again later.",
                           title="❌ Conversion Error", border_style="red"))
        return

    # Header information
    header_text = "✅ Using current online data"
    header_style = "green"
    
    if result.get('is_offline'):
        header_text = "⚠️  USING OFFLINE DATA - rates may not be current"
        header_style = "yellow"
    
    # Format timestamps
    # updated_at = result.get('updated_at', 'Unknown')
    published_on = result.get('published_on', 'Unknown')
    
    # Create main table
    table = Table(box=box.ROUNDED, show_header=False, title="Currency Conversion Result")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="yellow")

    # Add status row with appropriate styling
    table.add_row("Status", f"[{header_style}]{header_text}[/{header_style}]")
    # table.add_row("Updated", updated_at)
    table.add_row("Published Rate Date", published_on)
    table.add_row("Amount", f"{amount:.2f} NPR")
    table.add_row("Target Currency", f"{result.get('to_currency')} (per {result.get('unit')} unit{'s' if result.get('unit', 1) > 1 else ''})")
    table.add_row("Buying Rate", f"{result.get('unit')} {result.get('to_currency')} = {result.get('buying_rate', 0):.4f} NPR")
    table.add_row("Selling Rate", f"{result.get('unit')} {result.get('to_currency')} = {result.get('selling_rate', 0):.4f} NPR")
    table.add_section()
    table.add_row("Converted Amount (Buying)", f"[bold green]{result.get('converted_buying', 0):.4f} {result.get('to_currency')}[/bold green]")
    table.add_row("Converted Amount (Selling)", f"[bold blue]{result.get('converted_selling', 0):.4f} {result.get('to_currency')}[/bold blue]")
    
    console.print(table)


def refresh_rates(converter):
    """Force refresh rates from API with visual feedback"""
    with console.status("[bold green]Refreshing exchange rates from Nepal Rastra Bank...", spinner="dots"):
        success = converter.load_rates(force_refresh=True)
    
    is_online = converter._check_internet_connection()

    if is_online:
        converter.load_rates(force_refresh=True)
        
        console.print(Panel.fit("✅ Exchange rates successfully updated!", 
                          title="Rate Refresh", border_style="green"))
    else:
        console.print(Panel.fit("❌ Failed to refresh exchange rates. Check your internet connection.", 
                          title="Rate Refresh Failed", border_style="red"))


def main():
    """Main entry point for currency converter CLI"""
    parser = argparse.ArgumentParser(
        description="Nepal Rastra Bank Currency Converter",
        epilog="Convert NPR to foreign currencies using official NRB exchange rates"
    )

    parser.add_argument(
        "-v", "--view-currencies",
        action="store_true",
        help="View all available currencies with their codes"
    )

    parser.add_argument(
        "-c", "--convert",
        type=float,
        metavar="AMOUNT",
        help="Amount in NPR to convert to foreign currency"
    )

    parser.add_argument(
        "-t", "--to-currency",
        type=str,
        help="Target currency code (e.g., USD, EUR, INR)"
    )

    parser.add_argument(
        "-r", "--refresh",
        action="store_true",
        help="Force refresh rates from the NRB API instead of using cached data"
    )

    parser.add_argument(
        "-i", "--interactive",
        action="store_true",
        help="Launch interactive mode to select currency and view rates"
    )

    args = parser.parse_args()
    converter = CurrencyConverter()

    if args.refresh:
        refresh_rates(converter)
        return
    
    if args.view_currencies:
        display_currencies(converter)
        return
    
    if args.interactive:
        choose_currency_menu(converter)
        return
    
    if args.convert is not None and args.to_currency:
        convert_currency(converter, args.convert, args.to_currency.upper())
        return

    # If no valid options were provided, show help
    parser.print_help()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user.[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        sys.exit(1)