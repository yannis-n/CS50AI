These are the projects that were implemented as part of following CS50's Artificial Intelligence from Harvard University. As stated in the course's description "CS50’s Introduction to Artificial Intelligence with Python explores the concepts and algorithms at the foundation of modern artificial intelligence, diving into the ideas that give rise to technologies like game-playing engines, handwriting recognition, and machine translation". The course touched on the following concepts:
  -graph search algorithms
  -adversarial search
  -knowledge representation
  -logical inference
  -probability theory
  -Bayesian networks
  -Markov models
  -constraint satisfaction
  -machine learning
  -reinforcement learning
  -neural networks
  -natural language processing

1. Degrees:
  In this problem, we’re interested in finding the shortest path between any two actors by choosing a sequence of movies that connects them. Thiis problem was framed as a Seach Problem in order to familirize ourselves with this kind of problems: our states are people. Our actions are movies, which take us from one actor to another. Our initial state and goal state are defined by the two people we’re trying to connect. By using breadth-first search, we can find the shortest path from one actor to another.
  
2. Tic-Tac-Toe:
  The goal of this project was to design an AI that is able to play tic-tac-toe performing the most optimal move. This was framed as an adverserial problem using Minimax.
  
3. Knights:
  Based on the book of logical puzzles published by Raymond Smullyan in 1978, "What is the name of the this book?", the project required
to draw conclusion for a puzzle of Knights and Knaves. The principle is simple: In a Knights and Knaves puzzle, the following information is given: Each character is either a knight or a knave. A knight will always tell the truth: if knight states a sentence, then that sentence is true. Conversely, a knave will always lie: if a knave states a sentence, then that sentence is false. This project required the use of knowledge-based agents and a knowledge represantation.

4. Minesweeper:
  This project required the implementation of an Ai designed to play minesweeeper in the most optimal way, achieving this by making inferences about the safety of a move and the state of the board.
 
5. Pagerank:
  In this project, we were required to emulate the evaluation of the importance of a web page. To define importance, the PageRank algorithm was created by Google’s co-founders (including Larry Page, for whom the algorithm was named). In PageRank’s algorithm, a website is more important if it is linked to by other important websites, and links from less important websites have their links weighted less. This definition seems a bit circular, but it turns out that there are multiple strategies for calculating these rankings.
  
6. Heredity:
  This project required to make inferences about a population. Given information about people, who their parents are, and whether they have a particular observable trait (e.g. hearing loss) caused by a given gene, your AI will infer the probability distribution for each person’s genes, as well as the probability distribution for whether any person will exhibit the trait in question. The relationships between parents and children and the probabilities were modelled by forming a Bayesian Network
  
7. Crossword:
  This project required the generation of a crossword puzzle. Given the structure of a crossword puzzle (i.e., which squares of the grid are meant to be filled in with a letter), and a list of words to use, the problem becomes one of choosing which words should go in each vertical or horizontal sequence of squares. This problem can be modelled as a constraint satisfaction problem. Each sequence of squares is one variable, for which we need to decide on its value (which word in the domain of possible words will fill in that sequence).
  
8. Shopping:
  In this problem we were requiored to build a nearest-neighbor classifier to solve this problem. Given information about a user — how many pages they’ve visited, whether they’re shopping on a weekend, what web browser they’re using, etc. — your classifier will predict whether or not the user will make a purchase. To train the classifier, we were provided with some data from a shopping website from about 12,000 users sessions.
  
9. Nim:
  In the game Nim, we begin with some number of piles, each with some number of objects. Players take turns: on a player’s turn, the player removes any non-negative number of objects from any one non-empty pile. Whoever removes the last object loses. By playing against itself repeatedly and learning from experience, eventually our AI will learn which actions to take and which actions to avoid. In particular, Q-learning was uded for this project. In Q-learning, we try to learn a reward value (a number) for every (state, action) pair. An action that loses the game will have a reward of -1, an action that results in the other player losing the game will have a reward of 1, and an action that results in the game continuing has an immediate reward of 0, but will also have some future reward.
  
10. Traffic:
  In this project, Tensorflow was uded too build a neural network to build a neural network to classify road signs based on an image of those signs.
  
11. Parser
  In this problem, we’ll use the context-free grammar formalism to parse English sentences to determine their structure, using the NLTK

12. Questions
  In this project we were required to create a Question Answering system that would perform two tasks: document retrieval and passage retrieval. The system has access to a corpus of text documents. When presented with a query (a question in English asked by the user), document retrieval first identifies which document(s) are most relevant to the query. Once the top documents are found, the top document(s) are be subdivided into passages (in this case, sentences) so that the most relevant passage to the question can be determined.

 
