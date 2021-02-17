# spoken-language-processing

## Requirements if you want to train with Icelandic fasttext word embeddings
pip install "rasa_nlu_examples[all] @ https://github.com/RasaHQ/rasa-nlu-examples.git"

pip install "rasa_nlu_examples[fasttext] @ https://github.com/RasaHQ/rasa-nlu-examples.git"

download icelandic fast_text vectors (cc.en.300.bin) from https://fasttext.cc/docs/en/crawl-vectors.html and move to downloaded/beforehand

rasa train -c config_fasttext.yml
