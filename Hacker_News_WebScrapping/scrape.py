import requests as req
from bs4 import BeautifulSoup as bs


def sort_by_votes(hnlist):
    return sorted(hnlist,key=lambda k:k['votes'],reverse=True)

def create_custom_hn(links,subtext):
    hn=[]
    for idx,item in enumerate(links):
        title=item.getText()
        href= item.select('a')[0].get('href',None)
        votes=subtext[idx].select('.score')
        if len(votes):
            points = int(votes[0].getText().replace(' points', ''))
            if points>=100:
                hn.append({'title':title,'link':href,'votes':points})
    return hn
def main():
    listing=[]
    try:
        user_page_input=int(input("Enter the number of pages you want to scrape:"))
    except ValueError:
        user_page_input = 1
    print(f"Displaying News from {user_page_input} page(s) of Hacker News....")
    for i in range(1,user_page_input+1):
        res=req.get(f'https://news.ycombinator.com/?p={i}')
        soup=bs(res.text,'html.parser')
        links=soup.select('.titleline')
        subtext=soup.select('.subtext')
        listing.extend(create_custom_hn(links,subtext))
    listing=sort_by_votes(listing)
    for i in listing:
        print("-"*10)
        for j in i.keys():
            print(j,':',i[j])
        print("-"*10)
        print()

if __name__=='__main__':
    main()


