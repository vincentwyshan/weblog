<%inherit file="blog_base.mako"/>

<%block name="meta_head">
<title>${entry.title if entry else 'New entry'}</title>
<style type="text/css">
input, textarea { width: 100%; }
input[type=submit] {width:50%; display:block;margin:auto}
#entry-links a:first-child {margin:0}
#entry-links a {margin-left:10px}
#new-entry {text-align:right; padding-right:20%}
#delete-entry {color:red}
</style>
</%block>


<%block name="_body">

<div id="new-entry">
<a href="/update">New entry</a>
</div>


<form action="/update" method="POST">
%if entry:
<input name="id" type=hidden value="${entry.id}" />
%endif
<div class="clearfix">
<label for="title">Title</label>
<div class="input">
<input class="xxlarge" id="post-title" name="title" value="${entry.title if entry else ''}" />
</div>
</div>

<div class="clearfix">
<label for="tags">Tags</label>
<div class="input">
<input class="xlarge" id="post-tags" name="tags" 
    value="${','.join([tag.name for tag in entry.tags]) if entry else ''}"/>
</div>
</div>

<div class="clearfix">
<label for="tags">Summary</label>
<div class="input">
<textarea class="xxlarge" rows=3 id="post-summary"
name='summary'/>${entry.summary if entry else ''}</textarea>
</div>
</div>

<div class="clearfix">
<label for="content">Content</label>
<div class="input">
<textarea class="xxlarge" rows=30 id="post-content" name='content'/>${entry.content if entry else ''}</textarea>
</div>
</div>

<div class="actions">
<input type="submit" class="btn primary" value="${'update' if entry else 'insert'}"/>
</div>
</form>
%if entry:
<br>
<form action="/delete" method="GET">
    <input hidden value="${entry.id}" name="post_id"/>
    <input type="submit" id="delete-entry" value="delete entry"/>
</form>
%endif

<hr>
<div id="entry-links">
%for e in entries:
<a href="/update?id=${e.id}">${e.title or repr(e)}</a>
%endfor
</div>

</%block>


