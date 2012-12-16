<%inherit file="blog_base.mako" />

<%block name="meta_head">
<title>Blog | Vincent W's Thoughts and Writings</title>
</%block>


<%block name="_body">


%for post in posts:

<div class="entry-overview">
    <div class="date">${post.date.strftime('%b %d, %Y')}</div>
    <div class="detail">
	<h1><a href="/post/${post.url}">${post.content_title}</a></h1>
	<div class="summary">${post.summary}</div>
    </div>
    <div class="tags">
	%for tag in post.tags:
	<span class="post-tag"><a href="">${tag.name}</a></span>
	%endfor 
    </div>
</div>

%endfor


<div class="pagination">
    %if page_num > 0:
	<span><a class="prev" href="/page/${page_num-1}" >Previous</a></span>
    %else:
	<span class="disabled"><a class="prev">Previous</a></span>
    %endif
    -
    <strong>${page_num+1}</strong>
    -
    %if max_page_num > page_num:
	<span><a class="next" href="/page/${page_num+1}" >Next</a></span>
    %else:
	<span class="disabled"><a class="next">Next</a></span>
    %endif
</div>
    
</%block>
