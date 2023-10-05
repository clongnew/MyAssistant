from langchain.embeddings.huggingface import HuggingFaceEmbeddings


class MyEmbeddings(HuggingFaceEmbeddings):
    def __int__(self, model_name, **kwargs):
        super().__init__(model_name='shibing624/text2vec-base-chinese', **kwargs)
