# WikiGather

# Requirements
- python 3.5.2

# API functions

The API comes with a different set of functions that lets you adjust your Wikipedia datasets to the users needs:

```
Enconding function to resolve encoding issues`
def enconding():`
```

```
# Generate list of the dataset names stored online
def get_URL():
```

```
# create a Dataset with 9 columns from the original DS,contains all languages 
def create_ds():
```

```
#create a Dataset with 8 columns from the original contains just the defined language for 24 hours	
def create_ds_lang(desiredLang):
```

```
#increment or create new register for each new line read
def add_to_ds(n):
```

```
#Write create DS out in CSV format		
def write_CSV():
```

```
#calculates the average,standard deviaton for request and webpage size
def calculate_all():
```

```
#clear all variables to be reused on the next step
def clearData():
```


### 4 Hours functions

```
#create a Dataset with 41 columns from the original DS(40 input att and 1 output att),contains just the defined language	
def create_ds_4h(desiredLang):
```

```
#write csv with 41 columns
def write_CSV_4h():
```

```
#increment or create new register for each new line read
def add_to_ds_4h(rawline,lan):
```

```
#calculates the average,standard deviaton for request and webpage size
def calculate_all_4h(desiredLang):
```
