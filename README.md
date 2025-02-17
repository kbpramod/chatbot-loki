

# **Loki Chatbot**  

Loki is a machine-learning-based chatbot that reads response data from a JSON file, processes input sentences, and predicts the most appropriate response using a trained neural network model.  

## **Features**  
- Reads predefined responses from a JSON file.  
- Processes and cleans input sentences for better understanding.  
- Uses pattern recognition to classify user input into different tags.  
- Implements a TensorFlow-based neural network with 128 and 64 neurons in hidden layers.  
- Stores words and classes using `pickle` for faster processing.  
- Predicts response classes and provides appropriate replies.  

## **Project Structure**  
```
Loki-Chatbot/
│── data.json                # JSON file containing predefined responses
│── train.py                 # Script to train the chatbot model
│── chat.py                  # Chat interface for user interaction
│── model.h5                 # Trained model file
│── words.pkl                # Stored words list
│── classes.pkl              # Stored classes list
│── nltk_utils.py            # NLP helper functions for text processing
│── README.md                # Project documentation
```  

## **Dependencies**  
Install required packages using:  
```bash
pip install nltk tensorflow keras numpy json pickle
```  

## **How It Works**  
1. **Data Processing**:  
   - Reads response patterns and tags from `data.json`.  
   - Tokenizes and lemmatizes words using NLTK.  
   - Stores processed words and classes using `pickle`.  

2. **Model Training** (`train.py`):  
   - Uses a feedforward neural network with two hidden layers (128 and 64 neurons).  
   - Categorical cross-entropy loss and Adam optimizer for training.  
   - Trained model is saved as `model.h5`.  

3. **Chatting with Loki** (`chat.py`):  
   - Cleans user input.  
   - Predicts the most likely class using the trained model.  
   - Fetches the best response from `data.json`.  

## **Usage**  
Run the chatbot:  
```bash
python chat.py
```  

Enter questions, and Loki will respond based on learned patterns!  

## **Future Improvements**  
- Enhance NLP processing with transformers.  
- Expand the dataset for better responses.  
- Implement voice interaction.  
