
# Kirthan Rama Chandra, 17-04-2024
# Student id : 123101451
# Description:
# This Python program implements a simple plagiarism detector based on the attribute counting approach. 
# It analyzes Python programs to compute attribute counts for seven different metrics and calculates similarity correlation scores between pairs of programs.

import tokenize
import os

#CodeProfiler class - object used to calculates attribute metrices for given python file and get correlation score
class CodeProfiler():
    #init function intialize the attribute set
    def __init__(self,progpath):
        self.metrics = {"unique operators":0, "unique operands" :0,
                       "total operators":0, "total operands": 0, 
                       "code lines":0, "names used":0,
                       "control statements":0}
        self.path = progpath
        self.profile()

    #profile function read the program code and get values for each metric in attribute set
    def profile(self):
        attribute_type = {"operators":["OP"], "operands" :["NUMBER","STRING"], 
                           "new lines":["NEWLINE"], "names":["NAME"]}
        dict_operator = {}
        dict_operand ={}
        list_names = []
        control_words = ["if","for","while"]
        stop_words_names = ["if","for","while","else","elif"] 
        codelines_count, controlsmt_count,mult_comment  = 0,0,0

        #tokenizing python code
        with tokenize.open(self.path) as f:
            tokens = tokenize.generate_tokens(f.readline)
            #looping through each token to get required count for each metric
            for token in tokens:
                token_string = token.string.strip()
                token_name = tokenize.tok_name[token.type]                     
                if token_name.upper() in attribute_type["operators"]:
                    dict_operator[token_string] = 1 if token_string not in dict_operator.keys() else dict_operator[token_string]+1
                elif token_name.upper() in attribute_type["operands"] :
                    if not(token_string.strip()[0:3] == "'''" and token_string.strip()[-3:] == "'''"):
                        dict_operand[token_string] = 1 if token_string not in dict_operand.keys() else dict_operand[token_string]+1
                    else:
                        mult_comment +=1
                elif token_name.upper() in attribute_type["new lines"]:
                    codelines_count +=1
                elif (token_name.upper() in attribute_type["names"]) and (token_string in control_words):
                    controlsmt_count +=1
                elif token_name.upper() in attribute_type["names"] and (token_string not in list_names) and (token_string not in stop_words_names):
                    list_names.append(token_string)     

        #updating metric count
        self.metrics["unique operators"] = len(dict_operator) 
        self.metrics["unique operands"] = len(dict_operand)  
        self.metrics["total operators"] = sum(dict_operator.values())   
        self.metrics["total operands"] = sum(dict_operand.values())  
        self.metrics["code lines"] = codelines_count - mult_comment
        self.metrics["names used"] = len(list_names)
        self.metrics["control statements"] = controlsmt_count
            
    #Correlation function compares metrics of two python codes and calculate correlation score and returns the score
    def correlation(self,otherprog):
        prog_profile = self.metrics
        otherprog_obj = CodeProfiler(otherprog)
        otherprog_profile = otherprog_obj.metrics
        attribute_wind_imp = {"unique operators":[3,5], "unique operands" :[3,5],
                       "total operators":[5,6], "total operands": [5,6], 
                       "code lines":[3,5], "names used":[2,3],
                       "control statements":[1,2]}
        score = 0
        #loop through each attribute
        for key,value in prog_profile.items():
            a = prog_profile[key]
            b = otherprog_profile[key]
            #calculate the attribute difference, comparing it with attribute window and calculating score using
            #attribute importance and difference
            diff = abs(a - b)
            if diff <= attribute_wind_imp[key][0]:
                score += abs((attribute_wind_imp[key][1]- diff))            
        return score

#inspect function finds the correlation score between each program file present in subdripath 
#and print the file pairs in decreasing order of score where correlation score >= cutoff 
def inspect(subdirpath, cutoff):
    dict_pair_score = {}
    str_python_file_ext = ".py"
    for path, root, files in os.walk(subdirpath):
        #extracting files with .py extension
        py_files =[files[i] for i in range(len(files)) if files[i].endswith(str_python_file_ext)] 

        #looping through each program files and calculating the score and storing it in dictionary       
        for i in range(0, len(py_files)):
            obj_curr_codeprofiler = CodeProfiler(os.path.join(path,py_files[i]))
            for j in range(i+1, len(py_files)):
                score = obj_curr_codeprofiler.correlation(os.path.join(path,py_files[j]))
                dict_pair_score[py_files[i]+" - "+ py_files[j]] = score
    
    #sorting based on score
    sorted_out_dict = dict(sorted(dict_pair_score.items(), key=lambda item: item[1],reverse=True))
    
    #printing program pairs and score where score >= cutoff
    print(f"The program pairs with score greater than of equal to {cutoff} are :")
    for key,value in sorted_out_dict.items():
        if value >= cutoff:
            print(f"{key} {value}") 
