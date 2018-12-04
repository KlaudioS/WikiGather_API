# WikiGather

# Requirements
- python 3.5.2

# API functions

The API comes with a different set of functions that lets you adjust your Wikipedia datasets to the users needs:

```python
# Enconding function to resolve encoding issues
def enconding():
```

```python
#Generate list of the dataset names stored online
def get_URL():
```

```python
# Create a Dataset with 9 columns from the original DS,contains all languages 
def create_ds():
```

```python
# Create a Dataset with 8 columns from the original contains just the defined language for 24 hours	
def create_ds_lang(desiredLang):
```


```python
# Write create DS out in CSV format		
def write_CSV():
```

```python
# Calculates the average,standard deviaton for request and webpage size
def calculate_all():
```

```python
# Clear all variables to be reused on the next step
def clearData():
```


#### 4 Hours functions

```python
# Create a Dataset with 41 columns from the original DS(40 input att and 1 output att),contains just the defined language	
def create_ds_4h(desiredLang):
```

```python
# Write csv with 41 columns
def write_CSV_4h():
```

```python
# Calculates the average,standard deviaton for request and webpage size
def calculate_all_4h(desiredLang):
```
