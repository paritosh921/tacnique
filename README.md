# Chat Assistant for SQLite Database

Welcome to the Chat Assistant project! This application allows users to interact with an SQLite database using natural language queries. The chat assistant translates the user’s questions into SQL queries and fetches the relevant data from the database.

## 🌟 Public URL

You can try out the live version of the chat assistant hosted on PythonAnywhere:

[**Try it now!**](https://paritosh921.pythonanywhere.com/)

## 📸 Output Images

Here are a few screenshots showcasing the application:

![Example 1](https://github.com/user-attachments/assets/863b83b8-5e75-4ea3-a174-a1a3edbdb8ac)
![Example 2](https://github.com/user-attachments/assets/6c8616c0-a635-4a02-9539-5c0d548ecc95)

## 🚀 How It Works

The chat assistant processes natural language queries and converts them into SQL commands that interact with the SQLite database. It supports various types of queries, such as:

- Show me all employees in the [department] department.
- Who is the manager of the [department] department?
- List all employees hired after [date].
- What is the total salary expense for the [department] department?

## ⚙️ Running the Project Locally

Follow these steps to run the project on your local machine:

### Step 1: Clone the Repository

Start by cloning the repository:

```bash
git clone https://github.com/paritosh921/tacnique.git
```

### Step 2: Navigate to the Project Directory

Once the repository is cloned, navigate to the project directory:

```bash
cd tacnique
```

### Step 3: Install the Required Dependencies

Install the required dependencies from the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### Step 4: Run the Flask Application

Start the Flask app by running:

```bash
python app.py
```

### Step 5: Test the Application

Make sure to test the app with different queries to ensure it handles edge cases effectively.

### Step 6: Host the Application

Once you're happy with the app locally, you can deploy it to a cloud service like Heroku, AWS, or PythonAnywhere. Don't forget to share the public URL with others!

## 💡 Additional Information

This project provides a foundational framework for building a chat assistant that interacts with an SQLite database using Flask. You can easily extend the functionality by adding more query types, improving error handling, and optimizing database interactions to suit your needs.
