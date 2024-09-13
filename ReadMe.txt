Using the tool

calculate:
    python tax_calculator.py calculate -i 50000 -fS Single


update-file:
    python tax_calculator.py update -s Alabama -b "[{\"lower\": 0, \"upper\": 12000, \"rate\": 0.015}, {\"lower\": 12000, \"upper\": 25000, \"rate\": 0.025}, 
    {\"lower\": 25000, \"upper\": 50000, \"rate\": 0.035}, {\"lower\": 50000, \"upper\": 1.7976931348623157e+308, \"rate\": 0.045}]"

    -s; --state: define the state to be modified
    -f; --file: JSON file path with new tax brackets.


update-input
    Update a tax bracket by manually prompting the user for brackets and rates.

    -s; --state: define the state to be modified.
    --manual: prompt the user to input tax bracket info manually.


restore-backup
    -F: Restore federal tax brackets from backup of 2024 historical tax rates.
    -S: Restore state tax brackets from backup of 2024 historical tax rates.






create_state_files.ps1
    Description: This file creates the StateTaxes directory and files with an empty json file for each StateTaxes

        If execution of powershell file is restricted 
            1. Get-ExecutionPolicy { Restricted | RemoteSigned | Unrestricted }.
            2. Set-ExecutionPolicy { Restricted | RemoteSigned | Unrestricted }.
