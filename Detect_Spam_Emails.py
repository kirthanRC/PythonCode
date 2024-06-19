from email.parser import Parser 
import os
import re

#function to check whether the suspects email id is present in the list of email id
def check_suspects_in_recipents(list_emailId, dict_suspects):
    bool_emailId_present = False
    #Loop through email ids present in list of email ids
    for emailID in list_emailId:
        for key, value in dict_suspects.items():
            if emailID in value:
                bool_emailId_present = True
    #returns true if email id of suspect present else return false
    return bool_emailId_present

#function to get email ids present in string in_str
def check_email_id(in_str):
    list_email_id = []
    #regular expression to search email id
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    for values in regex.finditer(in_str):
        list_email_id.append(values.group())
    
    #returns list of email ids present in in_str
    return list_email_id

#the function emails_between returns 
def emails_between(suspects):
    #__file__ will give the file path of current python file, we are using this file directory to get enron_email_corpus folder path 
    #as file is stored in same location
    Efile = os.path.join(os.path.dirname(__file__),"enron_email_corpus")
    #creating Praser object
    parser =  Parser()
    suspected_email_list =[]
    for path, root, files in os.walk(Efile):
        #looping through each files present in enron_email_corpus folder
        for email_file in files:
            file_path = os.path.join(path,email_file)
            try:
                    
                read_email = open(file_path, "r").read()                
                email_message = parser.parsestr(read_email)
                to_recipients = check_email_id(email_message.get("To")) if  email_message.get("To") != None else []
                
                if len(to_recipients) <= 20:
                    #extract sender email id
                    from_mailid =  check_email_id(email_message.get("From")) if  email_message.get("From") != None else []
                    #check whether from email id is present in suspect
                    from_check = check_suspects_in_recipents(from_mailid,suspects)  
                    if from_check:
                        #check whether from email id is present in suspect
                        to_check = check_suspects_in_recipents(to_recipients,suspects) 
                        if to_check:
                            #append email message to output list
                            suspected_email_list.append(email_message)  
            except:
                print("Error reading email ",file_path)
                continue

    return suspected_email_list


red_flags = {
"lay-k": ["kenneth.lay@enron.com", "klay@enron.com"],
"skilling-j": ["skilling@enron.com", "jeff.skilling@enron.com"]
}

list_out = emails_between(red_flags)
for emailmessage in list_out:
    print(emailmessage.get("From"), " and ", emailmessage.get("To"))