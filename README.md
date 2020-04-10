# K-Maps
The rest of this guide assumes that you know what K-Maps are and how they are used to simplify logical expressions. If this is unfamiliar to you, read the following guide: https://en.wikichip.org/wiki/karnaugh_map

# Installation
Downnload the latest version of Python 3 to your computer from python.org. The program was built and tested using Python 3.8.

You must also install `forseti`, a parsing library used by this program. Open a terminal window and run `pip install forseti` on Windows or `pip3 install forseti` on Mac/Linux.

This application also requires Tkinter/Tcl version 8.6+ for 4-variable K-Maps (if you are not going to be working with 4-variable K-Maps, earlier versions should work). On Mac, you may have to reinstall Python as described at https://www.reddit.com/r/Python/comments/54x1mu/help_with_installing_tkinter_86_on_mac/. 

Download all the files in this repo to your computer.

# Running K-Map Generator
To run the program, simply double-click on the `frontend.pyw` file.

# Using the program
## Specifying an Expression Manually
When the program first launches, you will be greeted with a dialogue box that asks you to enter an expression. The K-Map Generator will help you create a K-Map for this expression and use it to simplify this expression.

The following syntax is used for inputting expressions:

AND = &
OR = |
NOT = ~
CONDITIONAL = ->
BICONDITIONAL = <->

An example of a valid input is `((~P & Q) <-> (R & S))`.

Expressions with more than 4 variables are not supported at this time.

![Figure 2](https://github.com/venkatrsrinivas/K-MapGenerator/blob/master/screenshots/2.png)

## Opening a File
Instead of specify an expression to simplify manually, you can opt to open an existing K-Map file. To do this, type `open` into the dialogue box (pre-filled by default) and hit OK. You will then be prompted to select the file to open. A sample file, 4variables.kmap, is included in this repo if you wish to play around.

![Figure 1](https://github.com/venkatrsrinivas/K-MapGenerator/blob/master/screenshots/1.png)

## The Main Interface
After you have either manually entered an expression or opened an existing K-Map file, you will be presented with the following screen.

![Figure 3](https://github.com/venkatrsrinivas/K-MapGenerator/blob/master/screenshots/3.png)

Let's take some time to explore this interface.

- At the top of the screen, the program prints the expression that you entered in a human-readable format. 
- Directly below this, in the center of the screen, is the K-Map. The program labels the cells in the K-Map for you.
- To the left of the K-Map is an Instructions button, which refers the user to this document.
- To the right of the K-Map is a list of all the groupings you have created on your K-Map. Currently, we have not created any groupings, so this list is empty.
- Underneath the K-Map, there are entry fields for creating and merging groupings. We will discuss this in more detail later.
- Finally, at the bottom, there is a text field where you can enter your final answer (that is, the final expression that you get after simplifying the original expression using the K-Map). There is also a Check Answer button, which allows you to check your work. This will be discussed in more detail later.

## Creating Groupings
The Create Grouping panel allows you to create groupings on your K-Map. Each grouping is a square, and the number of cells in a grouping must be a power of 2. To allow you to specify which cells you wish to enclose within your grouping, K-Map Generator uses a coordinate system, where the upper-left corner is 0,0 and the bottom-right corner (in this case) is 3,3. The y-values increase as you move down the K-Map, and the x-values increase as you move to the right. 

The figure below shows how this system can be used to create and label a new grouping.

![Figure 4](https://github.com/venkatrsrinivas/K-MapGenerator/blob/master/screenshots/4.png)

In this example, the user created the grouping (0, 2), (1, 3); (0, 2) are the coordinates of the upper-left corner of the grouping, and (1, 3) are the coordinates of the lower-right corner. After the user enters these coordinates and clicks the "Create Grouping" button, the grouping is created, and the corresponding cells on the K-Map are colored in red. This is how K-Map Generator allows you to visualize groupings you have created on the K-Map; all of the cells in a certain grouping are shaded in a certain color. Each grouping is shaded in its own unique color; for instance, if we create another grouping, we notice that the cells in this new grouping are colored in pink, rather than red. This way, we can differentiate between the different groupings while looking at the K-Map by observing the different colors. In K-Map Generator, groupings are labelled by what color they are on the K-Map using this coloring system.

![Figure 5](https://github.com/venkatrsrinivas/K-MapGenerator/blob/master/screenshots/5.png)

Also notice how, in addition to being able to visualize the colored groupings, the Groupings list on the right is now populated with the coordinates of the two groupings we have just added.

## Merge Groupings
Sometimes, you may find yourself in a situation where you have two separate groupings sitting next to each other, and you wish to merge them. For instance, in the figure below, the red and pink grouping can be merged.

![Figure 6](https://github.com/venkatrsrinivas/K-MapGenerator/blob/master/screenshots/6.png)

To merge these groupings, we merely need to go to the Merge Groupings panel, select the two groupings we wish to merge, and hit Merge Groupings.

![Figure 7](https://github.com/venkatrsrinivas/K-MapGenerator/blob/master/screenshots/7.png)

After hitting Merge Groupings, the pink and red grouping merge into one large red grouping.
![Figure 8](https://github.com/venkatrsrinivas/K-MapGenerator/blob/master/screenshots/8.png)

## Rules for Groupings
The following rules apply to groupings:
1. All groupings must be rectangular
2. The number of cells in a grouping must be a power of 2
3. Groupings that "wrap around" the edges of the K-Map either vertically or horizontally are allowed and encouraged! For instance, the following Red grouping is valid:

![Figure 9](https://github.com/venkatrsrinivas/K-MapGenerator/blob/master/screenshots/9.png)

4. Groupings cannot be diagonal
5. Groupings can overlap with each other
6. All 1's in a K-Map must belong in a grouping. There cannot be any ungrouped 1's left in the K-Map. This includes single cells containing a 1; in this case, you must create a grouping that contains only 1 cell, as shown below.

![Figure 10](https://github.com/venkatrsrinivas/K-MapGenerator/blob/master/screenshots/10.png)

## Checking Final Answer
Once you have created all of your groupings and are sure they are correct, use them to come up with a simplified logical expression. If you are unsure how to do this, read the following guide on K-Maps: https://en.wikichip.org/wiki/karnaugh_map

Write your simplified logic expression in the "Your Answer" box, using the same syntax described earlier, then click the Check Answer button. The Check Answer button will first verify that you created your groupings correctly; if you did not, it will tell you to correct your groupings. If your groupings were made correctly, the program will then check whether the answer you inputted matches the groupings you created. If your expression can be simplified more, or if it is not logically equivalent to the original expression, the program will throw an error message; otherwise, it will declare that your answer is correct.

![Figure 11](https://github.com/venkatrsrinivas/K-MapGenerator/blob/master/screenshots/11.png)

## Saving Files
To save your current progress, or save the solved K-Map after you have completed it, go to the File menu and click Save.
