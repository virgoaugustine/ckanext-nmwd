import ckan.plugins as p
from ckan.lib.base import BaseController
from ckan.common import _, c, request, response
# import ckan.lib.mailer as mailer
import smtplib
from email.mime.text import MIMEText
# from email.message import EmailMessage
import logging
# import config
import requests
import json
import pylons.config as config

logger = logging.getLogger(__name__)


class NMWDController(BaseController):
    def map(self):
        return p.toolkit.render('map.html')
    def team(self):
        return p.toolkit.render('team.html')
    def news(self):
        return p.toolkit.render('news.html')
    def faq(self):
        return p.toolkit.render('faq.html')
    def contact(self):
        return p.toolkit.render('contact.html')
    def reports(self):
        return p.toolkit.render('reports.html')
    def photos(self):
        return p.toolkit.render('photos.html')
    def events(self):
        return p.toolkit.render('events.html')  
    def contactmail(self):

        recapsecret = config.get('ckan.recaptchasecret', '')
        grecaptcharesponse=request.params.get('g-recaptcha-response', '')
        data={'secret': recapsecret,'response': grecaptcharesponse}
        # try:
        r=requests.post('https://www.google.com/recaptcha/api/siteverify',data)
        recapjson=json.loads(r.text)
        if recapjson["success"]:
            first=request.params.get('first', 'NOFIRSTNAME')
            last=request.params.get('last', 'NOLASTNAME')
            email=request.params.get('email', '')
            body=request.params.get('message', '')
            if len(email)==0 or len(body)==0:
                return p.toolkit.render('emailerror.html')
            sender = email
            # recipients = ['Stacy Timmons <stacy.timmons@nmt.edu> ','Jeri Graham <jeri.graham@nmt.edu>']
            recipients = ['Virgo <virgo.anankum@datopian.com']
            
            msg = MIMEText(body)
            msg['Subject'] = "Message from newmexicowaterdata.org contact form"
            msg['From'] = first+' '+last+' <'+sender+'>'
            msg['To'] = ", ".join(recipients)

            try:
                smtpObj = smtplib.SMTP('localhost')
                smtpObj.sendmail(sender, recipients, msg.as_string())     
                logger.debug("Successfully sent email")
            except SMTPException as e:
                logger.debug(e)
                return p.toolkit.render('emailerror.html')

            return p.toolkit.render('emailgood.html')
        else: 
               #body=request.params.get('message', '')
               logger.debug("captcha failed for "+request.environ['REMOTE_ADDR'])
              # logger.debug("FAILED MESSAGE:"+str(body))
               return p.toolkit.render('emailerror.html')

