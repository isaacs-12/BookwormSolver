# BookwormSolver
This houses scripts to play the game Bookworm Deluxe (2003) automatically.

Uses OpenCV to read the 53 letter tiles on a screen like below, and maps them to a graph.
![image](https://user-images.githubusercontent.com/61003769/121995121-519e9f00-cd5b-11eb-9c4f-131aa4e1aafc.png)

The graph is then traversed, and is weighted as necessary based on tile value (green, gold, diamond/blue) or urgency (fire).

Features to come:
- Smart solving to bring the board closer to, and prioritize bonus words.
