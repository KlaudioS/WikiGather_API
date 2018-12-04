# WikiGather

The WikiGather API appeared from the need to download large raw data quantities from the Wikimedia foundation, with a simple and efficient tool.  The API allows an easy integration in researchers python projects.

##### Disclosure
API stil under development


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
# Create a Dataset with 9 attributes from the raw file,contains data from all languages 
def create_ds():
```

```python
# Create a Dataset with 8 attributes from the raw file, contains just data from the desired language	
def create_ds_lang(desiredLang):
```


```python
# Write a dataset out in CSV format		
def write_CSV():
```

```python
# Calculate the average,standard deviaton for request and webpage size
def calculate_all():
```

```python
# Clear data from all variables, used when in need to restart a process
def clearData():
```

#### 4 Hours functions

```python
# Create a dataset with 4 hours worth of data per record,contains data just from the defined language	
def create_ds_4h(desiredLang):
```

```python
# Write out a 4 hours record dataset in CSV format
def write_CSV_4h():
```

```python
# Calculate the average,standard deviaton for request and webpage size
def calculate_all_4h(desiredLang):
```
