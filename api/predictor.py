import joblib
import pandas as pd
import numpy as np
import json
import os
import re # For sanitizing feature names when loading
from django.conf import settings # Or define BASE_DIR directly

# --- Define Paths ---
MODEL_DIR = os.path.join(settings.BASE_DIR, 'api', 'trained_model')
MODEL_PATH = os.path.join(MODEL_DIR, 'full_engineered_model.joblib')
SCALER_PATH = os.path.join(MODEL_DIR, 'scaler_full.joblib')
ENCODER_PATH = os.path.join(MODEL_DIR, 'encoder_full.joblib')
FEATURES_PATH = os.path.join(MODEL_DIR, 'full_feature_names_sanitized.json')

# --- Load Objects ---
try:
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    encoder = joblib.load(ENCODER_PATH)
    with open(FEATURES_PATH, 'r') as f:
        # These are the sanitized feature names in the correct order
        FINAL_FEATURE_ORDER_SANITIZED = json.load(f)
    print("ML objects for full model loaded successfully.")
except FileNotFoundError as e:
    print(f"Error loading ML objects: {e}. Ensure files are in {MODEL_DIR}")
    model = None; scaler = None; encoder = None; FINAL_FEATURE_ORDER_SANITIZED = []
except Exception as e:
     print(f"An unexpected error occurred loading ML objects: {e}")
     model = None; scaler = None; encoder = None; FINAL_FEATURE_ORDER_SANITIZED = []

# --- Define Feature Lists Needed for Preprocessing ---
# These lists should match the ones used *before* sanitization in the training script
# Base features
BASE_NUMERICAL_COLS = ['age_1', 'age_2']
BASE_CATEGORICAL_COLS = ['gender_1', 'gender_2']
# Importance scores 
IMPORTANCE_COLS = [
    'age_importance_1', 'age_importance_2', 'degree_importance_1', 'degree_importance_2',
    'children_importance_1', 'children_importance_2', 'ethnicity_importance_1', 'ethnicity_importance_2',
    'politics_importance_1', 'politics_importance_2', 'religion_importance_1', 'religion_importance_2',
    'height_importance_1', 'height_importance_2'
]
# Other categorical for encoding/similarity
OTHER_CATEGORICAL_COLS = [
    'degree_1', 'degree_2', 'children_1', 'children_2',
    'relationship_status_1', 'relationship_status_2', 'politics_1', 'politics_2',
    'religion_1', 'religion_2', 'substances_alcohol_1', 'substances_alcohol_2',
    'substances_cannabis_1', 'substances_cannabis_2', 'substances_nicotine_1', 'substances_nicotine_2'
]
# For age preference engineering
AGE_LOWER_BOUND_COLS = ['age_expected_lower_bound_1', 'age_expected_lower_bound_2']
AGE_UPPER_BOUND_COLS = ['age_expected_upper_bound_1', 'age_expected_upper_bound_2']

# Combine lists for easier processing
ALL_INITIAL_NUMERICAL = sorted(list(set(BASE_NUMERICAL_COLS + IMPORTANCE_COLS)))
ALL_INITIAL_CATEGORICAL = sorted(list(set(BASE_CATEGORICAL_COLS + OTHER_CATEGORICAL_COLS)))
AGE_BOUND_COLS = AGE_LOWER_BOUND_COLS + AGE_UPPER_BOUND_COLS

# List of numerical features AFTER engineering but BEFORE sanitization/scaling
# This list is used to select columns for the scaler
# It must exactly match the `final_numerical_features` list from Step 7 of the training script
FINAL_NUMERICAL_FEATURES_ORIGINAL = [
    'age1_in_p2_range', 'age2_in_p1_range', 'age_1', 'age_2', 'age_diff',
    'age_importance_1', 'age_importance_2', 'children_importance_1', 'children_importance_2',
    'degree_importance_1', 'degree_importance_2', 'ethnicity_importance_1', 'ethnicity_importance_2',
    'height_importance_1', 'height_importance_2', 'politics_importance_1', 'politics_importance_2',
    'religion_importance_1', 'religion_importance_2', 'same_alcohol', 'same_cannabis',
    'same_children', 'same_degree', 'same_gender', 'same_nicotine', 'same_politics',
    'same_relationship_status', 'same_religion'
]
# List of categorical features BEFORE encoding
# Must match `final_categorical_features` from Step 7 of the training script
FINAL_CATEGORICAL_FEATURES_ORIGINAL = [
    'children_1', 'children_2', 'degree_1', 'degree_2', 'gender_1', 'gender_2',
    'politics_1', 'politics_2', 'relationship_status_1', 'relationship_status_2',
    'religion_1', 'religion_2', 'substances_alcohol_1', 'substances_alcohol_2',
    'substances_cannabis_1', 'substances_cannabis_2', 'substances_nicotine_1', 'substances_nicotine_2'
]


def preprocess_single_pair_full(profile1: dict, profile2: dict) -> pd.DataFrame:
    """
    Preprocesses raw profile data for ONE pair using the FULL feature set.
    Args:
        profile1: Dict for user 1. Must contain keys for ALL needed features.
        profile2: Dict for user 2. Must contain keys for ALL needed features.
    Returns:
        Pandas DataFrame with one row, preprocessed and ordered features.
    Raises:
        ValueError if expected keys are missing or preprocessing fails.
        RuntimeError if ML objects aren't loaded.
    """
    if not all([scaler, encoder, FINAL_FEATURE_ORDER_SANITIZED]):
        raise RuntimeError("ML preprocessing objects not loaded.")

    # --- 1. Create DataFrame from Input Dicts ---
    # Extract all potentially needed fields, adding _1 and _2 suffixes
    data = {}
    all_needed_keys = set( # Get unique base keys needed
        [k[:-2] for k in ALL_INITIAL_NUMERICAL + ALL_INITIAL_CATEGORICAL + AGE_BOUND_COLS if k.endswith('_1')] +
        [k[:-2] for k in ALL_INITIAL_NUMERICAL + ALL_INITIAL_CATEGORICAL + AGE_BOUND_COLS if k.endswith('_2')]
    )
    try:
        for key in all_needed_keys:
            data[f"{key}_1"] = profile1.get(key) # Use .get() for safety
            data[f"{key}_2"] = profile2.get(key)
    except Exception as e:
         raise ValueError(f"Error extracting data from profile dicts: {e}")

    input_df = pd.DataFrame([data])

    # --- 2. Handle NaNs (Must mirror training Step 5 exactly) ---
    # Numerical
    for col in ALL_INITIAL_NUMERICAL:
        if col in input_df.columns:
            input_df[col] = pd.to_numeric(input_df[col], errors='coerce')
            if input_df[col].isnull().any():
                if col in IMPORTANCE_COLS: fill_value = 0
                else: fill_value = 30 # Use a reasonable default/precalculated median for age etc.
                input_df[col] = input_df[col].fillna(fill_value)
            input_df[col] = input_df[col].astype(float)

    # Categorical
    for col in ALL_INITIAL_CATEGORICAL:
        if col in input_df.columns:
            if input_df[col].isnull().any(): input_df[col] = input_df[col].fillna('Unknown')
            input_df[col] = input_df[col].astype(str)

    # Age Bounds
    for col in AGE_BOUND_COLS:
         if col in input_df.columns:
            input_df[col] = pd.to_numeric(input_df[col], errors='coerce')
            if col in AGE_LOWER_BOUND_COLS: default_fill = 18
            else: default_fill = 99
            input_df[col] = input_df[col].fillna(default_fill).astype(int)

    # --- 3. Engineer Features (Must mirror training Step 6 exactly) ---
    # Assign results directly to the DataFrame row
    row = input_df.iloc[0] # Get the single row
    input_df['age_diff'] = abs(row['age_1'] - row['age_2']) if 'age_1' in row and 'age_2' in row else 0
    input_df['same_gender'] = 1 if ('gender_1' in row and 'gender_2' in row and row['gender_1'] == row['gender_2']) else 0
    input_df['age1_in_p2_range'] = 1 if ('age_1' in row and 'age_expected_lower_bound_2' in row and 'age_expected_upper_bound_2' in row and row['age_expected_lower_bound_2'] <= row['age_1'] <= row['age_expected_upper_bound_2']) else 0
    input_df['age2_in_p1_range'] = 1 if ('age_2' in row and 'age_expected_lower_bound_1' in row and 'age_expected_upper_bound_1' in row and row['age_expected_lower_bound_1'] <= row['age_2'] <= row['age_expected_upper_bound_1']) else 0

    similarity_pairs = [('alcohol', 'substances_alcohol_1', 'substances_alcohol_2'), ('cannabis', 'substances_cannabis_1', 'substances_cannabis_2'), ('nicotine', 'substances_nicotine_1', 'substances_nicotine_2'), ('degree', 'degree_1', 'degree_2'), ('children', 'children_1', 'children_2'), ('relationship_status', 'relationship_status_1', 'relationship_status_2'), ('politics', 'politics_1', 'politics_2'), ('religion', 'religion_1', 'religion_2')]
    for name, col1, col2 in similarity_pairs:
        feature_name = f'same_{name}'
        input_df[feature_name] = 1 if (col1 in row and col2 in row and row[col1] == row[col2] and row[col1] != 'Unknown') else 0

    # --- 4. Select Features for Encoding/Scaling ---
    # Use the exact lists defined above based on training script
    numerical_cols_for_scaling = [col for col in FINAL_NUMERICAL_FEATURES_ORIGINAL if col in input_df.columns]
    categorical_cols_for_encoding = [col for col in FINAL_CATEGORICAL_FEATURES_ORIGINAL if col in input_df.columns]

    # --- 5. Apply Encoding ---
    if categorical_cols_for_encoding:
        cat_data_to_encode = input_df[categorical_cols_for_encoding]
        encoded_cats_array = encoder.transform(cat_data_to_encode)
        # Get feature names from the loaded encoder
        encoded_feature_names = encoder.get_feature_names_out(categorical_cols_for_encoding)
        encoded_cats_df = pd.DataFrame(encoded_cats_array, columns=encoded_feature_names)
    else:
        encoded_cats_df = pd.DataFrame()

    # --- 6. Apply Scaling ---
    if numerical_cols_for_scaling:
        num_data_to_scale = input_df[numerical_cols_for_scaling]
        scaled_nums_array = scaler.transform(num_data_to_scale)
        # Use the original numerical feature names here
        scaled_nums_df = pd.DataFrame(scaled_nums_array, columns=numerical_cols_for_scaling)
    else:
        scaled_nums_df = pd.DataFrame()

    # --- 7. Combine and Sanitize Feature Names ---
    combined_df = pd.concat([scaled_nums_df.reset_index(drop=True), encoded_cats_df.reset_index(drop=True)], axis=1)

    # Sanitize column names to match the saved list format
    combined_df.columns = [re.sub(r'[\[\]{}:",><]', '_', str(col)) for col in combined_df.columns]

    # --- 8. Reorder and Fill Missing Columns ---
    # Create an empty DataFrame with the final sanitized order
    final_ordered_df = pd.DataFrame(columns=FINAL_FEATURE_ORDER_SANITIZED)
    # Concatenate, which aligns columns and fills missing ones with NaN
    final_ordered_df = pd.concat([final_ordered_df, combined_df], axis=0).fillna(0)
    # Select columns in the exact order
    final_ordered_df = final_ordered_df[FINAL_FEATURE_ORDER_SANITIZED]
    # Ensure only one row (take the last one which has the data)
    final_ordered_df = final_ordered_df.iloc[[-1]]

    # Final check for NaNs before returning
    if final_ordered_df.isnull().any().any():
         nan_cols = final_ordered_df.columns[final_ordered_df.isnull().any()].tolist()
         raise ValueError(f"NaNs detected in final preprocessed data for prediction in columns: {nan_cols}")

    return final_ordered_df


def predict_match_probability_full(profile1: dict, profile2: dict) -> float:
    """
    Predicts match probability using the full feature engineered model.
    """
    if not model:
        print("Error: Full model not loaded.")
        return -1.0

    try:
        processed_features = preprocess_single_pair_full(profile1, profile2)
        probability = model.predict_proba(processed_features)[0, 1]
        return float(probability)
    except ValueError as e:
         print(f"Error during preprocessing (full): {e}")
         return -1.0
    except Exception as e:
        print(f"An error occurred during prediction (full): {e}")
        return -1.0

# --- Example Usage ---
# if __name__ == '__main__':
#     # IMPORTANT: These dicts MUST contain ALL keys needed for the features
#     # defined in ALL_INITIAL_NUMERICAL, ALL_INITIAL_CATEGORICAL, AGE_BOUND_COLS
#     sample_profile_1 = {
#         'age': 30, 'gender': 'Man', 'degree': 'BA/BS', 'children': 'Unknown',
#         'relationship_status': 'Single', 'politics': 'Moderate', 'religion': "['Christian']",
#         'substances_alcohol': 'Occasionally', 'substances_cannabis': 'Never', 'substances_nicotine': 'Never',
#         'age_importance': 3, 'degree_importance': 2, 'children_importance': 1, 'ethnicity_importance': 0,
#         'politics_importance': 1, 'religion_importance': 2, 'height_importance': 1,
#         'age_expected_lower_bound': 28, 'age_expected_upper_bound': 35
#         # ... add ALL other needed keys ...
#     }
#     sample_profile_2 = {
#         'age': 28, 'gender': 'Woman', 'degree': 'Advanced degree', 'children': 'Yes, definitely',
#         'relationship_status': 'Single', 'politics': 'Slightly liberal', 'religion': "['Spiritual']",
#         'substances_alcohol': 'Rarely', 'substances_cannabis': 'Rarely', 'substances_nicotine': 'Never',
#         'age_importance': 4, 'degree_importance': 3, 'children_importance': 5, 'ethnicity_importance': 1,
#         'politics_importance': 2, 'religion_importance': 3, 'height_importance': 2,
#         'age_expected_lower_bound': 29, 'age_expected_upper_bound': 38
#         # ... add ALL other needed keys ...
#     }
#
#     # Ensure the keys in sample_profile match the expected keys in preprocess_single_pair_full
#     # You might need to adjust the example dicts significantly based on your actual profile data structure
#
#     prob = predict_match_probability_full(sample_profile_1, sample_profile_2)
#     if prob >= 0: print(f"Predicted probability (full features): {prob:.4f}")
#     else: print("Prediction failed (full features).")

