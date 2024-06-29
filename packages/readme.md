# Conda Environment

The game may not work if you don't have the correct version of Python installed. To ensure compatibility, you can create a Conda environment with the required Python version and dependencies.

To create a Conda environment with Python 3.12, you can follow these steps:

Make sure you have Conda installed on your system. If not, you can download and install Miniconda or Anaconda from the official website.

1. Open your terminal or command prompt.
2. Run the following command to create a new Conda environment named "trashfall" with Python 3.12:

    ```
    conda create -n trashfall python=3.12
    ```

3. Activate the newly created environment by running the following command:

    ```
    conda activate trashfall
    ```

4. You can now install any Python packages with:

    ```
    pip install -r requirements.txt
    ```

5. To deactivate the environment, simply run:

    ```
    conda deactivate
    ```