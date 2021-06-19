# BookwormSolver
This houses scripts to play the game Bookworm Deluxe (2003) automatically.

Uses OpenCV to read the 53 letter tiles on a screen like below, and maps them to a graph.
![image](https://user-images.githubusercontent.com/61003769/121995121-519e9f00-cd5b-11eb-9c4f-131aa4e1aafc.png)

Letters are individually cropped by the tile and grey-scaled. Then I max the pixel value of every pixel outside a radius of the letter, and then apply an inverse or regular binary threshold. This shows like below:

<img width="172" alt="A_test" src="https://user-images.githubusercontent.com/61003769/122630021-be74aa80-d075-11eb-8574-6ffa00237cdd.png"><img width="172" alt="Screen Shot 2021-06-18 at 8 38 16 PM" src="https://user-images.githubusercontent.com/61003769/122630012-b157bb80-d075-11eb-8036-5c1444404424.png">!<img width="172" alt="z" src="https://user-images.githubusercontent.com/61003769/122630239-398a9080-d077-11eb-896e-0327ff18af3b.png"><img width="172" alt="Screen Shot 2021-06-18 at 8 38 27 PM" src="https://user-images.githubusercontent.com/61003769/122630014-b583d900-d075-11eb-94b9-ab22820afc16.png"><img width="172" alt="Screen Shot 2021-06-18 at 8 40 10 PM" src="https://user-images.githubusercontent.com/61003769/122630019-b9aff680-d075-11eb-9c61-033d267f51b0.png">


The graph is then traversed, and is weighted as necessary based on tile value (green, gold, diamond/blue) or urgency (fire).

Features to come:
- Smart solving to bring the board closer to, and prioritize bonus words.
