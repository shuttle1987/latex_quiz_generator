"""
Tests for question class
"""
import pytest

from quiz_generator.question import Question

def test_question_with_no_substitution():
    """Test that a question with no function to substitute values works as expected"""
    simple_question = Question("1+1 = ?", "2")
    assert simple_question.render_question() == "1+1 = ?"
    assert simple_question.render_answer() == "2"

def test_question_with_template():
    """Test that a question with a templated input works as expected"""
    import jinja2
    input_name = { "name": "bob" }
    q_template = jinja2.Template("Hi I'm {{ name }}!")
    a_template = jinja2.Template("This wasn't really a question, so there's no answer")
    question_with_template = Question(
        question_template=q_template,
        answer_template=a_template,
        inputs=input_name
    )
    assert question_with_template.render_question() == "Hi I'm bob!"
    assert question_with_template.render_answer() == "This wasn't really a question, so there's no answer"

def test_question_with_function():
    """Test a question is generated with a provided function"""
    import jinja2
    inputs = {"a": 1, "b": 2}
    def answer_function(input_values):
        """
        Simple function that adds 2 numbers. These are stored in the input
        values dictionary under the keys 'a' and 'b'.
        Note the return value is a dictionary because this is required for rendering
        the answer.
        """
        ans = input_values['a'] + input_values['b']
        return {"answer": ans}

    q_template = jinja2.Template("What is {{a}}+{{b}} ?")
    a_template = jinja2.Template("{{answer}}")
    question_with_function = Question(
        question_template=q_template,
        answer_template=a_template,
        inputs=inputs,
        answer_generation_function=answer_function
    )
    assert question_with_function.render_question() == "What is 1+2 ?"
    assert question_with_function.render_answer() == "3"

def test_bad_parameters_to_question():
    """Test that bad parameters passed to Question raise exceptions"""
    with pytest.raises(TypeError):
        Question(
            question_template="This is a string",
            answer_template=0.123
        )

    with pytest.raises(TypeError):
        Question(
            question_template=1234,
            answer_template="This is a string"
        )
