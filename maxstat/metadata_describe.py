from matplotlib import pyplot as plt

# Made with help from ChatGPT
def metadata_describe(df,drugs_of_interest=[]):
    ''' This function takes in the provided dataframe (in our case, the MEDI-prepared metacardis data)
        and it plots relavent plots describing the data, as well as outputting a dataframe 
         containing the concatinated describe functions for each column.'''
    # Store original column names for reference
    original_columns = df.columns.copy()
    # Standardize column names
    df.columns = df.columns.str.lower().str.replace(" ", "_")

    # Remove client ID column if present
    df = df.loc[:, df.nunique() > 1]
    
    # Separate categorical and numerical columns
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    # Identify binary medication columns (0/1 values)
    medication_cols = [col for col in df.select_dtypes(include=['number']).columns if df[col].nunique() == 2]
    numerical_cols = [col for col in df.select_dtypes(include=['number']).columns if col not in medication_cols]
    
    # Store descriptive statistics
    summary_df = df[numerical_cols].describe().T

    # Mapping standardized names back to original names for labeling purposes
    col_name_map = dict(zip(df.columns, original_columns.str.replace("_"," ")))

    # # Prompt user for drug of interest
    # if medication_cols:
    #     print("Available medications in dataset:")
    #     for i, med in enumerate(medication_cols, 1):
    #         print(f"{i}. {col_name_map.get(med, med)}")
        
    #     while True:
    #         try:
    #             choices = input("Select one or more drugs of interest by entering numbers separated by commas: ")
    #             selected_indices = [int(choice.strip()) for choice in choices.split(',')]
    #             if all(1 <= choice <= len(medication_cols) for choice in selected_indices):
    #                 drugs_of_interest = [medication_cols[i - 1] for i in selected_indices]
    #                 break
    #             else:
    #                 print("Invalid choice. Please select valid numbers.")
    #         except ValueError:
    #             print("Invalid input. Please enter numbers separated by commas.")
    # else:
    #     drugs_of_interest = None
    
    # Visualizations
    # Bar chart for medication usage
    medication_usage = df[medication_cols].mean() * 100
    plt.figure(figsize=(12,6))
    colors = ['crimson' if col in drugs_of_interest else 'steelblue' for col in medication_usage.index]
    medication_usage.sort_values().plot(kind='barh', color=colors, edgecolor='black', alpha=0.8)
    plt.xlabel('Percentage of Patients Taking Medication', fontsize=12)
    plt.title('Medication Usage Among Patients', fontsize=14)
    plt.xticks(rotation=0)
    plt.gca().xaxis.set_major_formatter(mticker.PercentFormatter())
    plt.yticks(ticks=range(len(medication_usage)), labels=[col_name_map.get(col, col) for col in medication_usage.index])
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.show()

    # histograms
    for col in numerical_cols:
        if col != 'id':
            plt.figure(figsize=(6,4))
            sns.histplot(df[col].dropna(), kde=True, bins=30, color="royalblue", alpha=0.7)
            plt.title(f'Distribution of {col_name_map.get(col, col)}', fontsize=14)
            plt.xlabel(col_name_map.get(col, col))
            plt.ylabel('Frequency')
            plt.grid(axis='y', linestyle='--', alpha=0.7)
            plt.show()
    # pie charts 
    for col in categorical_cols:
        if col != 'id':
            plt.figure(figsize=(6,4))
            df[col].value_counts().plot.pie(autopct='%1.1f%%', startangle=90, cmap='Set3', wedgeprops={'edgecolor': 'black'}) # cmap='Set3')
            plt.title(f'Distribution of {col_name_map.get(col, col)}', fontsize=14)
            plt.ylabel('')
            plt.show()
    
    return summary_df