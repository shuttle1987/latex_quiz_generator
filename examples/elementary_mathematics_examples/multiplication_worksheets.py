"""
Example quiz containing elementary multiplication exercies.
"""

import random

import jinja2

from quiz_generator.ranged_question import RangedQuestion
from quiz_generator.input_variation import Variation
from quiz_generator.quiz import Quiz

# 3 times tables questions

inputs = {"x": Variation(random.sample(range(15), 5))}

def multiplication_answer_function(input_values):
    return {"answer": 3 * input_values['x']}

three_times_questions = RangedQuestion(
    question_template=jinja2.Template("3 \\times {{x}} = ?"),
    answer_template=jinja2.Template("{{answer}}"),
    inputs=inputs,
    answer_generation_function=multiplication_answer_function
)

quiz_version1 = Quiz(
    questions=three_times_questions.create_all_questions(),
    quiz_name="Three times table quiz",
    quiz_version="1",
    preamble="Questions to test your three times tables",
)

print(quiz_version1.render())
print(quiz_version1.create_marking_sheet())
