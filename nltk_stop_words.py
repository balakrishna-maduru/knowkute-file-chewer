# Fetch and print all NLTK stop words for all supported languages
import nltk
from nltk.corpus import stopwords

# Ensure stopwords data is downloaded
try:
	stopwords.words('english')
except LookupError:
	nltk.download('stopwords')

def get_all_stopwords():
	all_stops = {}
	for lang in stopwords.fileids():
		all_stops[lang] = set(stopwords.words(lang))
	return all_stops

if __name__ == "__main__":
	all_stopwords = get_all_stopwords()
	with open("stopwords_all_languages.txt", "w", encoding="utf-8") as f:
		for lang, words in all_stopwords.items():
			f.write(f"--- {lang} stopwords ({len(words)}) ---\n")
			f.write(', '.join(sorted(words)) + "\n\n")
	print("All stop words saved to stopwords_all_languages.txt")
