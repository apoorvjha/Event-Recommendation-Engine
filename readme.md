[Introduction]
The repository contains [WIP] end-2-end code for the event recommendation engine. 

- Pretrained BERT model is used to create embeddings for context words which are essentially word tags for events. 
- The query word which is expression of interest is also passed through the model to compute the embedding. 
- Top <K> context words are fetched using cosine similarity metric and events having these words as tags are recommended.


TODO:
    1. Modify the vector DB to be persistent. -> Done
    2. Create following backend APIs:
        a. Auth Token issue / check
        b. User Signup
        c. Event Induction
        d. Event Invitation
        e. Event Aceeptance
        f. Event Deletion
        g. Event Recommendation
        h. Password Change
        i. Logout
    3. Create the frontend screens.