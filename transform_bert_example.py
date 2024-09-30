from transformers import BertTokenizer, BertForSequenceClassification
import torch
from transformers import Trainer, TrainingArguments
from datasets import load_dataset


# Путь к вашим загруженным файлам
model_path = "./bert-base-multilingual-cased"

# Загрузка токенайзера и модели из локальной директории
tokenizer = BertTokenizer.from_pretrained(model_path)
NUM_LABELS = 2
model = BertForSequenceClassification.from_pretrained(model_path, num_labels=NUM_LABELS)

# Пример текста для классификации
sample_text = "Это пример текста."

# Токенизация текста
inputs = tokenizer(sample_text, return_tensors='pt')

# Получение предсказаний
with torch.no_grad():
    outputs = model(**inputs)
    predictions = torch.argmax(outputs.logits, dim=-1)

print(f"Predicted class: {predictions.item()}")

# Предполагается, что у вас есть файлы data/train.csv и data/test.csv
datasets = load_dataset('csv', data_files={'train': 'data/train.csv', 'test': 'data/test.csv'})

# Определение TrainingArguments
training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=3,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir='./logs',
    logging_steps=10,
)

# Создание Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=datasets['train'],
    eval_dataset=datasets['test'],
    tokenizer=tokenizer
)

# Запуск обучения
trainer.train()


def predict(text):
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=128)
    outputs = model(**inputs)
    preds = torch.argmax(outputs.logits, dim=-1)
    return preds.item()


# Пример использования
print(predict("Новый текст для классификации"))
