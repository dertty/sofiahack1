import numpy as np
import torch
import joblib


class NagibatorClassifier:
    def __init__(self, classifier, model_class, tokenizer_class, pretrained_weights, max_length=512, batch_size=512):
        self.classifier = joblib.load(classifier)
        self.tokenizer = tokenizer_class.from_pretrained(pretrained_weights)
        self.model = model_class.from_pretrained(pretrained_weights)
        self.device = torch.device('cuda:0') if torch.cuda.is_available() else torch.device('cpu')
        self.max_length = max_length
        self.batch_size = batch_size

    def tokenizing_tokens(self, data):
        return [self.tokenizer.encode(x, add_special_tokens=True, max_length=self.max_length) for x in data]

    def pad_texts(self, texts_tokenized):
        max_len = 0
        for i in texts_tokenized:
            if len(i) > max_len:
                max_len = len(i)
        return np.array([j + [0] * (max_len - len(j)) for j in texts_tokenized])

    def attention_mask(self, padded_text):
        return np.where(padded_text != 0, 1, 0)

    def preparing_data(self, data):
        data_tokenized = self.tokenizing_tokens(data)
        padded_data = self.pad_texts(data_tokenized)
        attention_mask_data = self.attention_mask(padded_data)
        output_data = []

        self.model.to(self.device)
        self.model.eval()

        for idx in range(0, data.shape[0], self.batch_size):
            batch = torch.tensor(padded_data[idx:idx + self.batch_size]).to(self.device)
            local_attention_mask = torch.tensor(attention_mask_data[idx:idx + self.batch_size]).to(self.device)
            with torch.no_grad():
                last_hidden_states = self.model(batch, attention_mask=local_attention_mask)[0][:, 0,
                                     :].cpu().detach().numpy()
                output_data.append(last_hidden_states)

        return np.vstack(output_data)

    def predict(self, data):
        # data - numpy array
        sample_data = self.preparing_data(data)
        return self.classifier.predict_proba(sample_data)[:, 1]