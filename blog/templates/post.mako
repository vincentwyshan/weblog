<%inherit file="base.mako"/>

<form action="/post" method="POST">
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
<label for="category">Category</label>
<div class="input">
<input class="xlarge" id="post-category" name="category" value="${entry.category.name if entry else ''}" />
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
<label for="content">Content</label>
<div class="input">
<textarea class="xxlarge" rows=30 id="post-content" name='content'/>${entry.content if entry else ''}</textarea>
</div>
</div>
<div class="actions">
<input type="submit" class="btn primary" value="提交"/>
</div>
</form>
