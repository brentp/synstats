
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import os, sys
PATH = os.path.dirname(__file__)
sys.path.insert(0, PATH)
import stats
import re

char_re = re.compile(r'[,\t\s]')

class MainPage(webapp.RequestHandler):
    def get(self):
        d = {}
        tmpl = os.path.join(PATH, "templates/index.html")
        self.response.out.write(template.render(tmpl, d))

    def post(self):
        content = self.request.get('content').strip()
        data = content.replace('\r', '').split('\n')
        oe = []
        chisq = ""
        p = ""

        d = {'data': content}
        if data:
            for row in data:
                row = row.strip()
                if row[0] == '#': continue
                row = map(float, char_re.split(row))
                assert len(row) in (1, 2), row
                if len(row) == 2:
                    oe.append(row)
                elif len(row) == 1:
                    oe.append((row[0], None))
                else:
                    raise Exception("row should have either 1 or 2 values")
            if None in [r[1] for r in oe]:
                obs = [r[0] for r in oe]
                avg = sum(obs) / float(len(obs))
                exp = [avg for i in range(len(oe))]
            else:
                obs, exp = zip(*oe)
            chisq, p = stats.chisq(obs, exp)
            d['chisq'] = '%.3f' % chisq
            d['p'] = '%.4f' % p
        tmpl = os.path.join(PATH, "templates/index.html")
        self.response.out.write(template.render(tmpl, d))


application = webapp.WSGIApplication(
                                     [('/', MainPage)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
