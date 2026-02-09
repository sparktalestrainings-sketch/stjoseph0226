from sklearn.linear_model import LinearRegression
model = LinearRegression() # we are creating an empty brain

hours = [[1],[2],[3],[4],[5]] 
marks = [50,60,70,80,90]

model.fit(hours,marks) # learning from data

print(model.predict([[6]])) #predicting the output [82]
print(model.predict([[10]])) #predicting the output [92]