import random
import fitz
import json
import re
import warnings
import spacy

# Suppress warning messages related to misaligned entities during training
warnings.filterwarnings("ignore", message="[W030]", category=UserWarning)

# Load JSON data from file
try:
    with open("notebooks/data/train_data (2).json", "r") as json_file:
        json_data = json.load(json_file)
except FileNotFoundError:
    print("The specified file does not exist.")
except json.JSONDecodeError:
    print("The file is not a valid JSON file.")

# Extract text and annotations from each entry
train_data = []
for entry in json_data:
    text = entry[0]  # Extract text from the first element of the entry list
    annotations = entry[1]["entities"]  # Extract annotations from the "entities" key of the second element
    train_data.append((text, {"entities": annotations}))

nlp = spacy.blank('en')

def train_model(train_data):
    """
    Train the spaCy NER model using the provided training data.
    """
    if 'ner' not in nlp.pipe_names:
        ner = nlp.create_pipe('ner')
        nlp.add_pipe("ner", last=True)

    for _, annotation in train_data:
        for ent in annotation['entities']:
            ner.add_label(ent[2])

    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
    with nlp.disable_pipes(*other_pipes):  # only train NER
        optimizer = nlp.begin_training()
        for itn in range(10):
            random.shuffle(train_data)
            losses = {}
            index = 0
            for text, annotations in train_data:
                try:
                    nlp.update(
                        [text],  # batch of texts
                        [annotations],  # batch of annotations
                        drop=0.2,  # dropout - make it harder to memorize data
                        sgd=optimizer,  # callable to update weights
                        losses=losses)
                except Exception as e:
                    pass

# Train the model
train_model(train_data)

# Save the model to disk
nlp.to_disk('nlp_model')

# Load the spaCy model
nlp_model = spacy.load('nlp_model')

def extract_text_from_pdf(file_path):
    """
    Extract text from a PDF file.
    """
    try:
        # Open the PDF file
        doc = fitz.open(file_path)
        text = ""
        # Extract text from each page and concatenate
        for page in doc:
            text += page.get_text()
        return text
    except FileNotFoundError:
        print("The specified file does not exist.")

def extract_entities_from_text(text):
    """
    Extract named entities from a text using the trained spaCy model.
    """
    # Process the text with the spaCy model
    doc = nlp_model(text)
    # Extract entities from the processed text
    entities = [(ent.label_, ent.text) for ent in doc.ents]
    return entities

def extract_skills(text):
    """
    Extract the skills section from a text.
    """
    # Convert the text to lowercase for case-insensitive matching
    lowercase_text = text.lower()

    # Define keywords that may indicate the start of the skills section
    skill_keywords = ["skills", "technical skills", "proficiency", "expertise", "competencies"]

    # Find the index of the keyword that indicates the start of the skills section
    start_index = None
    for keyword in skill_keywords:
        index = lowercase_text.find(keyword)
        if index != -1:
            start_index = index
            break

    # If no keyword is found, return None
    if start_index is None:
        return None

    # Find the end of the skills section (assuming it ends at the next section)
    end_index = lowercase_text.find("achievements", start_index)
    if end_index == -1:
        end_index = len(text)

    # Extract the skills section
    skills_section = text[start_index:end_index].strip()

    return skills_section

# Example usage:
def main():
    file_path = input("Enter the path to the PDF file: ")
    text = extract_text_from_pdf(file_path)
    print("Extracted Text:")
    print(text)
    entities = extract_entities_from_text(text)
    print("Entities:")
    for label, text in entities:
        print(f"{label.upper():{20}} - {text}")

    skills_section = extract_skills(text)
    if skills_section:
        print("\nSkills Section:")
        print(skills_section)
    else:
        print("\nSkills section not found.")

if __name__ == "__main__":
    main()
