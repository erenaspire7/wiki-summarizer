# Wiki Summarizer Bot

## The Problem
Wikipedia serves as a vast repository of information, encompassing a wide array of topics. However, the sheer volume of content on the platform can be overwhelming for individual readers to navigate. To address this, summaries are crafted to distill the essential points from comprehensive articles, offering a concise yet informative overview of the subject matter. These summaries provide readers with a quick grasp of the main concepts, making it easier to access and comprehend the wealth of knowledge that Wikipedia offers.


## How To Setup

- Create a virtual environment using this command in your terminal 
```
python -m venv venv
```

- Activate the virtual environment

```
# For Bash Terminals
source bin/venv/activate
```

```
# PowerShell Terminals
.\venv\Scripts\Activate.ps1
```

- Install the requirements and download spacy's web model

```
pip install -r requirements.txt && python -m spacy download en_core_web_sm
```

- Run the chatbot

```
python app.py
```

- Go to the bot's telegram link (https://t.me/erenaspire7_bot), and start summarizing!

## Limitations / Development Concerns

Naturally, a project like this is best suited for summarizing articles, but that would require extensive data scraping, as we will be dealing with a lot of cases, which isn't ideal, given the time constraints.

Secondly, spacy's keywords generation/intent analysis, often needs to be coupled with an external model/software, hence it's not a conversational bot. Instead, it does what I think spacy does best, being assigning weights to sentences for extractive summarization, then coupling that with abstractive summarization, enabled by the power of GPT-3.5.

Finally, a limitation I've noticed is it just gives an overview on things like movies, and might exclude major plot points, as it's highly dependent on the frequency of words.
