# python
import shutil
import stat
import warnings
import re
import codecs
import os
import logging
from random import random
from subprocess import Popen, PIPE
import urllib2
import socket

# django
from django.template.loader import get_template
from django.template import Context, Template, RequestContext
from django.http import HttpResponse
from django.conf import settings
from django.contrib.sites.models import RequestSite

PDF_FILE_ROOT = getattr(settings, 'PDF_FILE_ROOT', '/tmp')

__version__ = '0.1'

def _run_wkhtmltopdf_command(input_filename, output_filename,
                             header_filename=None,
                             footer_filename=None,
                             **extra_options):
    assert os.path.isfile(input_filename),\
      "%s does not exist" % input_filename
    assert os.path.isdir(os.path.dirname(output_filename)), \
      "%s does not exist" % os.path.dirname(output_filename)
    parameters = dict(input_filename=input_filename,
                      output_filename=output_filename)
    
    command = "wkhtmltopdf  -q "

    #--margin-bottom %(margin_bottom)s    

    if header_filename:
        assert os.path.isfile(header_filename)
        parameters = dict(parameters, 
                          header_filename=header_filename,
                          margin_bottom='60mm',
                         )
        command += "--header-html  %(header_filename)s "
        
    if footer_filename:
        assert os.path.isfile(footer_filename)
        parameters = dict(parameters, 
                          footer_filename=footer_filename,
                          margin_bottom='50mm',
                         )
        command += "--footer-html  %(footer_filename)s "
        
    for key in extra_options:
        command += "--%s %s " % (key, extra_options[key])
    
    command += "--encoding utf-8 %(input_filename)s %(output_filename)s"
    command = command % parameters
    #print command
    logging.debug("COMMAND: %s" % command)
    proc = Popen(command, shell=True, stdout=PIPE, stderr=PIPE)
    return proc.wait()
    

def pdf(request, template_path, context, filename,
        template_footer=None, template_header=None, **extra_options):
    """Renders a pdf using the given template and a context dict"""
       
    template = get_template(template_path)
    context = Context(context)
    
    context_instance=RequestContext(request)
    context_instance.update(context)
    html = template.render(context_instance)
    
    def is_template_path(s):
        return not s.count('\n') and s.endswith('.html')
    
    html_header = None
    if template_header:
        if isinstance(template_header, basestring):
            if is_template_path(template_header):
                template_header = get_template(template_header)
            else:
                template_header = Template(template_header)
        html_header = template_header.render(context_instance)

    html_footer = None
    if template_footer:
        if isinstance(template_footer, basestring):
            if is_template_path(template_footer):
                template_footer = get_template(template_footer)
            else:
                template_footer = Template(template_footer)
        html_footer = template_footer.render(context_instance)
    
    # next we need to download all the relevant image srcs
    if not getattr(settings, 'DEBUG_PDF', False):
        html = _download_static_resources_and_rewrite_html(
          request,
          html, 
          PDF_FILE_ROOT)
    
    randstr = str(int(random() * 100000))
    input_filename = os.path.join(PDF_FILE_ROOT, 
                                 '%s__%s' % (randstr, 
                                             filename.replace('.pdf','.html')))
    output_filename = os.path.join(PDF_FILE_ROOT, filename)
    
    # remove potential old HTML version
    if os.path.isfile(output_filename):
        os.remove(output_filename)
        
    header_filename = None
    if html_header:
        header_filename = os.path.join(PDF_FILE_ROOT,
                                       '%s__header.html' % randstr)
        codecs.open(header_filename, 'w', 'utf8').write(html_header)
        
    footer_filename = None
    if html_footer:
        footer_filename = os.path.join(PDF_FILE_ROOT,
                                       '%s__footer.html' % randstr)
        codecs.open(footer_filename, 'w', 'utf8').write(html_footer)
    
    codecs.open(input_filename, 'w', 'utf8').write(html)
    result = None
    try:
        output = _run_wkhtmltopdf_command(input_filename, output_filename,
                                          header_filename=header_filename,
                                          footer_filename=footer_filename,
                                          **extra_options
                                         )
        if output == 0:
            #result = codecs.open(output_filename, 'rb', 'utf8').read()
            result = file(output_filename, 'rb').read()
        else:
            result = None
        
    finally:
        
        if True: # change to False if you want to debug
            if os.path.isfile(input_filename):
                os.remove(input_filename)
                
            if os.path.isfile(output_filename):
                os.remove(output_filename)
                
            if header_filename and os.path.isfile(header_filename):
                os.remove(header_filename)
                
            if footer_filename and os.path.isfile(footer_filename):
                os.remove(footer_filename)
                
    if getattr(settings, 'DEBUG_PDF', False):
        return HttpResponse(html)
    
    if result:
        response = HttpResponse(result, mimetype='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
        return response
    
    return HttpResponse(html)
    
    
src_regex = re.compile('src=["\']([^"\']+)["\']')
href_regex = re.compile('href=["\']([^"\']+\.css)["\']')
def _download_static_resources_and_rewrite_html(request, html, save_dir):
    site = RequestSite(request)
    base_url = 'http://%s' % site.domain
    
    def replacer(match):
        path = match.groups()[0]
        if path.startswith('/'):
            if settings.DEBUG or site.domain in ('localhost', '127.0.0.1'):
                # If you're running in a development mode 
                # (e.g. ./manage.py runserver) you won't be able to download as
                # it's single thread and that one thread is busy running this
                # main request that needs the PDF.
                fullpath = os.path.join(settings.MEDIA_ROOT, path[1:])
            else:
                fullpath = base_url + path
        elif path.startswith('http'):
            fullpath = path
        else:
            fullpath = os.path.join(settings.MEDIA_ROOT, path)
            
        basename = os.path.basename(path)
        if os.path.isfile(os.path.join(save_dir, basename)) and \
          os.stat(os.path.join(save_dir, basename))[stat.ST_SIZE]:
            #warnings.warn("Reusing existing image %s" % basename)
            return match.group().replace(path, basename)
        elif fullpath.startswith('http://'):
            socket.setdefaulttimeout(5)
            req = urllib2.Request(fullpath)
            out = open(os.path.join(save_dir, basename), 'w')
            try:
                out.write(urllib2.urlopen(req).read())
            except urllib2.URLError:
                if settings.DEBUG:
                    raise
                warnings.warn("Unable to download URL: %s" % fullpath)
                logging.error("Unable to download URL: %s" % fullpath, exc_info=True)
            finally:
                out.close()
        elif os.path.isfile(fullpath):
            # copy it 
            shutil.copyfile(fullpath,
                            os.path.join(save_dir, basename))
            return match.group().replace(path, basename)
        else:
            warnings.warn("Could not find %s" % fullpath)
            
        return match.group()
    
    html = href_regex.sub(replacer, html)
    html = src_regex.sub(replacer, html)
    
    return html

