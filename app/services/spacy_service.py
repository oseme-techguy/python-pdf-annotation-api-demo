"""SpacyAnnotation Service"""

from __future__ import unicode_literals, print_function

import spacy
from app.config.settings import SETTINGS
from app.helpers.utilities import Utilities

class SpacyAnnotationService:
    """SpacyAnnotation Service"""

    SELECTED_MODEL = "en_core_web_sm"

    def __init__(self, logger=None):
        self.logger = logger

    def set_model(self, model):
        """Sets the Spacy Model to use

        Arguments:
            model {str} -- the model to use -> "en_core_web_sm", "en_core_web_md", "en_core_web_lg"
        """
        self.SELECTED_MODEL = model


    def get_annotations(self, pdf_text=None, named_entity='MONEY'):
        """Fetches the annotations by the Entities within the PDF document
            using spacy.
            Actions:
                - Makes API call to their search endpoint
                - Gets list of all results (first 10)
                - Since they are sorted by "importance", 
                    I just start from the top and iterate through until I find a match

        Arguments:
            pdf_text {string} -- the content of the PDF
            named_entities {string} -- the named entity to use

        Returns:
            object -- the object containing log. and lat. info or None
        """

        if pdf_text is None:
            raise ValueError('the pdf_text cannot be None')
        
        if named_entity is None:
            raise ValueError('the named_entities cannot be None')

        nlp = spacy.load(self.SELECTED_MODEL)
        print("Loaded model '%s'" % self.SELECTED_MODEL)

        doc = nlp(pdf_text)
        relations = self.extract_currency_relations(doc, named_entity)
        for r1, r2 in relations:
            print("{:<10}\t{}\t{}".format(r1.text, r2.ent_type_, r2.text))


        return None


    def filter_spans(self, spans):
        # Filter a sequence of spans so they don't contain overlaps
        get_sort_key = lambda span: (span.end - span.start, span.start)
        sorted_spans = sorted(spans, key=get_sort_key, reverse=True)
        result = []
        seen_tokens = set()
        for span in sorted_spans:
            if span.start not in seen_tokens and span.end - 1 not in seen_tokens:
                result.append(span)
                seen_tokens.update(range(span.start, span.end))
        return result


    def extract_currency_relations(self, doc, named_entity='MONEY'):
        # Merge entities and noun chunks into one token
        seen_tokens = set()
        spans = list(doc.ents) + list(doc.noun_chunks)
        spans = self.filter_spans(spans)
        with doc.retokenize() as retokenizer:
            for span in spans:
                retokenizer.merge(span)

        relations = []
        for money in filter(lambda w: w.ent_type_ == named_entity, doc):
            if money.dep_ in ("attr", "dobj"):
                subject = [w for w in money.head.lefts if w.dep_ == "nsubj"]
                if subject:
                    subject = subject[0]
                    relations.append((subject, money))
            elif money.dep_ == "pobj" and money.head.dep_ == "prep":
                relations.append((money.head.head, money))
        return relations
