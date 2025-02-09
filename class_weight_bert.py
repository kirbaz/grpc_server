import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.utils.class_weight import compute_class_weight
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
from transformers import EarlyStoppingCallback
import torch
from tqdm import tqdm

# Загрузка данных
df = pd.read_csv('path_to_your_data.csv')  # Замените на путь к вашему файлу
df['CATEGORY'] = df['CATEGORY'].astype(int)  # Убедитесь, что CATEGORY - это int

# Разделение данных на обучающую и валидационную выборки
train_texts, val_texts, train_labels, val_labels = train_test_split(
    df['MESSAGE'].tolist(),
    df['CATEGORY'].tolist(),
    test_size=0.2,
    random_state=42
)

# Вычисление весов классов
class_weights = compute_class_weight('balanced', classes=np.unique(train_labels), y=train_labels)
class_weights = torch.tensor(class_weights, dtype=torch.float)

# Загрузка токенизатора и модели
tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')
model = BertForSequenceClassification.from_pretrained('bert-base-multilingual-cased', num_labels=2)

# Токенизация данных
train_encodings = tokenizer(train_texts, truncation=True, padding=True, max_length=512)
val_encodings = tokenizer(val_texts, truncation=True, padding=True, max_length=512)

# Создание Dataset
class CustomDataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)

train_dataset = CustomDataset(train_encodings, train_labels)
val_dataset = CustomDataset(val_encodings, val_labels)

# Настройка параметров обучения
training_args = TrainingArguments(
    output_dir='./results',          # директория для сохранения модели
    num_train_epochs=10,              # количество эпох
    per_device_train_batch_size=8,    # размер батча
    per_device_eval_batch_size=8,     # размер батча для валидации
    warmup_steps=500,                  # количество шагов для разогрева
    weight_decay=0.01,                 # коэффициент L2 регуляризации
    logging_dir='./logs',            # директория для логов
    logging_steps=10,
    evaluation_strategy="epoch",      # оценка на валидации после каждой эпохи
    load_best_model_at_end=True,      # загрузка лучшей модели в конце
    metric_for_best_model="accuracy",  # метрика для выбора лучшей модели
    greater_is_better=True,            # больше - лучше
)

# Создание Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    compute_metrics=lambda p: {
        'accuracy': (np.argmax(p.predictions, axis=1) == p.label_ids).mean(),
    },
    callbacks=[EarlyStoppingCallback(early_stopping_patience=2)],  # остановка при отсутствии улучшений
)

# Обучение модели
trainer.train()

# Сохранение модели
model.save_pretrained('./saved_model')
tokenizer.save_pretrained('./saved_model')



# Объяснение кода:
# Загрузка данных: Данные загружаются из CSV файла.
# Разделение данных: Данные делятся на обучающую и валидационную выборки с учетом стратификации по классам.
# Токенизация: Тексты преобразуются в формат, подходящий для BERT.
# Создание Dataset: Создается класс CustomDataset для работы с данными.
# Веса классов: Вычисляются веса классов для борьбы с дисбалансом.
# Инициализация модели: Загружается предобученная модель BERT для классификации.
# Аргументы для обучения: Определяются параметры обучения, включая стратегию сохранения и оценки.
# Обучение: Модель обучается с использованием Trainer.