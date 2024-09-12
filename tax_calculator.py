import argparse;
import json;

#Load tax brackets
def load_tax_brackets(filename):
    with open(filename, 'r') as file:
        return json.load(file)
    
#Path to tax brackets file
tax_brackets_file = 'tax_brackets.json'
tax_brackets = load_tax_brackets(tax_brackets_file)

def calculate_tax(income, filing_status):
    brackets = tax_brackets.get(filing_status)
    if not brackets:
        raise ValueError("Invalid filing status")
    tax = 0
    previous_bracket_max = 0

    for bracket in brackets:
        lower = float(bracket['lower'])
        upper = float(bracket['upper'])
        rate = float(bracket['rate'])
        #print(lower, ' ', upper, ' ', rate)
        if income > lower:
            taxable_income = min(income, upper) - lower
            tax += taxable_income * rate
            #print("TAX:", tax)
        else:
            break

    return tax


def main():
    parser = argparse.ArgumentParser(description = 'Calculate US Federal Income Tax')
    parser.add_argument('-i', '--income', type=float, help='Annual income')
    parser.add_argument('-fS', 'filing_status', choices=['single', 'married_joint'], help='File status')
    args = parser.parse_args()

    try:
        tax = calculate_tax(float(args.income), args.filing_status)
        print(f'The calculated tax for an income of ${args.income} as {args.filing_status} is ${tax:.2f}')
    except ValueError as e:
        print(e)

if __name__ == '__main__':
    main()