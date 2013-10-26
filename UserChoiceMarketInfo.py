#!/usr/bin/ python3
#
######### Script Header #########
#  
#::Script Name::
#  UserChoiceMarketInfo.py
#  
#  
#::About Author::
#  Miles Nielsen
#  MilesNielsen.net
#  Miles.Nielsen@swe.org
#  
#  
#::Script Purpose::
#  Grab Performance, Investment Style, Risk//Reward, and Morningstar Star-Rating data from Morningstar.com
#     for user-specified Mutual Fund(s), Stock(s), or ETF(s) and output the data to a .csv file onto the Desktop.
#     |-> Foreign %, Bond %, and Sector Distribution % data is possible, but script-modification is required.
#  
#  
#::Philosophy of the Script::
#  Script Author desired to collect specific data for one arbitrary ETF, Stock, or Mutual Fund per script iteration;
#     |-> ETF, Stock, or Mutual Fund is chosen by User, then re-process is repeat if User-desired.
#  Script Author desired to avoid dependencies external to the script, e.g. BeautifulSoup, wget, WindMill, &c.
#     |-> Therefore: BeautifulSoup, and similar script-external html parsers, shall not be used.
#  User must input the market ticker for desired ETF, Stock, or Mutual Fund.
#  Script creates & deletes several temp/slush files in /home/your_user for data processing.
#     |-> Temp/slush files are: holdingstyle.txt, star_rating.txt, performance.txt, risk_reward.txt, and Final_Data.txt. Include cbf.txt if Foreign %, Bond %, & Sector Distribution % is included in the data-gathering.
#     |-> In case of the Author, temp/slush file location is /home/harry.
#  Script creates "permanent" file on Desktop, "Final_Data.csv", for all data collected; readable through spreadsheet-capable program, comma-delimited.
#     |-> "Final_Data.csv" file is re-named from "Final_Data.txt" file, as written throughout the script.
#     |-> In case of the Author, Desktop is /home/harry/Desktop.
#     |-> Desktop location must be altered for all users not the original Author.
#  
#  
#::Restrictions::
#  Intended to be run on linux, e.g. LinuxMint13 "Maya", or similar OS [Ubuntu, &c].
#  User must provide a market ticker for each ETF, Mutual Fund, or Stock they are interested in researching.
#     |-> Fat-finger errors are accounted for.
#  Written for Python ~3.2.3.
#     |-> Not Python 2 compatible.
#  User home and Desktop locations must be altered for all users not the original Author.
#  
#  
#::Notes::
#  The Performance numbers given in Final_Data.csv are %.
#  Re-ordering the sequence of data written to file requires re-ordering the titles;
#     |-> Also, the last '-- [for Holding Style] must be moved to the end of the Stock section;
#     |-> Keep an eye out for how 'Performance' numbers line up, especially for empty 10-yrs & 15-yrs.
#  There is one global variable: market_ticker.
#  
#  
#::Sample Usage::
#  1) In Linux terminal, do:
#        python3 /file/location/UserChoiceMarketInfo.py
#           ...script will run, follow the prompts, provide requested information...
#  2) On Desktop, find Final_Data.csv.
#  3) Open Final_Data.csv via Thy Favorite Spreadsheet program, e.g. Excel, comma-delimited.
#  4) Analyze Data & Carry On.
#
#  
#::Back to the Future::
#  Consider retrieving the current share price of the Fund//ETF//Stock.
#  Consider allowing historical risk/reward data to be written to file.
#     |-> Requires altering the titles in the .csv//.txt output file.
#  Consider the value, or lack thereof, of gathering a fund's Foreign %, Bond %, & Sector Distribution % here; remove as desired.
#  Consider colourizing the txt outputs, possibly via colorama.
#     |-> Leave OS-prints as white txt, black background
#     |-> ETF txt as green, black background
#     |-> Stock txt as cyan, black background
#     |-> MF txt as red, black background
#  
#  
#  Verify that a blank-zero value at the end of a holding_style still allows it to be processed, and correctly.
#  Verify the formatting//spacing in .csv's Performance area, [accounting for ETF/S/MFs w/o 15-yr, 10-year, &c values].
#  
#  
#::Revision History::
#  v1.0 - Initial release; Modified from FundsBFSD.py && http://www.goldb.org/ystockquote.html;
#              Miles Nielsen [.net]. 2011.10.30
#  v2.0 - Script overhauled; Script-extracted data is the performance ["total trailing returns"], investment//holding_style, risk & reward, and
#              MorningStar star rating data for a user-given ETF, Stock, and/or Mutual Fund from MorningStar.com; Output file is .csv, comma-delimited, 
#              for spreadsheet analysys; User must provide valid ETF, Mutual Fund, and/or Stock market tickers, though fat-finger'd errors are
#              accounted for; the ability of gathering Foreign %, Bond %, & Sector Distribution % is available, but currently unused;
#              Miles Nielsen [.net]. 2012.08.13
#  
#  
######### End Script Header #########

#Pound-include Leh Stuff
import urllib, urllib.request
import re, sys
import os, datetime
from html.parser import HTMLParser


##### Define Ye Classes & Functions #####
class MLStripper(HTMLParser): #Supports the stripping of tags from "straight html"
     def __init__(self):
          super().__init__()
          self.reset()
          self.fed = []
     def handle_data(self, d):
          self.fed.append(d)
     def get_data(self):
          return ''.join(self.fed)

#This strips html tags from html; input must be "straight html"
def strip_tags(html):
     s = MLStripper()
     s.feed(html)
     return s.get_data()
##### Ye Functions Are Defined #####


#Time, Right Now.
now = datetime.datetime.now()
print(now.strftime("%Y-%m-%d %H:%M")) #Print to Terminal time, time right now;
print('========== =========== ==========')

rf = open('/home/harry/Desktop/Final_Data.txt', 'w') #Create-Write date & time to Final_Data.txt, & close
rf.write(now.strftime("%Y-%m-%d %H:%M") + ',Star Rating,Return,Risk,Investment Style,Performance,,,,,,' + '\n')
rf.write('Ticker,Overall,Reward,Risk,Holding Style,YTD,1 Years,3 Years,5 Years,10 Years,15 Years,' + '\n')
###rf.write('========== =========== ==========' + '\n' + '\n' + '\n')
rf.close()


####### Subroutine: Risk vs Reward #######
def get_riskreward_data():
     #Define temp file variable for CBF.txt in the User harry's Home folder;
     risk_reward_file = "/home/harry/risk_reward.txt"

     with open(risk_reward_file, 'r+') as risk_reward: #risk/reward data
          for line in risk_reward:
               if "Morningstar Return" in line:
                    for line in risk_reward:
                         if "	                      	" in line:
                              three_year = line
##                              rf = open('/home/harry/Desktop/Final_Data.txt', 'a')
##                              rf.write(three_year.replace(' ','').replace('\t',"").replace('\n',"").replace('\r',"") + ',')
##                              rf.close()
                              
                              five_year = risk_reward.__next__()
##                              rf = open('/home/harry/Desktop/Final_Data.txt', 'a')
##                              rf.write(five_year.replace(' ','').replace('\t',"").replace('\n',"").replace('\r',"") + ',')
##                              rf.close()

                              ten_year = risk_reward.__next__()
##                              rf = open('/home/harry/Desktop/Final_Data.txt', 'a')
##                              rf.write(ten_year.replace(' ','').replace('\t',"").replace('\n',"").replace('\r',"") + ',')
##                              rf.close()

                              overall = risk_reward.__next__()
                              rf = open('/home/harry/Desktop/Final_Data.txt', 'a')
                              rf.write(overall.replace(' ','').replace('\t',"").replace('\n',"").replace('\r',""))
                              rf.write(',')
                              rf.close()
                              break

               if "Morningstar Risk" in line:
                    for line in risk_reward:
                         if "	                      	" in line:
                              three_year = line
##                              rf = open('/home/harry/Desktop/Final_Data.txt', 'a')
##                              rf.write(three_year.replace(' ','').replace('\t',"").replace('\n',"").replace('\r',"") + ',')
##                              rf.close()

                              five_year = risk_reward.__next__()
##                              rf = open('/home/harry/Desktop/Final_Data.txt', 'a')
##                              rf.write(five_year.replace(' ','').replace('\t',"").replace('\n',"").replace('\r',"") + ',')
##                              rf.close()


                              ten_year = risk_reward.__next__()
##                              rf = open('/home/harry/Desktop/Final_Data.txt', 'a')
##                              rf.write(ten_year.replace(' ','').replace('\t',"").replace('\n',"").replace('\r',"") + ',')
##                              rf.close()

                              overall = risk_reward.__next__()
                              rf = open('/home/harry/Desktop/Final_Data.txt', 'a')
                              rf.write(overall.replace(' ','').replace('\t',"").replace('\n',"").replace('\r',"") + ',')
                              rf.close()
                              break
     #Remove the risk_reward.txt temp file
     os.remove('/home/harry/risk_reward.txt')
     return
####### End Subroutine #######

####### Subroutine: Rating #######
def get_star_rating_data():
     #Create the temporary file, star_rating.txt, in the User harry's Home folder;
     rating_file = "/home/harry/star_rating.txt"

     with open(rating_file, 'r+') as star_rating: #Morning star ratings
          for line in star_rating:
               if "r_title" in line:
                    if "r_star0" in line:
                         rf = open('/home/harry/Desktop/Final_Data.txt', 'a')
                         rf.write('0 Stars' + ',')
                         rf.close()
                    elif "r_star1" in line:
                         rf = open('/home/harry/Desktop/Final_Data.txt', 'a')
                         rf.write('1 Stars' + ',')
                         rf.close()
                    elif "r_star2" in line:
                         rf = open('/home/harry/Desktop/Final_Data.txt', 'a')
                         rf.write('2 Stars' + ',')
                         rf.close()
                    elif "r_star3" in line:
                         rf = open('/home/harry/Desktop/Final_Data.txt', 'a')
                         rf.write('3 Stars' + ',')
                         rf.close()
                    elif "r_star4" in line:
                         rf = open('/home/harry/Desktop/Final_Data.txt', 'a')
                         rf.write('4 Stars' + ',')
                         rf.close()
                    elif "r_star5" in line:
                         rf = open('/home/harry/Desktop/Final_Data.txt', 'a')
                         rf.write('5 Stars' + ',')
                         rf.close()
                    else:
                         rf = open('/home/harry/Desktop/Final_Data.txt', 'a')
                         rf.write('N/A Stars' + ',')
                         rf.close()
     #Remove the mrating.txt temp file
     os.remove('/home/harry/star_rating.txt')
     return
####### End Subroutine #######

####### Subroutine: Performance #######
def get_performance_data():
     #Create the temporary file, performance.txt, in the User charley's Home folder;
     performance_file = "/home/harry/performance.txt"

     with open(performance_file, 'r+') as performance: #risk/reward data
          for line in performance:
               if '"marks"' in line:
                    for line in performance:
                         if "[5," in line:
                              if "#28366D" in line:
                                   YTD_number = line[5:11:1]
                                   rf = open('/home/harry/Desktop/Final_Data.txt', 'a')
                                   rf.write(YTD_number.replace(' ','') + ',')
                                   rf.close()
                              else:
                                   rf = open('/home/harry/Desktop/Final_Data.txt', 'a')
                                   rf.write("'--," + "'--," + "'--," + "'--," + "'--," + "'--,")
                                   rf.close()
                                   break
                         if "[6," in line:
                              if "#28366D" in line:
                                   one_year_number = line[5:11:1]
                                   rf = open('/home/harry/Desktop/Final_Data.txt', 'a')
                                   rf.write(one_year_number.replace(' ','') + ',')
                                   rf.close()
                              else:
                                   rf = open('/home/harry/Desktop/Final_Data.txt', 'a')
                                   rf.write("'--," + "'--," + "'--," + "'--," + "'--,")
                                   rf.close()
                                   break
                         if "[7," in line:
                              if "#28366D" in line:
                                   three_year_number = line[5:11:1]
                                   rf = open('/home/harry/Desktop/Final_Data.txt', 'a')
                                   rf.write(three_year_number.replace(' ','') + ',')
                                   rf.close()
                              else:
                                   rf = open('/home/harry/Desktop/Final_Data.txt', 'a')
                                   rf.write("'--," + "'--," + "'--," + "'--,")
                                   rf.close()
                                   break
                         if "[8," in line:
                              if "#28366D" in line:
                                   five_year_number = line[5:11:1]
                                   rf = open('/home/harry/Desktop/Final_Data.txt', 'a')
                                   rf.write(five_year_number.replace(' ','') + ',')
                                   rf.close()
                              else:
                                   rf = open('/home/harry/Desktop/Final_Data.txt', 'a')
                                   rf.write("'--," + "'--," + "'--,")
                                   rf.close()
                                   break
                         if "[9," in line:
                              if "#28366D" in line:
                                   ten_year_number = line[5:11:1]
                                   rf = open('/home/harry/Desktop/Final_Data.txt', 'a')
                                   rf.write(ten_year_number.replace(' ','') + ',')
                                   rf.close()
                              else:
                                   rf = open('/home/harry/Desktop/Final_Data.txt', 'a')
                                   rf.write("'--," + "'--,")
                                   rf.close()
                                   break
                         if "[10," in line:
                              if "#28366D" in line:
                                   fifteen_year_number = line[5:11:1]
                                   rf = open('/home/harry/Desktop/Final_Data.txt', 'a')
                                   rf.write(fifteen_year_number.replace(' ',''))
                                   rf.close()
                              else:
                                   rf = open('/home/harry/Desktop/Final_Data.txt', 'a')
                                   rf.write("'--,")
                                   rf.close()
                                   break
     #Remove the performance.txt temp file
     os.remove('/home/harry/performance.txt')
     return
####### End Subroutine #######

####### Subroutine: Categories, Bond, & Foreign #######
def get_holding_style_data():
     #Create the temporary file, holdingstyle.txt, in the User harry's Home folder;
     style_file = "/home/harry/holdingstyle.txt"

     with open(style_file, 'r+') as holdingstyle: #for the Foreign % and Bond % of the Fund
          for line in holdingstyle:

               if "var HoldingStyle_Box" in line:

                    no_garbage_line = re.sub(r'\W+', ' ', line)

                    exclude_these_strings = ("0", "BColor ", "Labels ", "HLabels ", "VLabels ", "Label ", "FColor ", "28366D ", "7c87a7 ", "c8cbd9 ", "ffffff", "FFFFFF ", " var ", "HoldingStyle_Box ", "Type ", "Names ", "Value ", "Blend ", "Growth ", "Names ", "Large ", "Mid ", "Small ", "Grids ", "")
                    exclusions = '|'.join(exclude_these_strings)
                    less_crap_line = re.sub(exclusions, '', no_garbage_line) #this is a string

                    less_crap_line = re.sub(exclusions, '', no_garbage_line) #this is a string

                    the_truncated_line = less_crap_line.split() #this is a list

                    #Re-adjust the_truncated_line to full length, if missing Zeros are present
                    if the_truncated_line[2] == 'Order':
                         the_truncated_line.insert(2, '0')
                    if the_truncated_line[5] == 'Order':
                         the_truncated_line.insert(5, '0')
                    if the_truncated_line[8] == 'Order':
                         the_truncated_line.insert(8, '0')
                    if the_truncated_line[11] == 'Order':
                         the_truncated_line.insert(11, '0')
                    if the_truncated_line[14] == 'Order':
                         the_truncated_line.insert(14, '0')
                    if the_truncated_line[17] == 'Order':
                         the_truncated_line.insert(17, '0')
                    if the_truncated_line[20] == 'Order':
                         the_truncated_line.insert(20, '0')
                    if the_truncated_line[23] == 'Order':
                         the_truncated_line.insert(23, '0')

                    max_item = max((int(num), i) for i, num in enumerate(the_truncated_line[2::3])) #find the max value of every 3rd element list

                    if max_item[1] == 0:
                         rf = open('/home/harry/Desktop/Final_Data.txt', 'a')
                         rf.write("Large Value" + ',')
                         rf.close()
                    if max_item[1] == 1:
                         rf = open('/home/harry/Desktop/Final_Data.txt', 'a')
                         rf.write("Large Blend" + ',')
                         rf.close()
                    if max_item[1] == 2:
                         rf = open('/home/harry/Desktop/Final_Data.txt', 'a')
                         rf.write("Large Growth" + ',')
                         rf.close()
                    if max_item[1] == 3:
                         rf = open('/home/harry/Desktop/Final_Data.txt', 'a')
                         rf.write("Mid Value" + ',')
                         rf.close()
                    if max_item[1] == 4:
                         rf = open('/home/harry/Desktop/Final_Data.txt', 'a')
                         rf.write("Mid Blend" + ',')
                         rf.close()
                    if max_item[1] == 5:
                         rf = open('/home/harry/Desktop/Final_Data.txt', 'a')
                         rf.write("Mid Growth" + ',')
                         rf.close()
                    if max_item[1] == 6:
                         rf = open('/home/harry/Desktop/Final_Data.txt', 'a')
                         rf.write("Small Value" + ',')
                         rf.close()
                    if max_item[1] == 7:
                         rf = open('/home/harry/Desktop/Final_Data.txt', 'a')
                         rf.write("Small Blend" + ',')
                         rf.close()
                    if max_item[1] == 8:
                         rf = open('/home/harry/Desktop/Final_Data.txt', 'a')
                         rf.write("Small Growth" + ',')
                         rf.close()
     #Remove the holdingstyle.txt temp file
     os.remove('/home/harry/holdingstyle.txt')
     return
####### End Subroutine #######

####### Subroutine: Categories, Bond, & Foreign #######
#Get data for Category distributions, Foreign %, & Bond %
def get_cbf_data():
     #Define temp file variable for CBF.txt in the User harry's Home folder;
     cbf_file = "/home/harry/CBF.txt"

     with open(cbf_file, 'r+') as cbf: #for the Foreign % and Bond % of the Fund
          for line in cbf:
               #Bond & Non US Stock; numbers are in the same line;
               if "'Non US Stock" in line:
                    only_numbers_and_period_in_line = re.sub(r'([^\d.])+', '', line)
                    rf = open('/home/harry/Desktop/Final_Data.txt', 'a')
                    rf.write(only_numbers_and_period_in_line.strip() + "%" + ',')
                    rf.close()
               if "'Bond" in line:
                    only_numbers_and_period_in_line = re.sub(r'([^\d.])+', '', line)
                    rf = open('/home/harry/Desktop/Final_Data.txt', 'a')
                    rf.write(only_numbers_and_period_in_line.strip() + "%" + ',')
                    rf.close()

               if "Asset Distribution" in line: #this is a key-o%sff value [MDISX & BEGRX]
                    for line in cbf:
                         if "Non US Stock" in line and "assetalloc" not in line:
                              only_numbers_and_period_in_line = re.sub(r'([^\d.])+', '', line)
                              rf = open('/home/harry/Desktop/Final_Data.txt', 'a')
                              rf.write(next(cbf).strip() + "%" + ',')
                              rf.close()
                         if "Bond" in line and "assetalloc" not in line:
                              only_numbers_and_period_in_line = re.sub(r'([^\d.])+', '', line)
                              rf = open('/home/harry/Desktop/Final_Data.txt', 'a')
                              rf.write(next(cbf).strip() + "%" + ',')
                              rf.close()

     with open(cbf_file, 'r+') as cbf: #for the Category Weight %s of the Fund
          for line in cbf:
               if "Fund Weight" in line: #this is a key-off value 
                    for line in cbf:
                         #Category distributions; numbers are in the next line;
                         if "Basic Materials" in line:
                              rf = open('/home/harry/Desktop/Final_Data.txt', 'a')
                              rf.write(next(cbf).strip() + "%" + ',')
                              rf.close()
                         if "Consumer Cyclical" in line:
                              rf = open('/home/harry/Desktop/Final_Data.txt', 'a')
                              rf.write(next(cbf).strip() + "%" + ',')
                              rf.close()
                         if "Financial Services" in line:
                              rf = open('/home/harry/Desktop/Final_Data.txt', 'a')
                              rf.write(next(cbf).strip() + "%" + ',')
                              rf.close()
                         if "Real Estate" in line:
                              rf = open('/home/harry/Desktop/Final_Data.txt', 'a')
                              rf.write(next(cbf).strip() + "%" + ',')
                              rf.close()
                         if "Communication Services" in line:
                              rf = open('/home/harry/Desktop/Final_Data.txt', 'a')
                              rf.write(next(cbf).strip() + "%" + ',')
                              rf.close()
                         if "Energy" in line.strip() and " " not in line.strip():
                              rf = open('/home/harry/Desktop/Final_Data.txt', 'a')
                              rf.write(next(cbf).strip() + "%" + ',')
                              rf.close()
                         if "Industrials" in line.strip() and " " not in line.strip():
                              rf = open('/home/harry/Desktop/Final_Data.txt', 'a')
                              rf.writ
#               de(next(cbf).strip() + "%" + ',')
                              rf.close()
                         if "Technology" in line:
                              rf = open('/home/harry/Desktop/Final_Data.txt', 'a')
                              rf.write(next(cbf).strip() + "%" + ',')
                              rf.close()
                         if "Consumer Defensive" in line:
                              rf = open('/home/harry/Desktop/Final_Data.txt', 'a')
                              rf.write(next(cbf).strip() + "%" + ',')
                              rf.close()
                         if "Healthcare" in line:
                              rf = open('/home/harry/Desktop/Final_Data.txt', 'a')
                              rf.write(next(cbf).strip() + "%" + ',')
                              rf.close()
                         if "Utilities" in line.strip() and " " not in line.strip():
                              rf = open('/home/harry/Desktop/Final_Data.txt', 'a')
                              rf.write(next(cbf).strip() + "%" + ',')
                              rf.close()
     #Remove the CBF.txt temp file
     os.remove('/home/harry/CBF.txt')
     return
####### End Subroutine #######

####### Subroutine: Ask User If There Is More Research To Do #######
def ask_user_if_more_research():
     #Ask User regarding desire to research another ETF, Stock, or Mutual Fund
     #Note that only a 1-letter case-insensitive response is valid for 'yes'
     ask_again = input("Would You Like To Check Another ETF, Stock, or Mutual Fund? ('y' or 'n'): ")

     #Middleman variable to provide case insensitivity to 'yes' response
     match = re.match("y", ask_again, re.IGNORECASE)

     if match is None:
          os.rename('/home/harry/Desktop/Final_Data.txt','/home/harry/Desktop/Final_Data.csv')
          print(('\n' + '\n' + '\n' + 'Your Data Is Located At ~Desktop/Final_Data.csv [comma delimited].'))
          print(("I Now Retire To My Humble Abode."))
          print(("Thank You, User, For This Opportunity."))
          input("Press ENTER To Quit, As I Have.")
          sys.exit(0)
     if match is not None:
          search_type_control = True
          mega_loop_control = True
     else:
          os.rename('/home/harry/Desktop/Final_Data.txt','/home/harry/Desktop/Final_Data.csv')
          print(('\n' + '\n' + '\n' + "Very Well."))
          print(('Your Data Is Located At ~Desktop/Final_Data.csv [comma delimited].'))
          input("Press ENTER To Quit, As I Have. Goodbye.")
          sys.exit(0)
####### End Subroutine #######

####### Subroutine: Check If Market Ticker is Invalid #######
def check_ticker_validity():

     #One of Two Global Variables [the other is search_type]
     global market_ticker
     #One of Two Global Variables [the other is search_type]

     initial_url = urllib.request.urlopen("http://quote.morningstar.com/quote/quote.aspx?ticker=%s" % (market_ticker))
     final_url = initial_url.geturl()
     if "TickerNotFound" in final_url:
          print('\n' + "That Market Ticker Doesn't Exist, You Nit." + '\n')
          market_ticker = " "
     else:
          pass
####### End Subroutine #######


#Dah Mega-Loop is Active
mega_loop_control = True
#Dah Mega-Loop is Active


####### Start Mega-Loop #######
while mega_loop_control:

     #Set search_type_control is Active
     search_type_control = True
     #Set search_type_control is Active

     while search_type_control:

          search_type = input('Would you like to search for an ETF [ETF], Stock [S], or Mutual Fund [MF] (required): ')

          if search_type == "ETF" or search_type == "etf" or search_type == "S" or search_type == "s" or search_type == "MF" or search_type == "mf":
               break
          elif search_type != "ETF" and search_type != "etf" and search_type != "S" and search_type != "s" and search_type != "MF" and search_type != "mf":
               print(('\n' + "Try Telling Me That Again, Boyo." + '\n'))
          else:
               print(('\n' + '\n' + '\n' + "User, You Do Not Know What You Want."))
               print(("I Now Retire To My Humble Abode."))
               input("Press ENTER To Quit.")
               sys.exit(0)
     #End Of The search_type_control

     if search_type in ( 'ETF', 'etf' ):
          #Ask & receive user input for ETF market ticker
          market_ticker = input('Please provide the ticker code of the ETF (required): ')

          check_ticker_validity()
          if market_ticker == " ":
               continue
          else:
               pass

       #Write ETF name//ticker to file
          rf = open('/home/harry/Desktop/Final_Data.txt', 'a')
          rf.write('ETF: ' + market_ticker + ',')
          rf.close()

       #Create Temporary Files For SubRoutines
          ##...for the risk/reward...
          #Get the HTML source code from Morningstar's URL for Fund
          website = urllib.request.urlopen("http://performance.morningstar.com/RatingRisk/fund/rating-risk.action?t=%s&ops=clear" % (market_ticker)).read()
          #Save Website to risk_reward.txt [file will be removed when the data is retrieved]
          strip_write = open('/home/harry/risk_reward.txt', 'w') #Create-Write the stripped website data
          strip_write.write(strip_tags(website.decode('utf-8')))
          strip_write.close()

          ##...for the star rating...
          #Get the HTML source code from Morningstar's URL for Fund
          website = urllib.request.urlopen("http://performance.morningstar.com/fund/ratings-risk.action?t=%s" % (market_ticker)).read()
          #Save Website to star_rating.txt [file will be removed when the data is retrieved]
          strip_write = open('/home/harry/star_rating.txt', 'w') #Create-Write the stripped website data
          strip_write.write(website.decode('utf-8'))
          strip_write.close()

          ##...for the performance data...
          #Get the HTML source code from Morningstar's URL for Fund
          website = urllib.request.urlopen("http://performance.morningstar.com/Performance/fund/trailing-total-returns.action?t=%s&ops=clear" % (market_ticker)).read()
          write_webfile = open('/home/harry/performance.txt', 'w')
          write_webfile.write(website.decode('utf-8'))
          #Save Website to performance.txt [file will be removed when the data is retrieved]
          strip_write = open('/home/harry/performance.txt', 'w') #Create-Write the stripped website data
          strip_write.write(strip_tags(website.decode('utf-8')))
          strip_write.close()

          ##...for the holding style data...
          #Get the HTML source code from Morningstar's URL for Fund
          website = urllib.request.urlopen("http://portfolios.morningstar.com/fund/summary?t=%s" % (market_ticker)).read()
          #Save Website to holdingstyle.txt [file will be removed when the data is retrieved]
          strip_write = open('/home/harry/holdingstyle.txt', 'w') #Create-Write the stripped website data
          strip_write.write(strip_tags(website.decode('utf-8')))
          strip_write.close()

          ##...for the holding style data...
          ## //// needs to be filled in


          #Run the SubRoutines for data-gathering
          get_star_rating_data()

          get_riskreward_data()

          get_holding_style_data()

#          get_cbf_data()

          get_performance_data()


          #Terminate the txt-written line for kosher .csv conversion
          rf = open('/home/harry/Desktop/Final_Data.txt', 'a')
          rf.write('\n')
          rf.close()

          #Run the SubRoutine to ask if there is more research
          ask_user_if_more_research()
     #######End Section: ETF#######


     #####Start Section: User Selected a Stock.#####
     elif search_type in ( 'S', 's' ):
          #Ask & receive user input for ETF market ticker
          market_ticker = input('Please provide the ticker code of the Stock (required): ')

          check_ticker_validity()
          if market_ticker == " ":
               continue
          else:
               pass
       
       #Write Stock name//ticker to file
          rf = open('/home/harry/Desktop/Final_Data.txt', 'a')
          rf.write('St: ' + market_ticker + ',')
          rf.close()

       #Create Temporary Files For SubRoutines
          ##...for the star rating...
          #Get the HTML source code from Morningstar's URL for Fund
          website = urllib.request.urlopen("http://quote.morningstar.com/stock/s.aspx?t=%s" % (market_ticker)).read()
          #Save Website to star_rating.txt [file will be removed when the data is retrieved]
          strip_write = open('/home/harry/star_rating.txt', 'w') #Create-Write the stripped website data
          strip_write.write(website.decode('utf-8'))
          strip_write.close()

          ##...for the performance data...
          #Get the HTML source code from Morningstar's URL for Fund
          website = urllib.request.urlopen("http://performance.morningstar.com/Performance/fund/trailing-total-returns.action?t=%s&ops=clear" % (market_ticker)).read()
          write_webfile = open('/home/harry/performance.txt', 'w')
          write_webfile.write(website.decode('utf-8'))
          #Save Website to performance.txt [file will be removed when the data is retrieved]
          strip_write = open('/home/harry/performance.txt', 'w') #Create-Write the stripped website data
          strip_write.write(strip_tags(website.decode('utf-8')))
          strip_write.close()


          #Run the SubRoutines for data-gathering
          get_star_rating_data()

          #Place in empty filler for proper .csv spacing
          rf = open('/home/harry/Desktop/Final_Data.txt', 'a')
          rf.write("'--,'--,'--,")
          rf.close()

          get_performance_data()

          #Terminate the txt-written line for kosher .csv conversion
          rf = open('/home/harry/Desktop/Final_Data.txt', 'a')
          rf.write('\n')
          rf.close()

          #Run the SubRoutine to ask if there is more research
          ask_user_if_more_research()
     #######End Section: Stock#######


     #####Start Section: User Selected a Mutual Fund.#####
     elif search_type in ( 'MF', 'mf' ):
          #Ask & receive user input for ETF market ticker
          market_ticker = input('Please provide the ticker code of the Mutual Fund (required): ')

          check_ticker_validity()
          if market_ticker == " ":
               continue
          else:
               pass
       
       #Write Mutual Fund name//ticker to file
          rf = open('/home/harry/Desktop/Final_Data.txt', 'a')
          rf.write('MF: ' + market_ticker + ',')
          rf.close()

       #Create Temporary Files For SubRoutines
          ##...for the risk/reward...
          #Get the HTML source code from Morningstar's URL for Fund
          website = urllib.request.urlopen("http://performance.morningstar.com/RatingRisk/fund/rating-risk.action?t=%s&ops=clear" % (market_ticker)).read()
          #Save Website to risk_reward.txt [file will be removed when the data is retrieved]
          strip_write = open('/home/harry/risk_reward.txt', 'w') #Create-Write the stripped website data
          strip_write.write(strip_tags(website.decode('utf-8')))
          strip_write.close()

          ##...for the star rating...
          #Get the HTML source code from Morningstar's URL for Fund
          website = urllib.request.urlopen("http://performance.morningstar.com/fund/ratings-risk.action?t=%s" % (market_ticker)).read()
          #Save Website to star_rating.txt [file will be removed when the data is retrieved]
          strip_write = open('/home/harry/star_rating.txt', 'w') #Create-Write the stripped website data
          strip_write.write(website.decode('utf-8'))
          strip_write.close()

          ##...for the performance data...
          #Get the HTML source code from Morningstar's URL for Fund
          website = urllib.request.urlopen("http://performance.morningstar.com/Performance/fund/trailing-total-returns.action?t=%s&ops=clear" % (market_ticker)).read()
          write_webfile = open('/home/harry/performance.txt', 'w')
          write_webfile.write(website.decode('utf-8'))
          #Save Website to performance.txt [file will be removed when the data is retrieved]
          strip_write = open('/home/harry/performance.txt', 'w') #Create-Write the stripped website data
          strip_write.write(strip_tags(website.decode('utf-8')))
          strip_write.close()

          ##...for the holding style data...
          #Get the HTML source code from Morningstar's URL for Fund
          website = urllib.request.urlopen("http://portfolios.morningstar.com/fund/summary?t=%s" % (market_ticker)).read()
          #Save Website to holdingstyle.txt [file will be removed when the data is retrieved]
          strip_write = open('/home/harry/holdingstyle.txt', 'w') #Create-Write the stripped website data
          strip_write.write(strip_tags(website.decode('utf-8')))
          strip_write.close()

          ##...for the cbf data...
          ## //// needs to be filled in

          #Run the SubRoutines for data-gathering
          get_star_rating_data()

          get_riskreward_data()

          get_holding_style_data()

#          get_cbf_data()

          get_performance_data()

          #Terminate the txt-written line for kosher .csv conversion
          rf = open('/home/harry/Desktop/Final_Data.txt', 'a')
          rf.write('\n')
          rf.close()

          #Run the SubRoutine to ask if there is more research
          ask_user_if_more_research()
     #######End Section: Mutual Fund#######

#   + '\n'
#   + ','
