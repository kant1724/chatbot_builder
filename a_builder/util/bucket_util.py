from b_trainer.file import training_file_creator as tfc

def get_bucket_id_by_sentence(buckets, sentence):
    token = tfc.char_tokenizer(sentence)
    for j in range(len(buckets)):
        if len(token) < int(buckets[j]):
            return max(j - 1, 0)
