import os

from deeppavlov.utils.telegram import interact_model_by_telegram

db_auto_token=os.environ["AUTO_TG"]

interact_model_by_telegram(model_config="model.json", token=db_auto_token)
