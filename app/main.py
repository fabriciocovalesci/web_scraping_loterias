#!/usr/bin/env python3

import argparse
from lotofacil import LotofacilBot


parser = argparse.ArgumentParser(description="Get url from API")
parser.add_argument('-u', '--url')

args = parser.parse_args()


def main():
    bot = LotofacilBot(args.url)
    find_concurso = (bot.check_consurso())-2
    # obj_loteria = bot.scraping_page(int(find_concurso)+1)
    obj_loteria = bot.scraping_page(2572)
    bot.send_loteria(find_concurso ,obj_loteria)
    
if __name__ == "__main__":
    main()