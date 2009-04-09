import csv
import numpy as np
import pickle
from names import Taxonomy

class DateReleaseObj():
    # self.date = ''
    # self.release_name = ''
    # self.dateweek = 0
     
    def __init__(self, dr):
         """ Init the data structure"""
         self.date, self.dateweek, self.release_name = dr  
         
    def get_release_name(self): 
        return self.release_name
    def get_dateweek(self):
        return self.dateweek
    def get_date(self):
        return self.date 
    def __str__(self):
        return self.date, self.dateweek, self.release_name
        
def find_window(product, signified):
    pickle_dir = '/Users/nernst/Documents/current-papers/icsm09/data/pickles/'        
    pickle_file = pickle_dir + product+'-'+ signified + '.pcl'
    data = pickle.load(open(pickle_file, 'rb'))
    #print product, signified, len(data)
    tmp = gnome_dates_dict.keys()
    tmp.sort() #in place sort
    for lst in data:#ev_eff_list:
        for key in tmp:
        #find the key with the correct index
            if int(lst[0]) > key:
                index = key
            #stick the list in the bucket
        gnome_dates_dict[index] = gnome_dates_dict[index] + [lst]

#generate arrays of data for each and plot the trends.
# a release window is the weeks following a release but before the next release. We want to see what effects there are.
# for each window, measure the slope and r2 values and store them
    tmp2 = gnome_dates_dict.keys()
    tmp2.sort()
    for window in tmp2:
            dates = []
            values = []
            if gnome_dates_dict[window] != []:
                # print 'Key is ' + str(window) + ' values are: ' + str(gnome_dates_dict[window])
                for tup in gnome_dates_dict[window]:
                    # normalize
                    normal =  tup[1] #float(lst[1]) / float(e_all_dict[lst[0]]) * 1000
                    #print normal
                    dates.append(lst[0])
                    #values.append(lst[1])
                    values.append(normal)
                if len(values) > 3: #don't bother with those smaller than 4, not significant
                    new_x = []
                    for i in range(len(dates)):
                       new_x.append(i)
                    int_corr = np.corrcoef(new_x, values)
                    corr = int_corr[0][1] #note, not r^2 value
                    r2 = corr*corr
                    y = [float(x) for x in values]
                    z = np.polyfit(new_x, y, 1) # a 1-degree regression
                    slope, intercept = z
                    slope = round(slope,2)
                    r2 = round(r2, 2)
                    print product, signified, len(values)
                    #print '\\textbf{' + product + '-' + signified + '}&'+ release_map[window].get_release_name() +  '& '+ str(r2) + ' & ' + str(slope) + ' & ' + str(len(values)) + '\\\\'

def main():
    gnome_dates = '/Users/nernst/Documents/projects/msr/data/yearweek.csv'
    release_dates = '/Users/nernst/Documents/projects/msr/data/dates-releases.csv'
    global gnome_dates_dict
    global release_map
    
    reader = csv.reader(open(gnome_dates, 'rb'))
    gnome_dates_list = [int(x[0]) for x in reader]
    gnome_dates_dict = dict.fromkeys(gnome_dates_list,[])
    #open the list of Gnome releases
    dr = csv.reader(open(release_dates, 'rb'))
    release_map = gnome_dates_dict.copy() #shallow copy
    releases = [x for x in dr]
    for release in releases:
        release_map[int(release[1])] = DateReleaseObj(release)
    print release_map
    t = Taxonomy()     
    #for signified in t.get_signified(): # e.g. usability, performance, etc
    for product in t.get_products():
            #print 'Project - Quality & Release & $r^2$ & slope & N \\\\'
        find_window(product, 'Usability')
            #print '\\hline'
            #pass
    #find_window("Evolution", "Usability")

if __name__ == '__main__':
    main()