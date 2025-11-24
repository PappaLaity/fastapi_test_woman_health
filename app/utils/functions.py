import pickle

# Load models from disk (Model Trained and Stored by Fatima)
def load_model(path: str):
    model = None
    with open(path, "rb") as f:
        model = pickle.load(f)
    return model
