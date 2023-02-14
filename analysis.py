import pandas as pd
import matplotlib.pyplot as plt
import re
import seaborn as sns

# Set the theme to seaborn-poster
sns.set_theme(style='whitegrid')

FILENAME = "OJ_static.xlsx"
# Load the first sheet (Contest1)
df1 = pd.read_excel(FILENAME, sheet_name='Contest1')

# Load the second sheet (Contest2)
df2 = pd.read_excel(FILENAME, sheet_name='Contest2')

# Load the third sheet (Contest3)
df3 = pd.read_excel(FILENAME, sheet_name='Contest3')

# Combine the three sheets into a single dataset
df = pd.concat([df1, df2, df3], ignore_index=True)

for index, row in df.iterrows():
    print("Index:", index)
    for column in df.columns:
        # Print the value of the column
        print(column, ":", row[column])
    print("\n")


def get_certain_type(df, result_type):
    status = []
    for index, row in df.iterrows():
        status.append(row["Status"])
    total = len(status)

    # A regular expression pattern to match strings that contain "Accepted"

    pattern = re.compile(r".*"+result_type+".*")
    result = [string for string in status if re.match(pattern, string)]
    return result,total


def success_rate_per_question(df):
    problems = []
    success_rates = []
    table_data = df.groupby("Problem")["Status"].apply(list).to_dict()
    for key, values in table_data.items():
        pattern = re.compile(r".*Accepted.*")
        accepted = [string for string in values if re.match(pattern, string)]

        # Use a regular expression to extract the problem number and title
        match = re.search(r'P(\d+)\s+(\w+(\s+\w+)*)', key)

        # Extract the problem number and title from the match object
        problem_number = match.group(1)
        problem_title = match.group(2)
        # Print the results
        #print(f'Problem number: {problem_number}')
        #print(f'Problem title: {problem_title}')
        problems.append(problem_title)
        success_rate = len(accepted) / len(values) * 100
        success_rates.append(success_rate)
    #print(problems) 
    #print(success_rates)
        

    # Create the bar plot
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.bar(problems, success_rates)

    # Set the x-axis labels
    ax.set_xticklabels(problems, rotation=25, ha='right')

    # Add title to the figure
    plt.title("Success Rate Based on 8 Problems", fontsize=20, fontweight='bold')

    # Add labels to the x and y axes
    plt.xlabel("Problem #", fontsize=16, fontweight='bold')
    plt.ylabel("Success Rate (%)", fontsize=16, fontweight='bold')
    # Show the plot
    plt.show()

#success_rate_per_question(df)


def success_rate_per_contest(df1, df2, df3):
    res1, total1 = get_certain_type(df1, "Accepted")
    res2, total2 = get_certain_type(df2, "Accepted")
    res3, total3 = get_certain_type(df3, "Accepted")
    rate1 = len(res1) / total1 * 100
    rate2 = len(res2) / total2 * 100
    rate3 = len(res3) / total3 * 100
    # Data for the bar chart
    contests = ['Contest 1', 'Contest 2', 'Contest 3']
    success_rates = [rate1, rate2, rate3]

    # Plot the bar chart
    plt.bar(contests, success_rates)

    # Add labels and title with larger and bolder font
    #plt.xlabel('Contest #', fontsize=15, fontweight='bold')
    plt.ylabel('Success Rate (%)', fontsize=15, fontweight='bold')
    plt.title('Success Rate by Contest', fontsize=15, fontweight='bold')

    plt.xticks(fontsize=16, fontweight='bold')
    plt.yticks(fontsize=16, fontweight='bold')

    # Show the plot
    plt.show()


def error_analysis(df):
    status = []
    for index, row in df.iterrows():
        status.append(row["Status"])

    # A regular expression pattern to match strings that contain "Accepted"
    pattern = re.compile(r".*Compile Error.*")
    compile_error = [string for string in status if re.match(pattern, string)]

    # A regular expression pattern to match strings that contain "Runtime Error"
    pattern = re.compile(r".*Runtime Error.*")
    runtime_error = [string for string in status if re.match(pattern, string)]
    

    # A regular expression pattern to match strings that contain "Accepted"
    pattern = re.compile(r".*Accepted.*")
    accepted = [string for string in status if re.match(pattern, string)]

    # A regular expression pattern to match strings that contain "Wrong Answer"
    pattern = re.compile(r".*Wrong Answer.*")
    wrong_answer = [string for string in status if re.match(pattern, string)]

    # Data for the pie chart
    total_data = len(status)
    print("total submissions are:", total_data)
    error_types = ['Compile Error', 'Runtime Error', 'Accepted', 'Wrong Answer']
    p_compile_error = len(compile_error) / total_data * 100
    p_runtime_error = len(runtime_error) / total_data * 100
    p_accepted = len(accepted) / total_data * 100 
    #p_wrong_answer = len(wrong_answer) / total_data * 100
    p_wrong_answer = 100 - p_compile_error - p_runtime_error - p_accepted

    percentages = [p_compile_error, p_runtime_error, p_accepted, p_wrong_answer]

    # Calculate the sum of the percentages
    total = sum(percentages)
    adjusted_percentages = [p / total * 100 for p in percentages]
    formatted_percentages = [format(p, '.2f') for p in adjusted_percentages]


    plt.pie(formatted_percentages, labels=error_types, autopct='%1.2f%%',textprops={'fontsize': 15, 'fontweight': 'bold'})
    plt.axis('equal')
    plt.show()

#error_analysis(df)
success_rate_per_contest(df1, df2, df3)
#success_rate_per_question(df)
