def onerror(function):
    def __onerror__(*a,**b):
        try:
            return function(*a,**b)
        except HTTP, e:
            import os
            status=int(e.status.split(' ')[0])
            filename=os.path.join(request.folder,'views/onerror%i.html'%status)
            if os.access(filename,os.R_OK):
                e.body=open(filename,'r').read()
            e.body="test"
            raise e
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
    return __onerror__