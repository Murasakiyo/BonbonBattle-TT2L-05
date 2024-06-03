# tutorial - https://blog.hubspot.com/website/python-pickle

import pickle

# define a python object to pickle (in dictionary)
my_object = {"a": 123, 
             "b": [1, 2, 3], 
             "c": {"x": 0, "y": 9}}

# serialize the object to a file
with open('my_object.pickle','wb') as f:
    pickle.dump(my_object, f)

# deserialize the object from the file
with open('my_object.pickle', 'rb') as f:
    loaded_object = pickle.load(f)


# check that the deserialized object is the same as the original object
print(my_object == loaded_object) # OUTPUT: TRUE