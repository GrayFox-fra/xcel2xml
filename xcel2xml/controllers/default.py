#from applications.xcel2xml.modules.const2 import dir_excelxml
from applications.xcel2xml.modules.excelread import readexcel,createxml
import os,os.path,urllib
dir_excelxml=os.path.join(request.folder,'uploads/')
@onerror
def index():
    try:
        
        T.force('xcel2xml_it')
        #response.flash=T('Welcome to xcel2xml')
        response.menu=[['Home',True,URL(r=request,f='index')],
                       ['Upload Excel',False,URL(r=request,f='upload_file')],
                       ['Archivio',False,URL(r=request,f='archive')]]
        #path=dir_excelxml
        #path=request.application+'/uploads/'
        
        #lista=os.listdir(path)
        #listoffiles=[]
        #for file in lista:
        #    if re.search (r".*\.xls",file):
            #print """<tr><td>%s</td><td><INPUT TYPE=RADIO NAME="scegliexcel" VALUE="%s" CHECKED ></td></tr>"""%(file,file)
        #        listoffiles.append(file)
        records=deposit().select(deposit.archivio.ALL)
        tt=[]
        tt.append(TR(TH('File Excel'),TH('Cliente'),TH('Operatore'),TH('Converti')))
        for ff in records:
            tt.append(TR(ff.filename,ff.cliente,ff.nome_operatore,INPUT(_type='radio',_name='scegliexcel',_value=ff.id,\
            _CHECKED=True)))
        form=FORM(TABLE(*tt),INPUT(_type='submit',_value='Invia'))
        if form.accepts(request.vars,session):
            session.id_fileexcel=form.vars.scegliexcel
            redirect(URL(r=request,f='step2') )
              
        return dict(form=form)
    except Exception:
        import os,gluon.restricted
        e=gluon.restricted.RestrictedError(function.__name__)
        SQLDB.close_all_instances(SQLDB.rollback)
        ticket=e.log(request)
        filename=os.path.join(request.folder,'views/onerror.html')
        if os.access(filename,os.R_OK):
            body=open(filename,'r').read()
        else:
            body="""<html><body><h1>Interno Error</h1>Ticket inviato:
                <a href="/admin/default/ticket/%(ticket)s" target="_blank">
                %(ticket)s</a></body></html>"""
        body=body % dict(ticket=ticket)
        raise HTTP(200,body=body)        

def upload_file():
    ### create an insert form from the table
    T.force('xcel2xml_it')
    response.menu=[['Home',False,URL(r=request,f='index')],
                   ['Upload Excel',True,URL(r=request,f='upload_file')],
                   ['Archivio',False,URL(r=request,f='archive')]]
    form=SQLFORM(deposit.archivio,fields=['nome_operatore','file','cliente','data'],\
    submit_button=T('Submit'))
    #form.components[0].components[4].components[1].components[0].attributes['_value'] = T("Invia") 
    if request.vars.file!=None:
        form.vars.filename=(request.vars.file.filename).strip()
    ### if form correct perform the insert
    if form.accepts(request.vars,session):
        #response.flash='Inserito! Dal Menu Home per iniziare la conversione'
        session.flash="Inserito!" 
        redirect(URL(r=request,f='index'))
    elif form.errors:
        response.flash="Errore"
    
    #records=SQLTABLE(deposit().select(deposit.archivio.nome_operatore,deposit.archivio.filename))
    return dict(form=form)

def step2():
    
    T.force('xcel2xml_it')
    response.menu=[['Home',False,URL(r=request,f='index')],
                   ['Upload Excel',False,URL(r=request,f='upload_file')],
                   ['Archivio',False,URL(r=request,f='archive')]]
    #import gluon.contrib.simplejson as sj
    #response.headers['Content-Type']='text/json'
    id_fileexcel=session.id_fileexcel
    riga=0
    #RESPONSE['Content-type']='text/json'
    record=deposit(deposit.archivio.id==id_fileexcel).select(deposit.archivio.ALL)
    fileexcel=record[0].file
    file_realname=record[0].filename
    nomefile=dir_excelxml+urllib.unquote(fileexcel)
    #nomefile_realname=dir_excelxml+urllib.unquote(file_realname)
    #nomefile=dir_excelxml+fileexcel
    #riga=int(riga)
    copia=[]
    while riga<4:
        xl = readexcel(nomefile,riga)
        sheetnames = xl.worksheets()
        colonne=xl.variables(sheetnames[0])
        copia.append(colonne)
        riga=riga+1
    #simboli_col=[A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,Y,X,Z]
    j=0
    tt=[]
    for col in copia:
        tt.append(TR(col,INPUT(_type='radio',_name='sceglicol',_value=str(j),_CHECKED=True)))
        j=j+1
    form=FORM(TABLE(TR(TH('Colonne'),TH('Scegli')),*tt),INPUT(_type='submit',_value='Invia'))
    if form.accepts(request.vars,session):
        session.filename=nomefile
        session.file_realname=fileexcel
        session.riga=form.vars.sceglicol
        redirect(URL(r=request,f='step3') )
    elif form.errors:
        response.flash="Compilazione errata!"
    
    
    return dict(form=form)
    
        
def step3():
    
    T.force('xcel2xml_it')
    response.menu=[['Home',False,URL(r=request,f='index')],
                   ['Upload Excel',False,URL(r=request,f='upload_file')],
                   ['Archivio',False,URL(r=request,f='archive')]]
    #id_fileexcel=request.vars.idfile
    riga=int(session.riga)
    #record=deposit(deposit.archivio.id==id_fileexcel).select(deposit.archivio.ALL)
    #fileexcel=record[0].file
    nomefile=session.filename
    xl = readexcel(nomefile,riga)
    sheetnames = xl.worksheets()
    colonne=xl.variables(sheetnames[0])
    
    j=0
    tt=[]
    
    tt.append(TR(TH('Tipo Immagine',_colspan='8'),TH('Nome Campo'),TH('Cartella')))
    tt.append(TR(TD(HR(),_colspan='12')))
    while j<3:
        tt.append(TR('tif',INPUT(_type='radio',_name='scegli_img'+str(j),_value='tif'),\
        'jpg',INPUT(_type='radio',_name='scegli_img'+str(j),_value='jpg'),\
       'psd',INPUT(_type='radio',_name='scegli_img'+str(j),_value='psd'),\
    'eps',INPUT(_type='radio',_name='scegli_img'+str(j),_value='eps'),\
    SELECT(_name='campo'+str(j),*[OPTION(col.encode('latin-1'),_value=col) for col in colonne]),\
    INPUT(_type='text',_name='folder'+str(j),_value='alte')))
        j=j+1
    
    form=FORM(TABLE(*tt),INPUT(_type='submit',_value=T('Submit')),_name='test',)
    
    
    if form.accepts(request.vars,session):
        session.tipo_img1=form.vars.scegli_img0
        session.tipo_img2=form.vars.scegli_img1
        session.tipo_img3=form.vars.scegli_img2
        session.img1=form.vars.campo0
        session.img2=form.vars.campo1
        session.img3=form.vars.campo2
        session.folder1=form.vars.folder0
        session.folder2=form.vars.folder1
        session.folder3=form.vars.folder2
        
        
        redirect(URL(r=request,f='step4') )
    elif form.errors:
        response.flash="form is invalid!"
    return dict(form=form)
    

def step4():
           
    T.force('xcel2xml_it')
    response.menu=[['Home',False,URL(r=request,f='index')],
                   ['Upload Excel',False,URL(r=request,f='upload_file')],
                   ['Archivio',False,URL(r=request,f='archive')]]
    nomefile=session.filename
    id_fileexcel=session.id_fileexcel
    file_realname=session.file_realname
    riga=int(session.riga)
    tipo_img1=session.tipo_img1
    tipo_img2=session.tipo_img2
    tipo_img3=session.tipo_img3
    col_img1=session.img1
    col_img2=session.img2
    col_img3=session.img3
    folder_img1=session.folder1
    folder_img2=session.folder2
    folder_img3=session.folder3
    images=[]
    if tipo_img1:
        images.append(tipo_img1)
        images.append(col_img1)
        images.append(folder_img1)
    else:
        images.append('no')
        images.append(0)
        images.append("")
    if tipo_img2:
        images.append(tipo_img2)
        images.append(col_img2)
        images.append(folder_img2)
    else:
        images.append('no')
        images.append(0)
        images.append("")
    if tipo_img3:
        images.append(tipo_img3)
        images.append(col_img3)
        images.append(folder_img3)
    else:
        images.append('no')
        images.append(0)
        images.append("")
    #col=request.vars.col
    #if col==None:
        #col=""
    
    #bool_img=request.vars.bool_img
    #if bool_img==None:
        #bool_img="0"
    
    #nomefile=dir_excelxml+urllib.unquote(fileexcel)
    #riga=int(riga)
    #xl = readexcel(nomefile,riga)
    #sheetnames = xl.worksheets()
    file_realname=file_realname.strip('xls')+'xml'
    
    #testo="File correttamente generato: "+nomefile_out
    #a=dict(testo=testo)
    #riga_letta=[riga]
    #a['rigaletta']=riga_letta
    createxml(nomefile,riga,images)
    deposit(deposit.archivio.id==id_fileexcel).update(filexml=file_realname)
    response.flash='File correttamente archiviato'
    redirect(URL(r=request,f='archive'))
    return dict()
            

def archive():
    T.force('xcel2xml_it')
    response.menu=[['Home',False,URL(r=request,f='index')],
                   ['Upload Excel',False,URL(r=request,f='upload_file')],
                   ['Archivio',True,URL(r=request,f='archive')]]
    records=deposit().select(deposit.archivio.ALL)
    
    tt=[]
    tt.append(TR(TH('Id'),TH('File Excel'),TH('Cliente'),TH('Operatore'),TH('Data'),TH('File XML')))
    for ff in records:
        lbl_xml=ff.filename.strip('xls')+'xml'
        datait=deposit.archivio.data.formatter(ff.data) 
        tt.append(TR(A(ff.id,_href=URL(r=request,f='update/%s'%(ff.id))),ff.filename,ff.cliente,ff.nome_operatore,datait,A(lbl_xml,_href=URL(r=request,f='download/%s'%(ff.filexml)))))
    table=TABLE(*tt)
    return dict(table=table)

def download():
    import os
    filename=os.path.join(request.folder,'uploads/','%s' % request.args[0])
    return response.stream(open(filename,'rb'))

def update():
    response.menu=[['Home',False,URL(r=request,f='index')],
                   ['Upload Excel',False,URL(r=request,f='upload_file')],
                   ['Archivio',False,URL(r=request,f='archive')]]
    id=int(request.args[0])
    record=deposit(deposit.archivio.id==id).select()[0]
    form=SQLFORM(deposit.archivio,record,deletable=True,submit_button='Invia',delete_label='Cancella')
    if form.accepts(request.vars,session): 
        response.flash='Fatto!'        
        redirect(URL(r=request,f='archive'))
    return dict(form=form)