<!DOCTYPE html>
<html>
    <head>
	<meta charset=utf-8>
	<link rel="stylesheet" href="/static/style.css">
	<%block name="meta_head">
	</%block>
    </head>
    <body>
    <div class="container">
	<div class="header">
	    <%block name="header">
	    <a href="/about">Vincent W</a>'s Thoughts and Writings

	    </%block>
	</div>

	<div class="navigation">

	    <%block name="nav">
		<ul>
		    <li><a href="/">blog</a></li>
		    <li><a href="/about">about</a></li>
		    <li><a href="/rss">rss</a></li>
		</ul>
	    </%block>

	</div>

	<div class="body">
	    <%block name="_body">
	    <article>
		<p>hello</p>
	    </article>
	    </%block>
	</div>
	<div class="footer">
	    <%block name="footer">
<p>© Copyright 2012 by Vincent w.</p>

<p>Content licensed under the Creative Commons attribution-noncommercial-sharealike License.</p>

<p>Contact me via <a href="mailto:phostu@gmail.com">mail</a>, <a href="http://weibo.com/2119986460">weibo</a>, <a href="https://github.com/vincentwv">github</a>. </p>
	    </%block>
	</div>
    </div>
    </body>
</html>

