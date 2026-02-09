from sklearn.linear_model import LinearRegression
model = LinearRegression() # we are creating an empty brain

experience = [[0],[1],[2],[3],[4],[5]] 
salary = [10,15,22,30,38,50]

model.fit(experience,salary) # learning from data

print("The predicted salary for 10 years of exp:",model.predict([[10]])) 
print("The predicted salary for 20 years of exp:",model.predict([[20]])) 