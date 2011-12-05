<%inherit file="base.mako"/>

<%block name="css">
<style type="text/css">
    #post-page {
    }
    #post-top {
        border-bottom: 1px dotted;
        padding : 10px 0 10px;
    }
    .document {
        margin-top:10px;
        font-family: Georgia, "Bitstream Charter", serif;
        padding:0 20px 0 20px;
    }
    .post-header {
        background: #eee;
        text-align: center;
        -webkit-border-radius: 3px;
         -moz-border-radius: 3px;
              border-radius: 3px;
        min-height: 30px;
        line-height: 30px;
    }
    #categories ul {
        margin-bottom:0px;
    }
    #tags {
        padding-left:19px;
    }

</style>
</%block>


<div class="span10">
%for entry in entries:
<div class="post-header">
<h3 id="post-header-${entry.id}"><a href="/${entry.date.year}/${entry.date.month}/${entry.id}">${entry.title}</a></h3>
</div>
<%
    import datetime
%>
<%def name="createspan(name)">
<span class="label success">${name}</span>
</%def>
<span class="label">${datetime.datetime.fromtimestamp(entry.timestamp).strftime("%b %d %Y %H:%M:%S")}</span>
${''.join([createspan(t.name) for t in entry.tags])}
<%
    from docutils.core import publish_parts
    content = publish_parts(entry.content, writer_name='html')['html_body']
%>
${content.replace('literal-block', 'literal-block prettyprint') | n,trim}

%endfor
</div>


<div class="span4">
<h5>Categories</h5>
<div id="categories">
<ul>
%for cat in categories:
<li>
${cat.name}
</li>
%endfor 
</ul>
</div>

<h5>Tags</h5>
<p id="tags">
%for tag in tags:
<span class="label">${tag.name}</span>
%endfor
</p>
</div>


