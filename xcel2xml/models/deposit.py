# try something like
import datetime
T.force('xcel2xml_it')
now=datetime.date.today()
#now=now.strftime("%d-%m-%Y")
deposit=SQLDB("sqlite://deposit.db")
deposit.define_table('archivio',
                SQLField('nome_operatore'),
                SQLField('file','upload'),
                SQLField('cliente'),SQLField('filename'),SQLField('filexml'),
            SQLField('data','date',default=now))
#deposit.archivio.nome_operatore.requires=IS_NOT_EMPTY()
deposit.archivio.file.requires=IS_NOT_EMPTY()
#f,em=str(T('%d-%m-%Y')),T('Invalid Date')

deposit.archivio.data.requires=IS_DATE(T('%d-%m-%Y'),\
error_message=T("Formato corretto: gg-mm-aaaa"))