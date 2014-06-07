import cgi
import webapp2
from google.appengine.ext.webapp.util import run_wsgi_app

import MySQLdb
import os

# Define your production Cloud SQL instance information.
_INSTANCE_NAME = 'cfiwebapp:events'

class GetAllEvents(webapp2.RequestHandler):
    def get(self):
        if (os.getenv('SERVER_SOFTWARE') and
            os.getenv('SERVER_SOFTWARE').startswith('Google App Engine/')):
            db = MySQLdb.connect(unix_socket='/cloudsql/' + _INSTANCE_NAME, db='cfi', user='root', passwd='root123')
        else:
            db = MySQLdb.connect(host='173.194.248.153', port=3306, db='cfi', user='root', passwd='root123')

        cursor = db.cursor()
        cursor.execute('SELECT * from events')

        # Create a list.
        eventlist = [];
        for row in cursor.fetchall():
          eventlist.append(dict([
            ('id',row[0]),
            ('name',cgi.escape(row[1])),
            ('date',cgi.escape(row[2])),
            ('time',cgi.escape(row[3])),
            ('venue',cgi.escape(row[4])),
            ('max_attendees',cgi.escape(row[5])),
            ('fb_event_id',cgi.escape(row[6])),
            ('gplus_event_id',cgi.escape(row[7]))]));

        variables = {'eventlist': eventlist}
        self.response.write(variables)
        db.close()

class GetAnEvent(webapp2.RequestHandler):
    def get(self):
        if (os.getenv('SERVER_SOFTWARE') and
            os.getenv('SERVER_SOFTWARE').startswith('Google App Engine/')):
            db = MySQLdb.connect(unix_socket='/cloudsql/' + _INSTANCE_NAME, db='cfi', user='root', passwd='root123')
        else:
            db = MySQLdb.connect(host='173.194.248.153', port=3306, db='cfi', user='root', passwd='root123')

        cursor = db.cursor()
        cursor.execute('SELECT * from events where id = ' + self.request.get('id'))

        event = dict();
        for row in cursor.fetchall():
          event['id'] = row[0];
          event['name'] = row[1];
          event['date'] = row[2];
          event['time'] = row[3];
          event['venue'] = row[4];
          event['max_attendees'] = row[5];
          event['fb_event_id'] = row[6];
          event['gplus_event_id'] = row[7];
        
        self.response.write(event)
        db.close()


class CreateMeetUpEvent(webapp2.RequestHandler):
    def get(self):
        # TODO: Create event in meetup.com using their API with the specified params. Get the event id and update that in the insert query below.
        eventId = 100;
        if (os.getenv('SERVER_SOFTWARE') and
            os.getenv('SERVER_SOFTWARE').startswith('Google App Engine/')):
            db = MySQLdb.connect(unix_socket='/cloudsql/' + _INSTANCE_NAME, db='cfi', user='root', passwd='root123')
        else:
            db = MySQLdb.connect(host='173.194.248.153', port=3306, db='cfi', user='root', passwd='root123')

        cursor = db.cursor()
        cursor.execute('insert into events(id,name,date,time,venue,max_attendees) values (' + 
             str(eventId) + ","
             "'" + self.request.get('name') + "',"
             "'" + self.request.get('date') + "',"
             "'" + self.request.get('time') + "',"
             "'" + self.request.get('venue') + "',"
             "'" + self.request.get('max_attendees') + "')")
        db.commit()
        self.response.write("written to db")
        db.close()


application = webapp2.WSGIApplication([('/getAllEvents', GetAllEvents), (r'/getEvent.*', GetAnEvent), (r'/createEvent.*', CreateMeetUpEvent)],
                              debug=True)

def main():
    application = webapp2.WSGIApplication([('/getAllEvents', GetAllEvents), (r'/getEvent.*', GetAnEvent), (r'/createEvent.*', CreateMeetUpEvent)],
                                          debug=True)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()






