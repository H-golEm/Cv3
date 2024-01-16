import os

def get_last_test_case(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in reversed(lines):
                if line.startswith('<h2>Test '):
                    return int(line.split()[1])
    except FileNotFoundError:
        return 0

def update_test_number_log(log_file_path, current_test_case):
    with open(log_file_path, 'w') as log_file:
        log_file.write(str(current_test_case))

def read_test_number_log(log_file_path):
    try:
        with open(log_file_path, 'r') as log_file:
            return int(log_file.read())
    except FileNotFoundError:
        return 0

def generate_html(file_path, test_case, questions, answers):
    mode = 'a' if os.path.exists(file_path) else 'w'

    with open(file_path, mode) as html_file:
        if mode == 'w':
            # If the file is empty, add initial HTML structure
            html_file.write("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
        }
        .container {
            border: 1px solid #ccc;
            padding: 10px;
        }
        .question {
            margin-top: 10px;
        }
        .answer {
            white-space: pre-wrap;
            margin-top: 5px;
        }
    </style>
    <title>Test Log</title>
</head>
<body>
""")

        html_file.write(f"""
    <div class="container">
        <h2>Test {test_case}</h2>
""")

        for i, (question, answer) in enumerate(zip(questions, answers)):
            html_file.write(f"""
        <div class="question">
            <strong>Question {i + 1}:</strong> {question}
        </div>
        <div class="answer">
            <strong>Answer {test_case}.{i + 1}:</strong><br>{answer}
        </div>
""")

        html_file.write("""
    </div>
</body>
</html>
""")

    print(f"HTML log updated: {file_path}")

if __name__ == "__main__":
    script_path = os.path.realpath(__file__)
    file_path = os.path.join(os.path.dirname(script_path), "test_log.html")
    log_file_path = os.path.join(os.path.dirname(script_path), "test_number_log.txt")

    # Ask the user for answers
    questions = [
        "What would you like ChatGPT to know about you to provide better responses?",
        "How would you like ChatGPT to respond?"
    ]

    answers = []
    for i in range(len(questions)):
        user_input = input(f"Enter the answer for Question {i + 1} (type 'send to log' to finish):\n")
        if user_input.lower() == 'send to log':
            break
        answers.append(user_input)

    # Generate or update the HTML log with the new test case and answers
    last_test_case = read_test_number_log(log_file_path)
    generate_html(file_path, last_test_case + 1, questions, answers)

    # Update the test number log
    update_test_number_log(log_file_path, last_test_case + 1)
