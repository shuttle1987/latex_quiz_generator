"""
Representation of a quiz
"""

import jinja2

default_quiz_template = jinja2.Template("""
{{ quiz_name }} (version: {{ quiz_version }})
{{ preamble }}

{% for question in questions %}
    Question #{{ loop.index }}:
    {{ question.question_to_latex}}
{% endfor %}
""")

default_marking_sheet_template = jinja2.Template("""
Marking sheet for {{ quiz_name }} version {{ quiz_version }}
{% for question in questions %}
    Answer for question ${{loop.index}}: {{ question.answer_to_latex }}
{% endfor %}
""")

class Quiz:
    """Represents a particlar instance of a Quiz"""

    def __init__(self, questions, quiz_name="", quiz_version="",
                 preamble=None, quiz_questions_template=default_quiz_template,
                 marking_sheet_template=default_marking_sheet_template):
        """
        :questions: A collection of questions that comprises this quiz
        :quiz_name: The name of this quiz
        :quiz_version: The version of the quiz
        :preamble: Text to appear before quiz any questions
        :quiz_questions_template: A template to display the quiz questions.
                                  See the default for an example.
        :default_marking_sheet_template: A template to display the marking sheet.
                                         See the default for an example.
        """
        self.questions = questions
        self.quiz_name = quiz_name
        self.quiz_version = quiz_version
        self.preamble = preamble
        self.quiz_questions_template = quiz_questions_template
        self.marking_sheet_template = marking_sheet_template

    def add_question(self, question):
        """Add a question to the Quiz"""
        self.questions.append(question)

    def create_marking_sheet(self):
        """Create a marking sheet for this quiz"""
        rendered_output = self.marking_sheet_template.render({
            "quiz_name": self.quiz_name,
            "quiz_version": self.quiz_version,
            "questions": self.questions,
        })
        return rendered_output

    def render(self):
        """
        Render the quiz using the provided template
        :rtype: str
        :returns: A string with the rendered quiz
        """
        rendered_output = self.quiz_questions_template.render({
            "quiz_name": self.quiz_name,
            "quiz_version": self.quiz_version,
            "questions": self.questions,
        })
        return rendered_output
