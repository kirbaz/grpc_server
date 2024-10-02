from transformers import BertTokenizer, BertForSequenceClassification
import torch
from transformers import Trainer, TrainingArguments
from datasets import load_dataset
import pandas as pd
from sklearn.model_selection import train_test_split


# Путь к вашим загруженным файлам
model_path = "./bert-base-multilingual-cased"

# Загрузка токенайзера и модели из локальной директории
tokenizer = BertTokenizer.from_pretrained(model_path)
NUM_LABELS = 2
model = BertForSequenceClassification.from_pretrained(model_path, num_labels=NUM_LABELS)

# Загрузим данные
data = pd.read_csv('your_data.csv')

# Разделим данные на обучающую и тестовую выборки
train_texts, val_texts, train_labels, val_labels = train_test_split(data['txt'], data['label'], test_size=0.2)

# Токенизируем тексты
train_encodings = tokenizer(list(train_texts), truncation=True, padding=True)
val_encodings = tokenizer(list(val_texts), truncation=True, padding=True)

### Подготовка датасетов для модели
# Создаем PyTorch датасет для наших данных:

class Dataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)


train_dataset = Dataset(train_encodings, train_labels)
val_dataset = Dataset(val_encodings, val_labels)

### Обучение модели
# Настройка и обучение модели BERT:

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

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
)

trainer.train()

### Предсказания на новых текстах
# Загрузка новых текстов и получение предсказаний:

new_texts = ["This is a new text", "Another new text"]  # замените своими текстами
new_encodings = tokenizer(new_texts, truncation=True, padding=True, return_tensors='pt')

model.eval()
with torch.no_grad():
    outputs = model(**new_encodings)
    predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
    print(predictions)

### Проверка на новых текстах
# Если хотите сразу проверить модель на новых текстах и получить метрики качества, можно использовать Trainer.evaluate():
results = trainer.evaluate()
print(results)
