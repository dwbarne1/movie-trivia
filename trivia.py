from functools import wraps
import difflib


def decorator(gen):
    """Outer function; generates question number"""
    question = gen()

    @wraps(gen)
    def wrapper(*args, **kwargs):
        """Wrapper function"""
        gen(*args, **kwargs)
        number = next(question)
        return f'Question {number}'
    return wrapper


@decorator
def question_number():
    """Generates question numbers"""
    num = 1
    while True:
        yield num
        num += 1


def get_questions(path):
    """Reads lines from specified file"""
    with open(path, 'r') as fp:
        for line in fp:
            name_movie = line.split(',')
            name = name_movie[0].strip()
            movie = name_movie[1].strip().casefold()
            yield name, movie


def grade_question(entry, answer):
    """Checks if answer is correct and adjusts points accordingly"""
    ratio = difflib.SequenceMatcher(None, entry, answer).ratio()
    return ratio


questions = get_questions('questions.txt')

print(f'{"Movie Trivia":*^30}\n')
print('You will be given a character and you must respond with their movie:')

totalPoints = 0
totalQuestions = 0

for q in questions:
    questionAndNumber = question_number()
    entry = input(f'{questionAndNumber} {q[0]}: ').casefold()
    ratioCorrect = grade_question(entry, q[1])
    if ratioCorrect >= .7:
        totalPoints += 1
    elif ratioCorrect < .7:
        totalPoints += 0
    totalQuestions += 1
print(f'You scored {totalPoints} out of {totalQuestions} questions')
