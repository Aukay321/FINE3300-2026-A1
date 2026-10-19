from pathlib import Path # I imported the Path module to make it easier to work from the script's own folder.

class ExchangeRates:
    #As required by the assignment, the class was created in order to read the exchange rate from a CSV file and perform currency conversions.
    #After importing the Path module, the path to the CSV file is in the same folder as the script, so it can be read.
    def __init__(self, filename):
        path = Path(__file__).parent / filename
        #I implement the concept from chapter 14 of the Python book, which is using the read mode to the CSV file.
        f = open(path, "r")
        data = f.read().split("\n") #Read the whole CSV file as a string and split it into a list of lines.  
        f.close() #Close the file after reading it.
        rows = []
        for n in data:
            row = n.split(",") #Split each line into a list of values and append it to the rows list.
            rows.append(row) #add the row to the rows list.
        self.rate = float(rows[-1][-2]) 
        #Since the second last column contain the correct exchange rate and the last row contrains the latest exchange rate, I can access it by using the index -1 for the last row and -2 for the second last column.
#Defining the convert method to perform the currency conversion based on the input and output currencies.
    def convert(self, amount, input_currency, output_currency):
        if input_currency.upper() == output_currency.upper(): 
            #if the input and output currencies are the same, just print the amount without any conversion.
            print(f"The amount is {amount} {input_currency.upper()}")
        elif input_currency.upper() == "CAD" and output_currency.upper() == "USD": 
            # if the input currency is CAD and the output currency is USD, convert the amount to USD by dividing it by the exchange rate and print it.
            print(f"The amount is {amount / self.rate:.2f} USD")
        elif input_currency.upper() == "USD" and output_currency.upper() == "CAD":
            # if the input currency is USD and the output currency is CAD, convert the amount to CAD by multiplying it by the exchange rate and print it.
            print(f"The amount is {amount * self.rate:.2f} CAD")
        else:
            # if the input and output currencies are not USD or CAD, print an error message.
            print("Please only enter USD or CAD.")


converter = ExchangeRates("BOC_ExchangeRate2026.csv") #create an instance of the ExchangeRates class and pass the CSV file name to it.
amount = float(input("Enter the amount: ")) #Ask the user the amount.
input_currency = input("Input currency (CAD or USD): ") #Ask the user the input currency.
output_currency = input("Output currency (CAD or USD): ") #Ask the user the output currency.

converter.convert(amount, input_currency, output_currency) #execute the convert method of the ExchangeRates class with the user inputs.
