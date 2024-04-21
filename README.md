# cleric-THA (take home assignment)


This Flask application serves as a simple Question Answering system that takes a question and a set of documents(call transcripts) as input, and returns relevant facts based on the input. It provides a web interface for users to interact with.

To run the application, ensure you have Python installed on your system. Then follow these steps:
1. Clone this repository to your local machine - git clone https://github.com/riyasinghal04/cleric-THA.git
2. Navigate to the project directory
3. Install the required dependencies using pip
4. Start the Flask server by running the following command: python3 app.py

Once the server is running, you can access the application through your web browser at http://localhost:5000.
Enter a question and a set of documents in the provided input fields and submit the form.
The application will process the input and return relevant facts based on the question and documents.


## Folder Structure - 
- `requirements.txt`: Contains all the libraries used for the app
- `app.py`: Contains the main Flask application code.
- `get_facts.py`: Contains the function to extract facts based on the question and documents using OpenAI API and Langchain.
- `templates/`: Directory containing HTML templates for the web interface. </br>
    -- index.html: Template for the home page with input fields. </br>
    -- output.html: Template for displaying the output facts.</br>
- `llm_playground`: Jupyter notebook for testing ML pipeline before integrating it in the app
  


## API Endpoints -
- `/` : Home page of the web interface where users can input their question and documents. </br>
- `/submit_question_and_documents` : Endpoint to submit a question and documents via JSON. </br>
- `/get_question_and_facts` : Endpoint to retrieve the question and relevant facts. </br>


## Document Processing System Design - 
Following are the various components of the get_facts.py : 

`1. Input Processing:`
  The system takes two inputs: A question that specifies the information the user wants to retrieve and URLs to text files containing call transcripts.

`2. Text Processing:`
The process_txt_files function fetches the content of the text files from the provided URLs and concatenates them into a single string.
The concatenated content is then split into smaller chunks using a recursive character-based text splitter. This is done to ensure that the input texts are manageable for the subsequent processing steps.

`3. Language Model:`
The system utilizes a language model (in this case, GPT-4) provided by OpenAI to understand and generate text responses.
It employs the ChatOpenAI class to interact with the language model and generate responses based on the input question and call transcripts.

`4. Prompt Templates:`
The system uses custom prompt templates to structure the interactions with the language model. These templates guide the model on how to interpret the input question and transcripts and generate relevant facts.
There are separate templates for system messages (instructions) and human messages (transcript content).

`5. Summarization Chain:`
The core functionality of the system is encapsulated in a summarization chain. This chain orchestrates the interactions between the language model and the input data to produce the desired output. It uses a map-reduce approach, where the map step processes individual chunks of text, and the reduce step aggregates the results to produce the final output.The summarization chain is configured with specific prompts for mapping and combining, which define how the language model should handle the input data and generate responses.

`6. Output Formatting:`
The generated facts are formatted as bulleted points according to a predefined format specified in the output template.
This ensures consistency and clarity in presenting the extracted facts to the user.

`7. Output:`
The system returns the extracted facts as a list of bulleted points, which can be further processed or presented to the user as needed.

References:
https://github.com/gkamradt/langchain-tutorials/blob/main/data_generation/Working%20With%20Call%20or%20Video%20Transcripts.ipynb
