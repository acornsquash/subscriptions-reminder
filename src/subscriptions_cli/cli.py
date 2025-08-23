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

# add a new subscription
@cli.command()
@click.argument("name")
@click.option("--cost", type=float, required=True)
@click.option("--renewal", type=click.DateTime(formats=["%Y-%m-%d"]), required=True)
@click.option("--interval", type=click.Choice(["monthly", "yearly"]), required=True)
def add(name, cost, renewal, interval):
    """Add a new subscription"""
    data = load_data()
    data.append({
        "name": name,
        "cost": cost,
        "renewal_date": renewal.strftime("%Y-%m-%d"),
        "interval": interval,
        "active": "true"
    })
    save_data(data)
    click.echo(f"✨ Added subscription: {name}")

# change a subscription's data, also update the renewal date once it passes
@cli.command()
@click.argument("name")
@click.option("--cost", type=float, help="New cost")
@click.option("--renewal", type=click.DateTime(formats=["%Y-%m-%d"]), help="New renewal date")
@click.option("--interval", type=click.Choice(["monthly", "yearly"]), help="Update billing interval")
@click.option("--active", type=click.Choice(["true", "false"]), help="set active or inactive")
def update(name, cost, renewal, interval, active):
    """Update an existing subscription"""
    data = load_data()
    updated = False

    for sub in data:
        if sub["name"].lower() == name.lower():
            if cost:
                sub["cost"] = cost
            if renewal:
                sub["renewal_date"] = renewal.strftime("%Y-%m-%d")
            if interval:
                sub["interval"] = interval
            if active:
                sub["active"] = active

            updated = True
            break

    if updated:
        save_data(data)
        click.echo(f"✨ Updated {name}")
    else:
        click.echo(f"🙅🏼‍♀️ Subscription not found: {name}")

@cli.command()
def auto_update():
    """Automatically update any subscriptions whose renewal date has passed"""
    data = load_data()
    today = datetime.today().date()
    bumped = []

    for sub in data:
        renewal_date = datetime.strptime(sub["renewal_date"], "%Y-%m-%d").date()
        if today > renewal_date:  # renewal date has passed
            if sub["interval"] == "monthly":
                # move forward one month
                month = renewal_date.month + 1
                year = renewal_date.year
                if month > 12:
                    month = 1
                    year += 1
                new_date = renewal_date.replace(year=year, month=month)
            else:  # yearly
                new_date = renewal_date.replace(year=renewal_date.year + 1)

            sub["renewal_date"] = new_date.strftime("%Y-%m-%d")
            bumped.append(f"{sub['name']} → {sub['renewal_date']}")

    if bumped:
        save_data(data)
        click.echo("🔄 Auto-updated renewals:\n" + "\n".join(bumped))
    else:
        click.echo("✨ No renewals to update today")



@cli.command()
def check():
    """Check for upcoming renewals"""
    data = load_data()
    today = datetime.today().date()

    for sub in data:
        renewal_date = datetime.strptime(sub["renewal_date"], "%Y-%m-%d").date()
        days_until = (renewal_date - today).days
        if days_until <= 1:
            click.echo(f"⚠️  {sub['name']} renews tomorrow at (${sub['cost']})")

if __name__ == "__main__":
    cli()
