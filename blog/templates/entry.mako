<%inherit file="base_new.mako"/>

<%block name="contentleft">
                    <!-- post -->
                    <div class="" id="post-${entry.id}">

                        <div class="post-title">
                            <h1>
                                <a href="/${entry.date.year}/${entry.date.month}/${entry.id}" rel="bookmark">${entry.title}</a>
                            </h1>
                            <%
                            import datetime, urllib
                            %>
                            <span class="post-date">
                                ${datetime.datetime.fromtimestamp(entry.timestamp).strftime("%b %d %Y %H:%M:%S")}
                            </span>
                            <span class="post-categories">
                                in <a href="?category=${urllib.quote(entry.category.name)}" title="">${entry.category.name}</a>
                            </span>
                            <span class="post-categories">
                                taged as 
                                %for i in range(len(entry.tags)):
                                <% tag=entry.tags[i] %>
                                <a href="?tag=${urllib.quote(tag.name)}">${tag.name}</a>
                                %if i != len(entry.tags)-1:
                                ,
                                %endif    
                                %endfor
                            </div>


                            <div class="post-text">
                                <%
                                from docutils.core import publish_parts
                                content = publish_parts(entry.content, writer_name='html')['html_body']
                                %>
                                ${content.replace('literal-block', 'literal-block prettyprint') | n,trim}
                            </div>

                            <div class="post-pages" style="display:none"></div>
                            <div class="post-foot">
                                <a href="" class="comments-link" title="" style="display:none">0 Comments and 0 Reactions</a>				<div class="post-meta">
                                    <div class="post-tags"></div>
                                </div>
                            </div>
                        </div>
                        <div class="sep"></div>

 
</%block>

<%block name="pagination">
</%block>
