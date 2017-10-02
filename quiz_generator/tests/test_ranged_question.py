"""
Tests for ranged questions
"""
from unittest.mock import Mock

from quiz_generator.ranged_question import (
    RangedQuestion,
    extract_input_combination,
)
from quiz_generator.question import Question
from quiz_generator.input_variation import Variation

def test_question_generation_no_inputs():
    """Test that a specific question can be generated from the RangedQuestion"""
    # The specific case where the question inputs are not iterable or form a
    # collection in any way should only ever produce one Question
    r_question = RangedQuestion(
        question_template="mock_question_template",
        answer_template="mock_answer_template",
        inputs=None,
    )

    generated_question = r_question.create_specific_question()
    assert isinstance(generated_question, Question)

def test_question_generation():
    """Test that a specific question can be generated from the RangedQuestion"""
    import jinja2
    inputs = {"x": Variation([1, 2])}
    def answer_function(input_values):
        """
        Simple function that squares a number. The input
        values dictionary stores this under the key for 'x'
        Note the return value is a dictionary because this is required for rendering
        the answer.
        """
        ans = input_values['x']**2
        return {"answer": ans}

    q_template = jinja2.Template("What is {{x}}^2 ?")
    a_template = jinja2.Template("{{answer}}")
    question_with_function_over_range = RangedQuestion(
        question_template=q_template,
        answer_template=a_template,
        inputs=inputs,
        answer_generation_function=answer_function
    )

    generated_question = question_with_function_over_range.create_specific_question()
    assert generated_question.render_question() in ("What is 1^2 ?", "What is 2^2 ?")
    assert generated_question.render_answer() in ("1", "4")

def test_extract_input_combination():
    """Test helper function that extracts a single value from a dictionary containing choices"""
    # case where values are not Variations must return the same value back
    no_variations1 = {
        'a': 1,
        'b': 2,
    }

    assert extract_input_combination(no_variations1) == no_variations1

    no_variations2 = {
        'a': 1,
        'b': ['a', 'b'],
        'c': "xyz",
    }
    assert extract_input_combination(no_variations2) == no_variations2
