"""
Topic: HR System Assignment
Change_Log:
IBRAR, Created file, 05/30/2021
IBRAR, Added code, 06/01/2021
"""

# !/usr/bin/env python3
import sys
import csv
from datetime import datetime, date, timedelta


# Read data from csv file
def read_data(csv_file):
    data_list = []
    with open(csv_file, mode="r") as infile:
        csv_reader = csv.DictReader(infile)
        for line in csv_reader:
            data_list.append(line)
    return data_list


# Write data to csv file
def write_data(csv_file, updated_data_list):
    with open(csv_file, mode='w') as outfile:
        csv_writer = csv.DictWriter(outfile, updated_data_list[0].keys())
        csv_writer.writeheader()
        csv_writer.writerows(updated_data_list)
    print("\nFile updated")


# convert date strings into datetime format
def reformat_list(list_to_be_reformatted):
    reformatted_list = []
    for employee in list_to_be_reformatted:
        employee["Employee_Date_of_birth"] = datetime.strptime(str(employee["Employee_Date_of_birth"]), "%m/%d/%y").date()
        employee["Start_date"] = datetime.strptime(str(employee["Start_date"]), "%y-%m-%d").date()
        if employee["End_date"] != "":
            employee["End_date"] = datetime.strptime(str(employee["End_date"]), "%y-%m-%d").date()
        reformatted_list.append(employee)
    return reformatted_list


# Produce list of current employees
def get_current_employees(list_of_all_employees):
    current_employees = []
    for employee in list_of_all_employees:
        if employee["End_date"] == "":
            current_employees.append(employee)
    return sorted(current_employees, key=lambda i: i["Employee_ID"])


# Produce list of employees that left in the past month
def get_past_month_leaving_employees(list_of_employees):
    past_employees = []
    previous = (date.today().replace(day=1) - timedelta(days=1))
    previous_month = previous.month
    for employee in list_of_employees:
        if employee["End_date"] != "":
            if employee["End_date"].month == previous_month:
                past_employees.append(employee)
    return sorted(past_employees, key=lambda i: i["Employee_ID"])


def print_employee_report(list_to_be_printed):
    headers = list(list_to_be_printed[0].keys())
    employee_table = [headers]
    for employee in list_to_be_printed:
        employee_table.append([str(employee[header]) for header in headers])
    column_width = [max(map(len, column)) for column in zip(*employee_table)]
    table_format = " ".join(["{{:<{}}}".format(i) for i in column_width])
    for row in employee_table:
        print(table_format.format(*row))


# Add new employee
def get_new_employee_data( ):
    ID = input("Please enter Employee_ID: ")
    name = input("Please enter Employee_name: ")
    address = input("Please enter Employee_address: ")
    ssn = input("Please enter Employee_SSN (###-##-####): ")
    dob = input("Please enter Employee_Date_of_birth (mm/dd/yy): ")
    title = input("Please enter Job_title: ")
    start_date = input("Please enter Start_date (mm/dd/yy): "),
    employee_dict = {}
    employee_dict["Employee_ID"] = str(ID)
    employee_dict["Employee_name"] = str(name)
    employee_dict["Employee_address"] = str(address)
    employee_dict["Employee_SSN"] = str(ssn)
    employee_dict["Employee_Date_of_birth"] = str(dob)
    employee_dict["Job_title"] = str(title)
    employee_dict["Start_date"] = str(start_date)
    employee_dict["End_date"] = ""
    return employee_dict

def add_new_employee(list_of_dictionaries):
    new_employee_list = []
    new_employee_list.append(get_new_employee_data())
    updated_list = []
    list_of_dictionaries.extend(new_employee_list)
    for myDict in list_of_dictionaries:
        if myDict not in updated_list:
            updated_list.append(myDict)
    print("\nThe employee has been successfully added to the list.")
    return updated_list


# Display reminders for annual review 3 months before individual review date
def review_reminder_list(employees_list):
    reminder_list = []
    for employee in employees_list:
        review_date = employee["Start_date"].replace(year=date.today().year)
        reminder_date = review_date - timedelta(days=-90)
        employee_review_data = {"Review_date": review_date, "Reminder_date": reminder_date}
        if reminder_date.month == date.today().month:
            reminder_list.append(employee)
            for employee_up_for_review in reminder_list:
                employee_up_for_review.update(employee_review_data)
    return reminder_list

def lookup_employee_entry(name, list_to_be_searched):
    employee_entry = []
    for employee in list_to_be_searched:
        if employee["Employee_name"].lower() == name.lower():
            employee_entry.append(employee)
    return employee_entry

# Edit employee data
def update_employee(list_to_be_updated):
    name = input("\nPlease input employee's name: ")
    print("Here are the current employee details:\n")
    print_employee_report(lookup_employee_entry(name, list_to_be_updated))
    print("\nPlease enter the information you would like to enter:")
    key_to_update = input("Data_field: ")
    if key_to_update in ("Employee_Date_of_birth", "Start_date","End_date"):
        updated_value = input("New date (mm/dd/yy): ")
    else:
        updated_value = input ("New data: ")
    updated_employee_list = []
    for employee in list_to_be_updated:
        if employee["Employee_name"].lower() == name.lower():
            employee[key_to_update] = updated_value
        updated_employee_list.append(employee)
    print("\nThe employee data has been successfully updated.")
    return updated_employee_list

#menu of options
def menu_and_choice():
    while True:
        try:
            user_main_choice = int(input("""
    The menu options are:
          1 - View a report,
          2 - Add a new employee,
          3 - Change an existing employee data,
          4 - Save updated data to file,
          5 - Quit
    Please input your choice [1-5]: """))
        except ValueError:
            print("\tInvalid Input")
            continue

        if user_main_choice not in range(1, 5 + 1):
            print("\tInvalid Input")
            continue

        return user_main_choice

def report_menu():
    while True:
        try:
            user_sub_choice = int(input("""
    The report menu options are:
          1 - View list of all current employees,
          2 - View list of all employees who left in the previous month,
          3 - View list of all employees who are due for an annual review reminder
          4 - Return to main menu
    Please input your choice [1-4]: """))
        except ValueError:
            print("\tInvalid Input")
            continue

        if user_sub_choice not in range(1, 4 + 1):
            print("\tInvalid Input")
            continue

        return user_sub_choice


def report_action(source_list):
    while True:
        choice = report_menu()
        if choice == 1:
            list_of_all_employees = reformat_list(source_list)
            print_employee_report(get_current_employees(list_of_all_employees))
        elif choice == 2:
            list_of_employees = reformat_list(source_list)
            print_employee_report(get_past_month_leaving_employees(list_of_employees))
        elif choice == 3:
            employees_list = reformat_list(source_list)
            print_employee_report(review_reminder_list(employees_list))
        elif choice == 4:
            break

def exit_program():
    print("\nGood Bye!")
    sys.exit()  # exit the interactive script

def main():
    print("\tWelcome to the HR System!")
    employees_list = read_data("Employees.csv")
    while True:
        response = menu_and_choice()
        if response == 1:
            report_action(employees_list)
        elif response == 2:
            employees_list = add_new_employee(employees_list)
        elif response == 3:
            employees_list = update_employee(employees_list)
        elif response == 4:
            write_data("Employees.csv", employees_list)
        elif response == 5:
            exit_program()


if __name__ == "__main__":
    main()

