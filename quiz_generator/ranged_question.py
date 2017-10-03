"""
Representation of a question with a range of input values
"""
import copy

from .question import Question
from .input_variation import Variation

def extract_input_combination(inputs_mapping):
    """Extract an input combination from the possible inputs.
    For each key this will chose an element from a Variation otherwise it and will
    choose the value directly.
    Example usage:

    >>> extract_input_combination({1: ['a', 'b'], 2: ['c']})
    {1: ['a', 'b'], 2: 'c'}
    >>> extract_input_combination({1: Variation(['a', 'b']), 2: ['c']})
    {1: 'b', 2: 'c'}
    >>> extract_input_combination({1: 'Example string', 2: ['c']})
    {1: 'not a collection', 2: 'c'}


    :returns: An input combination allowed by this input mapping
    """
    results = {}
    for key, value in inputs_mapping.items():
        if isinstance(value, Variation):
            results[key] = next(value.get())
        else:
            results[key] = value
    return results

def expand_variations(inputs_mapping):
    """Expand all Variations values in a mapping to create all possible input combinations.

    >>> create_all_inputs({"a": 1, "b": Variation([2,3])})
    [{"a": 1, "b": 2}, {"a": 1, "b": 3}]

    :inputs_mapping: a mapping of template keys to values
    """
    results = []
    if any(isinstance(value, Variation) for value in inputs_mapping.values()):
        #expand every Variation value
        for key, value in inputs_mapping.items():
            if isinstance(value, Variation):
                for instance in value.get():
                    inputs_copy = copy.copy(inputs_mapping)
                    inputs_copy[key] = instance
                    results.extend(expand_variations(inputs_copy))
    else:
        results = [inputs_mapping]
    return results

class RangedQuestion:
    """Helper class for generating questions that have a range of possible inputs."""
    def __init__(self, question_template, answer_template,
                 inputs, answer_generation_function=None):
        """
        :question_template: a template for the question
        :answer_template: a template for the answer
        :inputs: a dictionary of substitutions to make in the templates
        :answer_generation_function: a function that takes the variables found in the
                                     question template and returns a dictionary of answer
                                     keys with values for use in the answer_template
        """
        self.question_template = question_template
        self.answer_template = answer_template
        self.question_inputs = inputs
        self.answer_generation_function = answer_generation_function

    def create_specific_question(self):
        """
        Create a specific singular instance of this Question by choosing a value
        from the inputs.
        :returns: A specific Question instance
        :rtype: Question
        """
        # If no inputs then we have only one choice possible which is as follows:
        if self.question_inputs is None:
            return Question(
                question_template=self.question_template,
                answer_template=self.answer_template,
                inputs=None,
                answer_generation_function=self.answer_generation_function
            )

        specific_input = extract_input_combination(self.question_inputs)
        return Question(
            question_template=self.question_template,
            answer_template=self.answer_template,
            inputs=specific_input,
            answer_generation_function=self.answer_generation_function
        )

    def create_all_questions(self):
        """
        Create all possible questions from the input combinations
        :returns: A list of Questions
        """
        questions = []
        for input_instance in expand_variations(self.question_inputs):
            questions.append(
                Question(
                    question_template=self.question_template,
                    answer_template=self.answer_template,
                    inputs=input_instance,
                    answer_generation_function=self.answer_generation_function
                )
            )
        return questions
