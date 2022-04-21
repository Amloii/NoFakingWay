from urlextract import URLExtract

def URL_filter(text):

     extractor = URLExtract()
     if extractor.has_urls(text):
          result_dict = {}
          result_dict['suspicious'] = True
          result_dict['filter_failed'] = 'URL'
          result_dict['motive'] = "Given text contains some URL"  
     else: 
          result_dict = {}
          result_dict['suspicious'] = False
          result_dict['filter_failed'] = ''
          result_dict['motive'] = ''
          
     return result_dict