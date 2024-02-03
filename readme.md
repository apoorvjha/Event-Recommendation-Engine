[Introduction]
The repository contains [WIP] end-2-end code for the event recommendation engine. 

- Pretrained BERT model is used to create embeddings for context words which are essentially word tags for events. 
- The query word which is expression of interest is also passed through the model to compute the embedding. 
- Top <K> context words are fetched using cosine similarity metric and events having these words as tags are recommended. 