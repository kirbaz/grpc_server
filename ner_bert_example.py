from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline

# Используйте мультилингвальную модель BERT
model_name = "Davlan/xlm-roberta-base-ner-hrl"

# Загрузите токенайзер и модель
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForTokenClassification.from_pretrained(model_name)

# Создайте pipeline для NER
nlp = pipeline("ner", model=model, tokenizer=tokenizer)

# Пример текста на другом языке
text = "Барселона выиграла Лигу чемпионов УЕФА в 2015 году."

# Анализ текста
ner_results = nlp(text)

for entity in ner_results:
    print(entity)
