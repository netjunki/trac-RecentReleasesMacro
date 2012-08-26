# vim: expandtab
import re, time
from StringIO import StringIO

from genshi.builder import tag

from trac.core import *
from trac.wiki.formatter import format_to_html, format_to_oneliner
from trac.util import TracError
from trac.util.text import to_unicode
from trac.web.chrome import Chrome, add_stylesheet, ITemplateProvider
from trac.wiki.api import parse_args, IWikiMacroProvider
from trac.wiki.macros import WikiMacroBase
from trac.wiki.model import WikiPage
from trac.wiki.web_ui import WikiModule

class RecentReleasesMacro(WikiMacroBase):
    """A macro to extract content from other pages and display as a table
    """
    implements(IWikiMacroProvider,ITemplateProvider)

    def expand_macro(self, formatter, name, content, args):
        data = parse_args(content)[1]
        self.log.debug("EXPAND ARGUMENTS: %s " % data)
        req = formatter.req
        wiki = formatter.wiki
        db = self.env.get_db_cnx()
        releasedata = {}
        fields = []
        first = True
        for page in wiki.get_pages(data["prefix"]):
            self.log.debug("PAGE: %s " % page)
            if page == data["prefix"]:
                continue
            else:
                sql  = "SELECT tag from tags where name = '%s'" % page
                cs = db.cursor()
                cs.execute(sql)
            
                row = cs.fetchone()
                if row == None:
                    continue
                pagetag = row[0]
                if pagetag != data["tag"]:
                    continue
                version = page.split("/")[-1]
                releasedata[version] = []
            sql  = "SELECT text from wiki where name = '%s' order by version desc limit 1" % page
            cs = db.cursor()
            cs.execute(sql)
            
            row = cs.fetchone()
            if row == None:
                continue
            text = row[0].split("----")[0]
            self.log.debug("CONTENT: %s" % text)
            lines = text.split("\n")
            for line in lines:
                if line.startswith("||"):
                    parts = line.split("||")
                    releasedata[version].append(parts[2])
                    if first:
                        fields.append(parts[1])
            first = False
        self.log.debug("DATA: %s" % releasedata)
        if data.has_key("subset"):
            subset = data["subset"].split(" ")
            self.log.debug("SUBSET: %s" % subset)
            newfields = []
            newreleasedata = {}
            for x in subset:
                x = int(x)-1
                newfields.append(fields[x])
                for release in releasedata:
                    if not newreleasedata.has_key(release):
                        newreleasedata[release] = []
                    newreleasedata[release].append(releasedata[release][x])
            fields = newfields
            releasedata = newreleasedata
            self.log.debug("FIELDS: %s" % fields)
            self.log.debug("DATA: %s" % releasedata)
        
        if data.has_key("limit"):
            limit = int(data["limit"])
        else:
            limit = len(releasedata.keys())
        template = Chrome(self.env).load_template('recentreleases.html',method='xhtml')
        data = Chrome(self.env).populate_data(req, {"context": formatter.context, "env": self.env, "fields":fields,"releasedata":releasedata,"limit":limit})
        rendered_result = template.generate(**data)
        return rendered_result

    # ITemplateProvider methods
    def get_templates_dirs(self):
        from pkg_resources import resource_filename
        return [resource_filename('recentreleases', 'templates')]

    def get_htdocs_dirs(self):
        from pkg_resources import resource_filename
        return [resource_filename('recentreleases', 'htdocs')]
