# Prepare an NSC Data Return File for Import into DRDFS Salesforce
[Detroit Regional Dollars for Scholars](https://drdfs.org/) gets data from the National Student Clearinghouse on its alumni outcomes using the [StudentTracker service](https://www.studentclearinghouse.org/colleges/studenttracker/). This program takes a file returned from NSC as input, manipulates the data into the format needed to import it into DRDFS's student information system (Salesforce CoPilot), and outputs a file ready to be imported.

There are three types of records produced from the NSC Data:
1. An Academic Semester record of a student enrolled at a particular school in a particular semester
1. A Degree record of a student earning a degree at a particular school on a particular date
1. A record that no record was found for a student by the NSC

## Files Needed
Note that a future improvement to this program will source the Salesforce data from the Salesforce API.
- `NSC_Return.csv` = The exact file returned by the NSC.
- `schools.csv` = 'NSC Import--Schools' report from Salesforce to get the Salesforce ID for the school (account).
- `students.csv` = 'NSC Import--Students' report from Salesforce to get the Salesforce ID for the student (contact).
- `academic_semesters.csv` = 'NSC Import--Academic Semesters' report from Salesforce to compare the NSC data to academic semesters already in Salesforce to ensure the import doesn't duplicate data.
- `schools_to_replace.csv` = A file of some schools' NSC and IPEDS names. School names in Salesforce are sourced from IPEDS and don't always neatly match the same school's name as reported by the NSC. Thus, this file provides a convenient way to store known NSC Name to IPEDS name mappings to use to streamline merging in the schools data.

## Process
1. Drop unnecessary columns and format the ID field to prepare to merge with the student data
1. Merge the data from `students.csv` with the NSC data to get the Salesforce ID for the students
1. Use `schools_to_replace.csv` to replace the names of the schools to make the merge easier
1. Merge data from `schools.csv` with the NSC data to get the Salesforce ID for the school accounts
1. Manipulate the columns of the data returned from the NSC into the format needed by Salesforce, including dropping unnecessary columns
1. Merge data from `academic_semesters.csv` with the NSC data to determine which academic semesters already exist to be omitted from the import
1. Drop rows that already exist in Salesforce
1. Drop columns that are unnecessary for the import
1. Output a CSV file that is ready to be imported into Salesforce
