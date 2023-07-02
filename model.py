import os

from transformers import (DataCollatorForLanguageModeling, GPT2LMHeadModel,
                          GPT2Tokenizer, TextDataset, Trainer,
                          TrainingArguments)


class LyricsGenerator:
    def __init__(self, artist_name):
        self.is_trained = False
        self.artist_name = artist_name
        model = self.find_existing_model()
        if model:
            self.tokenizer = model[0]
            self.model = model[1]
        else:
            self.load_model()
            dataset = self.read_dataset()
            if not dataset:
                return print(f"Could not find data for artist {artist_name}")
            self.train(dataset[0], dataset[1])
            self.save_model()

    def load_model(self):
        model_name = "gpt2"
        self.tokenizer = GPT2Tokenizer.from_pretrained(model_name)
        self.model = GPT2LMHeadModel.from_pretrained(
            model_name, pad_token_id=self.tokenizer.eos_token_id)

    def find_existing_model(self):
        model_path = f"models/{self.artist_name}"
        if os.path.exists(model_path) and os.path.isdir(model_path):
            tokenizer = GPT2Tokenizer.from_pretrained(model_path)
            model = GPT2LMHeadModel.from_pretrained(model_path)
            self.is_trained = True
            return tokenizer, model
        return False

    def generate_text(self, start, max_length):
        if not self.is_trained:
            return "Model is not trained :-("
        input_ids = self.tokenizer.encode(start, return_tensors="pt")
        output = self.model.generate(input_ids,
                                     min_length=100,
                                     max_length=max_length,
                                     no_repeat_ngram_size=2,
                                     early_stopping=True,
                                     num_return_sequences=1,
                                     temperature=float(1),
                                     top_p=0.95,
                                     top_k=50,
                                     repetition_penalty=1.0)
        return self.decode_lyrics(output)

    def decode_lyrics(self, outputs):
        generated_sequences = []
        for output in outputs:
            generated_sequence = self.tokenizer.decode(
                output, skip_special_tokens=True)
            generated_sequences.append(generated_sequence)
        return generated_sequences

    def train(self, train_dataset, data_collator):
        training_args = TrainingArguments(
            output_dir='./results',  # output directory
            num_train_epochs=3,  # total number of training epochs
            per_device_train_batch_size=32,  # batch size per device during training
            per_device_eval_batch_size=64,  # batch size for evaluation
            warmup_steps=500,  # number of warmup steps for learning rate scheduler
            weight_decay=0.01,  # strength of weight decay
            logging_dir='./logs',  # directory for storing logs
            logging_steps=10,
        )
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=train_dataset,
            data_collator=data_collator,
        )
        print(f"Starting to train model for artist: {self.artist_name}")
        trainer.train()
        print(f"Training is finished")
        self.is_trained = True

    def read_dataset(self):
        file_path = f"data/{self.artist_name}.txt"

        if not os.path.exists(file_path):
            print(f"Cannot find file {file_path}")
            return False

        train_dataset = TextDataset(file_path=file_path,
                                    block_size=128,
                                    tokenizer=self.tokenizer)
        data_collator = DataCollatorForLanguageModeling(
            tokenizer=self.tokenizer, mlm=False)
        return train_dataset, data_collator

    def save_model(self):
        output_dir = f"./models/{self.artist_name}"
        self.model.save_pretrained(output_dir)
        self.tokenizer.save_pretrained(output_dir)