import pandas as pd
import ast


def downsize_dataset(csv_file_path):
    # Load the dataset
    df = pd.read_csv(csv_file_path)

    # Convert the skills column from string to list
    df['course_skills'] = df['course_skills'].apply(ast.literal_eval)

    # Get a list of all unique skills
    all_skills = set()
    for skills in df['course_skills']:
        all_skills.update(skills)

    # Create a dictionary of skill:False
    skill_dict = {skill: False for skill in all_skills}

    # Sort the dataset by rating (assuming you have a 'rating' column)
    df = df.sort_values('course_rating', ascending=False)

    # Initialize a list to store rows to keep
    rows_to_keep = []

    # Iterate through the sorted dataframe
    for index, row in df.iterrows():
        keep_row = False
        for skill in row['course_skills']:
            if not skill_dict[skill]:
                skill_dict[skill] = True
                keep_row = True
        if keep_row:
            rows_to_keep.append(index)

    # Create a new dataframe with only the kept rows
    downsized_df = df.loc[rows_to_keep]

    return downsized_df


# Usage
csv_file_path = '/Users/ramgopalravi/ResumeAnalyzer/Server/coursera_courses_english.csv'
downsized_dataset = downsize_dataset(csv_file_path)

# Save the downsized dataset to a new CSV file
downsized_dataset.to_csv('downsized_dataset.csv', index=False)
