
#To traverse through the code and find the data from the tables, 
#hence we need to search the tr tag in the HTML source code
soup= BeautifulSoup(url.text)
soup_data= soup.find_all('tr')
soup_data

#Traversing all the pages to for the csv file
data_page1 = pd.read_html("https://top500.org/list/2019/06/?page=1")
data_page2 = pd.read_html("https://top500.org/list/2019/06/?page=2")
data_page3 = pd.read_html("https://top500.org/list/2019/06/?page=3")
data_page4 = pd.read_html("https://top500.org/list/2019/06/?page=4")
data_page5 = pd.read_html("https://top500.org/list/2019/06/?page=5")

#Checking the data contents
print(data_page1)
print(data_page2)
print(data_page3)
print(data_page4)
print(data_page5)

#Concatinating the each page values into a sinfle data frame
list_comp=pd.concat([data_page1[0],data_page2[0],data_page3[0],data_page4[0],data_page5[0]])
list_comp

#Exporting the dataframe into CSV file
exporttocsv=list_comp.to_csv(r'C:\Users\chandana\Documents\Chandana_ListSuperComputers.csv')


#Cleaning up of data

#Replacing the blank values with NA values using errors=coerce and to_numeric functions
list_comp['Cores']=pd.to_numeric(list_comp['Cores'],errors='coerce')
list_comp['Rpeak (TFlop/s)']=pd.to_numeric(list_comp['Rpeak (TFlop/s)'],errors='coerce')
list_comp['Rmax (TFlop/s)']=pd.to_numeric(list_comp['Rmax (TFlop/s)'],errors='coerce')
list_comp['Power (kW)']=pd.to_numeric(list_comp['Power (kW)'],errors='coerce')

#Filling the NA values using mean on the column
list_comp['Cores']=list_comp['Cores'].fillna(list_comp['Cores'].mean())
list_comp['Rpeak (TFlop/s)']=list_comp['Rpeak (TFlop/s)'].fillna(list_comp['Rpeak (TFlop/s)'].mean())
list_comp['Rmax (TFlop/s)']=list_comp['Rmax (TFlop/s)'].fillna(list_comp['Rmax (TFlop/s)'].mean())
list_comp['Power (kW)']=list_comp['Power (kW)'].fillna(list_comp['Power (kW)'].mean())

#Summary for Cores, RMax, RPeak and Power
print(list_comp['Cores'].describe())
print(list_comp['Rmax (TFlop/s)'].describe())
print(list_comp['Rpeak (TFlop/s)'].describe())
print(list_comp['Power (kW)'].describe())

#Visualizations for Cores, RMax, RPeak and Power
plt.hist(list_comp['Cores'],color='red',bins=20)
plt.xlabel('Cores')
plt.title('Visualization for Cores')

plt.hist(list_comp['Rpeak (TFlop/s)'],color='orange')
plt.xlabel('Rpeak (TFlop/s)')
plt.title('Visualization for RPeak (TFlop/s)')

plt.hist(list_comp['Rmax (TFlop/s)'],color='green')
plt.xlabel('Rmax (TFlop/s)')
plt.title('Visualization for Rmax (TFlop/s)')

plt.hist(list_comp['Power (kW)'],color='blue',width=2500)
plt.xlabel('Power (kW)')
plt.title('Visualization for Power (kW)')


#Relationship between Cores and RPeak
plt.scatter(list_comp['Rpeak (TFlop/s)'],list_comp['Cores'],color='Green')
plt.xlabel('Rpeak (TFlop/s)')
plt.ylabel('Cores')
plt.title('Relation between Cores and Rpeak(TFlop/s)')

#Relationship between Cores and Power
plt.scatter(list_comp['Power (kW)'],list_comp['Cores'],color='Red')
plt.xlabel('Power (kW)')
plt.ylabel('Cores')
plt.title('Relation between Cores and Power (kW)')


list_comp.corr()



