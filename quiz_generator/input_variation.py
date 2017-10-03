"""
This module supplies code to handle arbitrary choices in the question input.
This is done via a class that handles how a specific location in the text is filled in.

When a question can have multiple inputs of an arbitrary nature we wish to make it convienent
to pass that directly to the templating engine but the difficulty arises when we must
deal with choices.

For example say we have the following template:

    what is {{ parameter1 }} combined with {{ parameter2 }}?
    
That we wish to pass in the following input parameters:

{
"parameter1": ['a', 'b', 'c'],
"parameter2": ['z'],
}

If no choices are possible then simple substitution can occur.
However if as is desired with this package we wish to have multiple questions
generated from the given input we have ambiguity in substituting here.

When substituting into the template is `parameter1` here the whole list or
just an element from the list?

Without a wrapper class or other metadata we cannot simultaneously make that distinction
and allow for choices to be taken from the items.

Variations make the intent explicit:

{
"parameter1": Variation(['a', 'b', 'c']),
"parameter2": ['z'],
}

This explicitly chooses an item from the list.

"""


def sequential_selection(items):
    """Sequentially yield items from an iterable"""
    for item in items:
        yield item

class Variation:
    """This class manages choice based inputs"""

    def __init__(self, items, selection_method=None):
        """
        :items: the items we can choose from
        :selection_method: A function that contains the strategy to pick items,
                           defaults to sequentially selecting.
        """
        self.items = items
        if selection_function is None:
            self.selection_function = sequential_selection
        else:
            self.selection_function = selection_function

    def get(self):
        """Yield next item"""
        return self.selection_function(self.items)

