from promptlab.evaluator.evaluator import Evaluator


class ExactMatch(Evaluator):
    def evaluate(self, data: dict):
        inference = data["response"]
        reference = data["reference"]
            
        if inference == reference:
            return 'match'
        else:
            return 'mismatch'


