import nltk
import os

# Set NLTK data path to a directory in the project
nltk.data.path.append(os.path.join(os.path.dirname(__file__), 'nltk_data'))

# Download required NLTK data to the project directory
nltk.download('vader_lexicon', download_dir=os.path.join(os.path.dirname(__file__), 'nltk_data'))
nltk.download('punkt', download_dir=os.path.join(os.path.dirname(__file__), 'nltk_data'))