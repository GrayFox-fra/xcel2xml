#HOST="192.168.9.1"
#USER="root"
#PASS=""
#dbb="da"
#DIR_UPLOADS="D:/programmi/Karrigell/webapps/da/files/"
#SERVER_MAIL="smtp.studiociquattro.it"
#FROMADDR="nicola@studiociquattro.it"
#TOADDRS_default="redazione@studiociquattro.it"
#TOADDRS_default="carlobazzo@syseng-p2p.it"
#loginmail="nicola@studiociquattro.it"
#passwmail="apache2005"
dir_excelxml="C:\\Python25\\web2py\\applications\\xcel2xml\\uploads\\"





		
	
		
def pagedisplay(nome):
	print """
	<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
        "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="it" xml:lang="it">

  <head>
    <title>Digital Assets</title>
    <meta http-equiv="content-type" content="text/html; charset=iso-8859-1" />
    <link rel="stylesheet" type="text/css" href="../css/login.css" title="default" media="screen" />
       </head>
        <body>
          <div id="container">
            <div id="header">
              <h1>Gestione Progetti </h1>
	      <h3> Utente: %s</h3>
			  
            </div>
            <div id="wrapper">
              <div id="content">
	      
                
                
              </div>
            </div>
            
                        <div id="footer">
                          <p>Hdemo by Syseng-p2p</p>
                        </div>
                      
                    
                
              
            
          </div>
        </body>
   
  
</html>
""" % nome
def selectfile(opzione1,len,opzione2):
	print"""
    
    <td><SELECT NAME="doc_originali" size="3"><OPTION VALUE="" SELECTED>"""
	i=0
	while i<len:
		
		chiamaop(opzione1[i],opzione2[i])
		i=i+1
	print"""
    
    
    </SELECT></td>
    
    """
def chiamaop(item1,item2):
	
	print"""
    <OPTION VALUE="%s">%s
    """ %(item1,item2)



	
