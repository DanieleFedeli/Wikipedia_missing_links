import page_manager.PageManager as pm
import requests
import cProfile


DATASET_PATH = './dataset.xml'
# Const path of the output folder path
OUTPUT_PATH = "./output/"

print('Starting.')
session = requests.Session()
listOfTitles = pm.SetOfPages(DATASET_PATH)
done = 0

for title in listOfTitles:
  if ":" in title: continue
  filename = OUTPUT_PATH+title+'.txt'
  backlinks = pm.GetBacklink(session, title)
  if len(backlinks) < 1: continue
  with open(filename, "w") as out_file:
    pm.FillTheFile(title, backlinks, out_file)
    done = done+1
    #print('We did the {percent:.2f}%'.format(percent=100 * done/len(listOfTitles)))

print('API CALLED %d TIMES' % len(listOfTitles))
print('Finish.')

