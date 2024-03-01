import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import numpy as np

def generate_sample_data(num_samples=100):
    """
    Generates a sample DataFrame for demonstration.
    """
    data = {
        'numerical_feature_1': np.random.rand(num_samples) * 100,
        'numerical_feature_2': np.random.randint(0, 50, num_samples),
        'categorical_feature_1': np.random.choice(['A', 'B', 'C'], num_samples),
        'categorical_feature_2': np.random.choice(['X', 'Y'], num_samples),
        'target': np.random.rand(num_samples) * 10
    }
    return pd.DataFrame(data)

def preprocess_data(df):
    """
    Applies standard preprocessing steps to a DataFrame.
    - Standard scaling for numerical features.
    - One-hot encoding for categorical features.

    Args:
        df (pd.DataFrame): The input DataFrame.

    Returns:
        pd.DataFrame: The preprocessed DataFrame.
        sklearn.compose.ColumnTransformer: The fitted preprocessor object.
    """
    # Identify numerical and categorical features
    numerical_features = df.select_dtypes(include=np.number).columns.tolist()
    categorical_features = df.select_dtypes(include='object').columns.tolist()

    # Remove target if present in features
    if 'target' in numerical_features:
        numerical_features.remove('target')

    # Create preprocessing pipelines for numerical and categorical features
    numerical_transformer = StandardScaler()
    categorical_transformer = OneHotEncoder(handle_unknown='ignore')

    # Create a column transformer to apply different transformations to different columns
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numerical_transformer, numerical_features),
            ('cat', categorical_transformer, categorical_features)
        ])

    # Create a pipeline that first preprocesses and then can be used with a model
    # For now, we just apply the preprocessing
    pipeline = Pipeline(steps=[('preprocessor', preprocessor)])

    # Fit and transform the data
    transformed_data = pipeline.fit_transform(df)

    # Get feature names after one-hot encoding
    # This part can be tricky with ColumnTransformer, a simpler way for demonstration:
    # num_feature_names = numerical_features
    # cat_feature_names = preprocessor.named_transformers_['cat'].get_feature_names_out(categorical_features)
    # all_feature_names = list(num_feature_names) + list(cat_feature_names)

    # For simplicity, we'll return a DataFrame without explicit column names for now
    # In a real scenario, you'd reconstruct the DataFrame with proper column names
    print(f"Data preprocessed. Shape: {transformed_data.shape}")
    return pd.DataFrame(transformed_data), preprocessor

if __name__ == "__main__":
    # Generate sample data
    sample_df = generate_sample_data(num_samples=200)
    print("Original Data Head:\n", sample_df.head())

    # Preprocess the data
    processed_df, preprocessor_obj = preprocess_data(sample_df)
    print("\nProcessed Data Head (first 5 rows, first 5 columns):\n", processed_df.iloc[:5, :5])
    print(f"\nShape of processed data: {processed_df.shape}")

    # Example of saving the preprocessor (useful for consistent preprocessing of new data)
    import joblib
    os.makedirs("models", exist_ok=True)
    joblib.dump(preprocessor_obj, "models/preprocessor.joblib")
    print("Preprocessor saved to models/preprocessor.joblib")

    # Create requirements.txt
    with open("requirements.txt", "w") as f:
        f.write("pandas\n")
        f.write("scikit-learn\n")
        f.write("numpy\n")
        f.write("joblib\n")
    print("requirements.txt created.")
