# Alpha Zero General for Waldmeister
This repository showcases my implementation of the game Waldmeister, complete with its logic and an AI implementation utilizing the AlphaZero algorithm, inspired by the principles outlined in the [AlphaGo Zero paper (Silver et al)](https://github.com/suragnair/alpha-zero-general/raw/master/pretrained_models/writeup.pdf). The framework is based on the [AlphaZero framework](https://github.com/suragnair/alpha-zero-general). It offers a flexible environment for training models, enabeling competitions between different AI agents and interactive gameplay. These features make it a valuable resource for experimentation and exploration of the game Waldmeister.


## Installation
Create a virtual environment (optional but recommended):
```
# example for windows
pip install virtualenv
virtualenv venv
. .\venv\Scripts\activate
```

Install the required dependencies:
```
pip install -r requirements.txt
```
Download the pretrained model from the provided [Google Drive link](https://drive.google.com/drive/folders/16oEcaHV_uyx0HnVO-ZLlJV0Is7M6f11o?usp=sharing) or train them by yourself ('Train a Model') and place them in the ```pretrained_models/Waldmeister/pytorch``` directory. 

(Link long version: https://drive.google.com/drive/folders/16oEcaHV_uyx0HnVO-ZLlJV0Is7M6f11o?usp=sharing )

## Usage
### Training a Model
To train a model for Waldmeister, use ```main.py```. This script initiates the training loop, allowing the model to learn from self-play:
```
python main.py
```
You can customize various training parameters inside ```main.py```, such as the number of training iterations, episodes per iteration, and Monte Carlo Tree Search (MCTS) simulations per turn. Additionally, you can adjust neural network parameters like batch size, epochs, and learning rate within the ```Waldmeister/keras/NNet.py``` file.

If you want to use the best trained model in the other parts of the Repository you need to copy the ```temp/best.h5``` to the ```pretrained_models/Waldmeister/pytorch``` directory and give it a desired filename.


### Competition
You can use ```pit.py``` to let two player implementations (```Waldmeister/WaldmeisterPlayers.py``` or models compete against each other. This script enabels evaluating the performance of different models against each other. You can modify this script to adjust the competition settings, such as the number of games to play and the opponents' configurations.

The models used in this file need to exist in the ```pretrained_models/Waldmeister/pytorch``` directory.


### Playing with GUI
```PygameGui.py``` provides a graphical user interface to play the game Waldmeister. This interface allows interactive gameplay, where you can engage with different opponents in a visually appealing environment. You can choose to play against human players, saved models, a random agent, or an alpha-beta implementation, providing a versatile platform for testing and enjoyment. In addidion you can let each of these players play against each of them by themselves.

To play with a certain model in the gui the mane of the model needs to be included in the ```MODELS``` variables (sorted by boardsize) as well as the filename of the stored model in the ```pretrained_models/Waldmeister/pytorch``` directory (```["name", "filename"]```).
Example:
```
MODELS = [[["Easy", "easy5x5.h5"], ["Difficult", "difficult5x5.h5"]], # first entry in Models for  boardsize 5x5
          [],                                                         # second entry in Models for  boardsize 6x6
          [],                                                         # third entry in Models for  boardsize 7x7
          [["Easy", "easy8x8.h5"], ["Difficult", "difficult8x8.h5"]]] # fourth entry in Models for  boardsize 8x8
# MODELS is expandable and the gui loads automatically all includet models
```


### Contributing
While the current code is fairly functional, we could benefit from the following contributions:
* threading to make the PygameGui klickable while the model or AlphaBeta algortihm is calculating
* training better models with other params as described in 'Training a Model'


### Contributors and Credits
* [Shantanu Thakoor](https://github.com/ShantanuThakoor) and [Megha Jhunjhunwala](https://github.com/jjw-megha) helped with core design and implementation.
* [Abdülkerim Kilinc](https://github.com/AbdulkerimKilinc) and [Nicolas Henrich](https://github.com/Skilsu) contributed rules, gui and a trained model for Waldmeister using pair programming.
* [Evgeny Tyurin](https://github.com/evg-tyurin) contributed rules and a trained model for TicTacToe.

