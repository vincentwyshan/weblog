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

</style>
</%block>



<div id="post-page" class="span10">
<div id="post-top">
<h3 id="post-title">
    ${entry.title}
</h3>
<%
    import datetime
%>
<%def name="createspan(name)">
<span class="label success">${name}</span>
</%def>
<span class="label">${datetime.datetime.fromtimestamp(entry.timestamp).strftime("%b %d %Y %H:%M:%S")}</span>
${''.join([createspan(t.name) for t in entry.tags])}
</div>
<%
    from docutils.core import publish_parts
    content = publish_parts(entry.content, writer_name='html')['html_body']
%>
${content.replace('literal-block', 'literal-block prettyprint') | n,trim}
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


