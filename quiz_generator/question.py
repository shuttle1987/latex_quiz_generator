"""
Representation of a question.
"""
import jinja2

class Question:
    """
    This class stores a simple question/answer pairing along with the required
    information to calculate an answer from given inputs.
    All formatting is done via templates that are passed in.
    """
    def __init__(self, question_template, answer_template, inputs=None, answer_generation_function=None):
        """
        :question_template: a template for the question
        :answer_template: a template for the answer
        :inputs: a dictionary of substitutions to make in the templates
        :answer_generation_function: a function that takes the variables found in the
                                     question template and returns a dictionary of answer
                                     keys with values for use in the answer_template
        """
        if isinstance(question_template, str):
            self.question_template = jinja2.Template(question_template)
        elif isinstance(question_template, jinja2.Template):
            self.question_template = question_template
        else:
            raise TypeError(
                    "question_template must be type str or jinja2.Template, got {} instead".format(
                    type(question_template)
                ))

        if isinstance(answer_template, str):
            self.answer_template = jinja2.Template(answer_template)
        elif isinstance(answer_template, jinja2.Template):
            self.answer_template = answer_template
        else:
            raise TypeError(
                    "answer_template must be type str or jinja2.Template, got {} instead".format(
                    type(answer_template )
                ))
        self.question_inputs = inputs
        self.answer_generation_function = answer_generation_function
        if answer_generation_function:
            self.answers = answer_generation_function(inputs)

    def render_question(self):
        """Render the question template with the question inputs"""
        if self.question_inputs:
            return self.question_template.render(self.question_inputs)
        else:
            return self.question_template.render()

    def render_answer(self):
        """Render the answer template with the answers"""
        if self.answer_generation_function:
            return self.answer_template.render(self.answers)
        else:
            return self.answer_template.render()

    def __eq__(self, other):
        return all([
            self.question_template == other.question_template,
            self.answer_template == other.answer_template,
            self.question_inputs == other.question_inputs,
            self.answer_generation_function == other.answer_generation_function,
        ])
