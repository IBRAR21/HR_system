"""
Topic: HR System Assignment
Change_Log:
IBRAR, Created file, 05/30/2021
IBRAR, Added code, 06/01/2021
"""

# !/usr/bin/env python3

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
    print("File updated")

#convert date strings into datetime format
def reformat_list(source_list):
    reformatted_list = []
    for employee in source_list:
       employee["Employee_Date_of_birth"] = datetime.strptime(employee["Employee_Date_of_birth"], "%m/%d/%y").date()
       employee["Start_date"] = datetime.strptime(employee["Start_date"], "%m/%d/%y").date()
       if employee["End_date"] != "":
           employee["End_date"] = datetime.strptime(employee["End_date"], "%m/%d/%y").date()
       reformatted_list.append(employee)
    return reformatted_list


# Produce list of current employees
def get_current_employees(source_list):
    current_employees = []
    for employee in source_list:
        if employee["End_date"] == "":
            employee.pop("End_date")
            current_employees.append(employee)
    return sorted(current_employees, key = lambda i: i["Employee_ID"])


# Produce list of employees that left in the past month
def get_past_month_leaving_employees(source_list):
    past_employees = []
    previous = (date.today().replace(day=1) - timedelta(days=1))
    previous_month = previous.month
    for employee in source_list:
        if employee["End_date"] != "":
            if employee["End_date"].month == previous_month:
                past_employees.append(employee)
    return sorted(past_employees, key = lambda i: i["Employee_ID"])


# Add new employee
def add_new_employee(source_list):
    New_employee = {
        "Employee_ID": input("Please enter Employee_ID: "),
        "Employee_name": input("Please enter Employee_name: "),
        "Employee_address": input("Please enter Employee_address: "),
        "Employee_SSN": input("Please enter Employee_SSN (###-##-####): "),
        "Employee_Date_of_birth": input("Please enter Employee_Date_of_birth (mm/dd/yyyy): "),
        "Job_title": input("Please enter Job_title: "),
        "Start_date": input("Please enter Start_date (mm/dd/yyyy): "),
        "End_date": ""
    }
    updated_list = source_list.append(New_employee)
    return updated_list


def print_employee_report(source_list):
    headers = list(source_list[0].keys())                                    
    employee_table = [headers]
    for employee in source_list:
        employee_table.append([str(employee[header]) for header in headers])
    column_width = [max(map(len, column)) for column in zip(*employee_table)]
    table_format = " ".join(["{{:<{}}}".format(i) for i in column_width])
    for row in employee_table:
        print(table_format.format(*row))

# Edit employee data


# Display reminders for annual review 3 months before individual review date

def review_reminder_list(source_list):
    review_reminder_list = []
    for employee in source_list:
        review_date = employee["Start_date"].replace(year=date.today().year)
        reminder_date = review_date - timedelta(days=-90)
        employee_review_data = {"Review_date" : review_date, "Reminder_date" : reminder_date}
        employee.update(employee_review_data)
        if reminder_date.month == date.today().month:
            review_reminder_list.append(employee)
    return review_reminder_list


# main
employees_list = reformat_list(read_data("Employees.csv"))
#print_employee_report(get_current_employees(employees_list))
#print_employee_report(get_past_month_leaving_employees(employees_list))
#updated_employees_list= add_new_employee(employees_list)
#print_employee_report(review_reminder_list(employees_list))