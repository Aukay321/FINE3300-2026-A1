import csv
import glob
import os
import sys


class ExchangeRates:
    """Reads a Bank of Canada exchange rate CSV and converts between USD and CAD."""

    PAIR_COLUMN = "FXAUSDCAD"  # 1 USD expressed in CAD
    SUPPORTED = ("USD", "CAD")

    def __init__(self, filename):
        self.filename = filename
        self.date = None
        self.usd_cad = self._load_latest_rate()

    def _load_latest_rate(self):
        """Return the USD/CAD rate from the last row of the file."""
        last_row = None
        # utf-8-sig strips the BOM that this file starts with
        with open(self.filename, newline="", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            if self.PAIR_COLUMN not in (reader.fieldnames or []):
                raise ValueError(f"Column {self.PAIR_COLUMN} not found in {self.filename}")
            for row in reader:
                if row.get(self.PAIR_COLUMN, "").strip():
                    last_row = row
        if last_row is None:
            raise ValueError("No USD/CAD data found in file.")
        self.date = last_row["Date"]
        return float(last_row[self.PAIR_COLUMN])

    def convert(self, amount, from_currency, to_currency):
        """Convert amount from one currency (USD or CAD) to the other."""
        src, dst = from_currency.strip().upper(), to_currency.strip().upper()
        for c in (src, dst):
            if c not in self.SUPPORTED:
                raise ValueError(f"Unsupported currency '{c}'. Use USD or CAD.")
        if src == dst:
            return amount
        if src == "USD":           # USD -> CAD
            return amount * self.usd_cad
        return amount / self.usd_cad   # CAD -> USD


def prompt_amount():
    while True:
        try:
            value = float(input("Enter the amount: ").replace(",", ""))
            if value < 0:
                print("Amount cannot be negative.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number.")


def prompt_currency(label):
    while True:
        c = input(f"Enter the '{label}' currency (USD or CAD): ").strip().upper()
        if c in ExchangeRates.SUPPORTED:
            return c
        print("Please enter either USD or CAD.")


def find_csv():
    """Find the exchange rate CSV in the same folder as this script.

    Tries the exact file name first, then any CSV with 'ExchangeRate' in its
    name (e.g. 'BankOfCanadaExchangeRate_2026 (1).csv').
    """
    folder = os.path.dirname(os.path.abspath(__file__))
    exact = os.path.join(folder, "BankOfCanadaExchangeRate_2026.csv")
    if os.path.exists(exact):
        return exact
    matches = sorted(glob.glob(os.path.join(folder, "*ExchangeRate*.csv")))
    if matches:
        return matches[0]
    print(f"Could not find the exchange rate CSV in:\n  {folder}\n")
    print("Files in that folder:")
    for name in sorted(os.listdir(folder)):
        print("  ", name)
    sys.exit(1)


def main():
    filename = sys.argv[1] if len(sys.argv) > 1 else find_csv()
    rates = ExchangeRates(filename)
    print(f"Latest USD/CAD rate ({rates.date}): 1 USD = {rates.usd_cad} CAD\n")

    amount = prompt_amount()
    src = prompt_currency("from")
    dst = prompt_currency("to")

    result = rates.convert(amount, src, dst)
    print(f"\n{amount:,.2f} {src} = {result:,.2f} {dst}")


if __name__ == "__main__":
    main()