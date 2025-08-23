import json
import os
import click
from datetime import datetime

DATA_FILE = os.path.expanduser("~/.subscriptions.json")

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

@click.group()
def cli():
    """Simple subscription reminder CLI."""
    pass

@cli.command()
@click.argument("name")
@click.option("--cost", type=float, required=True)
@click.option("--renewal", type=click.DateTime(formats=["%Y-%m-%d"]), required=True)
@click.option("--interval", type=click.Choice(["monthly", "yearly"]), required=True)
@click.option("--remind", type=int, default=1, help="Days before renewal to remind")
def add(name, cost, renewal, interval, remind):
    """Add a new subscription"""
    data = load_data()
    data.append({
        "name": name,
        "cost": cost,
        "renewal_date": renewal.strftime("%Y-%m-%d"),
        "interval": interval,
        "remind_days_before": remind
    })
    save_data(data)
    click.echo(f"✅ Added subscription: {name}")

@cli.command()
def check():
    """Check for upcoming renewals"""
    data = load_data()
    today = datetime.today().date()

    for sub in data:
        renewal_date = datetime.strptime(sub["renewal_date"], "%Y-%m-%d").date()
        days_until = (renewal_date - today).days
        if days_until <= sub["remind_days_before"]:
            click.echo(f"⚠️  {sub['name']} renews in {days_until} days (${sub['cost']})")

if __name__ == "__main__":
    cli()
