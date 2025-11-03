import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier

def train_ml_model():
    # Load dataset
    data = pd.read_csv("data/students.csv")

    # Encode categorical columns
    le_style = LabelEncoder()
    le_difficulty = LabelEncoder()

    data['learning_style_encoded'] = le_style.fit_transform(data['learning_style'])
    data['next_difficulty_encoded'] = le_difficulty.fit_transform(data['next_difficulty'])

    # Define features (X) and target (y)
    X = data[['last_score', 'learning_style_encoded']]
    y = data['next_difficulty_encoded']

    # Train the model
    clf = DecisionTreeClassifier(random_state=42)
    clf.fit(X, y)

    # Return trained model, encoders, and dataset
    return clf, (le_style, le_difficulty), data


def recommend_next_lesson(name, subject_interest, last_score, learning_style, clf, encoders):
    le_style, le_difficulty = encoders

    # Encode learning style
    encoded_style = le_style.transform([learning_style])[0]

    # Prepare input for prediction
    input_data = [[last_score, encoded_style]]
    pred_encoded = clf.predict(input_data)[0]
    predicted_difficulty = le_difficulty.inverse_transform([pred_encoded])[0]

    # Build recommendation text
    recommendation = (
        f"Hi {name}, since your last score in {subject_interest} was {last_score}, "
        f"and your learning style is {learning_style}, "
        f"the next recommended lesson difficulty is **{predicted_difficulty}**."
    )

    return recommendation
