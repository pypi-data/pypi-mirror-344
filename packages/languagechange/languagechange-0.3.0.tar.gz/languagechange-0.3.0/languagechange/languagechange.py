import argparse
import typer

app = typer.Typer()

class LanguageEvolution:
    def __init__(self):
        # Define common word replacements for each language stage
        self.old_english_replacements = {
            "the": "þe", 
            "is": "iƿ",
            "you": "þū",
            "I": "iċ",
            "and": "ond",
            "in": "in",
            "to": "tō",
            "a": "ān",
            "that": "þæt",
            "it": "hit",
            "not": "ne",
            "this": "þis",
            "have": "habban",
            "for": "for",
            "are": "ƿindon",
            "was": "wæs",
            "on": "on",
            "with": "mid",
            "they": "hīe",
            "be": "bēon",
            "at": "æt",
            "one": "ān",
            "all": "eall",
            "good": "gōd",
            "man": "mann",
            "day": "dæġ",
            "time": "tīma",
            "world": "woruld",
            "great": "grēat",
        }
        
        self.middle_english_replacements = {
            "the": "ye",
            "is": "is",
            "you": "thou",
            "I": "ich",
            "and": "and",
            "in": "yn",
            "to": "to",
            "a": "a",
            "that": "that",
            "it": "hit",
            "not": "nat",
            "this": "thys",
            "have": "haven",
            "for": "for",
            "are": "aren",
            "was": "was",
            "on": "on",
            "with": "wyth",
            "they": "thei",
            "be": "been",
            "at": "at",
            "one": "oon",
            "all": "al",
            "good": "goode",
            "man": "man",
            "day": "daie",
            "time": "tyme",
            "world": "worlde",
            "great": "grete",
        }
    
    def transform_sentence(self, sentence, replacements):
        words = sentence.split()
        transformed = []
        
        for word in words:
            # Check if the word is in our replacements dictionary
            lower_word = word.lower()
            is_capital = word[0].isupper() if word else False
            
            # Handle punctuation
            punctuation = ""
            if lower_word and lower_word[-1] in ".,:;!?":
                punctuation = lower_word[-1]
                lower_word = lower_word[:-1]
            
            # Replace if found
            if lower_word in replacements:
                replacement = replacements[lower_word]
                if is_capital and replacement:
                    replacement = replacement[0].upper() + replacement[1:]
                transformed.append(replacement + punctuation)
            else:
                transformed.append(word)
                
        return " ".join(transformed)
    
    def generate_evolution(self, modern_sentence):
        """
        Generator that yields the same sentence in three historical stages of English.
        
        Args:
            modern_sentence (str): The Modern English sentence to transform
            
        Yields:
            str: Old English approximation
            str: Middle English approximation
            str: Modern English (original)
        """
        # Yield each version of the sentence
        yield self.transform_sentence(modern_sentence, self.old_english_replacements)  # Old English
        yield self.transform_sentence(modern_sentence, self.middle_english_replacements)  # Middle English
        yield modern_sentence  # Modern English


def language_evolution_generator(modern_sentence):
    """
    Generator that yields the same sentence in three historical stages of English.
    
    Args:
        modern_sentence (str): The Modern English sentence to transform
        
    Yields:
        str: Old English approximation
        str: Middle English approximation
        str: Modern English (original)
    """
    evolution = LanguageEvolution()
    yield from evolution.generate_evolution(modern_sentence)

@app.command()
def transform(
    sentence: str = typer.Argument(
        None, 
        help="Modern English sentence to transform into historical forms"
    ),
):
    """
    Transform a sentence into different historical forms of English.
    If no sentence is provided, a test sentence will be used.
    """
    # Use test sentence if none provided
    if sentence is None:
        sentence = "Nothing ever comes to one that is worth having, except as a result of hard work." # Booker T Washington
        print(f"Using test sentence: \"{sentence}\"")
    
    print("\nLanguage evolution of the sentence:")
    for i, historical_form in enumerate(language_evolution_generator(sentence)):
        stage = ["Old English", "Middle English", "Modern English"][i]
        print(f"{stage}: {historical_form}")

if __name__ == "__main__":
    app()