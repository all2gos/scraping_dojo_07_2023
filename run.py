import requests, ast, re, json, os
from bs4 import BeautifulSoup
from dotenv import load_dotenv

#core of the program: the function that extracts all quotes from a given website
def scraping(url, proxy):
    page = requests.get(url, proxies = {'https':proxy, 'http:':proxy})
    soup = BeautifulSoup(page.content, 'html.parser')
    
    #noticed that all quotes are in one specific script object
    quotes = str(soup.find_all('script')[1])    

    #extracting only quotes from a script object
    quotes = quotes.split('var data =')[1]
    quotes = quotes.split(';\n')[0]
    list_of_quotes = ast.literal_eval(quotes.strip())
    return list_of_quotes

#function that converts extracted data to required syntax, the returned list will be used to create output file
def rearranging(l):
    output_list = []
    for line in l:
        inner_dict = dict()        
        inner_dict['text'] = re.sub(r"“|”|'",'',line['text'])
        inner_dict['by'] = line['author']['name']
        inner_dict['tags'] = line['tags']
        output_list.append(inner_dict)
    return output_list

#function that creates jsonl file
def save_file(output_list):
    json_lines = [json.dumps(l) for l in output_list]
    json_data = '\n'.join(json_lines)
    with open(OUTPUT_FILE, 'w') as file:
        file.write(json_data)

if __name__ == '__main__':

    #read environmental variables
    load_dotenv()
    PROXY=os.getenv('PROXY')
    INPUT_URL=os.getenv('INPUT_URL')
    OUTPUT_FILE=os.getenv('OUTPUT_FILE')

    #scraping and saving results to jsonl file    
    scraped_quotes = rearranging(scraping(url = INPUT_URL, proxy = PROXY))
    save_file(scraped_quotes)

    print(f'File {OUTPUT_FILE} has been succesfully created.')

