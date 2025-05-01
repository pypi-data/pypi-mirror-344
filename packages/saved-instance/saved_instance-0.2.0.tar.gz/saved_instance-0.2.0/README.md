# saved_instance



## About

SavedInstance is a persistent Python dictionary. It allows you to store and retrieve data based on key and value in a dictionary format.


## Introduction

SavedInstance is:

 - **Just dict**: For accessing or modifying data, there are no separate methods, you can just work with the same way as a dictionary.
 - **Flexi type**: SavedInstance can store all python types and custom user defined class
 - **Inbuilt secure**:  Provides a functionality to store the data in encrypted format, it automatically encrypts the data and decrypts it on demand.
 - **Thread safe**: Designed to work reliably in multi-threaded and multi-processing environments.

## Example 1
Alice.py
```
Alice.py

from saved_instace import simple_storage

simple_storage_obj = simple_storage()

# writing
simple_storage_obj["message"] = "Hello World"

```
Bob.py
```
Bob.py

from saved_instance import simple_storage

simple_storage_obj = simple_storage()

# Reading
print(simple_storage_obj["message"])

```

## Getting Started

### Install

```
pip install saved_instance
```

### Config
```
svd config init --project-name your-project-name
```
Run above the command in root of your project


## Storages

### Simple Storage

Simple storage allows you store all python type object using key and value based.

please refer Example 1

Note! : 
* simple storage can't track nested mutable object changes automatically, you have to make copy of the data then make change then resign. 
* please refer Example 2 and Example 3
* use rich_storage to track nested mutable object changes.



### Example 2
```
!---- Example for mutable object changes can't track automaticaly ----!

>>> from saved_instace import simple_storage

>>> simple_storage_obj = simple_storage()

>>> simple_storage_obj["shops"] = ["shop1", "shop2"]

>>> simple_storage_obj["shops"].append("shop3")

>>> simple_storage_obj["shops"]

>>> ["shop1", "shop2"] # shop3 won't come

```


### Example 3
```
!---- Solution for mutable object changes. ----!

>>> from saved_instace import simple_storage

>>> simple_storage_obj = simple_storage()

>>> # considered shops already got stored and we are reading it. data is ["shop1", "shop2"].

>>> temp_shops = simple_storage_obj["shops"] # make copy of data.

>>> temp_shops.append("shop3") # update the value

>>> simple_storage_obj["shops"] = temp_shops # write updated data back

>>> simple_storage_obj["shops"]

>>> ["shop1", "shop2", "shop3"]

```


### secure_storage

Secure Storage is allowing you to store data in encrypt format.
please refer Example 3.
Secure Storage is same as simple storage can't automatically track nested object changes.

### Example 3

```
>>> import saved_instance as sv

>>> secure_storage_obj = sv.secure_storage()      

>>> # Encryption

>>> secure_storage_obj["msg"] = "Hi"

>>> secure_storage_obj["msg"]
b'gAAAAABoEKIbKBQc8vq3Gft4r-_bS07PXNAy-qW8QcrTH4eb9q2cXZoOPSxS8XS9NuPy9jXtBCLH6G184I3zExx4UEZZgGQ9WszHeRX7-VgfaJ7m_8ZmH6Q='

>>> # Manual Decryption

>>> secure_storage_obj,decrypt("msg")
Hi


>>> # Auto Decrypt

>>> secure_storage_obj = sv.secure_storage(auto_decrypt=True)      

>>> secure_storage_obj["msg"] = "Hi"

>>> secure_storage_obj["msg"]
'Hi'

```

### Rich Storage

Rich Storage is advanced version simple storage.

* It will store all python types and also user defined custom class
* It automatically tracks nested mutable objects(List, Dict) changes

### Example 4 



## License
MIT