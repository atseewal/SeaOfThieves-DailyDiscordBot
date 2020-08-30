# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 10:53:50 2020

@author: seewa
"""

def parse_SoT_date(SoT_date):
    import re
    from datetime import datetime
    from datetime import timedelta
    
    SoT_date = re.sub(r'(\d)(st|nd|rd|th)', r'\1', SoT_date)
    SoT_date = re.sub(r':', '', SoT_date, 1)
    SoT_date = datetime.strptime(SoT_date, '%B %d %I:%M%p')
    year_correct = datetime.now() + timedelta(days=1)
    SoT_date = SoT_date.replace(year=year_correct.year)
    
    return(SoT_date)