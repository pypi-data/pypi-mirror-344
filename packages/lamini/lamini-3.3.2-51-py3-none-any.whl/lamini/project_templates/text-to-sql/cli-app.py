import subprocess
import os
import sys
import yaml
from prettytable import PrettyTable
import pandas as pd 
import time
from pathlib import Path
from tqdm import tqdm
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
import shutil
from models.project.projectdb import ProjectDB
import json
import re

# Add the parent directory (factual_qa_pipeline/) to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, '..'))

if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from utils.utils import clean_pycache

# Global to hold whatever project the user last selected/created/activated
current_project = None
current_experiment = None
try:
    df_exp = pd.read_parquet('local-db/experiments.parquet')
    df_proj = pd.read_parquet('local-db/projects.parquet')
    list_projects=df_proj['project_name'].to_list()
except Exception as e:
    db = ProjectDB()
    df_exp = pd.read_parquet('local-db/experiments.parquet')
    df_proj = pd.read_parquet('local-db/projects.parquet')
    list_projects=df_proj['project_name'].to_list()

def update_yml(project_name, yml_type, param, value):
    """
    Update a value in a YAML file using a colon-separated path.
    
    Args:
        project_name (str): Name of the project
        yml_type (str): Type of yml file to update (e.g., 'experiment', 'project')
        param (str): Colon-separated path to the parameter (e.g., 'parent:child1:child2')
        value: Value to set
    
    Example:
    """
    # Load the YAML file
    yml_path = os.path.join(Path(__file__).parent, 'projects', project_name, 'ymls', f'{yml_type}.yml')
    with open(yml_path, 'r') as file:
        loaded_yml = yaml.safe_load(file)
    
    # Split the parameter path
    path_parts = param.split(':')
    
    # Navigate to the nested location
    current = loaded_yml
    for i, part in enumerate(path_parts[:-1]):  # All parts except the last one
        if part not in current:
            raise KeyError(f"Path '{':'.join(path_parts[:i+1])}' not found in {yml_type}.yml")
        current = current[part]
    
    # Set the value at the final location
    last_part = path_parts[-1]
    if last_part not in current:
        raise KeyError(f"Final key '{last_part}' not found in {yml_type}.yml")
    current[last_part] = value
    
    # Save the updated YAML
    with open(yml_path, 'w') as file:
        yaml.dump(loaded_yml, file, default_flow_style=False)

def print_banner():
    print("=" * 100)
    print(" Welcome to the Lamini CLI ".center(100, " "))
    print(" Text-2-sql ".center(100, " "))
    if current_project:
        # show the active project on its own line, centered
        header = f"Active project: {current_project}"
        print(header.center(100, " "))
    if current_experiment:
        # show the active experiment on its own line, centered
        exp_header = f"Active experiment: {current_experiment}"
        print(exp_header.center(100, " "))
    print("=" * 100)
    
def print_options():
    print("\nPlease choose an option from the following tasks:")
    print("  [1] Start a new project")
    print("  [2] Update an existing project with the latest configurations")
    print("  [3] Activate an existing project for local use")
    print("  [4] Analyze generated data")
    print("  [q] Quit")
    print("=" * 100)

def display_dataframe_as_table(df, title):
    """Display a pandas DataFrame as a prettytable in the CLI with truncated data for readability"""
    MAX_WIDTH = 30  # Maximum width for any column
    
    table = PrettyTable()
    table.title = title
    table.field_names = df.columns.tolist()
    
    # Set max width for all columns
    for column in df.columns:
        table.max_width[column] = MAX_WIDTH
    
    # Function to truncate text
    def truncate_text(text):
        if isinstance(text, str) and len(text) > MAX_WIDTH:
            return text[:MAX_WIDTH-3] + "..."
        return text
    
    # Add rows with truncated values
    for _, row in df.iterrows():
        truncated_row = [truncate_text(val) for val in row.tolist()]
        table.add_row(truncated_row)
    
    print(table)

def load_jsonl_to_parquet(jsonl_path, parquet_path, description):
    """Load data from a JSONL file into a Parquet file."""
    try:
        with open(jsonl_path, 'r') as f:
            data = [json.loads(line) for line in f]
        df = pd.DataFrame(data)
        df.to_parquet(parquet_path, index=False)
        print(f"Loaded {description} from {jsonl_path} into {parquet_path}")
    except Exception as e:
        print(f"Error loading {description}: {str(e)}")

def main():
    global current_project, current_experiment

    clean_pycache()
    # Initialize the database
    db = ProjectDB()

    

    def load_jsonl_to_parquet_with_project_id(jsonl_path, parquet_path, description, project_id):
        """Load data from a JSONL file into a Parquet file with project_id."""
        try:
            with open(jsonl_path, 'r') as f:
                data = [json.loads(line) for line in f]
            df = pd.DataFrame(data)
            df['project_id'] = project_id  # Add project_id to the DataFrame
            df.to_parquet(parquet_path, index=False)
            print(f"Loaded {description} from {jsonl_path} into {parquet_path}")
        except Exception as e:
            print(f"Error loading {description}: {str(e)}")

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print_banner()
        print_options()
        df_exp = pd.read_parquet('local-db/experiments.parquet')
        df_proj = pd.read_parquet('local-db/projects.parquet')
        list_projects=df_proj['project_name'].to_list()

        choice = input("Enter your choice [1/2/3/4/q]: ").strip()
        if choice == 'q':
            print("\nExiting CLI. Goodbye!")
            break

        if choice not in ['1', '2', '3', '4']:
            print("\nInvalid choice. Try again.")
            input("Press Enter to continue...")
            continue
        

        if choice == '1':
            project_completer = WordCompleter(
            list_projects,
            ignore_case=True,
            sentence=True
            )

            project_name = prompt(
                "Enter project name: ",
                completer=project_completer
            ).strip()

            if project_name in list_projects:
                print('Project already exists use option 3 to make it active.')
                for _ in tqdm(range(50), bar_format='{bar}'):
                    time.sleep(0.1)
            else:
                print(f"🆕  Creating new project “{project_name}”")
                    
                print("=" * 100)
                if not project_name:
                    print("\nProject name cannot be empty. Try again.")
                    input("Press Enter to continue...")
                    continue

                
                if 'LAMINI_API_KEY' not in os.environ:
                    print("\nLAMINI_API_KEY environment variable is missing.")
                    while 'LAMINI_API_KEY' not in os.environ:
                        api_key = input("Please enter your LAMINI_API_KEY: ").strip()
                        if api_key:
                            os.environ['LAMINI_API_KEY'] = api_key
                            os.system('cls' if os.name == 'nt' else 'clear')
                            print_banner()
                            break
                        else:
                            print("API key cannot be empty. Please try again.")

                # Get SQLite database path from user
                sqlite_db_path = input("Enter the path to your SQLite database: ").strip()
                if not os.path.isfile(sqlite_db_path):
                    print("Invalid path. Please ensure the file exists.")
                    return

                # Copy the SQLite database to the project folder
                project_db_path = os.path.join(Path(__file__).parent, 'projects', project_name, 'data', os.path.basename(sqlite_db_path))
                os.makedirs(os.path.dirname(project_db_path), exist_ok=True)
                shutil.copy(sqlite_db_path, project_db_path)
                print(f"SQLite database copied to {project_db_path}")

                subprocess.run(["python", "main_scripts/init_project.py", "--project_name", project_name])
                with open(os.path.join(Path(__file__).parent,'projects',project_name,'ymls','experiment.yml'), 'r') as file:
                    exp_file = yaml.safe_load(file)
                with open(os.path.join('projects',project_name,'ymls','project.yml'), 'r') as file:
                    project_file = yaml.safe_load(file)
                
                project_file['Project']['project_name']=project_name
                project_file['Lamini']['api_key']=os.environ['LAMINI_API_KEY'] 

                
                with open(os.path.join('projects',project_name,'ymls','project.yml'), 'w') as file:
                    yaml.dump(project_file, file)
                
                print(f"\nProject '{project_name}' is set up in the 'projects' folder. Please feel free to adjust YML files as needed.")
                # Prompt for glossary and refset JSONL files
                glossary_jsonl_path = input("Enter the path to the glossary JSONL file: ").strip()
                refset_jsonl_path = input("Enter the path to the refset JSONL file: ").strip()
                # Prompt for evaluation set JSONL file
                evalset_jsonl_path = input("Enter the path to the evaluation set JSONL file: ").strip()
                # Load glossary and refset into Parquet files
                glossary_parquet_path = os.path.join(db.base_dir, "glossary.parquet")
                refset_parquet_path = os.path.join(db.base_dir, "refset.parquet")
                evalset_parquet_path = os.path.join(db.base_dir, "evalset.parquet")
                
                load_jsonl_to_parquet_with_project_id(glossary_jsonl_path, glossary_parquet_path, "glossary", project_name)
                load_jsonl_to_parquet_with_project_id(refset_jsonl_path, refset_parquet_path, "refset", project_name)
                load_jsonl_to_parquet_with_project_id(evalset_jsonl_path, evalset_parquet_path, "evalset", project_name)
                print("\nParquet files created. Restarting CLI to pick up new data...")
                time.sleep(1)
                os.execv(sys.executable, [sys.executable] + sys.argv)
                
        elif choice == '2':

            project_completer = WordCompleter(
            list_projects,
            ignore_case=True,
            sentence=True
            )

            project_name = prompt(
                "Enter project name: ",
                completer=project_completer
            ).strip()

            if not project_name:
                print("\nProject name cannot be empty. Try again.")
                input("Press Enter to continue...")
                continue

            if project_name not in list_projects:
                print(f"\nProject “{project_name}” does not exist. Returning to the main menu.")
                for _ in tqdm(range(50), bar_format='{bar}'):
                    time.sleep(0.1)
                continue

            print(f"✅  Using existing project “{project_name}”")
            print("=" * 100)

            subprocess.run(["python", "main_scripts/init_project.py", "--project_name", project_name, "--update"])
        
        elif choice == '3':
            project_completer = WordCompleter(
            list_projects,
            ignore_case=True,
            sentence=True
            )

            project_name = prompt(
                "Enter project name: ",
                completer=project_completer
            ).strip()

            if not project_name:
                print("\nProject name cannot be empty. Try again.")
                input("Press Enter to continue...")
                continue

            if project_name not in list_projects:
                print(f"\nProject “{project_name}” does not exist. Returning to the main menu.")
                for _ in tqdm(range(50), bar_format='{bar}'):
                    time.sleep(0.1)
                continue
            
            print(f"✅  Using existing project “{project_name}”")
            print("=" * 100)
            
            # Use a regular expression to remove trailing digits
            project_name_org = re.sub(r'\d{1,2}$', '', project_name)

            with open(os.path.join(Path(__file__).parent,'projects',project_name_org,'ymls','experiment.yml'), 'r') as file:
                exp_file = yaml.safe_load(file)

            if not os.path.exists(os.path.join('projects', project_name_org)):
                print(f"\nProject '{project_name_org}' does not exist. Returning to the main menu.")
                for _ in tqdm(range(50), bar_format='{bar}'):
                    time.sleep(0.1)
                continue
            
            if 'LAMINI_API_KEY' not in os.environ:
                with open(os.path.join('projects',project_name_org,'ymls','project.yml'), 'r') as file:
                    project_file = yaml.safe_load(file)
                os.environ['LAMINI_API_KEY']=project_file['Lamini']['api_key'] 
                
            while True:
                os.system('cls' if os.name == 'nt' else 'clear')
                print_banner()
                print("=" * 100)
                print("\nWhat would you like to do with the activated project?")
                print("  [d] Perform data generation")
                print("  [t] Tune the model")
                print("  [i] Run inference")
                print("  [m] Monitor project data")
                print("  [e] Evaluate model performance")
                print("  [a] Analyze generated data")
                print("  [r] Return to main menu")
                print("  [q] Quit")
                print("=" * 100)
                
                action_choice = input("Enter your choice [d/t/i/m/e/a/r/q]: ").strip().lower()
                if action_choice not in ['d', 't', 'i', 'm', 'e', 'a', 'r', 'q']:
                    print("\nInvalid choice. Try again.")
                    input("Press Enter to continue...")
                    continue
                
                if action_choice == 'd':
                    print("\nPerforming data generation...")
                    print("="*100)
                    print("\n Please make sure that PDFs are loaded into your project folder inside data folder!")
                    print("="*100)
                    filtered_df_exp = df_exp[df_exp['project_id'] == project_name_org]
                    list_experiments=filtered_df_exp['experiment_name'].to_list()
                    while True:
                        experiment_completer = WordCompleter(
                            list_experiments,
                            ignore_case=True,
                            sentence=True
                        )

                        experiment_name = prompt(
                            "Enter experiment name: ",
                            completer=experiment_completer
                        ).strip()

                        if experiment_name in list_experiments:
                            print(f"❌  Experiment name '{experiment_name}' already exists. Please try another.")
                        else:
                            print(f"🆕  Creating new experiment '{experiment_name}'")
                            break  # Exit the loop if a unique experiment name is entered
                        
                    current_experiment = experiment_name
    
                    
                    exp_file['Experiment']['experiment_name']['value']=experiment_name
                    with open(os.path.join(Path(__file__).parent,'projects',project_name,'ymls','experiment.yml'), 'w') as file:
                        yaml.dump(exp_file, file)
                    
                    pipeline_command = [
                        "python", "main_scripts/pipeline.py",
                        "--project_name", project_name,
                        "--experiment_name", experiment_name,
                    ]
                    subprocess.run(pipeline_command)
                    
                elif action_choice == 't':
                    print("\nTuning the model...")
                    while True:
                        experiment_completer = WordCompleter(
                            list_experiments,
                            ignore_case=True,
                            sentence=True
                        )

                        experiment_name = prompt(
                            "Enter experiment name: ",
                            completer=experiment_completer
                        ).strip()

                        if experiment_name not in list_experiments:
                            print(f"❌  Experiment name '{experiment_name}' does not exist. Please choose an existing experiment.")
                        else:
                            print(f"✅  Using existing experiment '{experiment_name}'")
                            current_experiment = experiment_name  # Assign within proper scope
                            break  # Exit the loop if a valid existing experiment name is entered
                    
                    output_file_path = input("Enter the output file path (optional): ").strip()
                    output_format = input("Enter the output format (choices: csv, parquet, json, default: csv): ").strip().lower()

                    if output_format not in ['csv', 'parquet', 'json']:
                        print("\nInvalid format. Defaulting to 'csv'.")
                        output_format = 'csv'

                    train_command = [
                        "python", "main_scripts/train.py",
                        "--experiment_name", experiment_name,
                        "--project_name", project_name,
                        "--format", output_format
                    ]

                    if output_file_path:
                        train_command.extend(["--output", output_file_path])

                    subprocess.run(train_command)
                elif action_choice == 'i':
                    print("\nRunning inference...")
                    eval_file_path = input("Enter the path to the evaluation JSONL data file: ").strip()
                    model_id = input("Enter the Model ID for the LLM: ").strip()
                    system_message = input("Enter the system message for the prompt (or press Enter to use default): ").strip()

                    inference_command = ["python", "main_scripts/run_inference.py", "--eval_file_path", eval_file_path, "--model_id", model_id]

                    if system_message:
                        inference_command.extend(["--system_message", system_message])
                
                    subprocess.run(inference_command)
                elif action_choice == 'm':
                    print("\nMonitoring project data...")
                    while True:
                        print("\nSelect data to monitor:")
                        print("  [1] Datasets")
                        print("  [2] Experiments")
                        print("  [3] Prompts")
                        print("  [4] Results")
                        print("  [b] Back to project menu")
                        
                        monitor_choice = input("\nEnter your choice [1/2/3/4/5/b]: ").strip().lower()
                        
                        if monitor_choice == 'b':
                            break
                            
                        try:
                            if monitor_choice == '1':
                                # Display datasets data
                                datasets_df = pd.read_parquet("local-db/datasets.parquet")
                                display_dataframe_as_table(datasets_df, "Datasets")
                            elif monitor_choice == '2':
                                # Display experiments data
                                experiments_df = pd.read_parquet("local-db/experiments.parquet")
                                display_dataframe_as_table(experiments_df, "Experiments")
                            elif monitor_choice == '3':
                                # Display prompts data
                                prompts_df = pd.read_parquet("local-db/prompts.parquet")
                                display_dataframe_as_table(prompts_df, "Prompts")
                            elif monitor_choice == '4':
                                # Display results data
                                results_df = pd.read_parquet("local-db/results.parquet")
                                display_dataframe_as_table(results_df, "Results")
                            else:
                                print("\nInvalid choice. Try again.")
                        except Exception as e:
                            print(f"\nError loading data: {str(e)}")
                        
                        input("\nPress Enter to continue...")
                elif action_choice == 'e':
                    print("\nEvaluating model performance...")
                    eval_file_path = input("Enter the path to the evaluation CSV data file: ").strip()
                    model_id = input("Enter the Model ID for the evaluation: ").strip()
                    
                    eval_command = [
                        "python", "main_scripts/evaluate.py",
                        "--eval_file_path", eval_file_path,
                        "--project_name", project_name
                    ]

                    subprocess.run(eval_command)
                    
                elif action_choice == 'a':
                    analyze_generated_data_script = os.path.join(parent_dir, 'main_scripts', 'analyze_generated_data.py')
                    subprocess.run([sys.executable, analyze_generated_data_script])
                    continue

                elif action_choice == 'r':
                    print("\nReturning to main menu...")
                    break

                elif action_choice == 'q':
                    print("\nExiting CLI. Goodbye!")
                    exit()

                input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()