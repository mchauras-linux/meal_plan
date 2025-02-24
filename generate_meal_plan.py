import json
import calendar
from datetime import datetime, timedelta

# Function to read the meal plan configuration from a JSON file
def read_meal_config(filename="meal_config.json"):
    with open(filename, "r") as file:
        config = json.load(file)
    return config["meals"]

# Function to generate the HTML file for a month's meal plan in a calendar grid format
def generate_meal_plan(year, month):
    # Read the meal configuration from the JSON file
    meals = read_meal_config()

    # Get the first and last day of the month
    first_day = datetime(year, month, 1)
    last_day = datetime(year, month, calendar.monthrange(year, month)[1])

    # Get the weekday of the first day of the month (0 = Monday, 6 = Sunday)
    first_weekday = first_day.weekday()

    # Prepare the HTML content
    html_content = f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Vegetarian North Indian Meal Plan</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 20px;
                background-color: #f7f7f7;
            }}
            table {{
                width: 100%;
                margin: 20px 0;
                border-collapse: collapse;
                background-color: white;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
            }}
            th, td {{
                padding: 15px;
                text-align: center;
                border: 1px solid #ddd;
                width: 14%;
                vertical-align: top;
            }}
            th {{
                background-color: #4CAF50;
                color: white;
            }}
            td {{
                background-color: #f9f9f9;
            }}
            td strong {{
                color: #4CAF50;
            }}
            tr:nth-child(even) td {{
                background-color: #f1f1f1;
            }}
            tr:hover {{
                background-color: #f1f1f1;
            }}
            caption {{
                font-size: 1.5em;
                font-weight: bold;
                margin: 10px 0;
            }}
            .meal {{
                margin-bottom: 5px;
            }}
        </style>
    </head>
    <body>
        <table>
            <caption>Meal Plan for {calendar.month_name[month]} {year}</caption>
            <thead>
                <tr>
                    <th>Mon</th>
                    <th>Tue</th>
                    <th>Wed</th>
                    <th>Thu</th>
                    <th>Fri</th>
                    <th>Sat</th>
                    <th>Sun</th>
                </tr>
            </thead>
            <tbody>
    '''

    # Create the meal plan for the calendar grid
    current_day = first_day
    meal_index = 0  # To rotate through meals
    current_weekday = first_weekday  # Start at the weekday of the first day

    # Iterate over the calendar grid
    for week in range(6):  # Maximum of 6 rows for a month in a calendar format
        html_content += '<tr>'

        # Loop over each day of the week (Mon-Sun)
        for day_of_week in range(7):
            if week == 0 and day_of_week < current_weekday:
                # Empty cells before the first day of the month
                html_content += '<td></td>'
            elif current_day <= last_day:
                # Add a meal plan for the current day
                breakfast = meals[meal_index]["breakfast"]
                dinner = meals[meal_index]["dinner"]

                html_content += f'''
                <td>
                    <div class="day">{current_day.day}</div>
                    <div class="meal"><strong>Breakfast:</strong> {breakfast}</div>
                    <div class="meal"><strong>Dinner:</strong> {dinner}</div>
                </td>
                '''
                # Move to the next day
                current_day += timedelta(days=1)
                # Rotate through meals, reset to the first one if we exceed the list
                meal_index = (meal_index + 1) % len(meals) if meal_index + 1 < len(meals) else 0
                # meal_index = (meal_index + 1) % len(meals)  # Rotate meals
            else:
                # Empty cells after the last day of the month
                html_content += '<td></td>'

        html_content += '</tr>'

    # Close the table and body tags
    html_content += '''
            </tbody>
        </table>
    </body>
    </html>
    '''

    # Write the HTML content to a file
    with open(f"meal_plan_{year}_{month}.html", "w") as file:
        file.write(html_content)
    print(f"Meal plan for {calendar.month_name[month]} {year} has been saved as 'meal_plan_{year}_{month}.html'.")

# Prompt for user input to select the year and month
current_year = datetime.now().year
current_month = datetime.now().month

year_input = input(f"Enter the year (default {current_year}): ")
month_input = input(f"Enter the month number (1-12, default {current_month}): ")

# Use default values if input is empty
year = int(year_input) if year_input else current_year
month = int(month_input) if month_input else current_month

# Call the generate_meal_plan function with the user input
generate_meal_plan(year, month)
