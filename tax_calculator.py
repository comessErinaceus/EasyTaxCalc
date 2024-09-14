import argparse
import json




CONSOLE_APP_NAME = "Quick Tax Calc"

# Federal and State backup file locations
DEFAULT_FEDERAL_BACKUP_PATH = 'backups/federal_backup.json'
DEFAULT_STATE_BACKUP_PATH = 'backups/state_backup.json'

# Federal and State working copy file locations
DEFAULT_FEDERAL_BRACKETS = 'federal_tax_brackets.json'
DEFAULT_STATE_BRACKETS = 'state_taxes.json'

#Load tax brackets
def load_tax_brackets(filename):
    with open(filename, 'r') as file:
        return json.load(file)
    
def save_tax_brackets(filename, tax_brackets):
    with open(filename, 'w') as file:
        json.dump(tax_brackets, file, indent=2)
    
#Path to tax brackets file
tax_brackets_file = DEFAULT_FEDERAL_BRACKETS
tax_brackets = load_tax_brackets(tax_brackets_file)

def calculate_tax(income, filing_status, tax_brackets):
    brackets = tax_brackets.get(filing_status)
    if not brackets:
        raise ValueError("Invalid filing status")
    tax = 0
    #previous_bracket_max = 0

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

def calculate_state_tax(income, filing_status, state):
    state_brackets = load_tax_brackets(DEFAULT_STATE_BRACKETS)

            #if we have the brackets modification is possible
    if state not in state_brackets:
        print(f"State '{state}' not found in the tax data.")

    brackets = state_brackets.get(state)
    tax=0

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
        

# Update the tax brackets for the state from json file
def update_tax_brackets_from_file(state, file_path):
    tax_brackets = load_tax_brackets(DEFAULT_STATE_BACKUP_PATH )

    if state not in tax_brackets:
        print(f"State '{state}' not found in the tax data.")
    

    try:
        with open(file_path, 'r') as input_file:
            new_brackets = json.load(input_file)
            #print(new_brackets)
        #print('...\n\n')
        tax_brackets[state] = new_brackets
        #print("All Data:{",tax_brackets)
        save_tax_brackets(DEFAULT_STATE_BACKUP_PATH , tax_brackets)
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON in file '{file_path}': {e}")


# Update the tax brackets for the state from manual inputs
def update_tax_brackets(state, brackets):
    if brackets:
        #get original brackets
        tax_brackets = load_tax_brackets(DEFAULT_STATE_BACKUP_PATH )

        #if we have the brackets modification is possible
        if state not in tax_brackets:
            print(f"State '{state}' not found in the tax data.")
        

        # input list should be a list of bracket dictionaries
        new_brackets = [
            {"lower": brackets[i], "upper":brackets[i + 1], "rate": brackets[i + 2]}
            for i in range(0, len(brackets), 3)
        ]

        #print("New brackets: ", new_brackets)
        tax_brackets[state] = new_brackets
        save_tax_brackets(DEFAULT_STATE_BRACKETS, tax_brackets)
        print(f"Tax brackets for '{state}' updated successfully.")


# Prompt user for brackets interactively
def prompt_user_for_brackets():
    brackets = []
    times_through_loop = 0
    while True:
        if(times_through_loop==0):
            try:
                lower = float(input("Enter the lower bound of the first bracket (or type 'done' to finish): "))
                upper = float(input("Enter the upper bound of the first bracket: "))
                rate = float(input("Enter the rate for this bracket (as a decimal, e.g., 0.05 for 5%)"))

                brackets.extend([lower, upper, rate])
                times_through_loop+=1
            except ValueError:
                user_input = input("Invalid input. Type 'done' to finish or press Enter to retry: ")
                if user_input == 'done':
                    break
                continue
        else:
            try:
                lower = upper
                upper = float(input("Enter the next upper bound (or type 'done' to finish): "))
                rate = float(input("Enter the rate for this bracket (as a decimal, e.g., 0.05 for 5%)"))
                brackets.extend([lower, upper, rate])
                
            except ValueError:
                user_input = input("Invalid input. Type 'done' to finish or press Enter to retry: ")
                if user_input == 'done':
                    break
                continue
            

    return brackets

# Restore Backup functionality
def restore_backup(backup_type):
    if backup_type == "Federal":
        backup_path = DEFAULT_FEDERAL_BACKUP_PATH

    elif backup_type == "State":
        backup_path = DEFAULT_STATE_BACKUP_PATH
    else:
        raise ValueError(f"Unknown backup type: {backup_type}")
    

    try:
        tax_brackets = load_tax_brackets(backup_path)
        
        if(backup_type == "Federal"):
            save_tax_brackets(DEFAULT_FEDERAL_BRACKETS, tax_brackets)
        elif(backup_type == "State"):
            save_tax_brackets(DEFAULT_STATE_BRACKETS, tax_brackets)
        print(f"{backup_type} tax brackets restored successfully from {backup_path}")
    except Exception as e:
        print(f"Error restoring {backup_type} tax brackets: {e}")




# Handle CLI args
def main():
    parser = argparse.ArgumentParser(description = 'Calculate US Federal Income Tax')
    subparsers = parser.add_subparsers(dest='command')

    # Subparser for tax calculation
    calc_parser = subparsers.add_parser('calculate', help='Calculate tax based on income and filing status.')

    calc_parser.add_argument('-i', '--income', type=float, help='Annual income')
    calc_parser.add_argument('-fS', '--filing_status', choices=['single', 'married_joint'], help='File status')
    calc_parser.add_argument('-s', '--state', help='State of Residence')


    #Subparser for updating the tax brackets
    update_parser = subparsers.add_parser('update-file', help='Update tax brackets for a state.')
    update_parser.add_argument('-s', '--state', type=str, required=True, help='The state to update')
    update_parser.add_argument('-f', '--file', type=str, required=True, help='Path to JSON file with new tax brackets.')


    update_parser = subparsers.add_parser('update-input', help='Update tax brackets for a state manually.')
    update_parser.add_argument('-s', '--state', type=str, required=True, help='The state to update')
    update_parser.add_argument('--manual', action='store_true',  help='Input the lower, upper bounds, and rates manually.')

     # Subparser for restoring backups
    restore_parser = subparsers.add_parser('restore-backup', help='Restore tax brackets from backup.')
    restore_parser.add_argument('-F', '--federal_tax_bracket_restore', action='store_true', help="Restore the working copy of Federal tax brackets to the 2024 default.")
    restore_parser.add_argument('-S', '--state_tax_bracket_restore', action='store_true', help="Restore the working copy of State tax brackets to the 2024 default.")
    

    args = parser.parse_args()



## Tool logic

    if args.command == 'calculate':
       

        try:
            #calculate_tax pulls in the tax brackets data in the function, why pass that data to the funct?
            tax = calculate_tax(float(args.income), args.filing_status, tax_brackets)
            print(f'The calculated tax for an income of ${args.income} as {args.filing_status} is ${tax:.2f}')

            state_tax = calculate_state_tax(args.income, args.filing_status, args.state)
            print(f'The calculated tax for an income of ${args.income} as {args.filing_status} is ${state_tax:.2f}')
        except ValueError as e:
            print(e)
    elif args.command == 'update-file':
        # try:
            # new_brackets = json.loads(args.brackets)
        update_tax_brackets_from_file(args.state, args.file)
        # except json.JSONDecodeError:
        #     print("Invalid JSON format for new tax brackets. ")
    elif args.command == 'update-input':
        if args.manual:
            brackets = prompt_user_for_brackets()
            update_tax_brackets(args.state, brackets)
        else:
            print("Please use the (-m) --manual flag to input tax brackets manually.")

    elif args.command == 'restore-backup':
        if args.federal_tax_bracket_restore:
            print("Restoring federal backup")
            restore_backup("Federal")
        if args.state_tax_bracket_restore:
            restore_backup("State")
            print("Restoring State backup")

if __name__ == '__main__':
    main()