from sqlmodel import SQLModel, Field, Column, ARRAY, String
from datetime import datetime
from enum import Enum

# WordType dictionary with original CSV keys and English uppercase underscore values
WORD_TYPES = {
  "Adjetivo": "ADJECTIVE",
  "Adjetivo / Numeral": "ADJECTIVE_NUMERAL",
  "Adjetivo / Sustantivo": "ADJECTIVE_NOUN",
  "Adjetivo/Pronombre": "ADJECTIVE_PRONOUN",
  "Adjetivo/Sustantivo": "ADJECTIVE_NOUN_ALT",
  "Adverbio": "ADVERB",
  "Adverbio / Marcador negativo": "ADVERB_NEGATIVE_MARKER",
  "Adverbio / Sustantivo": "ADVERB_NOUN",
  "Artículo indefinido": "INDEFINITE_ARTICLE",
  "Conjunción": "CONJUNCTION",
  "Conjunción / Nexo subordinante": "CONJUNCTION_SUBORDINATE_NEXUS",
  "Conjunción subordinada": "SUBORDINATE_CONJUNCTION",
  "Expresión": "EXPRESSION",
  "Expresión idiomática": "IDIOMATIC_EXPRESSION",
  "Expresión temporal": "TEMPORAL_EXPRESSION",
  "Frase": "PHRASE",
  "habitual en imperfecto": "HABITUAL_IMPERFECT",
  "Imperativo plural": "IMPERATIVE_PLURAL",
  "Imperativo singular": "IMPERATIVE_SINGULAR",
  "Imperfecto perifrástico": "PERIPHRASTIC_IMPERFECT",
  "imperfecto simple /  Sufijo": "SIMPLE_IMPERFECT_SUFFIX",
  "Interjección": "INTERJECTION",
  "Locución": "LOCUTION",
  "Locución adverbial": "ADVERBIAL_LOCUTION",
  "Marcador aspectual": "ASPECTUAL_MARKER",
  "Marcador aspectual en imperfecto": "ASPECTUAL_MARKER_IMPERFECT",
  "Marcador de existencia": "EXISTENCE_MARKER",
  "Marcador pragmático": "PRAGMATIC_MARKER",
  "Marcador preverbal aspectual temporal ": "PREVERBAL_ASPECTUAL_TEMPORAL_MARKER",
  "Marcador temporal aspectual": "TEMPORAL_ASPECTUAL_MARKER",
  "Marcador Temporal aspectual ": "TEMPORAL_ASPECTUAL_MARKER_ALT",
  "Marcador verbal": "VERBAL_MARKER",
  "Marcador verbal aspectual": "VERBAL_ASPECTUAL_MARKER",
  "Negativo/Nulo": "NEGATIVE_NULL",
  "Nexo subordinante": "SUBORDINATE_NEXUS",
  "Número": "NUMBER",
  "Participio": "PARTICIPLE",
  "Preposición": "PREPOSITION",
  "Preposición / Nexo subordinante ": "PREPOSITION_SUBORDINATE_NEXUS",
  "Préstamo del español": "SPANISH_BORROWING",
  "Pronombre": "PRONOUN",
  "Pronombre / Artículo Plural": "PRONOUN_PLURAL_ARTICLE",
  "Pronombre / Conjunción subordinada": "PRONOUN_SUBORDINATE_CONJUNCTION",
  "Pronombre / Interrogativo": "PRONOUN_INTERROGATIVE",
  "Pronombre / Preposición / Verbo": "PRONOUN_PREPOSITION_VERB",
  "Pronombre demostrativo": "DEMONSTRATIVE_PRONOUN",
  "Pronombre indefinido": "INDEFINITE_PRONOUN",
  "Pronombre personal": "PERSONAL_PRONOUN",
  "Pronombre Personal": "PERSONAL_PRONOUN_ALT",
  "Pronombre personal (enclítico)": "ENCLITIC_PERSONAL_PRONOUN",
  "Pronombre relativo": "RELATIVE_PRONOUN",
  "Sufijo": "SUFFIX",
  "Sustantivo": "NOUN",
  "Sustantivo / Adjetivo": "NOUN_ADJECTIVE",
  "Sustantivo / Despectivo": "NOUN_DEROGATORY",
  "Sustantivo colectivo": "COLLECTIVE_NOUN",
  "Sustantivo masculino/femenino": "MASCULINE_FEMININE_NOUN",
  "Sustantivo plural": "PLURAL_NOUN",
  "Sustantivo propio": "PROPER_NOUN",
  "Sustantivo/Adjetivo": "NOUN_ADJECTIVE_ALT",
  "Título": "TITLE",
  "Variante átona": "ATONIC_VARIANT",
  "Verbo": "VERB",
  "Verbo / Sustantivo": "VERB_NOUN",
  "Verbo copulativo": "COPULATIVE_VERB",
  "Verbo copulativo (Pretérito)": "COPULATIVE_VERB_PRETERITE",
  "Verbo copulativo / Variante ": "COPULATIVE_VERB_VARIANT",
  "Verbo copulativo imperfecto": "IMPERFECT_COPULATIVE_VERB",
  "Verbo copulativo presente": "PRESENT_COPULATIVE_VERB",
  "Verbo impersonal": "IMPERSONAL_VERB",
  "Verbo infinitivo": "INFINITIVE_VERB",
  "Verbo infinitivo / Marcador temporal ": "INFINITIVE_VERB_TEMPORAL_MARKER",
  "Verbo infinitivo / Verbo copulativo": "INFINITIVE_VERB_COPULATIVE_VERB",
  "Verbo intransitivo": "INTRANSITIVE_VERB",
  "Verbo modal en imperfecto": "IMPERFECT_MODAL_VERB",
  "Verbo pronominal": "PRONOMINAL_VERB",
  "Verbo reflexivo": "REFLEXIVE_VERB",
  "Verbo transitivo": "TRANSITIVE_VERB",
}

# Default value
DEFAULT_WORD_TYPE = "NONE"

class WordType(Enum):
  ADJECTIVE = "ADJECTIVE"
  ADJECTIVE_NUMERAL = "ADJECTIVE_NUMERAL"
  ADJECTIVE_NOUN = "ADJECTIVE_NOUN"
  ADJECTIVE_PRONOUN = "ADJECTIVE_PRONOUN"
  ADJECTIVE_NOUN_ALT = "ADJECTIVE_NOUN_ALT"
  ADVERB = "ADVERB"
  ADVERB_NEGATIVE_MARKER = "ADVERB_NEGATIVE_MARKER"
  ADVERB_NOUN = "ADVERB_NOUN"
  INDEFINITE_ARTICLE = "INDEFINITE_ARTICLE"
  CONJUNCTION = "CONJUNCTION"
  CONJUNCTION_SUBORDINATE_NEXUS = "CONJUNCTION_SUBORDINATE_NEXUS"
  SUBORDINATE_CONJUNCTION = "SUBORDINATE_CONJUNCTION"
  EXPRESSION = "EXPRESSION"
  IDIOMATIC_EXPRESSION = "IDIOMATIC_EXPRESSION"
  TEMPORAL_EXPRESSION = "TEMPORAL_EXPRESSION"
  PHRASE = "PHRASE"
  HABITUAL_IMPERFECT = "HABITUAL_IMPERFECT"
  IMPERATIVE_PLURAL = "IMPERATIVE_PLURAL"
  IMPERATIVE_SINGULAR = "IMPERATIVE_SINGULAR"
  PERIPHRASTIC_IMPERFECT = "PERIPHRASTIC_IMPERFECT"
  SIMPLE_IMPERFECT_SUFFIX = "SIMPLE_IMPERFECT_SUFFIX"
  INTERJECTION = "INTERJECTION"
  LOCUTION = "LOCUTION"
  ADVERBIAL_LOCUTION = "ADVERBIAL_LOCUTION"
  ASPECTUAL_MARKER = "ASPECTUAL_MARKER"
  ASPECTUAL_MARKER_IMPERFECT = "ASPECTUAL_MARKER_IMPERFECT"
  EXISTENCE_MARKER = "EXISTENCE_MARKER"
  PRAGMATIC_MARKER = "PRAGMATIC_MARKER"
  PREVERBAL_ASPECTUAL_TEMPORAL_MARKER = "PREVERBAL_ASPECTUAL_TEMPORAL_MARKER"
  TEMPORAL_ASPECTUAL_MARKER = "TEMPORAL_ASPECTUAL_MARKER"
  TEMPORAL_ASPECTUAL_MARKER_ALT = "TEMPORAL_ASPECTUAL_MARKER_ALT"
  VERBAL_MARKER = "VERBAL_MARKER"
  VERBAL_ASPECTUAL_MARKER = "VERBAL_ASPECTUAL_MARKER"
  NEGATIVE_NULL = "NEGATIVE_NULL"
  SUBORDINATE_NEXUS = "SUBORDINATE_NEXUS"
  NUMBER = "NUMBER"
  PARTICIPLE = "PARTICIPLE"
  PREPOSITION = "PREPOSITION"
  PREPOSITION_SUBORDINATE_NEXUS = "PREPOSITION_SUBORDINATE_NEXUS"
  SPANISH_BORROWING = "SPANISH_BORROWING"
  PRONOUN = "PRONOUN"
  PRONOUN_PLURAL_ARTICLE = "PRONOUN_PLURAL_ARTICLE"
  PRONOUN_SUBORDINATE_CONJUNCTION = "PRONOUN_SUBORDINATE_CONJUNCTION"
  PRONOUN_INTERROGATIVE = "PRONOUN_INTERROGATIVE"
  PRONOUN_PREPOSITION_VERB = "PRONOUN_PREPOSITION_VERB"
  DEMONSTRATIVE_PRONOUN = "DEMONSTRATIVE_PRONOUN"
  INDEFINITE_PRONOUN = "INDEFINITE_PRONOUN"
  PERSONAL_PRONOUN = "PERSONAL_PRONOUN"
  PERSONAL_PRONOUN_ALT = "PERSONAL_PRONOUN_ALT"
  ENCLITIC_PERSONAL_PRONOUN = "ENCLITIC_PERSONAL_PRONOUN"
  RELATIVE_PRONOUN = "RELATIVE_PRONOUN"
  SUFFIX = "SUFFIX"
  NOUN = "NOUN"
  NOUN_ADJECTIVE = "NOUN_ADJECTIVE"
  NOUN_DEROGATORY = "NOUN_DEROGATORY"
  COLLECTIVE_NOUN = "COLLECTIVE_NOUN"
  MASCULINE_FEMININE_NOUN = "MASCULINE_FEMININE_NOUN"
  PLURAL_NOUN = "PLURAL_NOUN"
  PROPER_NOUN = "PROPER_NOUN"
  NOUN_ADJECTIVE_ALT = "NOUN_ADJECTIVE_ALT"
  TITLE = "TITLE"
  ATONIC_VARIANT = "ATONIC_VARIANT"
  VERB = "VERB"
  VERB_NOUN = "VERB_NOUN"
  COPULATIVE_VERB = "COPULATIVE_VERB"
  COPULATIVE_VERB_PRETERITE = "COPULATIVE_VERB_PRETERITE"
  COPULATIVE_VERB_VARIANT = "COPULATIVE_VERB_VARIANT"
  IMPERFECT_COPULATIVE_VERB = "IMPERFECT_COPULATIVE_VERB"
  PRESENT_COPULATIVE_VERB = "PRESENT_COPULATIVE_VERB"
  IMPERSONAL_VERB = "IMPERSONAL_VERB"
  INFINITIVE_VERB = "INFINITIVE_VERB"
  INFINITIVE_VERB_TEMPORAL_MARKER = "INFINITIVE_VERB_TEMPORAL_MARKER"
  INFINITIVE_VERB_COPULATIVE_VERB = "INFINITIVE_VERB_COPULATIVE_VERB"
  INTRANSITIVE_VERB = "INTRANSITIVE_VERB"
  IMPERFECT_MODAL_VERB = "IMPERFECT_MODAL_VERB"
  PRONOMINAL_VERB = "PRONOMINAL_VERB"
  REFLEXIVE_VERB = "REFLEXIVE_VERB"
  TRANSITIVE_VERB = "TRANSITIVE_VERB"
  NONE = "NONE"

class Word(SQLModel, table=True):
	__allow_unmapped__ = True
	id: int = Field(index=True, primary_key=True)
	word: str = Field(max_length=100)
	created_at: datetime = Field(default_factory=datetime.now)
	updated_at: datetime = Field(default_factory=datetime.now)
	definitions: list[str] = Field(default=None, sa_column=Column(ARRAY(String), server_default='{}'))
	translations: list[str] = Field(default=None, sa_column=Column(ARRAY(String), server_default='{}'))
	examples: list[str] = Field(default=None, sa_column=Column(ARRAY(String), server_default='{}'))
	deleted: bool = Field(default=False)
	created_by: int = Field(default=None, foreign_key="user.id", nullable=True)
	updated_by: int = Field(default=None, foreign_key="user.id", nullable=True)
	type: WordType = Field(default=WordType.NONE)
