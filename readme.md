[Introduction]
The repository contains [WIP] end-2-end code for the event recommendation engine. 

- Pretrained BERT model is used to create embeddings for context words which are essentially word tags for events. 
- The query word which is expression of interest is also passed through the model to compute the embedding. 
- Top <K> context words are fetched using cosine similarity metric and events having these words as tags are recommended.


TODO:
    1. Modify the vector DB to be persistent. -> Done
    2. Create following backend APIs: -> In Progress
        a. Auth Token issue / check -> Done
        b. User Signup -> Done
        c. Event Induction -> Done
        d. Event Invitation -> TBU
        e. Event Aceeptance -> TBU
        f. Event Deletion -> TBU
        g. Event Recommendation -> TBU
        h. Password Change -> Done
        i. Logout -> Done
        j. Add Interest -> Done
        k. Delete Interest -> Done
        l. View Interest -> Done
        m. Change Profile Pic -> Done
        n. Change Password -> Done
    3. Create the frontend screens -> In-Progress