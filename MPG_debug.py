import pickle

from time import sleep

path_to_pickle = 'mpg.pkl'

# load average mpg data from file
with open(path_to_pickle, 'rb') as f:
    mpgData = pickle.load(f)

# calculate the average mpg
mpg_sum = 0
count = 0
for i in mpgData:
    mpg_sum = mpg_sum + i
    avg_mpg =  mpg_sum / (len(mpgData) + 0.000001) # add a small number to prevent divide by zero
    count += 1
    
print("Succesfully loaded 'mpg.pkl'")

print("\nSize of array: " + str(count))

print("\n\nAverage MPG: " + str(avg_mpg))

while(1):
    cal = input("\nPress ctrl + c to exit\nEnter calibration percentage: ")

    cal_mpg = (avg_mpg - (avg_mpg*float(cal)))
    
    print("\nOriginal Average MPG: " + str(avg_mpg))
    print(  "Adjusted Average MPG: " + str(cal_mpg))

