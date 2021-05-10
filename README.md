# Full Stack API Final Project
This was the second project of Udacity's Full Stacks Nanodegree. In this API Development and Documentation module, I learned to: 
* Organize API Endpoints
* Handle Cross-Origin Resource Sharing (CORS)
* Parse the request path and body
* Use POST, PATCH, and DELETE requests in Flask
* Handle errors

The API documentation I developed is README_API_doc.md.

## Full Stack Trivia

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a  webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out. 

That's where you come in! Help them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. The application must:

1) Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer. 
2) Delete questions.
3) Add questions and require that they include question and answer text.
4) Search for questions based on a text query string.
5) Play the quiz game, randomizing either all questions or within a specific category. 

Completing this trivia app shows the ability to structure plan, implement, and test an API - skills essential for enabling future applications to communicate with others. 

## Starting the Project

[Fork](https://help.github.com/en/articles/fork-a-repo) the [project repository]() and [Clone](https://help.github.com/en/articles/cloning-a-repository) your forked repository to your machine. Work on the project locally and make sure to push all your changes to the remote repository before submitting the link to your repository in the Classroom. 

## About the Stack

This full stack application was desiged with some key functional areas:

### Backend

The `./backend` directory contains Flask and SQLAlchemy server. app.py contain endpoints and can reference models.py for DB and SQLAlchemy setup. 

### Frontend

The `./frontend` directory contains a complete React frontend to consume the data from the Flask server. I updated the endpoints after defining them in the backend according to expected data for each API response.

[View the README.md within ./frontend for more details.](./frontend/README.md)
