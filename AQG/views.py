# from msilib.schema import File
from cv2 import groupRectangles
from django.conf import settings
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth
import os
from pathlib import Path
# from django.core.files import File
from django.contrib import messages
from django.http import Http404, HttpResponse
from numpy import full
from .models import Dbms,Os,Es,FilesAdmin
# from random import randint
import random
from django.contrib.auth.decorators import login_required
from .utils import render_to_pdf
from django.template.loader import get_template
from django.views.generic import View


# Create your views here.


def home(request):
    return render(request,'home.html')


def admin(request):
    return redirect('admin/login')

def tologin(request):
    return render(request,'login.html')



def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username = username , password = password)

        if user is not None:
            auth.login(request,user)
            return redirect('dashboard')
        else:
            messages.info(request,'Wrong credential!!!Ask admin for updating your details')
            return redirect('login')

        
    else:   
        return render(request, 'login.html' )






def logout(request):
    auth.logout(request)
    return redirect('/')

@login_required(login_url='tologin')
def dashboard(request):
    
    context = {
        'file': FilesAdmin.objects.all(),
        'user' : User.objects.all()
    }
    return render(request,'dashboard.html',context)
    


def download( request,path):
    file_path = os.path.join(settings.MEDIA_ROOT,path)
    if os.path.exists():
        with open(file_path,'rb')as fh:
            response=HttpResponse(fh.read(),content_type="application/adminupload")
            response['content-Disposition']='inline;filename='+ os.path.basename(file_path)
            return response
    
    raise Http404



def downloadfromhere(request):
    context={
        'file' : FilesAdmin.objects.all()
    }
    return render(request,'download.html',context)




global_context = None;
def getdata(request):
   
    global global_context
    try:
        full_mark = request.POST['f_marks']
        pass_mark = request.POST['p_marks']
        two_mark = request.POST['No_two']
        four_mark = request.POST['No_four']
        fac = request.POST["faculty"]
        year = request.POST["year"]
        part = request.POST["part"]
        sub = request.POST["subject"]
        
        full_mark = int(full_mark)
        two_mark = int(two_mark)
        four_mark = int(four_mark)
        pass_mark = int(pass_mark)
        total_two = 2*two_mark
        total_four = 4* four_mark
        if(full_mark==(total_two+total_four)):
            if fac == "BCT":
                if year=="3":
                    if part == "II":
                        if sub=="DBMS":
                            questionsdbms= Dbms.objects.all()
                            
                            q=[i for i in questionsdbms]
                            passing= randoms(q,four_mark,two_mark)
                            
                            grpasA = passing[0]
                            grpasB = passing[1]
                            
                            context = {
                                    'questionShort': grpasA,
                                    'questionLong': grpasB,
                                    
                                    'sub': "DBMS",
                                    'pass_mark': pass_mark,
                                    'full_mark': full_mark
                                    }
                            
                            global_context = context

                            
                            
                            
                            return render(request, "output.html",context)
                            
                            
                        elif sub == "Operating System":
                            questionsos = Os.objects.all()
                            q=[i for i in questionsos]
                            passing= randoms(q,four_mark,two_mark)
                            
                            grpasA = passing[0]
                            grpasB = passing[1]
                            
                            context = {
                                    'questionShort': grpasA,
                                    'questionLong': grpasB,
                                    'full_mark': full_mark,
                                    'pass_mark': pass_mark,
                                    'sub': "Operating System"
                                    }
                            global_context = context
                            
                            
                            return render(request, "output.html",context)

                        elif sub == "Embedded System":
                            questionses = Es.objects.all()
                            q=[i for i in questionses]
                            passing= randoms(q,four_mark,two_mark)
                            
                            grpasA = passing[0]
                            grpasB = passing[1]
                            
                            context = {
                                    'questionShort': grpasA,
                                    'questionLong': grpasB,
                                    'full_mark': full_mark,
                                    'pass_mark': pass_mark,
                                    'sub': sub
                                    }
                            
                            global_context = context
                            return render(request, "output.html",context)
                    else:
                        messages.info(request,'Select valid Part!!')
                    return redirect('dashboard')
                else:
                    messages.info(request,'Select valid year!!')
                    return redirect('dashboard')

            else:
                messages.info(request,'Select valid faculty!!')
                return redirect('dashboard')
                    
        else:
            messages.info(request,'Full marks not met!!')
            return redirect('dashboard')
    except:
        messages.info(request,"Please fill all the fields to proceed!!")
        return redirect('dashboard')
    


def randoms(q,four_mark,two_mark):
    
    qn_4 = four_mark
    qn_2 = two_mark
    grpA=[]
    grpB=[]
    qn=random.shuffle(q)
    for i in q:
        if i.mark==2 and qn_2>0:
            grpA.append(i.qn)
            qn_2 -=1
        elif i.mark==4 and qn_4>0:
            grpB.append(i.qn)
            qn_4 -=1
    grpasA = []
    grpasB = []
    for items in grpA:
        grpasA.append(f"{grpA.index(items)+1}) {items}")
    for items in grpB:
        grpasB.append(f"{grpB.index(items)+1}) {items}")
    return (grpasA,grpasB)

    


                        
       



    









def get_pdf(request,*args, **kwargs):
    global global_context
    template = get_template('output.html')
    
    passingtogetpdfdata = forpdfdownload()
    grpasA=[]
    grpasA = passingtogetpdfdata[0]
    grpasB = passingtogetpdfdata[1] 
    subject = passingtogetpdfdata[2]
    pass_mark = passingtogetpdfdata[3]
    full_mark = passingtogetpdfdata[4]
    # print(grpasA)
    # print(grpasB)

    
    context = global_context
    html = template.render(context)
    pdf = render_to_pdf('output.html', context)
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = 'output_%s.pdf' %("12341231")
        content = 'inline; filename='+'%s' %(filename)
        download = request.GET.get("download")
        if download:
            content = 'attachment; filename='+'%s' %(filename)
        response['Content-Disposition'] = content
        return response
    return HttpResponse("Not found")


def forpdfdownload(context={}):
    grpasA = context.get("questionShort")
    grpasB = context.get("questionLong")
    subject = context.get("sub")
    pass_mark = context.get("pass_mark")
    full_mark = context.get("full_mark")
# print(grpasA,grpasB,subject,pass_mark,full_mark)

    

    
   
    return (grpasA,grpasB,subject,pass_mark,full_mark)

    
