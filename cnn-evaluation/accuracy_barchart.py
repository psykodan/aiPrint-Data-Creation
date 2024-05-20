from matplotlib import pyplot as plt
import numpy as np

models = ["vgg19","MobileNetV3","ResNet50","Xception"]
#models = ["vgg19_line","vgg19_infill","MobileNetV3_line","MobileNetV3_infill","ResNet50_line","ResNet50_infill","Xception_line","Xception_infill"]
#res = [[924, 875], [938, 874], [919, 877], [934, 873]]
#synth_res = [[92.4, 93.8, 91.9, 93.4],[87.5, 87.4, 87.7, 87.3]]
#real_res = [[98.4,98.7,98.5,98.6,],[95.8, 95.7,96.8,96.3]]
res = [[98.3,98.3,97.9,97.9],[56.1,96.1,95.9,95.8]]
# Figure Size
fig, ax = plt.subplots(figsize =(5, 3))
barWidth = 0.25

# Set position of bar on X axis 
br1 = np.arange(4) 
br2 = [x + barWidth for x in br1] 

# Horizontal Bar Plot
plt.bar(br1, res[0], color ='firebrick', width = barWidth, label ='line') 
plt.bar(br2, res[1], color ='tomato', width = barWidth, label ='infill') 
 
# Adding Xticks 
plt.xlabel('Model', fontsize = 15) 
plt.ylabel('Accuracy (%)', fontsize = 15) 
plt.xticks([r + barWidth/2 for r in range(4)], 
        models)
plt.yticks([10,20,30,40,50,60,70,80,90,100,130])
 
plt.legend()
plt.tight_layout()
# Show Plot
plt.savefig("transfer-accuracies.png",dpi=300)
