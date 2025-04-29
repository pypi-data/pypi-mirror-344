class tensor:
    def displaydl(self):
        code = """
1. Real estate agents want help to predict the house price for regions in the USA. 
He gave you the dataset to work on and you decided to use the Linear Regression Model. 
Create a model that will help him to estimate what the house would sell for.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.model_selection import train_test_split
df = pd.read_csv('USA_Housing.csv')
df
df.isnull().sum()
sns.pairplot(df, diag_kind = 'kde')
plt.show()
corr = df.select_dtypes(include = 'number').corr()['Price'].drop('Price')
corr.sort_values().plot(kind = 'barh', figsize = (8,5), title = 'Correlation with Price')
plt.show()
df.drop('Address', axis = 1, inplace = True)
X = df.drop('Price',axis = 1)
y = df['Price']
X_train,X_test,y_train,y_test = train_test_split(X, y, test_size = 0.4, random_state = 101)
X_train = X_train.drop('Address', axis = 1)
X_test = X_test.drop('Address', axis = 1)
linear = LinearRegression()
linear.fit(X_train,y_train)
y_pred = linear.predict(X_test)
plt.scatter(y_test,y_pred)
plt.show()
sns.distplot((y_test - y_pred), bins = 50)
plt.show()
print("MAE: ", mean_absolute_error(y_test,y_pred))
print("MSE: ", mean_squared_error(y_test,y_pred))
print("RMSE: ", np.sqrt(mean_squared_error(y_test,y_pred)))

*********************************************************************************
2.Build a Multiclass classifier using the CNN model. 
Use MNIST or any other suitable dataset. 
a. Perform Data Pre-processing 
b. Define Model and perform training 
c. Evaluate Results using confusion matrix.

import tensorflow as tf
from tensorflow.keras.datasets import mnist
from tensorflow.keras.utils import to_categorical
import matplotlib.pyplot as plt
import numpy as np
(x_train, y_train), (x_test, y_test) = mnist.load_data()
def plot_sample(x,y,index):
    plt.figure(figsize=(15,2))
    plt.imshow(x[index],cmap='gray')
    plt.title(y[index])
    
plot_sample(x_train,y_train,4)
x_train = x_train.astype('float32') / 255.0
x_test = x_test.astype('float32') / 255.0
x_train = x_train.reshape(-1, 28, 28, 1)
x_test = x_test.reshape(-1, 28, 28, 1)
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
# Build CNN model
model = Sequential([
    Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape = (28, 28, 1)),
    MaxPooling2D(pool_size=(2, 2)),
    Conv2D(64, kernel_size=(3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),
    Flatten(),
    Dense(128, activation='relu'),
    Dropout(0.5),
    Dense(10, activation='softmax')  # 10 classes
])
# Compile model
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
history = model.fit(x_train, y_train, epochs=5, batch_size=128, validation_split=0.1)
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
# Predict test data
y_pred = model.predict(x_test)
y_pred_labels = np.argmax(y_pred, axis=1)
# Confusion matrix
cm = confusion_matrix(y_test, y_pred_labels)
disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=np.arange(10))
disp.plot(cmap='Blues')
plt.title("Confusion Matrix for MNIST CNN Classifier")
plt.show()
# Accuracy
test_loss, test_acc = model.evaluate(x_test, y_test)
print("Test Accuracy: {:.2f}%".format(test_acc * 100))
from sklearn.metrics import classification_report

# Generate classification report
report = classification_report(y_test, y_pred_labels, target_names=[str(i) for i in range(10)])
print("Classification Report:\n")
print(report)

************************************************************************************************************

3.Design RNN or its variant including LSTM or GRU
a) Select a suitable time series dataset. 
Example – predict sentiments based on product reviews 
b) Apply for prediction

import numpy as np
import tensorflow as tf
from tensorflow.keras.datasets import imdb
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense
from keras.utils import pad_sequences
vocab_size = 10000
(X_train, y_train), (X_test, y_test) = imdb.load_data(num_words=vocab_size)
X_train = pad_sequences(X_train, maxlen=100, padding='post')
X_test = pad_sequences(X_test, maxlen=100, padding='post')
word_index = imdb.get_word_index()
print(word_index)
index_word = {index+3: word for word, index in word_index.items()}
index_word[0] = '<PAD>'
index_word[1] = '<START>'
index_word[2] = '<UNK>'
index_word[3] = '<UNUSED>'
def decode_review(text):
    return ' '.join([index_word.get(i,'?') for i in text])
decoded = decode_review(X_test[0])
print(decoded)
model = Sequential()
model.add(Embedding(input_dim = vocab_size, output_dim=100))
model.add(LSTM(32, dropout=0.2, recurrent_dropout=0.2))
model.add(Dense(1, activation='sigmoid'))
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
history = model.fit(X_train, y_train, epochs=5, batch_size=128, validation_split=0.1)
plt.figure(figsize=(12,4))

plt.subplot(1,2,1)
plt.plot(history.history['accuracy'], label = 'Training Accuracy')
plt.plot(history.history['val_accuracy'], label = 'Validation Accuracy')
plt.title('Accuracy Over Epochs')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()

plt.subplot(1,2,2)
plt.plot(history.history['loss'], label = 'Training Loss')
plt.plot(history.history['val_loss'], label = 'Validation Loss')
plt.title('Loss Over Epochs')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()

plt.tight_layout()
plt.show()

y_pred = model.predict(X_test)
y_pred_labels = (y_pred > 0.5).astype('int')
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay
cm = confusion_matrix(y_test, y_pred_labels)
np.set_printoptions(suppress=True)
disp = ConfusionMatrixDisplay(cm)
disp.plot(cmap=plt.cm.Blues)
plt.show()
report = classification_report(y_test, y_pred_labels)
print(report)

word_index = imdb.get_word_index()
def encode_review(review):
    encoded = [1]
    for word in review.lower().split():
        index = word_index.get(word, 2)
        encoded.append(index + 3)
    
    encoded_review = pad_sequences([encoded], maxlen=100, padding='post')
    return encoded_review

review = input("Enter your review: ")
prediction = model.predict(encode_review(review))
if prediction[0][0] >= 0.5:
    print("This is a POSITIVE review!")
else:
    print("This is a NEGATIVE review!")

***************************************************************************************
4. Design and implement a CNN for Image Classification 
a) Select a suitable image classification dataset (medical imaging, agricultural, etc.). 
b) Optimized with different hyper-parameters including learning rate, filter size, no. of layers, optimizers, dropouts, etc.

import tensorflow as tf
from tensorflow.keras.datasets import fashion_mnist
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Dense, Flatten, Dropout
from tensorflow.keras.models import Sequential
import keras_tuner as kt
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import numpy as np

(X_train, y_train), (X_test, y_test) = fashion_mnist.load_data()


def plot_sample(X, y, index):
    plt.figure(figsize=(6,4))
    plt.imshow(X[index], cmap='grey')
    plt.title(y[index])

plot_sample(X_train, y_train, 9)

X_train = X_train.astype("float32") / 255.0
X_test = X_test.astype("float32") / 255.0

X_train = X_train.reshape(-1, 28, 28, 1)
X_test = X_test.reshape(-1, 28, 28, 1)

X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=42)

def build_model(hp):
    model = Sequential()
    for i in range(hp.Int('num_layers', min_value=1, max_value=4)):
        model.add(Conv2D(
            filters=hp.Int(f'filters_{i}', min_value=32, max_value=128, step=32), 
            kernel_size=hp.Choice(f'kernel_size_{i}', [3,5]),
            activation='relu',
            padding='same',
            input_shape=(28, 28, 1) if i == 0 else None 
        ))
        
        model.add(MaxPooling2D())
        
    model.add(Flatten())
    model.add(Dense(hp.Int('dense_units', 32, 128, step=32), activation='relu'))
    model.add(Dropout(rate=hp.Float('dropout', 0.2, 0.5, step=0.1)))
    model.add(Dense(10, activation='softmax'))
    
    model.compile(
        optimizer=hp.Choice('optimizer', values=['adam', 'sgd', 'nadam']),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )

    return model

tuner = kt.RandomSearch(
    build_model,
    objective='val_accuracy',
    max_trials=6,
    executions_per_trial=1,
    directory='my_dir',
    project_name='fashion_mnist'
)

tuner.search(X_train, y_train, epochs=3,  validation_data=(X_val, y_val))
tuner.get_best_hyperparameters()[0].values

best_model = tuner.get_best_models(num_models=1)[0]


best_model.fit(X_train, y_train, epochs=10, initial_epoch=3, validation_data=(X_test, y_test))


test_loss, test_accuracy = best_model.evaluate(X_test, y_test)
print(f"Accuracy: {test_accuracy*100:.2f}%")

********************************************************************************************
5.Sentiment Analysis in Network Graph using RNN

import pandas as pd
import networkx as nx
from tensorflow.keras.models import load_model, Sequential
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.layers import Embedding, LSTM, Dense
from tensorflow.keras.datasets import imdb
import pickle
import tensorflow as tf
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import tensorflow_hub as hub
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Hyperparameters
vocab_size = 10000
max_length = 200
embedding_dim = 128
lstm_units = 128
epochs = 10  # Increased for better training
batch_size = 64

# Step 1: Load and preprocess IMDB data
(X_train, y_train), (X_test, y_test) = imdb.load_data(num_words=vocab_size, skip_top=0, maxlen=None, start_char=1, oov_char=2, index_from=3)
X_train = pad_sequences(X_train, maxlen=max_length, padding='post', truncating='post')
X_test = pad_sequences(X_test, maxlen=max_length, padding='post', truncating='post')

# Step 2: Build the model with LSTM
model = Sequential([
    Embedding(input_dim=vocab_size, output_dim=embedding_dim, input_length=max_length),
    LSTM(units=lstm_units),
    Dense(1, activation='sigmoid')
])
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
model.summary()

# Step 3: Train the model
history = model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, validation_split=0.2)

# Step 4: Evaluate the model
test_loss, test_accuracy = model.evaluate(X_test, y_test)
print(f"Test Accuracy: {test_accuracy:.4f}, Test Loss: {test_loss:.4f}")

y_pred_probs = model.predict(X_test)
y_pred_classes = (y_pred_probs > 0.5).astype(int)
conf_matrix = confusion_matrix(y_test, y_pred_classes)

# Step 4.2: Visualize Confusion Matrix
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues',
            xticklabels=['Negative', 'Positive'], yticklabels=['Negative', 'Positive'])
plt.xlabel('Predicted Label')
plt.ylabel('True Label')
plt.title('Confusion Matrix for Sentiment Analysis')
plt.show()

# Print Confusion Matrix metrics
TN, FP, FN, TP = conf_matrix.ravel()
accuracy_cm = (TP + TN) / (TP + TN + FP + FN)
precision_cm = TP / (TP + FP)
recall_cm = TP / (TP + FN)
f1_score_cm = 2 * (precision_cm * recall_cm) / (precision_cm + recall_cm)
print("\nConfusion Matrix Metrics:")
print(f"Accuracy : {accuracy_cm:.4f}")
print(f"Precision: {precision_cm:.4f}")
print(f"Recall   : {recall_cm:.4f}")
print(f"F1-Score : {f1_score_cm:.4f}")

# Step 5: Save the model
model.save('sentiment_rnn_model.h5')

# Step 6: Save the tokenizer
word_index = imdb.get_word_index()
# Adjust word index for IMDB's offset
word_index = {k: (v + 3) for k, v in word_index.items()}
word_index["<PAD>"] = 0
word_index["<START>"] = 1
word_index["<UNK>"] = 2
word_index["<UNUSED>"] = 3

tokenizer = Tokenizer(num_words=vocab_size, oov_token="<UNK>")
tokenizer.word_index = word_index
with open('tokenizer.pickle', 'wb') as handle:
    pickle.dump(tokenizer, handle)
print("Model and tokenizer saved successfully!")

# Step 7: Sentiment Analysis on Graph
def perform_sentiment_analysis(graph, model_path, tokenizer_path, max_length):
    try:
        # Extract texts from nodes
        texts = [data['text'] for node, data in graph.nodes(data=True) if 'text' in data]
        if not texts:
            raise ValueError("No 'text' attributes found in the graph nodes.")

        # Load tokenizer
        with open(tokenizer_path, 'rb') as handle:
            tokenizer = pickle.load(handle)

        # Preprocess texts
        sequences = tokenizer.texts_to_sequences(texts)
        padded_sequences = pad_sequences(sequences, maxlen=max_length, padding='post', truncating='post')

        # Load model
        model = load_model(model_path)

        # Predict sentiments
        predictions = model.predict(padded_sequences)
        sentiments = ['positive' if p > 0.5 else 'negative' for p in predictions.flatten()]

        # Attach sentiments to nodes
        text_idx = 0
        for node, data in graph.nodes(data=True):
            if 'text' in data:
                graph.nodes[node]['sentiment'] = sentiments[text_idx]
                text_idx += 1

        return graph
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Could not find model or tokenizer file: {e}")
    except Exception as e:
        raise Exception(f"Error in sentiment analysis: {e}")

# Step 8: Add similarity-based edges
def get_text_embeddings(texts):
    embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")
    embeddings = embed(texts)
    return np.array(embeddings)

def add_similarity_edges(G, similarity_threshold=0.7):  # Increased threshold for fewer, stronger edges
    texts = [data['text'] for _, data in G.nodes(data=True)]
    embeddings = get_text_embeddings(texts)
    similarity_matrix = cosine_similarity(embeddings)

    for i, node_i in enumerate(G.nodes):
        for j, node_j in enumerate(G.nodes):
            if i < j:
                similarity = similarity_matrix[i, j]
                if similarity > similarity_threshold:
                    G.add_edge(node_i, node_j, weight=similarity, label=f"{similarity:.2f}")
    return G

# Step 9: Sentiment Propagation (Simple majority voting based on neighbors)
def propagate_sentiments(G):
    updated_graph = G.copy()
    for node in updated_graph.nodes:
        neighbors = list(updated_graph.neighbors(node))
        if neighbors:
            neighbor_sentiments = [updated_graph.nodes[n]['sentiment'] for n in neighbors]
            positive_count = sum(1 for s in neighbor_sentiments if s == 'positive')
            negative_count = len(neighbor_sentiments) - positive_count
            # Update sentiment based on majority
            updated_graph.nodes[node]['sentiment'] = 'positive' if positive_count > negative_count else 'negative'
    return updated_graph

# Example Usage
if _name_ == "_main_":
    # Create a sample graph with diverse movie reviews
    G = nx.Graph()
    nodes = [
        (1, {"text": "This movie was absolutely fantastic! Great acting and a gripping story."}),
        (2, {"text": "I was so disappointed by this film. It was slow and boring."}),
        (3, {"text": "The cinematography was stunning, but the plot felt predictable."}),
        (4, {"text": "An incredible experience! I loved every minute of this movie."}),
        (5, {"text": "The movie dragged on and lacked any real excitement."}),
        (6, {"text": "A masterpiece! The characters were so well-developed."}),
    ]
    G.add_nodes_from(nodes)

    model_path = 'sentiment_rnn_model.h5'
    tokenizer_path = 'tokenizer.pickle'

    try:
        # Perform sentiment analysis
        G_with_sentiments = perform_sentiment_analysis(G, model_path, tokenizer_path, max_length)
        # Add similarity edges
        G_with_edges = add_similarity_edges(G_with_sentiments)
        # Propagate sentiments
        G_final = propagate_sentiments(G_with_edges)

        # Print results
        print("\nSentiment Analysis Results (After Propagation):")
        for node in G_final.nodes(data=True):
            print(f"Node {node[0]}: Text='{node[1]['text']}', Sentiment='{node[1]['sentiment']}'")

        print("\nEdges (Similarity Relationships):")
        for edge in G_final.edges(data=True):
            print(f"Edge {edge[0]}–{edge[1]}: Similarity={edge[2]['weight']:.2f}")

        # Visualize the network graph
        plt.figure(figsize=(12, 10))
        pos = nx.spring_layout(G_final, k=0.9, iterations=100)  # Improved layout
        node_colors = ['green' if G_final.nodes[n]['sentiment'] == 'positive' else 'red' for n in G_final.nodes]
        node_sizes = [1000 for _ in G_final.nodes]

        # Draw nodes
        nx.draw_networkx_nodes(G_final, pos, node_color=node_colors, node_size=node_sizes, alpha=0.8)
        # Draw node labels (just node IDs)
        nx.draw_networkx_labels(G_final, pos, labels={n: str(n) for n in G_final.nodes}, font_size=12, font_weight='bold')
        # Draw edges
        edge_weights = [G_final[u][v]['weight'] * 3 for u, v in G_final.edges()]
        nx.draw_networkx_edges(G_final, pos, width=edge_weights, edge_color='gray', alpha=0.6)
        # Draw edge labels
        edge_labels = nx.get_edge_attributes(G_final, 'label')
        nx.draw_networkx_edge_labels(G_final, pos, edge_labels=edge_labels, font_size=8)

        # Add legend
        legend_labels = {n: f"Node {n}: {G_final.nodes[n]['text']} (Sentiment: {G_final.nodes[n]['sentiment']})" for n in G_final.nodes}
        plt.text(1.05, 0.5, '\n'.join(legend_labels.values()), transform=plt.gca().transAxes, fontsize=10, verticalalignment='center', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

        plt.title("Network Graph with Sentiment Analysis and Similarity Relationships", fontsize=14)
        plt.axis('off')
        plt.tight_layout()
        plt.show()

    except FileNotFoundError as e:
        print(f"Error: Could not find model or tokenizer file. {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
        
******************************************************************************************
        """
        print(code)
        
    def displaybi(self):
        code = """
        2. ETL:

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel("Ecommerce+Sales+Data.xlsx", sheet_name = 0)
df

df['OrderDate'] = pd.to_datetime(df['OrderDate'], errors = 'coerce')

nulls_before = df.isnull().sum()
rows_before = len(df)
nulls_before

df_clean = df.dropna()
df_clean


nulls_after = df_clean.isnull().sum()
rows_after = len(df_clean) 
rows_after

df_clean.isnull().sum()

df_clean.to_csv('clean_ecommerce_data.csv', index = 'False')


stages = ['Extracted','After Transform','Loaded']
record_counts = [rows_before, rows_after, rows_after]

plt.figure(figsize = (8,5))
plt.bar(stages, record_counts)
plt.title('ETL Process record flow')
plt.ylabel('Number of Records')
plt.grid(axis = 'y', linestyle = '--', alpha  = 0.6)
plt.ylim(0, rows_before+1000)


for i, count in enumerate(record_counts):
    plt.text(i, count + 200, f"{count:,}", ha = 'center',fontsize = 10)
    
plt.tight_layout()
plt.show()

************************************************************************************************

5. Classification:

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import StandardScaler, LabelEncoder

df = pd.read_csv('titanic.csv')
df

df.head()
df.tail()

df.isnull().sum()

sns.countplot(data=df, x='Survived',hue='Sex')
plt.title("Survival count by Gender")
plt.show()

df.drop(columns=['Name','PassengerId','Cabin','Ticket'], inplace = True)

df.isnull().sum()

df['Age'].fillna(df['Age'].median(), inplace = True)
df['Embarked'].fillna(df['Embarked'].mode()[0],inplace = True)

df['Sex'] = LabelEncoder().fit_transform(df['Sex'])

df = pd.get_dummies(df, columns = ['Embarked'], drop_first = True)

df['FamilySize'] = df['SibSp'] + df['Parch'] + 1
df.drop(columns = ['SibSp','Parch'], inplace = True)

X = df.drop('Survived',axis = 1)
y = df['Survived']
X_train,X_test,y_train,y_test = train_test_split(X,y, test_size = 0.2, random_state = 42)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)


logistic = LogisticRegression()
logistic.fit(X_train,y_train)

y_pred = logistic.predict(X_test)

classification = classification_report(y_test,y_pred)
print(classification)

accuracy = accuracy_score(y_test,y_pred)
print(accuracy)

from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
cm = confusion_matrix(y_test, y_pred)

disp = ConfusionMatrixDisplay(confusion_matrix=cm)
disp.plot(cmap=plt.cm.Blues)
plt.title('Confusion Matrix')
plt.show()

************************************************************************************************

6. Clustering:

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.cluster import KMeans

df = pd.read_csv('iris.csv')
df

df['Species'].unique()

X = df.drop('Species', axis = 1)
y = df['Species']

sns.pairplot(X)
plt.show()

plt.figure(figsize=(8,6))
corr = X.corr()
sns.heatmap(corr, annot = True)
plt.show()

wcss = []
for k in range(1, 11):
    km = KMeans(n_clusters = k, init = 'k-means++', max_iter =300, n_init = 100, random_state = 42 )
    km.fit(X)
    wcss.append(km.inertia_)
    print(f"k: {k}, wcss: {km.inertia_}")

plt.plot(range(1, 11), wcss, color = 'red', marker = 'o')
plt.axvline(x=3, ls = '--')
plt.title('Elbow Method')
plt.xlabel('No of clusters')
plt.ylabel('wcss')
plt.show()

optimal_k = 3
km = KMeans(n_clusters = optimal_k, n_init = 100, random_state = 42)
y_pred = km.fit_predict(X)


sns.scatterplot(x = X['SepalLengthCm'], y = X['PetalWidthCm'], hue = y)
plt.title('Classes before clustering')
plt.show()


sns.scatterplot(x = X['SepalLengthCm'], y = X['PetalWidthCm'], hue = y_pred,palette = 'viridis')
plt.title('Classes before clustering')
plt.show()





        """
        print(code)