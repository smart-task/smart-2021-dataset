# Datasets and evaluation scripts for SeMantic Answer Type and Relation Prediction Task ([SMART 2021](https://smart-task.github.io/2021/))

Question Answering is a popular task in the field of Natural Language Processing and Information Retrieval, in which, the goal is to answer a natural language question (going beyond the document retrieval). Question or answer type classification and relation prediction plays a key role in question answering. The questions can be generally classified based on Wh-terms (Who, What, When, Where, Which, Whom, Whose, Why). A granular answer type classification is possible with popular Semantic Web ontologies such as DBpedia (~760 classes) and Wikidata (~50K classes). On the other hand, relation prediction for question is a hard task, some relations are semantically far and sometimes tokens deciding the relations are spread across the question, some relations are implicit in text, and there are lexical gaps in relation surface forms and KG property labels.

Thus, in the second iteration of SMART challenge, we have two independent tasks:

Task 1 - Answer type prediction: Given a question in natural language, the task is to predict type of the answer using a set of candidates from a target ontology.

Task 2 - Relation set prediction: Given a question in natural language, the task is to predict relation to used for identifying the correct answer.
