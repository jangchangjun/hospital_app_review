import pandas as pd
import numpy as np
import torch
from torch.utils.data import TensorDataset, DataLoader, SequentialSampler
from transformers import ElectraTokenizer, ElectraForSequenceClassification

# 학습된 모델의 폴더명 넣기
model_path = 'koelectra_test'
model = ElectraForSequenceClassification.from_pretrained(model_path)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)
model.eval()

# 데이터 셋은 전체 데이터셋을 넣기
data_path = "labeled_reviews.txt"
dataset = pd.read_csv(data_path, sep='\t').dropna(axis=0)
text = list(dataset['content'].values)
label = dataset['label'].values

tokenizer = ElectraTokenizer.from_pretrained('koelectra-small-v3-discriminator')
inputs = tokenizer(text, truncation=True, max_length=256, add_special_tokens=True, padding="max_length")
input_ids = inputs['input_ids']
attention_mask = inputs['attention_mask']

batch_size = 32

test_inputs = torch.tensor(input_ids)
test_labels = torch.tensor(label)
test_masks = torch.tensor(attention_mask)
test_dataset = TensorDataset(test_inputs, test_masks, test_labels)
test_sampler = SequentialSampler(test_dataset)
test_dataloader = DataLoader(test_dataset, sampler=test_sampler, batch_size=batch_size)

all_preds = []

test_loss, test_accuracy, test_steps = 0, 0, 0
for batch in test_dataloader:
    batch_ids, batch_masks, batch_labels = tuple(t.to(device) for t in batch)
    with torch.no_grad():
        outputs = model(batch_ids, token_type_ids=None, attention_mask=batch_masks)

    logits = outputs[0]
    logits = logits.cpu().numpy()

    pred_flat = np.argmax(logits, axis=1).flatten()
    all_preds.extend(pred_flat)

    # label이 있을 경우에는 아래를 실행
    label_ids = batch_labels.cpu().numpy()
    label_flat = label_ids.flatten()
    test_accuracy_temp = np.sum(pred_flat == label_ids) / len(label_flat)
    test_accuracy += test_accuracy_temp
    test_steps += 1
    print(f"Test step : {test_steps}/{len(test_dataloader)}, Temp Accuracy : {test_accuracy_temp}")

# 마찬가지로 label이 있을 경우
avg_test_accuracy = test_accuracy / test_steps
print(f'Total Accuracy : {avg_test_accuracy}')

# 예측 결과를 데이터프레임에 추가
dataset['pred_label'] = all_preds

# 결과를 파일로 저장
dataset.to_csv('ratings_result.txt', sep='\t', index=False)
