import pandas as pd
df = pd.read_csv('./faq_school.csv')
print(df.sample(frac=1)[:5].to_string())


from deeppavlov import configs, build_model
faq = build_model(configs.faq.tfidf_autofaq, download = True)

from deeppavlov.contrib.skills.similarity_matching_skill import SimilarityMatchingSkill
faq = SimilarityMatchingSkill(data_path = './faq_school.csv',
                              x_col_name = 'Question', 
                              y_col_name = 'Answer',
                              save_load_path = './model',
                              config_type = 'tfidf_autofaq',
                              edit_dict = {},
                              train = True)
faq = SimilarityMatchingSkill(save_load_path='./model')
