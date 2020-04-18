#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import csv
from tools import year_to_period, degree_type

# ****************************** STEP 1 ******************************

# Read in the data returned from NSC
nsc = pd.read_csv('data/NSC_Return.csv')

# Get rid of empty columns
nsc = nsc.dropna(axis=1, how='all')

types = nsc.dtypes
for column in types.index:
    if types[column] == np.float64:
        nsc.loc[:,column] = nsc[column].astype('Int64')

# Strip the '_' to get the student's Salesforce ID but in all caps
nsc.loc[:,'ID'] = nsc['Requester Return Field'].str.strip('_')

# ****************************** STEP 2 ******************************

# Read in students from Salesforce to get Salesforce IDs
stus = pd.read_csv('data/students.csv')

# Create a new column "ID" where the ID is uppercase to match NSC data
stus.loc[:,'ID'] = stus['Contact ID'].str.upper()

# Reset Last Name to uppercase to match NSC data
stus.loc[:,'Last Name'] = stus['Last Name'].str.upper()

# Merge in the student data to get the properly-cased Salesforce IDs
merged_stu = nsc.merge(stus[['ID', 'Contact ID', 'Last Name']],
                       on=['ID','Last Name'],
                       how='left')

# ****************************** STEP 3 ******************************

# Create a column to note the 'Data Source' as 'NSC'
merged_stu.loc[:,'Data Source'] = 'NSC'

# Split the records into those found by NSC and those not found
found = merged_stu[ merged_stu['Record Found Y/N'] == 'Y']
not_found = merged_stu[ merged_stu['Record Found Y/N'] == 'N']

# Convert all string date columns to datetime
found.loc[:,['Search Date',
       'Enrollment Begin',
       'Enrollment End',
       'Graduation Date']] = found[['Search Date',
                                    'Enrollment Begin',
                                    'Enrollment End',
                                    'Graduation Date']].apply(pd.to_datetime,
                                                              format='%Y%m%d')

# Use year_to_period func to determine period based on enrollment begin date
found.loc[:,'Period'] = found['Enrollment Begin'].apply(year_to_period)

# ****************************** STEP 4 ******************************

# Read in a few NSC School Name to IPEDS School Name mappings to fix names
with open('schools_to_replace.csv', 'r') as schools_to_replace:
    schools = {}
    reader = csv.reader(schools_to_replace)
    next(reader) # Skip header row
    for row in reader:
        schools[row[0].upper()] = row[1].upper() # Ensure uppercase

# Replace a few school names to better match IPEDS names
found.loc[:,'College Name'] = found['College Name'].replace(schools)

# ****************************** STEP 5 ******************************

# Read in schools data downloaded from Salesforce
schools = pd.read_csv('data/schools.csv')

# Set name column to uppercase to match uppercase school name from NSC
schools.loc[:,'Name'] = schools['Account Name'].str.upper()

# Merge found_sems with schools to get the school's Salesforce ID
merged_school = found.merge(schools[['Account ID', 'Name']],
                               left_on='College Name',
                               right_on='Name',
                               how='left')

# Any records where school and name are null, the school couldn't be matched
# User will need to add school to schools_to_replace.csv
print('School match not found:\n', merged_school['Name'][ merged_school.Name.isnull()])

# ****************************** STEP 6 ******************************

# Split into Academic Semesters and Degrees records (Period is NaN if Degree)
found_sems = merged_school[ ~merged_school.Period.isnull()]
found_degrees = merged_school[ merged_school.Period.isnull()]

# Set year column to the year the enrollment started, as a string
found_sems.loc[:,'Year'] = found_sems['Enrollment Begin'].apply(lambda x: str(x.year))

# Set acad semester name column to "Period Year" as "Fall 2019" for example
found_sems.loc[:,'Academic Semester Name'] = found_sems['Period'] + ' ' + found_sems['Year']

found_sems.loc[:,'Record Type'] = '0124T000000giMk'

# ****************************** STEP 7 ******************************

# Read in academic semesters data downloaded from Salesforce
sems = pd.read_csv('data/academic_semesters.csv')

# Merge in sems to find sems that have previously been imported to omit
sems_merged = found_sems.merge(sems,
                               left_on=['Contact ID',
                                        'Academic Semester Name',
                                        'Account ID'],
                               right_on=['Contact ID',
                                         'Academic Semester: Semester Name',
                                         'School: Account ID'],
                               how='left')

# Pull out sems that didn't match an existing sem in the merge to import
sems_to_load = sems_merged[ sems_merged['School: Account ID'].isnull()]

# ****************************** STEP 8 ******************************

# Drop empty columns
sems_to_load = sems_to_load.dropna(axis=1, how='all')

# Drop columns that aren't needed in the import
sems_to_load = sems_to_load.drop(['First Name', 'Last Name', 'Middle Initial',
                                  'ID', 'Name', 'Year',
                                  'College Name', 'College State'], axis=1)

sems_to_load = sems_to_load.rename(columns={'Enrollment Begin_x': 'Enrollment Begin',
                                            'Enrollment End_x': 'Enrollment End',
                                            'Contact ID': 'Student: Contact ID',
                                            'Period_x': 'Period',
                                            'Account ID': 'School: Account ID'})

# Write the import file to a CSV ready to load
sems_to_load.to_csv('data/NSC_Import_Academic_Semesters.csv',
                    index=False,
                    date_format='%Y-%m-%d')

# ****************************** STEP 9 ******************************

# Read in degrees data downloaded from Salesforce
degrees = pd.read_csv('data/degrees.csv')

# Merge in degrees to find degrees that have previously been imported to omit
degrees_merged = found_degrees.merge(degrees,
                                     left_on=['Contact ID',
                                              'Degree Title',
                                              'Account ID',
                                              'Degree Major 1'],
                                     right_on=['Contact ID',
                                               'Degree: Degree Name',
                                               'School: Account ID',
                                               'Degree Major 1'],
                                     how='left')

# Pull out degrees that didn't match an existing degree in the merge to import
degrees_to_load = degrees_merged[ degrees_merged['School: Account ID'].isnull()]

# ****************************** STEP 10 ******************************

# Pull out only those columns needed for the import
degrees_to_load = degrees_to_load[['Contact ID', 'Account ID', 'Graduation Date',
                                   'Degree Title', 'Degree Major 1',
                                   'Degree CIP 1', 'Data Source']]

degrees_to_load = degrees_to_load.rename(columns={'Contact ID': 'Student: Contact ID',
                                                  'Account ID': 'School: Account ID'})

# Fill the empty Degree Title values since they are required in Salesforce
degrees_to_load.loc[:,'Degree Title'] = degrees_to_load['Degree Title'].fillna(value='UNKNOWN')

# Assign Degree Type when possible
degrees_to_load.loc[:,'Degree Type'] = degrees_to_load['Degree Title'].apply(degree_type)

# Write the import file to a CSV ready to load
degrees_to_load.to_csv('data/NSC_Import_Degrees.csv',
                       index=False,
                       date_format='%Y-%m-%d')
