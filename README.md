# BookwormSolver
This houses scripts to play the game Bookworm Deluxe (2003) automatically.

Uses OpenCV to read the 53 letter tiles on a screen like below, and maps them to a graph.
![image](https://user-images.githubusercontent.com/61003769/121995121-519e9f00-cd5b-11eb-9c4f-131aa4e1aafc.png)

**Image Recognition**

Letters are individually cropped by the tile. And to determine the letter value, I apply a custom set of filters before attempting OCR. In order to know what filter set to apply, I determine the type of tile by comparing the ratio of red:green values at a specific pixel in the background. I do this because it's very easy/fast, and performs with perfect accuracy (given fine-tuned windows for the ratios. Each filter behaves as below, totally isolating the letter into a binary image with no noticeable noise. 

For normal tiles: First I grey-scale the image. I then max the pixel value of every pixel outside a radius of the letter, and then apply a binary threshold to remove basically everything except the letter outline itself. This shows like below:

<img width="172" alt="A_test" src="https://user-images.githubusercontent.com/61003769/122630021-be74aa80-d075-11eb-8574-6ffa00237cdd.png"><img width="172" alt="Screen Shot 2021-06-18 at 8 38 16 PM" src="https://user-images.githubusercontent.com/61003769/122630012-b157bb80-d075-11eb-8036-5c1444404424.png">!<img width="172" alt="z" src="https://user-images.githubusercontent.com/61003769/122630239-398a9080-d077-11eb-896e-0327ff18af3b.png"><img width="172" alt="Screen Shot 2021-06-18 at 8 38 27 PM" src="https://user-images.githubusercontent.com/61003769/122630014-b583d900-d075-11eb-94b9-ab22820afc16.png"><img width="172" alt="Screen Shot 2021-06-18 at 8 40 10 PM" src="https://user-images.githubusercontent.com/61003769/122630019-b9aff680-d075-11eb-9c61-033d267f51b0.png">

For special tiles: I use the color images, and not greyscale. I then apply a mask based on color value using [HSV](https://en.wikipedia.org/wiki/HSL_and_HSV#/media/File:HSV_color_solid_cylinder_saturation_gray.png), to isolate only the dark black pixels of the letter, isolated from the hue of the surrounding. I invert the mask, use the same radius trick as above to get rid of noise, and then that leaves me with a pretty good letter:

<img width="164" alt="Screen Shot 2021-06-21 at 8 31 31 PM" src="https://user-images.githubusercontent.com/61003769/122859168-67b6dd00-d2d0-11eb-81c8-9dbabfe00430.png"><img width="164" alt="Screen Shot 2021-06-21 at 8 31 45 PM" src="https://user-images.githubusercontent.com/61003769/122859179-6dacbe00-d2d0-11eb-844f-c50e48f5080c.png"><img width="164" alt="Screen Shot 2021-06-21 at 8 32 00 PM" src="https://user-images.githubusercontent.com/61003769/122859201-74d3cc00-d2d0-11eb-9edd-da104a466d96.png"><img width="164" alt="Screen Shot 2021-06-21 at 8 32 20 PM" src="https://user-images.githubusercontent.com/61003769/122859206-78675300-d2d0-11eb-8fd7-dcebe10ab790.png">

The exact hue/saturation/value numbers varied for each type of tile, but the outcomes were the same.

The graph is then traversed with a sort of DFS algorithm, and is weighted as necessary based on tile value (green, gold, diamond/blue) or urgency (fire). Graph traversal is very fast as well with my implementation, varying from 0.007-0.010 seconds for the whole board. This is aided by:
- recognizing dead ends immediately
- using sets for the prefixes of every valid word, which gives constant-time complexity for checking containment. 

At the lowest end of efficiency, for argument say going down just four letters deep starting at each of the 52 tiles, we'd have in the ballpark of tens of thousands of branches/iterations possible branches to explore. But the method employed here will only investigate each promising path, which is in the neighborhood of 2-300 branches and only ~1000 iterations. Further improvements could be made still though. However the bottleneck is OCR and not traversal, so it wasn't a priority.

**Features to come:**
- Smart solving to bring the board closer to, and prioritize bonus words.
