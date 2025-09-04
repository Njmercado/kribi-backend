def transform_word_to_regexp(word: str) -> str:
	"""Transform a word into a regular expression pattern that matches the word with optional accents."""

  # Define a mapping of characters to their accented variants
	accent_mapping = {
    'a': '(a|à|á|ä)',
		'à': '(a|à|á|ä)',
		'á': '(a|à|á|ä)',
		'ä': '(a|à|á|ä)',
    'e': '(e|è|é|ë)',
		'è': '(e|è|é|ë)',
		'é': '(e|è|é|ë)',
		'ë': '(e|è|é|ë)',
    'i': '(i|ì|í|ï)',
		'ì': '(i|ì|í|ï)',
		'í': '(i|ì|í|ï)',
		'ï': '(i|ì|í|ï)',
    'o': '(o|ò|ó|ö)',
		'ò': '(o|ò|ó|ö)',
		'ó': '(o|ò|ó|ö)',
		'ö': '(o|ò|ó|ö)',
    'u': '(u|ù|ú|ü)',
		'ù': '(u|ù|ú|ü)',
		'ú': '(u|ù|ú|ü)',
		'ü': '(u|ù|ú|ü)',
		'n': '(n|ñ)',
	}

	return ''.join(accent_mapping.get(char) or char for char in word.lower())
