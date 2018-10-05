# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 13:33:38 2018
reference:
    To get commentary: http://www.cricbuzz.com/
    To get speeds for each bowler: https://www.icc-cricket.com/
    To get the service URL: https://stackoverflow.com/questions/43315307/python-web-scraping-unable-to-find-all-the-tags-in-a-webpage
    To get field position: https://en.wikipedia.org/wiki/Fielding_(cricket)/
"""

import requests
import pandas as pd
from pathlib import Path

COLUMN_NAMES=['Commentary','Runs','Delivery_Length','Delivery_Line','Shot_Type','Run/NoRun','Bowler_Type','Bowler_Name',
              'Avg_Ball_Speed','MatchID','Dismissal_Type','Beaten/NotBeaten','Home_Away','Good_Bad_Shot',
              'Opponent','Stadium','Shot_Zone','Delivery_Number','Toss','TossDecision','D/N']
dfmain=pd.DataFrame(columns=COLUMN_NAMES)
playername=input("Enter player name: ")
if Path('D:/knowledge/college docs/DSP/Project_1/New/'+playername+'.xlsx').exists():
    print('File found')
    df1= pd.read_excel('D:/knowledge/college docs/DSP/Project_1/New/'+playername+'.xlsx')
    #print(df1)
    dfmain=df1.copy()
else:
    df1=None
    print('File not found')
player_country=input("Enter the player country: ")
matchidstr=input("Enter the match ids: ")
if ',' in matchidstr:
    matchids=matchidstr.split(',')
else:
    matchids=matchidstr
for matchid in matchids:    
    print(matchid)
    df= pd.DataFrame(columns=COLUMN_NAMES)

#json response
    jobj = requests.get('http://push.cricbuzz.com/match-api/'+matchid+'/commentary-full.json').json()

#gets match id from json response
    matchid=jobj['id']
#gets stadium name
    stadium=jobj['venue']['name']
#gets country name
    country= jobj['venue']['country']
#gets opponent name
    if player_country.upper() not in jobj['team1']['name'].upper():
        opponent=jobj['team1']['name']
    else:
        opponent=jobj['team2']['name'].upper()
#if toss is won by player's team value is 1 or else 0    
    if player_country.upper() in jobj['toss']['winner'].upper():
        toss=1
    else:
        toss=0
#if toss is won by player's team what desicion is taken
    decision= jobj['toss']['decision']
    
    if jobj['dn'] is False:
        day_night= 'D'
    else:
        day_night= 'DN'
#gets full commentary of the match    
    all_comments = jobj['comm_lines'] 

#delivery length
    full_toss = ['full toss']
    full=['full','fullish','fuller','pitched up','overpitch','bat down','up on the stumps',
          'up to the stumps','dab','dig','dug out','block','negates ','dead bat','dead-bat','sweep','defend','yorker','tossed up',
          'tosses it up','darted on']
    good_length=['length','good length','straight','on to the pads','pad','punch','drive','square cut','flick',
                 'backward point','flatter']
    short=['short','bouncer','back of a length','shortish','shoulders arms','shouldering arms','pull','hook',
           'let it pass','let it go','lets it go','left alone','seeing it through']
    del_length_dic= {'FullToss':full_toss,'Short':short,'Full':full,'GoodLength':good_length}

#delivery line
    wicket_to_wicket = ['on off','stumps','middle','leg','pad','into the body','dab','dug out','block',
                        'dig','glance','flick','angled into','full and straight','punched back','on the off stump',
                        'top of off','base of off','within the sticks']
    outside_stumps = ['wide of off','cover','outside off', 'around off','past the defence',
                      'widish','shouldering arms','shoulders arms','let it pass','let it go','lets it go','cover','square cut',
                      'left alone','seeing it through','miss','shape away','backward point','square','cramped for room','wide one'
                      ,'sees width','close to off','lets it pass','fourth stump','close to off','short and wide','some width','wider of off']
    del_line_dic= {'wicket_to_wicket':wicket_to_wicket,'outside_stumps':outside_stumps}

#beaten or not beaten
    not_beaten = ['defend','block','clips it','knocks it','tap','drives it','tuck','dug out','flick','negates ','dead bat','dead-bat','hit back',
                  'push','punch','played back','negotiate','dig','cut','dab','defen','fence','negates the ball','glance','flick','square on the leg-side',
                  'square drive','pull','hook','mid-wicket','sweep','drive','mid-on','mid-off','to cover','towards the cover','swept',
                  'edge','square cut','backward point']
    beaten = ['beaten','past the outside edge','let it pass','let it go','shouldering arms','lets it go','edge','carry through','ball whizzes past',
              'splice off the bat','left alone','seeing it through','shoulders arms','miss','corridor of uncertainty','play and a miss']
    beaten_dic= {'beaten':beaten,'not_beaten':not_beaten}

#shot type
    defensive_shot = ['defensive shot','dab','defen','dug out','block','negates the ball','pushed back','punched back','played back','dig']
    glance=['glance']
    flick=['flick','square on the leg-side']
    late_cut=['down to third man','third man']
    pull_hook=['pull','hook','mid-wicket']
    sweep=['swept','slog','sweep']
    drive=['drive','mid-on','mid-off','to cover','towards the cover','square drive']
    edge=['edge','splice off the bat']
    cut=['square cut','backward point']
    no_shot=['beat','past the outside edge','let it pass','let it go','shouldering arms','lets it go','carry through',
             'ball whizzes past','left alone','seeing it through','shoulders arms','miss','ignore','lets it pass',
             'leave comfortably','jammed out',"can't make any contact"]
    shot_type_dic= {'Glance':glance,'Flick':flick,'Late_Cut':late_cut,
                'Pull_hook':pull_hook,'Sweep':sweep,'Edge':edge,'Cut':cut,'Drive':drive,
                'Defensive_shot':defensive_shot,'No_shot':no_shot}
    
    #Zones
    fine_leg = ['fine leg', 'long leg','fine-leg', 'long-leg']
    square_leg=['square leg', 'leg gully', 'short leg','square-leg', 'leg-gully', 'short-leg']
    midwicket=['silly mid on','mid wicket','mid-wicket','cow cover']
    long_on=['mid on', 'long on','mid-on', 'long-on']
    long_off=['mid off','long off','mid-off','long-off']
    cover=['extra cover','cover','silly mid off','extra-cover']
    point=['silly point','point', 'gully','silly-point']
    third_man=['third man', 'slip','third-man']
    shot_zone_dic= {'FineLeg':fine_leg,'SquareLeg':square_leg,'Midwicket':midwicket,'LongOn':long_on,'LongOff':long_off,
                     'Cover':cover,'Point':point,'ThirdMan':third_man}

#bowler type
#fetch list of bowlers
    bowlers_dic={}
    bowlers=jobj['players']
    for bowler in bowlers:
        if 'bowl_style' in bowler:
            bowlers_dic[bowler['name']]=bowler['bowl_style'].lower()
            #bowlers_dic
        
#runs list
    lstrun=[1,2,3,4,5,6]
    
#to get delivery number
    del_count=0    
    for comment in all_comments[:]:
        if 'comm' in comment:
            if 'to '+playername in str(comment['comm']):
                del_count=del_count+1
    delivery_number=del_count
    i=0
    for comment in all_comments[:]:
        if 'comm' in comment:
            if 'to '+playername in str(comment['comm']):
                #to fetch bowler name
                if 'to' in str(comment['comm']):
                    bowler_name=str(comment['comm']).split(' to')[0].strip()
                else:
                    bowler_name=None
                        
                # to fetch bowler type
                if bowler_name in bowlers_dic.keys():
                    bowler_type=bowlers_dic[bowler_name]
                else:
                    bowler_type=None
                
                #to fetch runs
                if '<b>four</b>' in str(comment['comm']).lower():
                    runs=4
                elif '<b>six</b>' in str(comment['comm']).lower():
                    runs=6
                elif '<b>single</b>' in str(comment['comm']).lower():
                    runs=1
                elif ('<b>wide</b>' in str(comment['comm']).lower()) or '<b>wides</b>' in str(comment['comm']).lower():
                    runs='wide'
                elif '<b>no ball</b>' in str(comment['comm']).lower():
                    runs='noball'
                elif 'run' in str(comment['comm']):
                    wrd=str(comment['comm']).split('run')[0]
                    if ',' in wrd:
                        runstr=wrd.split(',')[1].strip()
                        if runstr =='1':
                            runs=1
                        elif runstr =='2':
                            runs=2
                        elif runstr =='3':
                            runs=3
                        elif runstr =='no':
                            runs=0
                        else:
                            runs=None
                    else:
                        runs=None
                else:
                    runs=None
                #run or no run
                if runs ==0:
                    run_norun='norun'
                elif runs in lstrun:
                    run_norun='run'
                else:
                    run_norun='norun'
            
                #to fectch bowl speed
                if (',' in str(comment['comm'])) and (str(comment['comm']).count(',')>1) :
                    bs=str(comment['comm']).split(',')[2]
                    if 'kph' in bs.lower():
                        bowl_speed_str=bs.split('kph')[0]
                        bowl_speed=bowl_speed_str.split(' ')[-1].strip()
                    else:
                        bowl_speed=None
                else:
                    bowl_speed=None
                
                #Dismissal Type
                if "that's out!!" in str(comment['comm']).lower():
                    if '</b>' in str(comment['comm']):
                        dismissal_type=str(comment['comm']).split('</b>')[1]
                    else:
                        dismissal_type=None
                else:
                    dismissal_type=None
            
                #delivery length type
                delivery_length='Unknown'
                for k,v in del_length_dic.items():
                    for j in v:
                        if j in str(comment['comm']).lower():
                            delivery_length=k
                            break
                    if delivery_length != 'Unknown':
                        break
                #delivery line type  
                delivery_line='Unknown'
                for a,b in del_line_dic.items():
                    for q in b:
                        if q in str(comment['comm']).lower():
                            delivery_line=a
                            break
                    if delivery_line != 'Unknown':
                        break
                
                #shot type  
                shot_type= 'Unknown'
                for h,l in shot_type_dic.items():
                    if h=='Defensive_shot':
                        if ((runs==0) and (('push' in str(comment['comm']).lower()) or ('tap' in str(comment['comm']).lower()))):
                            shot_type=h
                            break
                        else:
                            for q in l:
                                if q in str(comment['comm']).lower():
                                    shot_type=h
                                    break
                    else:
                        for q in l:
                            if q in str(comment['comm']).lower():
                                shot_type=h
                                break
                        if shot_type != 'Unknown':
                            break
                    
                #shot type  
                beaten_notbeaten='Unknown'
                if (runs is not None) and (runs in ['1','2','3','4','5','6']):
                    beaten_notbeaten='not_beaten'
                else:
                    for u,o in beaten_dic.items():
                        for q in o:
                            if q in str(comment['comm']).lower():
                                beaten_notbeaten=u
                                break
                        if beaten_notbeaten != 'Unknown':
                            break
                
                #home or away
                if country.upper().strip() == player_country.upper():
                    home_away='home'
                else:
                    home_away='away'
                #clasify shot as good(if runs scores is >=2) or bad (if runs scores is <2)  
                if ((runs is not None) and (runs not in ['wide','noball']) and (runs >=1) 
                and (shot_type.lower().strip() in ['glance','flick','late_cut','pull_hook','sweep','cut','drive']) and (dismissal_type is None) ):
                    good_bad_shot='good'
                else:
                    good_bad_shot='bad'
                
                #delivery length type
                shot_zone='Unknown'
                for g,t in shot_zone_dic.items():
                    for j in t:
                        if j in str(comment['comm']).lower():
                            shot_zone=g
                            break
                    if shot_zone !='Unknown':
                        break
                    
                
                if runs not in ['wide','noball']:
                    #delivery number
                    delivery_number=delivery_number-1
                    df.loc[i]=[comment['comm'],runs,delivery_length,delivery_line,shot_type,run_norun,bowler_type,
                           bowler_name,bowl_speed,matchid,dismissal_type,beaten_notbeaten,home_away,good_bad_shot,opponent,
                           stadium,shot_zone,delivery_number,toss,decision,day_night]
                    i=int(i)+1
    #Appending new data to main dataframe, hence getting data from different matches
    dfmain=dfmain.append(df)
#write to a excel file at the specified location
writer = pd.ExcelWriter('D:/knowledge/college docs/DSP/Project_1/New/'+playername+'.xlsx')
dfmain.to_excel(writer)
writer.save()

