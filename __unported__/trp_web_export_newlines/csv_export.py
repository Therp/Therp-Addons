# -*- coding: utf-8 -*-
import logging
import csv
from cStringIO import StringIO

from openerp.osv.orm import except_orm
from openerp.tools.translate import _
from openerp.addons.web.controllers.main import CSVExport

MODULE='trp_web_export_newlines'
IGNORE_ATTRS = ['__metaclass__', '__module__']
OVERWRITE_ATTRS = ['from_data']

def monkeypatch_class(name, bases, namespace):
    """ 
    Generic monkeypatcher based on Van Rossum
    http://mail.python.org/pipermail/python-dev/2008-January/076194.html
    """
    assert len(bases) == 1, "Exactly one base class required"
    base = bases[0]
    for name, value in namespace.iteritems():
        if  name not in IGNORE_ATTRS:
            if  hasattr(base, name) and name not in OVERWRITE_ATTRS:
                raise except_orm(
                    _('trp_osv'),
                    _(('Attr %s is already present in %s and not ' +
                      'marked for overwriting, aborting') % (base.__name__, name))
                    )
            else:
                logging.getLogger(MODULE).info(
                    'Adding attr %s to %s' % (name, base.__name__)
                    )
                setattr(base, name, value)
    return base

class TherpCSVExport(CSVExport):
    __metaclass__ = monkeypatch_class

    def from_data(self, fields, rows):
        """
        This is a duplicate of the same method in 
        openerp-web/addons/web/controllers/main.py
        The only modification is that newlines are not
        filtered out.
        """
        fp = StringIO()
        writer = csv.writer(fp, quoting=csv.QUOTE_ALL)

        writer.writerow([name.encode('utf-8') for name in fields])

        for data in rows:
            row = []
            for d in data:
                if isinstance(d, basestring):
                    ### start of modifications
                    # d = d.replace('\n',' ').replace('\t',' ')
                    d = d.replace('\t',' ')
                    ### end of modifications
                    try:
                        d = d.encode('utf-8')
                    except UnicodeError:
                        pass
                if d is False: d = None
                row.append(d)
            writer.writerow(row)

        fp.seek(0)
        data = fp.read()
        fp.close()
        return data
