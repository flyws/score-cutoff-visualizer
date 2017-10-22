# score-cutoff-visualizer
This is a good visualizer for any numerical changes in strategy. You could visualize the effect of change on the variable that interests you (i.e. approval rate in this example dataset) in an easy but interactive way.  

## How to understand the program?
This program has two parts that need to be tuned to fit your needs. First part is in the class "dataChanger", and in this part you would need to write down the functions in an incremental way, for example, if you increase the "Zhima Score" cutoff value by 1%, what part of data will be affected, and how would they be affected? Breaking down the changes in an incremental way will help you to visualize it faster. Normally if we want to see the impact of strategy changes, we will have to simulate the data again in the decision making engine, which is slow and less convenient, especially when you just want to pinpoint the area that has the biggest influence to serve as a general understanding.  

Second part of this visualizer is the easy to understand and implement. You could add as many functions in the "main()" function as you like, so you would also need more sliders as well. Be sure to add necessary code accordingly whenever you want a new slider.  

Hope you all have fun with this tiny work from me. Thanks!
