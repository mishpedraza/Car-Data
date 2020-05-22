#!/usr/bin/env python
# coding: utf-8

# In[87]:


open('AppleStore.csv')


# **Profitable App Profiles for the App Store and Google Play Markets**
# Our aim is to help our developers understand what type of apps are likely to attract more users on Google Play and the App Store.

# In[88]:


from csv import reader


# In[89]:


opened_file = open('AppleStore.csv')
file = reader(opened_file)
ios = list(file)
ios_header = ios[0]
ios = ios[1:]


# In[90]:


opened_file = open('googleplaystore.csv')
file = reader(opened_file)
android = list(file)
android_header = android[0]
android = android[1:]


# In[91]:


def explore_data(dataset, start, end, rows_and_columns=False):
    dataset_slice = dataset[start:end]    
    for row in dataset_slice:
        print(row)
        print('\n') # adds a new (empty) line after each row

    if rows_and_columns:
        print('Number of rows:', len(dataset))
        print('Number of columns:', len(dataset[0]))
        
print(ios_header)
print('\n')
explore_data(ios,0,3,True)


# In[92]:


print(android_header)
print('\n')
explore_data(android,0,3,True)


# In[93]:


del android[10472]


# In[94]:


print(len(android))


# There are duplicates app rows in the datasets that we will need to remove. Instead of removing these randomly, we will leave the app data with the highest number of reviews which likely means it is the most recent.

# In[95]:


##Number of duplicates and some examples##
duplicates = []
unique = []

for row in android:
    name = row[0]
    if name in unique:
        duplicates.append(name)
    else:
        unique.append(name)
print('number of duplicates:', len(duplicates))
print('examples:', duplicates[:15])


# There are 1,181 duplicates. We will find out the max number of reviews to leave the app data with highest reviews.

# In[103]:


reviews_max = {}
for row in android:
    name = row[0]
    n_reviews = float(row[3])
    if name in reviews_max and reviews_max[name] < n_reviews:
        reviews_max[name] = n_reviews
    elif name not in reviews_max:
        reviews_max[name] = n_reviews


# In[104]:


print('Expected length:', len(android) - 1181)
print(android[0])


# In[105]:


android_clean = []
already_added = []

for app in android:
    name = app[0]
    n_reviews = float(app[3])
    
    if (reviews_max[name] == n_reviews) and (name not in already_added):
        android_clean.append(app)
        already_added.append(name)


# In[108]:


explore_data(android_clean,0,3,True)


# In[114]:


def is_english(string):
    non_ascci = 0
    
    for character in string:
        if ord(character) > 127:
            non_ascci += 1
            
    if non_ascci > 3:
        return False 
    else:
        return True
        


# In[115]:


print(is_english('instagram'))
print(is_english('爱奇艺PPS -《欢乐颂2》电视剧热播'))


# In[123]:


android_final = []
ios_final = []

for row in android_clean:
    name = row[0]
    if is_english(name):
        android_final.append(row)

for row in ios:
    name = row[1]
    if is_english(name):
        ios_final.append(row)
        
        


# In[124]:


explore_data(android_final,0,3,True)
print('\n')
explore_data(ios_final,0,3,True)


# In[135]:


ios_apps = []
android_apps = []

for row in ios_final:
    price = row[4]
    if price == '0.0':
        ios_apps.append(row)
for row in android_final:
    price = row[7]
    if price == '0':
        android_apps.append(row)


# In[136]:


print(len(android_apps))
print(len(ios_apps))


# Next, we want to find out what are the most common genres to find out what are the types of apps that are more likely to attract users. 

# In[149]:


def freq_table(dataset, index):
    table = {}
    total = 0
    for row in dataset:
        total += 1
        value = row[index]
        if value in table:
            table[value] += 1
        else:
            table[value] = 1
            
    table_percentages = {}
    for key in table:
        percentages = (table[key] / total) * 100
        table_percentages[key] = percentages
    return table_percentages

def display_table(dataset, index):
    table = freq_table(dataset, index)
    table_display = []
    for key in table:
        key_val_as_tuple = (table[key], key)
        table_display.append(key_val_as_tuple)
        
    table_sorted = sorted(table_display, reverse = True)
    for entry in table_sorted:
        print(entry[1], ':', entry[0])
        
display_table(android_apps, 1)


# In[150]:


display_table(ios_apps, -5)


# In[151]:


genres_ios = freq_table(ios_apps, -5)

for genre in genres_ios:
    total = 0
    len_genre = 0
    for app in ios_apps:
        genre_app = app[-5]
        if genre_app == genre:
            n_ratings = float(app[5])
            total += n_ratings
            len_genre += 1
    avg_n_ratings = total / len_genre
    print(genre, ':', avg_n_ratings)


# In[153]:


category_android = freq_table(android_apps, 1)

for category in category_android:
    total = 0
    len_category = 0
    for row in android_apps:
        category_app = row[1]
        if category_app == category:
            n_installs = row[5]
            n_installs = n_installs.replace("+", "")
            n_installs = n_installs.replace(",", "")
            total += float(n_installs)
            len_category += 1
    avg_installs = total / len_category
    print(category, ":", avg_installs)


# In[ ]:




