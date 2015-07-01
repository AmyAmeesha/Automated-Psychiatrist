from django.shortcuts import render
from main.models import *
from main.forms import *
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Template, Context
from django.template.loader import get_template
from django.template import Context, RequestContext 
from django.shortcuts import render_to_response,render
# Create your views here.
import csv
import matplotlib.pyplot as plt
import math

path_male = 'male.csv'
path_female = 'female.csv'
male_words = []
male_valence_mean = []
male_valence_std = []
male_arousal_mean = []
male_arousal_std = []
female_words = []
female_valence_mean = []
female_valence_std = []
female_arousal_mean = []
female_arousal_std = []

def create_data():
    """
    Adds all the data from csv files to the respective lists
    """
    global male_words
    with open(path_male) as f:
        mreader = csv.reader(f)
        for row in mreader:
            male_words.append(row[0])
            male_valence_mean.append(float(row[1]))
            male_valence_std.append(float(row[2]))
            male_arousal_mean.append(float(row[3]))
            male_arousal_std.append(float(row[4]))
    global female_words
    with open(path_female) as f:
        freader = csv.reader(f)
        for row in freader:
            female_words.append(row[0])
            female_valence_mean.append(float(row[1]))
            female_valence_std.append(float(row[2]))
            female_arousal_mean.append(float(row[3]))
            female_arousal_std.append(float(row[4]))

def word_list(string):
    """
    Extract indiviuals words from the string s
    """
#Problem1: if word appearing here is not in the same form of verb in the ANEW list
#           eg. 'winning' should be same as 'win'
#Problem2: Need to strip punctuation marks fromt the words
#           eg. 'win!' should be same as 'win'
    words = string.split()
    return words

def anew_word_list(sex, speech):
    """
    Returns a list of indices of words in csv file that are in the entered speech.
    """
    all_words = word_list(speech)
    relevant = []
    if sex == 'male':
        for word in all_words:
            if word in male_words:
                relevant.append(male_words.index(word))
        return relevant
    
    elif sex == 'female':
        for word in all_words:
            if word in female_words:
                relevant.append(female_words.index(word))
        return relevant
                
def total_valence(sex,indices_list):
    """
    Returns mean of valence by applying statistic mean of normal distributed data
    """
    num_sum = 0
    den_sum = 0
    if sex == 'male':
        for i in indices_list:
            num_sum = num_sum + (male_valence_mean[i]/male_valence_std[i])
            den_sum = den_sum + (1/male_valence_std[i])
        return (num_sum/den_sum)

    elif sex == 'female':
        for i in indices_list:
            num_sum = num_sum + (female_valence_mean[i]/female_valence_std[i])
            den_sum = den_sum + (1/female_valence_std[i])
        return (num_sum/den_sum)
    
def total_arousal(sex,indices_list):
    """
    Returns mean of arousal by applying statistic mean of normal distributed data
    """
    num_sum = 0
    den_sum = 0
    if sex == 'male':
        for i in indices_list:
            num_sum = num_sum + (male_arousal_mean[i]/male_arousal_std[i])
            den_sum = den_sum + (1/male_arousal_std[i])
        return (num_sum/den_sum)

    elif sex == 'female':
        for i in indices_list:
            num_sum = num_sum + (female_arousal_mean[i]/female_arousal_std[i])
            den_sum = den_sum + (1/female_arousal_std[i])
        return (num_sum/den_sum)

def get_theta(valence,arousal):
    x=valence-5
    y=arousal-5 
    theta = math.atan(y*1.0/x) / (2*math.pi) * 360
    if x < 0:
        theta += 180
    if theta < 0:
        theta += 360
    return theta 
    
def visualize(valence,arousal):
    plt.figure()
    ax = plt.gca()
    ax.plot([valence-5],[arousal-5], marker='o', color='r')
    ax.set_xlim([-5,5])
    ax.set_ylim([-5,5])
    plt.draw()
    plt.grid()
    plt.show()
    """
    Plot valence, arousal point on a 2D plot with valence as x-axis and arousal as y-axis.
    Require matplotlib for the same. Will update the code for it.
    """

def sex(request):
	a = get_template('t1.html')

	return HttpResponse(a.render(Context()))
	
def feeling(theta):
	if(0<=theta <22.5):
	  f="pleasure"
	else:
	  if(22.5<=theta <67.5):
	    f="excitement"
	  else:
	    if(67.5<=theta <112.5):
	      f="arousal"
	    else: 
	      if(112.5<=theta<157.5):
	        f="distress"
	      else: 
	        if(157.5<=theta<202.5):
	          f="misery"
	        else: 
	          if(202.5<=theta<247.5):
	            f="depression"
	          else: 
	            if(247.5<=theta<292.5):
	              f="sleepiness"
	            else:
	              f="contentment"
	return f			
	
def magnitude(y,x):
	return math.sqrt(x*x+y*y)	
	
def emotion(request):

	if request.POST:
		f=usrinput(request.POST)
		if f.is_valid():
			data=f.cleaned_data
			sex=data['sex']
			speech=data['feeling']
			   # sex = raw_input("Enter your sex(male/female) : ")
   			         #   speech = raw_input("How are you feeling? ")
    			create_data()
    			relevant_words = anew_word_list(sex,speech)
    			if not relevant_words :
        			return HttpResponse('The text you entered is not sufficient for your emotion analysis. Please try being more expressive')
        #input()
    			else:
        			valence = total_valence(sex,relevant_words)
        			arousal = total_arousal(sex,relevant_words)
        			al=str(arousal-5)
        			vl=str(valence-5)
        			theta = get_theta(valence, arousal)
        			f=feeling(theta)
        			m=magnitude(arousal-5,valence-5)
        			#visualize(valence,arousal)
				#tant=al/vl
				#mag=sqrt(al^2+vl^2)
				
        			#html = "<html><body>valence level is %s  and arousal level is %s.</body></html>" % (vl, al)
        			return render_to_response('t1.html', {'vl':vl,'al':al,'f':f,'m':m},context_instance=RequestContext(request))
        			#return HttpResponse(html)
        		#visualize(valence,arousal)
        #input()
	else:
		f=usrinput()
		return render(request,'main.html',{'form':f})
		
if __name__ == "__main__":
    emotion()

