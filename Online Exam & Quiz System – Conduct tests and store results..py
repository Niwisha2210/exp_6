import sqlite3

conn = sqlite3.connect("exam_system.db")
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT UNIQUE,
password TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS results (
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT,
score INTEGER
)
''')

conn.commit()


def register():
"""Registers a new user."""
  username = input("Enter a username: ")
  password = input("Enter a password: ")

  try:
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    print("Registration successful! Please log in.")
    except sqlite3.IntegrityError:
    print("Username already exists. Try another one.")


def login():
"""Logs in a user."""
  username = input("Enter your username: ")
  password = input("Enter your password: ")

  cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
  user = cursor.fetchone()

  if user:
    print("Login successful!")
    return username
  else:
    print("Invalid credentials!")
    return None


def take_quiz(username):
"""Conducts the quiz and stores the results."""
  questions = {
"What is the capital of France?": {"a": "Berlin", "b": "Madrid", "c": "Paris", "d": "Rome", "answer": "c"},
"What is 5 + 3?": {"a": "5", "b": "8", "c": "10", "d": "15", "answer": "b"},
"Which language is this program written in?": {"a": "Java", "b": "C++", "c": "Python", "d": "Ruby", "answer": "c"},
  }

  score = 0
  for question, options in questions.items():
      print("\n" + question)
  for key, value in options.items():
    if key != "answer":
        print(f"{key}. {value}")

answer = input("Your answer: ").lower()
if answer == options["answer"]:
  score += 1

print(f"\nQuiz Completed! Your score: {score}/{len(questions)}")
cursor.execute("INSERT INTO results (username, score) VALUES (?, ?)", (username, score))
conn.commit()


def view_results():
"""Displays all stored quiz results."""
  cursor.execute("SELECT * FROM results")
  results = cursor.fetchall()

print("\nQuiz Results:")
for res in results:
  print(f"User: {res[1]}, Score: {res[2]}")


def main():
"""Main function to run the exam system."""
  while True:
    print("\nOnline Exam System")
    print("1. Register")
    print("2. Login")
    print("3. View Results")
    print("4. Exit")

choice = input("Enter your choice: ")

if choice == "1":
  register()
