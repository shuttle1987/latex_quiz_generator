"""
This example shows you how you can handle names in a varied question.
"""

import random

import jinja2

from quiz_generator.ranged_question import RangedQuestion
from quiz_generator.input_variation import Variation

# Worded question

inputs = {
    "person": Variation([
        {"name": "Bob", "pronoun": "he"},
        {"name": "Alice", "pronoun": "she"},
        ],
        selection_method=random.choice),
    "number_of_tables": Variation([2,3,4], selection_method=random.choice),
    "cost_per_table": Variation([10,15,20], selection_method=random.choice),
}

def compute_total_cost(inputs):
    return {"total_cost": inputs["number_of_tables"] * inputs["cost_per_table"]}

question_text = jinja2.Template("""
{{person[name]}} went to an auction to buy tables. Each table cost {{cost_per_table}}.
How much did {{person[name]}} spend for the {{number_of_tables}} that {{person["pronoun"]}} bought?
""")

worded_question = RangedQuestion(
    question_template=question_text,
    answer_template=jinja2.Template("Total cost is {{total_cost}}"),
    inputs=inputs,
    answer_generation_function=compute_total_cost
)

for _ in range(3):
    question_instance = worded_question.create_specific_question()
    print(question_instance.render_question())
    print(question_instance.render_answer())
