# Knowledge builder Chatbot For Llama2


## Getting Started

To run the application locally please follow this steps:



open cmd or powershell and :
### Create a virtual environment for the project
```bash
 conda create -n "bahaalg" python=3.7.16

```
### Activate virtual environment
```bash
 conda activate bahaalg

```
### Create a new folder to host this project and getting into it 
```bash
 mkdir Lamadir
```
```bash
 cd Lamadir
```
### Clone the Repository
```bash
 git clone https://github.com/bahagh/Llama2-KnowledgeBuilder-QA.git
```
```bash
 cd Llama2-KnowledgeBuilder-QA
```
### Install required packages
```bash
 pip install -r requirements.txt

```
### Run the project
###### if you still want this chatbot to be helpful in the Llama2 topic you woldnt need the part related to loading embeddings every time that maks running the project takes quite longer time that's why running using the fastrun file makes it straight forward by initializing the embeddings related to Llama2 (remember that if this project is adapted to annother topic you 'll need to load the embeddings first of course via running the main file and then you can do the almost the same way that i did to win time by having those embeddings defined in the fastrun file )
```bash
 python fastrun.py runserver
```
###### full run with the loading of the embeddings
```bash
 python main.py runserver
```

Thank youuu :) !
