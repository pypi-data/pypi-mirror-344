def create_quiz():
  """
  Creates a new quiz dictionary with empty questions and answers lists."""
  quiz = {}
  quiz['questions'] = []
  quiz['answers'] = []
  return quiz

def add_question(quiz, question, answer):
  """
  Adds a question and its corresponding answer to the quiz."""
  quiz['questions'].append(question)
  quiz['answers'].append(answer)

def take_quiz(quiz):
  """
  Administers a quiz to the user, evaluates their answers, and provides feedback.

  Args:
    quiz (dict): A dictionary containing the quiz data. It should have two keys:
      - 'questions' (list of str): A list of questions to be asked.
      - 'answers' (list of str): A list of correct answers corresponding to the questions.

  Behavior:
    - Iterates through the list of questions in the quiz.
    - Prompts the user to input their answer for each question.
    - Compares the user's answer (case-insensitive) with the correct answer.
    - Provides feedback for each question (correct or wrong, with the correct answer if wrong).
    - Displays the user's final score at the end of the quiz.

  Returns:
    None
  """
  score = 0
  for i in range(len(quiz['questions'])):
    print(quiz['questions'][i])
    answer = input("Your answer: ")
    if answer.lower() == quiz['answers'][i].lower():
      score += 1
      print("Correct!")
    else:
      print(f"Wrong! The correct answer is {quiz['answers'][i]}.")
  print(f"Your final score is {score}/{len(quiz['questions'])}.")