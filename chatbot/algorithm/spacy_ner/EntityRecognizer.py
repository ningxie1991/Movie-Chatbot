import pickle
import random
import os
import srsly
import spacy
from spacy.training import Example
from spacy.util import minibatch, compounding

dirname = os.path.dirname(__file__)


def add_labels(ner, train_dataset, test_dataset):
    # Adding labels to the `ner`
    for text, annotations in train_dataset:
        for ent in annotations.get("entities"):
            ner.add_label(ent[2])

    for text, annotations in test_dataset:
        for ent in annotations.get("entities"):
            ner.add_label(ent[2])


def train_er():
    nlp = spacy.load(os.path.join(dirname, '../saved_models/spacy_nlp'))
    ner = nlp.get_pipe("ner")

    train_dataset = srsly.read_json(os.path.join(dirname, 'data/engtrain_cased.json'))
    test_dataset = srsly.read_json(os.path.join(dirname, 'data/engtest_cased.json'))

    add_labels(ner, train_dataset, test_dataset)

    random.shuffle(train_dataset)
    random.shuffle(test_dataset)

    # Disable pipeline components you dont need to change
    pipe_exceptions = ["ner", "trf_tok2vec"]
    unaffected_pipes = [pipe for pipe in nlp.pipe_names if pipe not in pipe_exceptions]

    # TRAINING THE MODEL
    with nlp.disable_pipes(*unaffected_pipes):
        optimizer = nlp.create_optimizer()
        # Training for 30 iterations
        for iteration in range(10):
            losses = {}
            # batch up the examples using spaCy's minibatch
            batches = minibatch(train_dataset, size=compounding(4.0, 32.0, 1.001))
            for batch in batches:
                examples = []
                for text, annotations in batch:
                    doc = nlp(text)
                    examples.append(Example.from_dict(doc, annotations))
                nlp.update(
                    examples,
                    drop=0.2,  # dropout - make it harder to memorise data
                    losses=losses,
                    sgd=optimizer,
                )
                print(iteration, "Losses", losses)  # print the training loss

    nlp.to_disk(os.path.join(dirname, './my_nlp_er'))
    with open(os.path.join(dirname, './data/test_set.pkl'), "wb") as f:
        pickle.dump(test_dataset, f)


def eval_er():
    """ Step 3: Evaluate the new Entity Linking component by applying it to unseen text. """
    nlp = spacy.load(os.path.join(dirname, 'output/model-best'))

    text = "Did Christopher Nolan ever work on a Batman movie?"
    doc = nlp(text)
    for ent in doc.ents:
        print(ent.text, ent.start_char, ent.end_char, ent.label_)


if __name__ == "__main__":
    eval_er()