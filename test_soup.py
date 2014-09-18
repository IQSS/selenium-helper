from bs4 import BeautifulSoup


page_source = open('input/test_dataset_page_source.html')

soup = BeautifulSoup(page_source)
soup_lnk = soup.find(attrs={'id':'pre-input-title'})
print '-' * 40
print (soup_lnk)
print '-' * 40
print (soup_lnk.next)
print '-' * 40
print (soup_lnk.findNext('input').get('id', 'no id'))
"""
for lnk in soup_lnk:
    print lnk.text
    print lnk
"""
#for lnk in soup_div.findAll('a', href=True):
#        d[lnk.text] = lnk['href']

#    return d